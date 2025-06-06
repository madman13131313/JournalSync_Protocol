
# JournalSync Protocol

## Features
- Upload journal entries
- Timestamped logs
- Retrieve latest journal entry
- Simple client-side operation menu

## How to Run

### Requirements
- Python 3

### Start the Server
```bash
cd server
python3 server.py
```

### Run the Client
```bash
cd client
python3 client.py
```

## Message Format

### Header (`js_header_t`)
- 2 bytes: Version
- 2 bytes: Operation Code (1 = Upload, 2 = ACK, 3 = Get Latest)
- 2 bytes: Payload Length

### Upload Entry (`js_upload_entry_t`)
- 2 bytes: Title length
- N bytes: Title (UTF-8)
- 2 bytes: Content length
- N bytes: Content (UTF-8)

### ACK (`js_ack_t`)
- Just the header with OpCode = 2

## State Machine
Client: CONNECTED → SYNC_REQUESTED → WAITING_FOR_ACK → SYNC_COMPLETE  
Server: LISTENING → RECEIVING → RESPONDING
