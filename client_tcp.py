import sys
import socket

if len(sys.argv) != 6:
    print("[ERROR] " + str(sys.argv[0]) + " Incorrect command line arguments.")
    exit(1)
else:
    print("Welcome to", str(sys.argv[0]), "\n")

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
execution_count = sys.argv[3]
time_delay = sys.argv[4]
command = sys.argv[5]

time_out = 1
time_out_long = float(time_delay) + 0.5
response_size = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, server_port))
sock.settimeout(time_out)

sock.send(str(execution_count + "," + time_delay + "," + command).encode())

for i in range(int(execution_count)):
    result = ""
    try:
        while True:
            result += str(sock.recv(response_size))[2:-1]
            sock.settimeout(time_out)
    except:
        print("Result:")

    if result == "":
        print("[WARNING] " + sys.argv[0] + " Command Unsuccessful")
        exit(1)
    else:
        print(result)
    sock.settimeout(time_out_long)
