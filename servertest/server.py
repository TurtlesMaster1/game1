import socket
import threading

# Define the host and port
HOST = '127.0.0.1'  # Localhost
PORT = 22037        # Port




# Handle job logic
def handle_job(job):
    if job[0] == 'RENDER':
        print("[JOB] Rendering job started...")
        # Your rendering logic here
    else:
        print(f"[JOB] Unknown job type: {job[0]}")





# Handle different types of responses
def handle_response(message):
    if isinstance(message, list):
        handle_job(message)
    else:
        print('[LOG]', message)





# Function to handle each client connection
def handle_client(conn, addr):
    with conn:
        print(f"[+] Connected by {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"[-] Client {addr} disconnected.")
                    break

                message = data.decode('utf-8')

                # Example: Try to parse as a Python list
                try:
                    parsed = eval(message)
                except:
                    parsed = message

                print(f"[{addr}] Received:", parsed)
                handle_response(parsed)

                # Send a basic echo back to the client
                response = f"Server received: {message}".encode('utf-8')
                conn.sendall(response)

            except ConnectionResetError:
                print(f"[!] Connection reset by {addr}")
                break
            except Exception as e:
                print(f"[!] Error with {addr}: {e}")
                break

            

# Main server code
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Server listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
            print(f"[~] Active connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
