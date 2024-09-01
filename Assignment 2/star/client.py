import socket
import time


serverIP = "10.0.1.2"
dst_ip = "10.0.1.2"
s = socket.socket()
port = 12346
s.connect((dst_ip, port))

def handle_get():
	key_value = raw_input("Key: ")
	return 'GET /assignment1?key=' + key_value + ' HTTP/1.1\r\n\r\n'

def handle_put():
	key_value, value = raw_input("Key: "), raw_input("Value: ")
	return 'PUT /assignment1/key=' + key_value + '/value=' + value + ' HTTP/1.1\r\n\r\n'


def handle_delete():
	key_value = raw_input("Key: ")
	return 'DELETE /assignment1/key=' + key_value + ' HTTP/1.1\r\n\r\n'



switch = {
	'G':handle_get,
	'P':handle_put,
	'D':handle_delete
}

while True:

	print("\r\n\r\n---------------------------------\nPlease enter the HTTP request type")
        print("\nG-GET\nP-PUT\nD-DELETE\nE-exit\n")
        r = raw_input()

        if r == 'E':
            break
        elif r in switch:
            request = switch[r]()
            s.send(request.encode())
            start_time = time.time()
            response = s.recv(1024)
            print('\r\n\r\nTime: %s seconds\r\n' % round(time.time() - start_time, 5) + '\n\nClient received: ' + response.decode())

        else:
            print("Invalid HTTP request type! Please choose among G, P, D Or E.")
            continue


s.close()
