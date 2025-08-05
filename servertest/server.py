import socket

# Define the host and port
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 22037        # Port to listen on (non-privileged ports are > 1023)

# Create a socket object
# AF_INET specifies the address family (IPv4)
# SOCK_STREAM specifies the socket type (TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    # Accept a connection
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            # Receive data from the client
            data = conn.recv(1024)
            
            
            # Decode the data and print it
            message = data.decode('utf-8')
            
            print(f"Received from client: {message}")

            # Send a response back to the client
            response = f"Echo: {message}".encode('utf-8')
            conn.sendall(response)
        input("Press Enter to exit...")

