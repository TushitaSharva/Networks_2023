import socket

# dictionary DS
data={}

dst_ip="10.0.1.3"

s = socket.socket()
print ("Socket successfully created")

dport = 12345

s.bind((dst_ip, dport))
print ("socket binded to %s" %(dport))

s.listen(5)
print ("socket is listening")

while True:
  c, addr = s.accept()
  print ('Got connection from', addr )

  while True:
      r = c.recv(1024).decode()
      if len(r)==0:
          break

      print("Server received the message: "+r)

      r = r.replace(" HTTP/1.1\r\n\r\n",'')
      r = r.replace(" ", '')

      x = r.split("=")

      if r[:3]=="PUT" :
          val = x[2]
          keyval = x[1].split("/")[0]
          if keyval in data:
              print('NOTE: Entered key value is already present!\n')
              c.send('HTTP/1.1 200 OK\r\n\r\n')
              data[keyval]=val
              print(data)
          else :
              data[keyval]=val
              print(data)
              c.send('HTTP/1.1 201 Created\r\n\r\n'.encode())

      elif r[:3]=="GET":
          y = r.split("=")
          if y[1] in data:
              reply='HTTP/1.1 200 OK \nThe Value is: '+data[y[1]]
          else :
              reply='HTTP/1.1 404 Value NOT FOUND\r\n\r\n'
          print(data)
          c.send(reply.encode())

      elif r[:6]=="DELETE":
          if x[1] in data :
              data.pop(x[1])
              c.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
          else :
              c.send('HTTP/1.1 404 Value NOT FOUND\r\n\r\n'.encode())

          print(data)

      else:
          print(data)
          c.send('HTTP/1.1 400 BAD REQUEST\r\n\r\n')

  c.close()
