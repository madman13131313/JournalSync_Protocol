import socket
import struct
from datetime import datetime

# Server will listen on this port
PORT = 44444

# Operation codes
OPCODE_UPLOAD = 1        # Client sends a journal entry
OPCODE_ACK = 2           # Server sends back acknowledgement
OPCODE_GET_LATEST = 3    # Client requests latest journal entry

def handle_upload(data):
    """
    Handle an upload operation from the client.
    Parses the data to extract the title and content,
    saves it to a file with a timestamp, and returns an ACK.
    """
    # Extract title length and title
    title_len = struct.unpack('!H', data[:2])[0]
    title = data[2:2+title_len].decode('utf-8')
    
    # Move to content length and content
    offset = 2 + title_len
    content_len = struct.unpack('!H', data[offset:offset+2])[0]
    content = data[offset+2:offset+2+content_len].decode('utf-8')

    # Add timestamp and save to file
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('journal_entries.txt', 'a') as f:
        f.write(f'Time: {timestamp}\nTitle: {title}\nContent: {content}\n---\n')

    # Return ACK message (just header with OpCode = 2)
    return struct.pack('!HHH', 1, OPCODE_ACK, 0)

def handle_get_latest():
    """
    Reads the last journal entry from the file and returns it as a string.
    """
    try:
        with open('journal_entries.txt', 'r') as f:
            entries = f.read().strip().split('---\n')
            if entries and entries[-1].strip():
                latest = entries[-1].strip()
            elif len(entries) > 1:
                latest = entries[-2].strip()
            else:
                latest = "No entries found."
    except FileNotFoundError:
        latest = "No entries found."

    return latest.encode('utf-8')

def main():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', PORT))

    print("Server listening on port", PORT)

    while True:
        # Wait for data from client
        data, addr = sock.recvfrom(2048)

        # Parse header
        header = struct.unpack('!HHH', data[:6])
        version, op_code, length = header

        # Handle based on opcode
        if op_code == OPCODE_UPLOAD:
            body = data[6:]
            response = handle_upload(body)
            sock.sendto(response, addr)

        elif op_code == OPCODE_GET_LATEST:
            latest_entry = handle_get_latest()
            sock.sendto(latest_entry, addr)

if __name__ == '__main__':
    main()
