import os
from applicationHelper import *



def handle_client(conn, address, verbose, directory):
    print ('New client from', address)
    try:
        dataBytes = conn.recv(1024) #what if bigger than 1024
        data = dataBytes.decode('utf-8')
        method, fileName, fileExtenstion = formatRequest(data)
        print(fileName)
        # default is directory containing this file
        # ensures that the files accessed are inside the directory
        # 
        body = formatBody(data)
        if verbose:
            print("------------------------------------------------------------------------------------------------")
            print(f"method: {method}, fileName: {fileName}, fileExtenstion: {fileExtenstion}, body: {body}, path: {directory}")
        try:
            # print(method)
            response = ''
            if method == 'GET':
                if verbose:
                    print("GET request")
                print(fileName)
                if fileName == '/' and os.path.isdir(directory): 
                    response = getAllFiles(directory)        
                    if verbose:
                        print("list of files inside the given directory")       
                elif securityThreat(fileName) or os.path.isdir(directory + fileName):
                    response = formatResponse(401, error="Unauthorized, attempting to read files outside of given directory")
                    if verbose:
                        print("Attempted to read outside of given directory")
                elif os.path.isfile(directory+fileName):
                    pathToFile = directory + fileName
                    if verbose:
                        print("output contents of the requested file")
                    with open(pathToFile, 'r') as f:
                        response = formatResponse(200, data=f.read())    
                else:
                    if verbose:
                        print("Path does not exist")
                    response = formatResponse(404, error="Path not found") 
            elif method == "POST": 
                if os.path.isdir(directory): 
                    if securityThreat(fileName):
                        response = formatResponse(401, error="Unauthorized: attempted to write a file outside the given directory")
                        if verbose:
                            print("Attempted to write outside given directory")
                    else:
                        pathToWrite = directory + fileName
                        with open(pathToWrite, 'w') as f:
                            f.write(body)
                        if verbose:
                            print(f"write contents of body to {pathToWrite}")
                        response = formatResponse(200, data=body)
                else:
                    if verbose:
                        print("directory does not exist")
                    response = formatResponse(404, error="Directory does not exist")
        finally:
            conn.sendall(response.encode())
            print(response)
            conn.close()
    finally:
        conn.close()


