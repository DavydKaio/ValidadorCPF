from socket import *
import json
import random

serverName = "localhost"
serverPort = 3001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


def operacao():
  requestId = random.randint(1, 10000)
  CPF = input("Digite o CPF ou 0 para encerrar conexão: ")

  data = {"requestId": requestId, "CPF": CPF}

  return json.dumps(data)


while True:
  comando = operacao()
  clientSocket.send(comando.encode(encoding='utf-8'))
  print("Preparando pra enviar")
  novocomando = clientSocket.recv(1024)
  print("Enviou")
  print("From server: ", novocomando)

  obj = json.loads(comando)
  if (obj["CPF"] == "0"):
    break

clientSocket.close()