import sys
import ChatDataKind
from dataclasses import dataclass

@dataclass
class ChatMessage:
    host = ""
    handle = ""
    message = ""

class ChatBuffer:
    messages =  [] 

    def AddMessageToBuffer(self, msg):
        self.messages.append(msg)

    # This should be a 'pickelized' version of the data to be sent over the wire
    # size information should have come in a packet preceding this data.
    def GetBufferData(self):
        return messages
    
    # This is ideally either a 'pickelized' version of data to be sent over the wire
    # where the first part of the tuple indicates that the contents of the message
    # are size data about the next packet coming in.
    def GetBufferSizePacket(self):
        return (ChatDataKind.CHAT_MESSAGE_KIND_SIZE_DATA, sys.getsizeof(messages))
