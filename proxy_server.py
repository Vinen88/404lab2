#!/usr/bin/env python3
import socket, time, sys


HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

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
    host = 'www.google.com'
    port = 80
    buffer_size = 4096
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)

        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            #recieve data, wait a bit, then send it back
            proxy_data = conn.recv(BUFFER_SIZE)
            time.sleep(0.5)
            prox_s = create_tcp_socket()
            remote_ip = get_remote_ip(host)
            prox_s.connect((remote_ip, port))
            prox_s.sendall(proxy_data)
            prox_s.shutdown(socket.SHUT_WR)
            full_data = b""
            while True:
                data = prox_s.recv(buffer_size)
                if not data:
                    break
                full_data += data
            conn.sendall(full_data)
            conn.close()
            prox_s.close()



if __name__ == "__main__":
    main()
