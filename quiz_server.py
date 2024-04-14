import socket
from threading import Thread
import random

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address='127.0.0.1'
port=5000

server.bind((ip_address,port))
server.listen()

list_of_clients=[]
nicknames=[]

print("Server has started...")

questions=[
    "Which is the largest country in the world by area? \n a.Brazil \n b.Russia \n c.China \n d.USA",
    "Which is the most populous country in the world? \n a.China \n b.USA \n c.Indonesia \n d.India",
    "Which is the largest planet of our solar system? \n a.Jupiter \n b.Earth \n c.Saturn \n. d.Neptune",
    "How many wonders are there in the world? \n a.5 \n b.9 \n c.7 \n d.8",
    "Which is the hardest known substance? \n a.Coal \n b.Diamond \n c.Brass \n d.Aluminium",
    "Which of the following is an inert gas? \n a.Oxygen \n b.Nitrogen \n c.Carbon dioxide \n d.Argon",
    "Which country gifted the Statue of Liberty to the USA? \n a.Russia \n b.France \n c.Germany \n d.Italy",
    "What is the capital of India? \n a.New Delhi \n b.Mumbai \n c.Bengaluru \n d.Chennai",
    "Which is the smallest country in the world by area? \n a.Canada \n b.Belgium \n c.Vatican City \n d.San Marino",
    "Who inevented the light bulb? \n a.Albert Einstein \n b.Issac Newton \n c.Thomas Edison \n d.Michael Faraday"
]

answers=["b","d","a","c","b","d","b","a","c","c"]

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn,nickname):
    score=0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should a,b,c, or d\n.".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index,question,answer=get_random_question_answer(conn)
    while True:
        try:
            message=conn.recv(2048).decode('utf-8')
            if message:
                if message.split(": ")[-1].lower()==answer:
                    score+=1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send(f"Incorrect! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index,question,answer=get_random_question_answer(conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


while True:
    conn, addr=server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname=conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print(nickname + " connected!")
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()
