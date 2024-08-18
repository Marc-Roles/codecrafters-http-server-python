import socket
import threading

def handle_client(client_socket):
    data = client_socket.recv(1024)
    request_data = data.decode().split("\r\n")
    request_line = request_data[0]
    user_agent = next((request.split(": ")[1] for request in request_data if request.startswith("User-Agent:")), "")

    method, path, http_version = request_line.split()

    if path == "/" and method == "GET":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/echo/") and method == "GET":
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}"
    elif path == "/user-agent" and method == "GET":
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    client_socket.sendall(response.encode("utf-8"))
    client_socket.close()

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
