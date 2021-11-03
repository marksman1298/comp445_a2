import socket, sys, os, threading, re, argParser
from datetime import datetime


def formatResponse(status: int, error = None, data =None)->str:
    if error:
        return f"""HTTP/1.1 {str(status)} {error} \r\n 
        Date: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} \r\n 
        Content-Type: text/html; charset=utf-8 \r\n
        Content-Length: {str(len(error.encode("utf-8")))} \r\n\r\n
        {error}"""
    elif data:
        return f"""HTTP/1.1 {str(status)} OK \r\n 
        Date: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} \r\n 
        Content-Type: text/html; charset=utf-8 \r\n
        Content-Length: {str(len(data.encode("utf-8")))} \r\n\r\n
        {data}"""
    else:
        return "how?"

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
        data = ''       
        for files in os.listdir(path):
            data += files + '\r\n'
        return formatResponse(200, data= data)            
    else:
        return formatResponse(404, error="The desired directory does not exist") 

def handle_client(conn, addr):
    print ('New client from', addr)
    try:
        # while True:
        dataBytes = conn.recv(1024) #what if bigger than 1024
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
        try:
            response = ''
            if method == 'GET':
                if args.VERBOSE:
                    print("GET request")
                print(fileName)
                if fileName == '/' and os.path.isdir(args.DIRECTORY): 
                    response = getAllFiles(args.DIRECTORY)        
                    if args.VERBOSE:
                        print("list of files inside the given directory")       
                elif os.path.isdir(args.DIRECTORY):
                    pathToFile = args.DIRECTORY + fileName
                    if os.path.isfile(pathToFile):
                        if args.VERBOSE:
                            print("output contents of the requested file")
                        with open(pathToFile, 'r') as f:
                            response = formatResponse(200, data=f.read())
                    else:
                        if args.VERBOSE:
                            print("File does not exist in directory")
                        response = formatResponse(404, error="File does not exist in given directory")
                else:
                    print(args.DIRECTORY)
                    if args.VERBOSE:
                        print("directory does not exist or could not be accessed")
                    response = formatResponse(404, error="Directory does not exist")  
            elif method == "POST":
                if body is None:
                    if args.VERBOSE:
                        print("body is empty, request failed")
                    response = formatResponse(400, error="Body of request is empty")
                elif os.path.isdir(args.DIRECTORY): #not writing outside directory where code is
                    pathToWrite = args.DIRECTORY + fileName
                    with open(pathToWrite, 'w') as f:
                        f.write(body)
                    if args.VERBOSE:
                        print(f"write contents of body to {pathToWrite}")
                    response = formatResponse(200, data=body)
                else:
                    response = formatResponse(403, error="Attempted to write outside given directory")
        finally:
            conn.sendall(response.encode())
            print(response)
            conn.close()
    finally:
        conn.close()

def connection():
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
connection()
