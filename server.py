#!/usr/bin/env python3

import os
import sys
import wolframalpha
import gtts

import socket
from serverKeys import *

# Default assignment
host = ''
s = None


server_port = int(sys.argv[2])
backlog_size = int(sys.argv[4])
socket_size = int(sys.argv[6])

# WolframAlpha client initialization
w_client = wolframalpha.Client(appid)

# Checkpoint 01 - Create socket on given port at 0.0.0.0 with exception handling
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,server_port))
    print("[Checkpoint 01] Created socket at 0.0.0.0 on port ", server_port)
    s.listen(backlog_size)
except socket.error as message:
    if s:
        s.close()
    print ("Could not open socket: " + str(message))
    sys.exit(1)

# Infinite loop
while True:
    # Checkpoint 02 and 07 - Listen for client
    print("[Checkpoint 02] Listening for client connections")
    client, address = s.accept()

    # Address of socket has pair of (host, port)
    print("[Checkpoint 07] Accepted client connection from {} on port {}".format(address[0], address[1]))
    data_byte = client.recv(socket_size)

    if data_byte:
        # Checkpoint 9 - Received data decode
        data = data_byte.decode()
        print ("[Checkpoint 09] Received question: " + data)

        # Checkpoint 10 to 13 - Wolframalpha and processing for TTS Response
        print ("[Checkpoint 10] Sending question to WolframAlpha: ", data)

        # Query to wolfram api and get response to text
        response = w_client.query(data)
        answer_string = next(response.results).text

        print("[Checkpoint 11] Received answer from WolframAlpha: " + answer_string)

        # TODO Parse to filter
        parsed_answer = answer_string

        # TODO FIX Call TTS object to parse into audio file
        #tts = gTTS(parsed_answer, lang='en')
        #tts.save("response.mp3")

        print("[Checkpoint 12] Speaking answer parsed for only Alphanumeric and Space characters: ", parsed_answer)

        string = "gtts-cli.py \"" + parsed_answer + "\" -l 'en-au' | mpg123 -q -"
        os.system(string)

        # Play audio file
        #os.system("gtts-cli.py ", parsed_answer, " -l 'en' | mpg123 -")

        # Checkpoint 13 - Sends answer encoded
        print("[Checkpoint 13] Sending answer: " + answer_string)
        client.send(answer_string.encode())

    # Close connection and await for next connection
    client.close()
