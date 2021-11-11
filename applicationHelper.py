import  os, re
from datetime import datetime

def formatResponse(status: int, error = None, data =None)->str:
    if error:
        return f"""HTTP/1.1 {str(status)} {error}\r\n 
        Date: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\r\n 
        Content-Type: application/json\r\n
        Content-Length: {str(len(error.encode("utf-8")))}\r\n\r\n
        {error}"""
    elif data is not None:
        return f"""HTTP/1.1 {str(status)} OK \r\n 
        Date: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\r\n 
        Content-Type: application/json\r\n
        Content-Length: {str(len(data.encode("utf-8")))}\r\n\r\n
        {data}"""
    else:
        return f"""HTTP/1.1 500 Internal Server Error\r\n 
        Date: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\r\n 
        Content-Type: text/html\r\n
        Content-Length: 0\r\n\r\n"""

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

def securityThreat(clientPath: str) -> bool:
    if clientPath.count("/") > 1:
        return True
    else:
        return False