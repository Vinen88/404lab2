#!/usr/bin/env python3
import socket, sys


def create_tcp_socket():
    print("Creating socket")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error):
        print(f'Failed to create socket. Error code: , error message :')
        sys.exit()
    print("socket created successfully")
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending Payload")
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print("Send failed")
        sys.exit()
    print("Payload sent successfully")

def main():
    try:
        #define address info, payload, and buffer size
        host = ''
        port = 8001
        payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
        buffer_size = 4096

        #make the socket, get the ip, and connect
        s = create_tcp_socket()
        remote_ip = get_remote_ip(host)

        s.connect((remote_ip, port))
        print(f'socket Connect to {host} on ip {remote_ip}')
        send_data(s, payload)
        s.shutdown(socket.SHUT_WR)

        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                break
            full_data += data
        print(full_data)
    except Exception as e:
        print(e)
    finally:
        s.close()

if  __name__ == "__main__":
    main()

#1. when you initialize the socket you can select TCP by passing the arugment socket.SOCK_STREAM
#2. we tell server socket to listen it also has the accept loop
#3. s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) the SO_REUSEADDR tells it to
#4. Connected by ('127.0.0.1', 52590) so their IP and the port they used to connect. 
#5. it returns the data as a byte string. 