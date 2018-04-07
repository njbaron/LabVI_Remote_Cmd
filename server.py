import sys
import socket
import threading
import datetime
from subprocess import check_output
from time import sleep

if len(sys.argv) != 2:
    print("[ERROR] " + str(sys.argv[0]) + " Incorrect command line arguments.")
    exit(1)
else:
    print("Welcome to", str(sys.argv[0]), "\n")

time_out = 1
client_count = 0
response_size = 1024

def handle_client(connection, address):
    global client_count
    client_count += 1
    arguments = str(connection.recv(response_size))[2:-1].split(",")
    print("[LOG]", sys.argv[0], datetime.datetime.now().strftime("%H:%M:%S.%f"), "Connection from:", str(address),
          "Instruction:", arguments[2])
    print("Client Count:", client_count)
    #print(arguments[2].split(" "))
    #print(check_output(arguments[2].split(" ")))
    for i in range(int(arguments[0])):
        result = (datetime.datetime.now().strftime("%H:%M:%S.%f") + " " + str(check_output(arguments[2].split(" ")))[2:-1]).encode()
        while len(result) > response_size:
            connection.send(result[0:1023])
            result = result[1024:]
        sleep(int(arguments[1]))
    connection.close()
    client_count -= 1
    print("Client Count:", client_count)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", int(sys.argv[1])))
sock.listen(1)

while True:
    connection, address = sock.accept()
    connection.settimeout(time_out)
    threading.Thread(target=handle_client, args=(connection, address)).start()



