# JournalSync Protocol - Final Project

## Overview
This project implements the JournalSync protocol using Python and UDP sockets.
It allows clients to upload journal entries and retrieve the most recent entry using a custom-defined message structure.

## Features
- Upload new journal entries with title and content.
- Retrieve the latest journal entry from the server.
- Server logs with timestamps.

## How to Run

### Requirements
- Python 3

### Run the Server
```bash
cd server
python3 server.py
```

### Run the Client
```bash
cd client
python3 client.py
```
You will be prompted to:
- Upload a new journal entry, or
- Get the latest entry stored on the server.

## Protocol Design
### Header (js_header_t)
- 2 bytes: Version
- 2 bytes: OpCode
    - 1: Upload
    - 2: ACK
    - 3: Request latest
    - 4: Latest entry (response)
- 2 bytes: Payload length (excluding header)

### Upload Entry (js_upload_entry_t)
- 2 bytes: Title length
- N bytes: Title (UTF-8)
- 2 bytes: Content length
- N bytes: Content (UTF-8)

### ACK (js_ack_t)
- Header only, OpCode = 2

### Latest Entry Response
- Same structure as Upload Entry

### Notes
- The server stores entries in a plain text file called journal_entries.txt.
- The communication is entirely based on UDP.