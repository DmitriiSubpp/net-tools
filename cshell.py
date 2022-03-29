import subprocess
import sys
import socket
import argparse
import shlex

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

def start_process(args):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = (args.target, args.port)

    sock.bind(server)
    sock.listen(1)

    buf = b''

    client, _ = sock.accept()

    while True:
        client.send(b'cmd:> ')
        while '\n' not in buf.decode():
            buf += client.recv(64)
        output = execute(buf.decode())
        client.send(output.encode())
        buf = b''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='remote command shell')
    parser.add_argument('-t', '--target', help='target ip')
    parser.add_argument('-p', '--port', type=int, help='target port')
    args = parser.parse_args()

    try:
        start_process(args)
    except Exception as err:
        print('Error: ', err)
