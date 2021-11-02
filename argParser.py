import argparse, os

def argumentParser():
    parser = argparse.ArgumentParser(prog="httpfs", description="httpfs is a simple file server.", 
        epilog="usage: httpfs [-v] [-p PORT] [-d PATH-TO-DIR]"
    )
    parser.add_argument("-v", help="Prints debugging messages.", action="store_true", dest="VERBOSE")
    parser.add_argument("-p", help="""Specifies the port number that the server will listen and serve at. Default is 8080.""", 
                        type=int, default=8080, dest="PORT", nargs="?", const=8080)
    parser.add_argument("-d", help="""-d Specifies the directory that the server will use to read/write
                        requested files. Default is the current directory when launching the
                        application.""", default=os.getcwd(), dest="DIRECTORY", nargs="?", const=os.getcwd()) 
    return parser
