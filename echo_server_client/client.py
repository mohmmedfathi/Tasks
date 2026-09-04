import socket

from constants import HOST, PORT, BUFFER_SIZE


def start_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            print(f"connected to server {HOST}:{PORT}")

            while True:
                message = input("enter message: ")

                # sending 0 bytes would leave recv waiting forever
                if not message.strip():
                    continue

                client_socket.sendall(message.encode("utf-8"))

                if message.strip().lower() == "exit":
                    break

                data = client_socket.recv(BUFFER_SIZE)

                if not data:
                    print("server closed the connection")
                    break

                try:
                    message = data.decode("utf-8")
                except UnicodeDecodeError:
                    print("server sent invalid utf-8 text")
                    continue

                print(f"server: {message}")

    except ConnectionRefusedError:
        print("could not connect to the server")

    except ConnectionError:
        print("connection with the server was lost")

    except (KeyboardInterrupt, EOFError):
        print("\nclosing connection")

    print("connection closed")


if __name__ == "__main__":
    start_client()
