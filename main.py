import os
import socket

import subprocess
import threading

from functools import partial
import time


HOST = '127.0.0.1'
PORT = 2728
ROOT = 'htdocs'


def php_obj(data):

    php_string = "$data = array(\n"

    for v in data:
        php_string += f"    '{v[0]}' => '{v[1]}',\n"

    php_string += ");"

    return php_string



def handle_request(conn, addr):
    # print(addr)
    temp_file_location = ""
    output = ""
    parameters = ""

    request = conn.recv(1024*4).decode("utf-8").split("\r\n")
    path = request[0].split(" ")[1]
    print(path)

    if 1 < len(path.split("?")):            
        path, parameters = path.split("?")
        print(parameters)

    method = request[0].split(" ")[0]

    file_path = os.path.join(ROOT, path.lstrip("/"))
    # print("check 1 : ", file_path)

    if os.path.exists(file_path):
        # print("check 2 : ", file_path)

        

        if os.path.isdir(file_path):
            if os.path.exists(os.path.join(file_path,"index.php")):
                file_path = os.path.join(file_path,"index.php")
            elif os.path.exists(os.path.join(file_path,"index.html")):
                file_path = os.path.join(file_path,"index.html")
                

        
        # print("check 3 : ", file_path)
        # print("check 4 : ", os.path.join(file_path, "index.php"))

        if not(os.path.isdir(file_path)):

            

            if file_path.endswith(".php"):

                if method == "POST":

                    post_data = request[request.index('')+1].split("&")
                    post_data = list(map(lambda x: [ it for it in x.split("=")],post_data ))
                    print(post_data)

                    # content_length = int(request[1].split(':')[1]) 
                    # post_data = conn.recv(content_length).decode('utf-8')
                    # output = subprocess.check_output(['php', file_path], input=post_data.encode('utf-8'))

                    print("PHP object : " , php_obj(post_data))


                    php_text = "<?php " + php_obj(post_data) + "\n $_POST = $data; ?> "


                    with open(file_path, 'r') as php_file:
                        php_code = php_file.read()
                        
                    directory_path = os.path.dirname(file_path)
                    file_name = "." + "temp" + "_" + os.path.basename(file_path)
                    file_path = os.path.join(directory_path,file_name)
                    temp_file_location = file_path


                    with open(file_path, 'w') as php_file:
                        php_file.write(php_text + php_code)

                # print(parameters)

                if method == "GET" and parameters != "": 
                    get_data = parameters.split("&")
                    get_data = list(map(lambda x: [ it for it in x.split("=")], get_data))  

                    php_text = "<?php " + php_obj(get_data) + "\n $_GET = $data; ?> "

                    with open(file_path, 'r') as php_file:
                        php_code = php_file.read()

                    directory_path = os.path.dirname(file_path)
                    file_name = "." + "temp" + "_" + os.path.basename(file_path)
                    file_path = os.path.join(directory_path, file_name)
                    temp_file_location = file_path

                    with open(file_path, 'w') as php_file:
                        php_file.write(php_text + php_code)

                    # print(post_data)
                
                        
                try:
                    # Execute PHP script and get output
                    # print("subp: ", file_path)
                    print("subp: ", file_path)

                    time.sleep(2)

                    output = subprocess.run(
                        ["php", file_path], capture_output=True, text=True, check=True
                    ).stdout

                    response = "HTTP/1.1 200 OK\r\n\r\n" + output
                    
                except subprocess.CalledProcessError as e:
                    response = "HTTP/1.1 500 Internal Server Error\r\n\r\nInternal Server Error\n"  + e.stderr
                
                # print(temp_file_location)
                    
                if temp_file_location:    
                    try:
                        os.remove(temp_file_location)
                        print(f"File '{temp_file_location}' has been deleted.")
                    except OSError as e:
                        print(f"Error deleting file: {e}")

            else:
                try:
                    with open(file_path, "rb") as file:
                        output = file.read().decode("utf-8")
                        response = "HTTP/1.1 200 OK\r\n\r\n" + output
                   
                except Exception as e:
                    response = "HTTP/1.1 500 Internal Server Error\r\n\r\n" + str(e)
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found" 

    else:
        response = "HTTP/1.1 403 Forbidden\r\n\r\nForbidden"

    # if os.path.exists(file_path) and os.path.commonpath([ROOT, file_path]) == ROOT:
        

    #     if os.path.isdir(file_path):

            

    #         if os.path.exists(os.path.join(file_path, "index.php")):
    #             file_path = os.path.join(file_path, "index.php")
    #         elif os.path.exists(os.path.join(file_path, "index.html")):
    #             file_path = os.path.join(file_path, "index.html")

    #         if method == "GET":
    #             if path.endswith('.php'):
                    

    #                 proc = subprocess.run(
    #                     ["php", file_path], capture_output=True, text=True, check=True
    #                 )
    #                 output = proc.stdout

    #             else:
    #                 try:
    #                     with open(file_path, "rb") as file:
    #                         output = file.read().decode("utf-8")
    #                         response = "HTTP/1.1 200 OK\r\n\r\n" + output
                    
    #                 except Exception as e:
    #                     response = "HTTP/1.1 500 Internal Server Error\r\n\r\n" + str(e)
            
    #         if method == 'POST':
    #             # Handle POST request
    #             content_length = int(request.split()[6])
    #             body = conn.recv(content_length)
    #             print(body)
    #             # Pass POST data to PHP as command line arg
    #             proc = subprocess.run(["php", ROOT + file_path, body], stdout=subprocess.PIPE)  
    #             output = proc.stdout.decode('utf-8')

    #     else:
    #         response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"

    # else:
    #     response = "HTTP/1.1 403 Forbidden\r\n\r\nForbidden"

    response = "HTTP/1.1 200 OK\r\n\r\n" + output
    conn.sendall(response.encode('utf-8'))
    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is running on http://{HOST}:{str(PORT)}")

    while True:
        conn, addr = s.accept()
        try:
            thread = threading.Thread(
                target=partial(handle_request, conn, addr)
            )
        except:
            print("Connection failed")

        thread.start()
