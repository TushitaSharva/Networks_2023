import socket

dst_ip = "10.0.1.2"

s = socket.socket()
print("Socket successfully created")

dport = 12346

s.bind((dst_ip, dport))
print("socket binded to %s" % (dport))

s.listen(5)
print("socket is listening")
my_dict = {}


def handle_get(c, rec_message):
  arg1 = rec_message.split("=")
  key_val = arg1[1].split()[0]
  if key_val in my_dict:
    msg = "Get successful! The value is " + my_dict[key_val] + "\r\n\r\n"
  else:
    msg = "Get unsuccessful! The entered key element is not found!\r\n\r\n"
  c.send(msg.encode())


def handle_put(c, rec_message):
  arg1 = rec_message.split("=")
  key_value = arg1[1].split("/")[0]
  value = arg1[2].split()[0]
  if key_value in my_dict:
    my_dict[key_value] = value
    print(my_dict)
    c.send(
        "Replacing the previous value of this key! Successful Anyways :)\r\n\r\n"
        .encode())
  else:
    my_dict[key_value] = value
    print(my_dict)
    c.send("Put successful!\r\n\r\n".encode())


def handle_delete(c, rec_message):
  arg1 = rec_message.split("=")
  key_val = arg1[1].split()[0]
  if key_val in my_dict:
    my_dict.pop(key_val)
    msg = "Delete successful!\r\n\r\n"
  else:
    msg = "Delete unsuccessful! The entered key element not found!\r\n\r\n"
  print(my_dict)
  c.send(msg.encode())


switch = {"PUT": handle_put, "GET": handle_get, "DELETE": handle_delete}

while True:

  c, addr = s.accept()
  print('Got connection from', addr)

  while True:
    rec_message = c.recv(1024).decode()
    print("Server received the message: " + rec_message)

    req = rec_message.split()[0]

    if len(rec_message) == 0:
      break
    elif req in switch:
      switch[req](c, rec_message)

c.close()
