from __future__ import print_function
import sys
import Pyro4
import Pyro4.util

import asyncio
sys.excepthook = Pyro4.util.excepthook

servidor = Pyro4.Proxy("PYRONAME:servidor.carona")

#cadastra a viagem do motorista, verifica a lista de interesse para caronas interessadas, inclui a corrida na lista de interesse
def consulta(idUser):
    if(not(idUser)):
        print("Antes de agendar a viagem, precisamos de um cadastro!\n")
        idUser = cadastro()
    destino = input("Para onde deseja ir? ").strip()
    origem = input("Aonde está? ").strip()
    data = input("Quando deseja ir? ").strip()
    if origem and destino and data:
        ## Sugestão: usar uma constante, que pode ser definida em servidor.py, ao invés do número 1.
        ## Exemplo é usar MOTORISTA = 1 e na chamada abaixo simplesmente usar servidor.consulta(origem, destino, data, MOTORISTA)  
        respConsulta = servidor.consulta(origem, destino, data, 1)   
        idCorrida = interesse(data, origem, idUser, destino)
        if (not (respConsulta)):
            adicionarALista = input(
                "Não encontrei nada deseja adicionar a sua lista de interesse? 1 - SIM/ 0 - NÃO\n").strip()
            if adicionarALista == '0':
                print('Tudo bem! Nos vemos na próxima\n')
                servidor.cancelarInteresseEmPassageiro(idCorrida)
        else:
            servidor.cancelarInteresseEmPassageiro(idCorrida)
            print(respConsulta)

# Registro de interesse em eventos (1,1)
## Sugestão: como esta função não adiciona comportamente adicional, 
## removê-la e usar diretamente o "servidor.interesseEmPassageiro" no lugar
def interesse(data, origem, idUser, destino):
    print(data)
    id = servidor.interesseEmPassageiro(idUser, origem, destino, data, signature)
    print(id)

#cadastro de usuario
def cadastro ():
    print("Novo por aqui? Cadastre-se\n")
    nome = input("Qual seu nome? ").strip().encode()
    telefone = input("Certo! \n Qual seu telefone?").strip().encode()
    ## Sugestão: incluir mais um campo, onde o interessado informe sua chave pública.
    ## Isto pode ser armazenado junto do nome e telefone e é usado depois para 
    ## confrontar solicitações posteriores (como no exercício de 0.25).
    # encryptor = PKCS1_OAEP.new(key)
    # nome = encryptor.encrypt(nome)
    # telefone = encryptor.encrypt(telefone)
    if nome and telefone:
        idUser = servidor.cadastroUsuario(nome, telefone, 1) #O ultimo campo - se 1 motorista, se 0 passageiro
    return idUser

#remocao da lista de interesse
def removeInteresse(idUser):
    remover = input("Digite o número da viagem que deseja remover").strip()
    servidor.cancelarInteresseEmPassageiro(remover)
    print("Feito! Nos vemos na próxima!\n")

#comunicacao assincrona para notificacao
async def notificaMotorista(idUser, data, origem, destino):
    servidor._pyroAsync()
    asyncresult = servidor.consulta(origem, destino, data, 1)
    while True:
        viagens = servidor.consulta(origem, destino, data, 1)
        print(viagens)
        if viagens != 0:
            return "AAEEEEEE"
        await asyncio.sleep(1)

def main():

    escolha = ''
    idUser = ''
    while escolha != '0':
        escolha = input("Olá, o que precisa hoje?\n "
                        "1 - Cadastro \n"
                        "2 - Buscar viagem \n"
                        "0 - Sair\n").strip()
        if escolha != '0':
            if escolha == '1' and idUser != '':
                idUser = cadastro()
            elif escolha == '2':
                consulta(idUser)
            else:
                removeInteresse(idUser)
    print("Até a próxima!")


if __name__ == "__main__":
    main()
