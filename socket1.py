# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr


running = False
while 1:
    data = conn.recv(1024)
    imp_data = str(data)
    print imp_data
    if not data:
        print 'data not found'
        conn.close()
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print 'Connected by', addr
        continue
        # break
    else :
        if imp_data == 'start' and not running:
            print 'video has started playing' # this means the video to start the script is executing
            running = True
        elif imp_data == 'stop' and running:
            print 'video has stopped playing' # this means the video to stop the script is executing
            running = False
        elif imp_data == 'close':
            conn.sendall(data)
            conn.close()
            break

    conn.sendall(data)

# conn.close()
