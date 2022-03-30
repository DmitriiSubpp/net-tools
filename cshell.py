import subprocess
import sys
import os
import socket
import argparse
import shlex

def execute(cmd = '', work_dir = os.getcwd()):
    try:
        cmd = shlex.split(cmd)
        if cmd[0] == 'cd':
            work_dir = cmd[1]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, cwd=work_dir)
        return output.decode(), work_dir
    except Exception as err:
        print('Error in execute: ', err)
        return str(err) + '\n'

def start_process(args):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(f'your ip: {ip}, hostname: {hostname}')
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = (args.target, args.port)

        sock.bind(server)
        sock.listen(1)

        buf = b''
        work_dir = os.getcwd()
        client, _ = sock.accept()

        while True:
            client.send(f'[{os.environ.get( "USERNAME" )}]-[{work_dir}]$'.encode())
            while '\n' not in buf.decode():
                buf += client.recv(64)
            output, work_dir = execute(buf.decode(), work_dir)
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

