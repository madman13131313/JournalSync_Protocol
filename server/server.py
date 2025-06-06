import socket
import struct
import time

PORT = 44444

def handle_upload(data):
    """
    Parses and stores a journal entry.
    """
    title_len = struct.unpack('!H', data[:2])[0]
    title = data[2:2 + title_len].decode('utf-8')
    offset = 2 + title_len
    content_len = struct.unpack('!H', data[offset:offset + 2])[0]
    content = data[offset + 2:offset + 2 + content_len].decode('utf-8')

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open('journal_entries.txt', 'a') as f:
        f.write(f'Time: {timestamp}\nTitle: {title}\nContent: {content}\n---\n')

    print(f"[{timestamp}] Received and saved journal entry: '{title}'")
    return struct.pack('!HHH', 1, 2, 0)  # ACK

def handle_get_latest():
    """
    Retrieves and returns the most recent journal entry using protocol format.
    """
    try:
        with open('journal_entries.txt', 'r') as f:
            entries = f.read().strip().split('---\n')
            last_entry = entries[-1].strip() if entries and entries[0] else ""
            lines = last_entry.split('\n')
            title = next((line.replace('Title: ', '') for line in lines if line.startswith('Title: ')), "N/A")
            content = next((line.replace('Content: ', '') for line in lines if line.startswith('Content: ')), "No entries found")
    except FileNotFoundError:
        title = "N/A"
        content = "Journal file not found"

    title_bytes = title.encode('utf-8')
    content_bytes = content.encode('utf-8')
    body = struct.pack(f'!H{len(title_bytes)}sH{len(content_bytes)}s',
                       len(title_bytes), title_bytes,
                       len(content_bytes), content_bytes)
    header = struct.pack('!HHH', 1, 4, len(body))
    return header + body

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', PORT))
    print(f"Server is listening on port {PORT}...")

    while True:
        data, addr = sock.recvfrom(2048)
        if len(data) < 6:
            continue

        version, op_code, length = struct.unpack('!HHH', data[:6])
        print(f"Received packet from {addr} with OpCode {op_code}")

        if op_code == 1:
            response = handle_upload(data[6:])
        elif op_code == 3:
            response = handle_get_latest()
        else:
            print("Unknown OpCode")
            continue

        sock.sendto(response, addr)

if __name__ == '__main__':
    main()
