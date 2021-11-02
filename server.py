import socket, sys, os, threading, re, argParser


# def formatRequest(data:str)
# b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.55.1\r\nAccept: */*\r\nReferer: t\r\n\r\n'
def formatRequest(data: str):
    # data = data.decode('utf-8')
    # dataGroups = data.split('\r\n\r\n')
    dataGroups = re.search("(\w+)\s(\/\w*[\/\w]*(\.\w+\/?)*)", data) 
    acceptedExtenstions = re.search('(Accept:)\s(\W+)(\\r\\n)', data)
    methodType = dataGroups.group(1)
    fileName = dataGroups.group(2)
    fileExtension = acceptedExtenstions.group(2)
    return (methodType, fileName, fileExtension)
    
    #new function formatBody
def formatBody(data: str):
    body = data.split('\r\n\r\n')
    if len(body) > 1:
        return (re.sub('\r\n', '', body[1]))
    return None

def getAllFiles(path: str, extension = None) -> str:
    if os.path.isdir(path):
        response = ''
        if extension:
            for files in os.listdir(path):
                if files.endswith(extension):
                    response += files + '\r\n'
        else:
            for files in os.listdir(path):
                response += files + '\r\n'
        return response            
    else:
        raise Exception('the desired directory does not exist')

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
        print(method, fileName, fileExtenstion, body)
        response = "hi"
        try:
            if method == 'GET':
                if args.VERBOSE:
                    print("GET request")
                if fileName == '/':
                    if fileExtenstion != '*/*':
                        response = getAllFiles(args.DIRECTORY, fileExtenstion)
                        if args.VERBOSE:
                            print("list of files that have the same file extensions as specified inside the given directory")
                    else:
                        response = getAllFiles(args.DIRECTORY)        
                        if args.VERBOSE:
                            print("list of files inside the given directory")           
                elif os.path.isdir(args.DIRECTORY):
                    pathToFile = args.DIRECTORY + fileName
                    if os.path.isfile(pathToFile):
                        if args.VERBOSE:
                            print("output contents of the requested file")
                        with open(pathToFile, 'r') as f:
                            response = f.read()
                    else:
                        response = "404 file does not exist in directory."
            else:
                response = "how am I here"        
            # elif method == "POST":
            # TODO POST request

        except OSError:
            print("error")
        finally:
            conn.sendall(response.encode())
    finally:
        conn.close()

def attempt1():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8080
    try:
        sock.bind(('', port))
        sock.listen(5) #queue 
        print(f"Server listening at port {port}")
    # parser = argparse.ArgumentParser(prog="httpfs")
        while True:
            clientsocket, address = sock.accept()
            print(f"Connection from {clientsocket} {address} has been established.")
            threading.Thread(target=handle_client, args=(clientsocket, address)).start()
    finally:
        clientsocket.close()


parser = argParser.argumentParser()
args = parser.parse_args()
attempt1()
# b'GET /file.txt HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.55.1\r\nAccept: */*\r\nReferer: t\r\n\r\n'
# b'POST /afile3.txt HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.55.1\r\nAccept: */*\r\nContent-Type:application/text\r\nContent-Length: 25\r\n\r\nwriting this data to file'
# print(formatRequest('GET / HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.55.1\r\nAccept: */*\r\nReferer: t\r\n\r\n'))
#Parser

# print(args.PORT)
# formatRequest('POST /afile3.txt HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/7.55.1\r\nAccept: */*\r\nContent-Type:application/text\r\nContent-Length: 25\r\n\r\nwriting this data to file')



# print(sys.argv)
# print(args.VERBOSE, args.PORT, args.DIRECTORY)