import socket
import struct

# Server configuration
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 44444

# Operation codes
OPCODE_UPLOAD = 1
OPCODE_ACK = 2
OPCODE_GET_LATEST = 3
OPCODE_LATEST_ENTRY = 4  # Server sends back the latest entry

def create_upload_message(title, content):
    """
    Constructs the upload message using the protocol format.
    """
    title_bytes = title.encode('utf-8')
    content_bytes = content.encode('utf-8')
    header = struct.pack('!HHH', 1, OPCODE_UPLOAD, len(title_bytes) + len(content_bytes) + 4)
    body = struct.pack(f'!H{len(title_bytes)}sH{len(content_bytes)}s',
                       len(title_bytes), title_bytes,
                       len(content_bytes), content_bytes)
    return header + body

def menu():
    """
    Displays the user menu and returns their choice.
    """
    print("Choose an operation:")
    print("1 - Upload new journal entry")
    print("2 - Get latest journal entry")
    return input("Enter 1 or 2: ")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    choice = menu()

    if choice == '1':
        title = input("Enter journal title: ")
        content = input("Enter journal content: ")
        msg = create_upload_message(title, content)
    elif choice == '2':
        # Empty message with header only
        msg = struct.pack('!HHH', 1, OPCODE_GET_LATEST, 0)
    else:
        print("Invalid choice")
        return

    sock.sendto(msg, (SERVER_ADDRESS, SERVER_PORT))
    response, _ = sock.recvfrom(2048)

    # Decode header
    if len(response) >= 6:
        version, opcode, length = struct.unpack('!HHH', response[:6])

        if opcode == OPCODE_ACK:
            print("Upload acknowledged by server.")
        elif opcode == OPCODE_LATEST_ENTRY:
            body = response[6:]
            title_len = struct.unpack('!H', body[:2])[0]
            title = body[2:2+title_len].decode('utf-8')
            offset = 2 + title_len
            content_len = struct.unpack('!H', body[offset:offset+2])[0]
            content = body[offset+2:offset+2+content_len].decode('utf-8')
            print(f"Latest Entry:\nTitle: {title}\nContent: {content}")
        else:
            print(f"Received unknown OpCode: {opcode}")
    else:
        print("Received empty or malformed response.")

if __name__ == '__main__':
    main()
