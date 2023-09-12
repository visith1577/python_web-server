# Web server using python sockets

## Author
 - Name: K.A.V.C Kumarapperuma
 - Index No : 21001057
 - Admission No : 2021/CS/105 

## Introduction
This is a simple web server to serve the PHP and HTML files as pat of SCS2205 assignment. It runs on `localhost:2728`, and it can identify the `index.php` files automatically.  you can simply search `localhost:2728` and the server will automatically navigate to the `index.php` file. Or you can rename the php file and replace it to `form.php` to view a form.

## Libraries used
- ### socket
  - It helps to create the socket and bind it with our server, it returns the web browser request to our server, and helps to send the server request to the web browser. 
- ### subprocess
  - This library helps to run php file by passing  the following on to the terminal `php <filename>. php`
- ### os
  - Handle the system functions
- ### threading
  - To provide multi-thread capabilities to the server.This allows the server to handle multiple requests
- ### functools
  - From functools , partial is used to pass the arguements and request handle function to the thread.
- ### time
  - Sleep is used instead of asyncio to handle a minor error that cold occur due to threading.

## How to run
Run main.py to start the Server. After that, go to your browser and browse to `localhost:2728` or click on the link that appear in the terminal.
To run your own .php files go to the htdocs directory and replace the `index.php` file with your files.

____



## Run from terminal

```bash
  python main.py
```
    