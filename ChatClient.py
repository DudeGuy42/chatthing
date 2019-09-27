import tkinter, ChatMessage, socket

class ChatClient:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def SendMessage(self, message : ChatMessage):

        return

    def Connect(self):

        return

    def __init__(self, args):
        print("Client Mode With Args: " + str(args))
        self.serverSocket.bind(socket.gethostname(), 65000) # only works on same machine

        return