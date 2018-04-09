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
running = True

def tcp_server():
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.bind(("localhost", int(sys.argv[1])))
    sock_tcp.listen(1)

    while running:
        connection, address = sock_tcp.accept()
        connection.settimeout(time_out)
        threading.Thread(target=handle_client_tcp, args=(connection, address), daemon=True).start()

def handle_client_tcp(connection, address):
    global client_count
    client_count += 1
    arguments = str(connection.recv(response_size))[2:-1].split(",")
    print("[LOG]", sys.argv[0], datetime.datetime.now().strftime("%H:%M:%S.%f"), "Connection from:", str(address),
          "Instruction:", arguments[2])
    print("Client Open:", client_count)
    try:
        for i in range(int(arguments[0])):
            result = (datetime.datetime.now().strftime("%H:%M:%S.%f") + " " + str(check_output(arguments[2]))[
                                                                              2:-1]).encode()
            while len(result) > response_size:
                connection.send(result[0:1023])
                result = result[1024:]
            sleep(int(arguments[1]))
    except ConnectionResetError:
        print("Connection Lost")
    except:
        print("Output Failed")
    connection.close()
    client_count -= 1
    print("Client Close:", client_count)

def udp_server():
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.bind(("localhost", int(sys.argv[1])))

    while running:
        data, address = sock_udp.recvfrom(4096)
        threading.Thread(target=handle_client_udp, args=(sock_udp, data, address), daemon=True).start()
    sock_udp.close()

def handle_client_udp(sock, data, address):
    global client_count
    client_count += 1
    arguments = str(data)[2:-1].split(",")
    print("[LOG]", sys.argv[0], datetime.datetime.now().strftime("%H:%M:%S.%f"), "Message from:", str(address),
          "Instruction:", arguments[2])
    print("Client Open:", client_count)
    try:
        for i in range(int(arguments[0])):
            result = (datetime.datetime.now().strftime("%H:%M:%S.%f") + " " + str(check_output(arguments[2]))[
                                                                              2:-1]).encode()
            while len(result) > response_size:
                sock.sendto(result[0:1023], address)
                result = result[1024:]
            sleep(int(arguments[1]))
    except ConnectionResetError:
        print("Connection Lost")
    except:
        print("Output Failed")
    client_count -= 1
    print("Client Close:", client_count)


if __name__ == "__main__":
    running = True
    threading.Thread(target=udp_server, daemon=True).start()
    threading.Thread(target=tcp_server, daemon=True).start()

    try:
        while True:
            running = True
    finally:
        running = False



