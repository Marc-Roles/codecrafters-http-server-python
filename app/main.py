import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()
    
    request = client_socket.recv(1024).decode("utf-8")

    url = request.split()[1]

    if url != "/":
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    else:
        response = "HTTP/1.1 200 OK\r\n\r\n"

    client_socket.sendall(response.encode("utf-8"))
    client_socket.close()

if __name__ == "__main__":
    main()
