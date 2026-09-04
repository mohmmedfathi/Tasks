import socket

from constants import BUFFER_SIZE


def handle_client(client_socket, client_address):
    print(f"client connected: {client_address}")

    try:
        with client_socket:
            while True:
                data = client_socket.recv(BUFFER_SIZE)

                # stop handling client if it closed the connection
                if not data:
                    break

                message = data.decode("utf-8")
                print(f"received from {client_address}: {message}")

                if message.strip().lower() == "exit":
                    break

                client_socket.sendall(message.encode("utf-8"))
                print(f"sent to {client_address}: {message}")

    except ConnectionError:
        print(f"connection lost: {client_address}")

    print(f"client disconnected: {client_address}")
