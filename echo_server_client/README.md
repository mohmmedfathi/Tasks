# Echo Server and Client

Multi-threaded TCP server 
and client on 127.0.0.1:65432

<img width="1000" height="481" alt="Image" src="https://github.com/user-attachments/assets/d8a8516d-323e-4ffd-a052-8a39d6560a11" />

## Run

    python3 server.py
    python3 client.py

## Features

- IPv4 TCP on 127.0.0.1:65432
- Thread per client
- Echo until `exit`
- Ctrl+C stops server and closes all clients
- Client quits on `exit`, Ctrl+C or Ctrl+D

Host, port and buffer size are in `constants.py`
