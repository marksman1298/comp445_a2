import socket,threading, argParser
from applicationLayer import handle_client 

def connection(port, verbose, directory):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('', port))
        sock.listen(5)  
        print(f"Server listening at port {port}")
        while True:
            clientSocket, address = sock.accept()
            print(f"Connection from {clientSocket} {address} has been established.")
            threading.Thread(target=handle_client, args=(clientSocket, address, verbose, directory)).start()
    finally:
        clientSocket.close()


def run():  
    parser = argParser.argumentParser()
    args = parser.parse_args()
    connection(args.PORT, args.VERBOSE, args.DIRECTORY)

run()