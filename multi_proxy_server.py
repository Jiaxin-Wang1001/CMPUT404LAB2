#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

#define address & buffer size
HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024

#get ip
def get_remote_ip(host):
    try:
        remote_ip = socket.gethostbyname(host)
    except:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    return remote_ip

def handle_requests(addr, conn, proxy_end):
    print('Connected by', addr)

    full_data = conn.recv(BUFFER_SIZE)
    proxy_end.sendall(full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    full_data = proxy_end.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def main():
    extern_host = 'www.google.com'
    port = 80

    #create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print('Starting proxy server')
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)

        while(True):
            #connect proxy_start
            conn, addr = proxy_start.accept()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                remote_ip = get_remote_ip(extern_host)
                #connect proxy_end
                proxy_end.connect((remote_ip, port))
                p = Process(target=handle_requests, args=(addr, conn, proxy_end))
                p.daemon = True
                p.start()
                print('Started process', p)
            proxy_end.close()

if __name__ == "__main__":
    main()