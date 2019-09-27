import socket
import tkinter
import sys
import time

import ChatServer
import ChatClient

def main(args):
    print("██████ ╗██╗  ██╗ █████╗ ████████╗    ████████╗██╗  ██╗██╗███╗   ██╗ ██████╗")
    print("██╔════╝██║  ██║██╔══██╗╚══██╔══╝    ╚══██╔══╝██║  ██║██║████╗  ██║██╔════╝")  
    print("██║     ███████║███████║   ██║          ██║   ███████║██║██╔██╗ ██║██║  ███╗")
    print("██║     ██╔══██║██╔══██║   ██║          ██║   ██╔══██║██║██║╚██╗██║██║   ██║")
    print("╚██████╗██║  ██║██║  ██║   ██║          ██║   ██║  ██║██║██║ ╚████║╚██████╔╝")
    print(" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝          ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ")
                                                                            
    if(len(args) <= 1):
        print("Please specify whether to run ChatThing in ServerMode ('serve') or ClientMode ('client')")
        return

    if("serve" == args[1]):
        print("Server Mode")

        args.pop(0)
        args.pop(0)

        server = ChatServer.ChatServer(args)
        server.Serve()

    elif("client" == args[1]):
        print("Client Mode")

        args.pop(0)
        args.pop(0)

        client = ChatClient.ChatClient(args)

    else:
        print("Please specify either 'serve' or 'client' after the script to indicate whether this script should run as server or client.")

    return
    
main(sys.argv)
