import socket
import struct

# Server IP and Port Configuration
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 44444

# Operation codes for different message types
OPCODE_UPLOAD = 1        # Upload journal entry
OPCODE_ACK = 2           # Acknowledgement from server (not used in client directly)
OPCODE_GET_LATEST = 3    # Request latest journal entry

def create_upload_message(title, content):
    """
    Packs the journal entry into a binary message according to the JournalSync protocol.
    Header: version, opcode, payload length
    Body: title length + title, content length + content
    """
    title_bytes = title.encode('utf-8')
    content_bytes = content.encode('utf-8')
    
    # Header: version = 1, opcode = 1 (upload), length = title + content + 4 bytes (2 for each length field)
    header = struct.pack('!HHH', 1, OPCODE_UPLOAD, len(title_bytes) + len(content_bytes) + 4)
    
    # Body: title length, title, content length, content
    body = struct.pack(f'!H{len(title_bytes)}sH{len(content_bytes)}s', 
                       len(title_bytes), title_bytes, 
                       len(content_bytes), content_bytes)
    
    return header + body

def menu():
    """
    Display the main menu to the user and return their choice.
    """
    print("Choose an operation:")
    print("1 - Upload new journal entry")
    print("2 - Get latest journal entry")
    return input("Enter 1 or 2: ")

def main():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Prompt user for desired operation
    choice = menu()

    # Build the appropriate message based on user's choice
    if choice == '1':
        title = input("Enter journal title: ")
        content = input("Enter journal content: ")
        msg = create_upload_message(title, content)
    elif choice == '2':
        # Send just the header for GET_LATEST
        msg = struct.pack('!HHH', 1, OPCODE_GET_LATEST, 0)
    else:
        print("Invalid choice")
        return

    # Send message to server
    sock.sendto(msg, (SERVER_ADDRESS, SERVER_PORT))
    
    # Receive and display response from server
    response, _ = sock.recvfrom(2048)
    print("Received response:\n", response.decode('utf-8', errors='ignore'))

if __name__ == '__main__':
    main()
