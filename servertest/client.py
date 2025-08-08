import socket
import time

HOST = '127.0.0.1'

PORT = 22037

def change_settings(host,port):

    HOST = host
    PORT = port

    return 'done'


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
conn.connect((HOST,PORT))

   

def manual_send(message):

        conn.sendall(message.encode('utf-8'))
        
        # Receive the server's response
        data = conn.recv(1024)
        
        # Decode and print the response
        response = data.decode('utf-8')
        
        return response

def send(message):
      return manual_send(message=message)



def create_job(type, headers,body):
      send([type, headers,body])

      
    








