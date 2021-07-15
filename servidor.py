from socket import *
import json
import _thread

serverPort = 3001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(True)


def validador(CPF):
  if(len(CPF) == 14):
    if(CPF[3] == '.' and CPF[7] == '.' and CPF[11] == '-'):
      parte1 = CPF[:3]
      parte2 = CPF[4:7]
      parte3 = CPF[8:11]
      parte4 = CPF[12:14]

      CPF = parte1 + parte2 + parte3 + parte4

      try:
        for i in CPF:
          int(i)
        return 'CPF Validado'
      except ValueError:
        return 'CPF nao validado'
  else:
      return 'valor digitado nao tem o tamanho de um CPF ou fora do formato padrao'

def execucao(connection, client):
  print(connection)
  print(client)

  while True:
    received = connection.recv(1024)
    print("Servidor recebeu a mensagem ", received, " do cliente")

    dados_em_dict = json.loads(received)
    print("requestId: ", dados_em_dict["requestId"])
    print("CPF: " + dados_em_dict["CPF"])

    print(received)

    resultado = validador(dados_em_dict["CPF"])

    if (dados_em_dict["CPF"] == "0"):
      response = {"message": "operation terminated by the client"}
      connection.send(json.dumps(response).encode(encoding='utf-8'))
      break

    response = {"message": resultado}
    connection.send(json.dumps(response).encode(encoding='utf-8'))

    # if(len(dados_em_dict["CPF"]) > 1 and len(dados_em_dict["CPF"]) != 14):
    #   connection.send(json.dumps({"Valor digitado nao e um CPF ou o comando de saida"}).encode(encoding='utf-8'))

        # if (dados_em_dict["operation"] == "sair"):
        #     response = {"requestId": dados_em_dict["requestId"], "message": "operation terminated by the client"}
        #     connection.send(json.dumps(response).encode(encoding='utf-8'))
        #     print("Cliente encerrou a comunicação")
        #     break

        # if (dados_em_dict["operation"] not in comandos):
        #     response = {"requestId": dados_em_dict["requestId"], "errorCode": "402", "message": "Operation unavailable"}
        #     connection.send(json.dumps(response).encode(encoding='utf-8'))

  connection.close()


print("The server is ready to receive")
while True:
  print("Esperando nova conexao")
  connection, addr = serverSocket.accept()
  _thread.start_new_thread(execucao, (connection, addr))
