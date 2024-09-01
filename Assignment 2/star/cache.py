import socket

# dictionary DS
cache={}


cache_ip="10.0.1.2"
serverIP="10.0.1.3"

s = socket.socket()
s1= socket.socket()
print ("Sockets successfully created")

dport = 12346
s_port= 12345

s.bind((cache_ip, dport))
print ("socket binded to %s" %(dport))

s1.connect((serverIP,s_port))

s.listen(5)
print ("socket is listening")

while True:
  c, addr = s.accept()
  print ('Got connection from', addr )
  while True:
      r = c.recv(1024).decode()
      original_message = r

      if len(r)==0:
          break

      print("\nCache received: "+ r)

      r = r.replace(' ','')
      r = r.replace("HTTP/1.1\r\n\r\n",'')

      x = r.split("/")

      if r[:3]=="PUT" :
          arg1 = x[2].split("=")[1]
          arg2 = x[3].split("=")[1]
          s1.send(original_message.encode())
          server_reply = s1.recv(1024).decode()
          code = server_reply.split(' ')
          if code[1] == '200':
              cache[arg1]=arg2
          print(cache)
          c.send(server_reply.encode())

      elif r[:3]=="GET":
          y = x[1].split("=")
          if y[1] in cache:
              c.send('HTTP/1.1 200 OK \nThe value is: '+cache[y[1]]+'\r\n\r\n'.encode())
          else :
              s1.send(original_message.encode())
              server_reply = s1.recv(1024).decode()
              z = server_reply.split()

              if z[1] == '200' :
                  print(server_reply)
                  server_reply.replace(" ", '')
                  value = server_reply.split(":")
                  cache[y[1]] = value[1]
              print(cache)
              c.send(server_reply.encode())

      elif r[:6]=="DELETE":
          y = x[2].split("=")
          if y[1] in cache :
              cache.pop(y[1])
          s1.send(original_message.encode())
          server_reply = s1.recv(1024).decode()
          print(cache)
          c.send(server_reply.encode())

      else:
          c.send('HTTP/1.1 400 BAD REQUEST\r\n\r\n')

  c.close()
