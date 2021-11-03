import socket, sys, os, threading, re, argParser
from datetime import datetime


# def formatRequest(data:str)
# b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.55.1\r\nAccept: */*\r\nReferer: t\r\n\r\n'
def formatRequest(data: str):
    dataGroups = re.search("(\w+)\s(\/\w*[\/\w]*(\.\w+\/?)*)", data) 
    acceptedExtenstions = re.search('(Accept:)\s(\W+)(\\r\\n)', data)
    methodType = dataGroups.group(1)
    fileName = dataGroups.group(2)
    fileExtension = acceptedExtenstions.group(2)
    return (methodType, fileName, fileExtension)
    
def formatBody(data: str):
    body = data.split('\r\n\r\n')
    if len(body) > 1:
        return (re.sub('\r\n', '', body[1]))
    return None

def getAllFiles(path: str) -> str:
    if os.path.isdir(path):
        response = ''       
        for files in os.listdir(path):
            response += files + '\r\n'
        return response            
    else:
        response = 'HTTP/1.1 404 error \r\n the desired directory does not exist.'
        return response 

def handle_client(conn, addr):
    print ('New client from', addr)
    try:
        # while True:
        dataBytes = conn.recv(1024)
            # if not data:
            #     break
            # print(data)
            # conn.sendall(data)
        data = dataBytes.decode('utf-8')
        method, fileName, fileExtenstion = formatRequest(data)
        # default is directory containing this file
        # ensures that the files accessed are inside the directory
        # 
        body = formatBody(data)
        if args.VERBOSE:
            print("------------------------------------------------------------------------------------------------")
            print(f"method: {method}, fileName: {fileName}, fileExtenstion: {fileExtenstion}, body: {body}, path: {args.DIRECTORY}")
        # response = "hi"
        try:
            if method == 'GET':
                if args.VERBOSE:
                    print("GET request")
                if fileName == '/' and os.path.isdir(args.DIRECTORY): 
                    response = getAllFiles(args.DIRECTORY)        
                    if args.VERBOSE:
                        print("list of files inside the given directory")    
                    else:
                        if args.VERBOSE:
                            print("directory does not exist")
                        response = "HTTP/1.1 404 error \r\n Directory does not exist"       
                elif os.path.isdir(args.DIRECTORY):
                    pathToFile = args.DIRECTORY + fileName
                    if os.path.isfile(pathToFile):
                        if args.VERBOSE:
                            print("output contents of the requested file")
                        with open(pathToFile, 'r') as f:
                            response = f.read()
                    else:
                        if args.VERBOSE:
                            print("File does not exist in directory")
                        # response = "HTTP/1.1 404 error \r\n File does not exist in directory."   
                        response = ''.join(['HTTP/1.1 ', "404", ' ', "not found", '\r\n', 
                        'Date: ', datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"), '\r\n',
                        'Content-Type: text/html; charset=utf-8\r\n','Content-Length: ', 
                        str(len("error")), '\r\n\r\n',"hello"])     #create method to format request
            elif method == "POST":
                if body is None:
                    if args.VERBOSE:
                        print("body is empty, request failed")
                    response = 'HTTP/1.1 400 error \r\n body is empty'
                elif os.path.isdir(args.DIRECTORY): #not writing outside directory where code is
                    pathToWrite = args.DIRECTORY + fileName
                    with open(pathToWrite, 'w') as f:
                        f.write(body)
                    if args.VERBOSE:
                        print(f"write contents of body to {pathToWrite}")
                    response = 'HTTP/1.1 200 OK \r\n'
                else:
                    response = 'HTTP/1.1 404 error \r\n directory not found'
        finally:
            conn.sendall(response.encode())
            print(response)
            conn.close()
            print("hihi")
            #responses not appearing in client
    finally:
        print("here")
        conn.close()

def attempt1():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('', args.PORT))
        sock.listen(5) #queue 
        print(f"Server listening at port {args.PORT}")
        while True:
            clientsocket, address = sock.accept()
            print(f"Connection from {clientsocket} {address} has been established.")
            threading.Thread(target=handle_client, args=(clientsocket, address)).start()
    finally:
        clientsocket.close()


parser = argParser.argumentParser()
args = parser.parse_args()
attempt1()
# print(''.join(['HTTP/1.1 ', "404", ' ', "not found", '\r\n',
                    # 'Date: ', datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"), '\r\n',
                    # 'Content-Type: text/html; charset=utf-8\r\n',
                    # 'Content-Length: ', str(len("error")), '\r\n\r\n',
                    # "error"]))
# b'GET /file.txt HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.55.1\r\nAccept: */*\r\nReferer: t\r\n\r\n'
# b'POST /afile3.txt HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.55.1\r\nAccept: */*\r\nContent-Type:application/text\r\nContent-Length: 25\r\n\r\nwriting this data to file'
# print(formatRequest('GET / HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.55.1\r\nAccept: */*\r\nReferer: t\r\n\r\n'))
#Parser

# print(args.PORT)
# formatRequest('POST /afile3.txt HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.55.1\r\nAccept: */*\r\nContent-Type:application/text\r\nContent-Length: 25\r\n\r\nwriting this data to file')



# print(sys.argv)
# print(args.VERBOSE, args.PORT, args.DIRECTORY)