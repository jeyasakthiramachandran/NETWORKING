import socket
from datetime import datetime

# Server configuration
server_port = 12345

# Create a server socket and bind it to the specified port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', server_port))

# Listen for incoming connections
server_socket.listen(5)
print("Server is listening on port", server_port)

while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print("Connection from:", client_address)

    try:
        # Send server's date and time to the client
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_socket.sendall(current_time.encode('utf-8'))

        # Read client's IP address sent by the client
        client_address_from_client = client_socket.recv(1024).decode('utf-8')
        print("Client details - IP Address:", client_address_from_client)

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the client socket
        client_socket.close()

# Close the server socket (This part is reached only if the server is terminated)
server_socket.close()