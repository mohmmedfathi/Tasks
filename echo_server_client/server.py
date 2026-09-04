import socket
import threading

from constants import HOST, PORT, BUFFER_SIZE

# to close every client when stop the server and lock since many threads share it
client_sockets = set()
client_sockets_lock = threading.Lock()


def handle_client(client_socket, client_address):
    print(f"client connected: {client_address}")

    try:
        with client_socket:
            while True:
                data = client_socket.recv(BUFFER_SIZE)

                # stop handling client if it closed the connection
                if not data:
                    break

                try:
                    message = data.decode("utf-8")
                except UnicodeDecodeError:
                    print(f"invalid utf-8 from {client_address}")
                    client_socket.sendall(
                        "please send valid utf-8 text".encode("utf-8")
                    )
                    continue

                print(f"received from {client_address}: {message}")

                if message.strip().lower() == "exit":
                    break

                client_socket.sendall(message.encode("utf-8"))
                print(f"sent to {client_address}: {message}")

    except ConnectionError:
        print(f"connection lost: {client_address}")

    finally:
        with client_sockets_lock:
            client_sockets.discard(client_socket)

        print(f"client disconnected: {client_address}")


def close_all_clients():
    # prevent the client set from changing while taking a shutdown snapshot
    with client_sockets_lock:
        sockets = list(client_sockets)

    for client_socket in sockets:
        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass # thread already closed


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # port stays busy a bit after a stop since tcp is not fully closed yet
        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"server listening on {HOST}:{PORT}")

        try:
            while True:
                client_socket, client_address = server_socket.accept()

                # prevent race conditions while registering a new client
                with client_sockets_lock:
                    client_sockets.add(client_socket)

                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.start()

        except KeyboardInterrupt:
            print("\nserver stopping")

        finally:
            close_all_clients()
            print("server stopped")


if __name__ == "__main__":
    start_server()
