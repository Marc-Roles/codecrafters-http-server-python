import socket
import threading
import sys

def handle_client(client_socket):
    data = client_socket.recv(1024)
    request_data = data.decode().split("\r\n")
    request_line = request_data[0]
    user_agent = next((request.split(": ")[1] for request in request_data if request.startswith("User-Agent:")), "")
    accept_encoding_data = [request.split(": ")[1] for request in request_data if request.startswith("Accept-Encoding:")]
    accept_encoding = [""]
    if len(accept_encoding_data) != 0:
        accept_encoding  = accept_encoding_data[0].split(", ")
    content_encoding = ["gzip"]     # Add more content encoding types here

    print(request_data)

    method, path, http_version = request_line.split()

    if path == "/" and method == "GET":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/echo/") and method == "GET":
        if any(encoding in content_encoding for encoding in accept_encoding): 
            encoding_to_use = next((encoding for encoding in accept_encoding if encoding in content_encoding), None)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: {encoding_to_use}\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}"
        else:
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}"
    elif path == "/user-agent" and method == "GET":
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
    elif path.startswith("/files/") and method == "GET":
        directory = sys.argv[2]
        try:
            with open(f"{directory}/{path[7:]}", "r") as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}"
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
    elif path.startswith("/files/") and method == "POST":
        directory = sys.argv[2]
        try:
            with open(f"{directory}/{path[7:]}", "w") as file:
                file.write(request_data[max(1, len(request_data) - 1)])
                file.close()
                response = "HTTP/1.1 201 Created\r\n\r\n"
        except:
            response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
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
