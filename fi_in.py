#!/usr/bin/python
import hashlib
import socket
import threading
import hmac


answer = input("Choose an option~\nClient or Server : ").lower()
print("\nEnter 'exit' to quit\n")



if(answer == 'server'):
    extension = input('\nEnter expected file extension(eg:pdf, docx)~')
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65433        # Port to listen on (non-privileged ports are > 1023)
    print('\nListening. . .')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        
        def handle_client(client_socket):
            
            while True:
                # print out what the client sends
                data = client_socket.recv(4096)

                #seperating message and the hash
                mess = data.decode("utf-8")[0:len(data.decode("utf-8"))-32]

                #compare hashes digests
                sha_hash = data.decode("utf-8")[len(data.decode("utf-8"))-32:]
                
                
                print("\n\n[*] Received: %s" % mess)

                #re hashing for comparison
                hasher =  hmac.new(b'abc123', bytes(mess, 'utf8'))
                
                #second HMAC
                sha_hash2 = hasher.hexdigest()

                
                print("\nIntegrity Verificaion....")
                if(hmac.compare_digest(sha_hash, sha_hash2)):
                    print("~VERIFIED~")
                    data2 = open('checked_file.' + extension, 'w')
                    data2.write(mess)
                    data2.close()

                else:
                    print("Verification Failed\n")
                #send back a packet
                client_socket.send("ACK!".encode())
       
        while(True):
            client,addr = s.accept()
            client_handler = threading.Thread(target=handle_client,args=(client,))
            client_handler.start()

if(answer == 'client'):


    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65433        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while(True):

            #getting file name 
            filename = input("\nEnter filename: ") 
            
                    
            #check for the message
            if(filename == 'exit'):
                break
            else:
                #getting file data
                data = open(filename, 'r')
                message = data.read(1024)
                data.close()

                #Creating a Hmac with the key of abc123
                hashing =  hmac.new(b'abc123', bytes(message, 'utf8'))
            

                #hashing of the message and adding it to the message
                n_message = message + hashing.hexdigest()
                s.sendall(bytes(n_message, 'utf8'))
              
                data = s.recv(1024)
                print('\nSuccess')




