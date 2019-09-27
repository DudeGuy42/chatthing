import tkinter, socket, sys, ChatMessage, time, keyboard
import ChatDataKind
## Server should:
# - Listen for incoming connections
# - Maintain connections / client states about clients
# - Disconnect clients that are 'idle' for too long.
# - Broadcast messages received from clients to all other clients (server->client model is being used)

class ClientConnection:
    clientSocket = None
    pingPong = False # borrowing this from IRC
    heartBeatFrequency = 15 # seconds
    lastHeartbeat = 0
    connectionStartTime = time.time()
    bufferedMessages = []

    # Sends a heartbeat to the client at the clientSocket (Im aiming to keep a single connection alive)
    def Heartbeat(self):
        self.clientSocket.send((ChatDataKind.CHAT_MESSAGE_KIND_CLIENT_HEARTBEAT, self.pingPong))
        self.pingPong = not self.pingPong
        self.lastHeartbeat = time.time()

        return

    def AppendChatMessageToBuffer(self, msg : ChatMessage):
        self.bufferedMessages.append(msg)

        return

    def SendBuffer(self):
        sizeOfMessage = sys.getsizeof(self.bufferedMessages)
        bytesSent = self.clientSocket.send(self.bufferedMessages)

        # Todo: Rumor has it that send may not send the entirety of msg.
        # We will need to add checks to determine that the size of msg is
        # equal to the number of bytes that were sent over the wire. If the checks
        # fail, we need to send the remainder of the message; consequently clients
        # need to be aware that only partial messages are sent and they need to be 
        # prepared to listen to the remainder 
        # for now, I will just raise up the note that a partial was sent, but we will
        # largely ignore it if it happens (I read that it is likely in high traffic situations
        # that the partial thing happens; in test environments and the like it should be ok like
        # this)

        # we may want to send 2 packets, the first to indicate size, the second
        # will be the entire buffer?

        if(sizeOfMessage != bytesSent):
            self.ServerLog("Server did not send the entire message to the client. It sent " + str(bytesSent) + " of " + str(sizeOfMessage))

        # clear the buffer after it is sent
        self.bufferedMessages.clear()

        return

    def Receive(self):
        return

    def Work(self):
        # Check if heartbeat should be sent
        # Send Buffers to clients
        if(time.time() - self.lastHeartbeat >= self.heartBeatFrequency):
            self.Heartbeat()

        return

    def __init__(self, socket : socket):
        self.clientSocket.setblocking(0)
        self.clientSocket = socket

        return


class ChatServer:
    shouldQuitServer = False
    serverStartTime = time.time()
    # the listening socket waits for new connections to the chat server
    listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## The server is responsible for maintaining the state of these client sockets.
    # The server sends data to clients on this socket.
    clientSockets = []

    def HandleClientConnect(self):
        try:
        # Accept is a blocking call; check for non blocking
        # or a check to see if there is actually someone listening?
            (newClientSocket, addr) = self.listeningSocket.accept()
            self.clientSockets.append(ClientConnection(newClientSocket))
            
            self.ServerLog("Connection from : " + str(newClientSocket) + " at addr " + str(addr))

        except BlockingIOError:
            return

        return

    def HandleDisconnect(self, client : socket):
        if(client in self.clientSockets):
            client.shutdown() # inform the client we're closing connection?
            client.close() # close socket
            self.clientSockets.remove(client) # stop thinking about the client

        return

    def ReceiveDataFromClients(self):
        
        for clientConnection in self.clientSockets:
            clientConnection.Receive()
            # todo: Depickle (?), place in buffers to emit to other clients 
        return

    def SetQuit(self, keyPressEvent):
        self.ServerLog(str(keyPressEvent))
        self.shouldQuitServer = True

    def Serve(self):
        self.ServerLog("Listening for incoming connections...")

        while True:
            self.listeningSocket.listen()
            
            self.HandleClientConnect()
            self.ReceiveDataFromClients()

            if(self.shouldQuitServer):
                # Todo: Inform clients the server is closing; possible countdown?
                # Close server
                # Todo: Error keeps occurring when closing; I dont care; i will later.
                quit()
        return
    
    def ServerLog(self, msg: str):
        print(str(time.time() - self.serverStartTime) + ": " + msg)

        return

    def __init__(self, args):
        self.hostname = socket.gethostname()
        self.port = 65000

        self.ServerLog("Running Server With Args: " + str(args))
        self.ServerLog("hostname: " + str(socket.gethostname()))

        self.listeningSocket.bind((self.hostname, self.port))
        self.listeningSocket.setblocking(0)

        keyboard.on_press_key('q', self.SetQuit)

        return