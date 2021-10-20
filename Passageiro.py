from __future__ import print_function
import sys
import Pyro4
import Pyro4.util

sys.excepthook = Pyro4.util.excepthook

servidor = Pyro4.Proxy("PYRONAME:servidor.carona")

# colocar em contato passageiro e motorista
# um motorista vai fazer uma viagem entre origem e destino e anuncia que tem interesse em aceitar passageiros
# um potencial passageiro tem interesse numa viagem como um carona e se cadastra, anunciando interesse em pegar viagens

# passageiro

# cadastra a carona, verifica a lista de interesse para viagens cadastradas por motoristas, inclui a corrida na lista de interesse
def consulta(idUser):
    if(not(idUser)):
        print("Antes de agendar a viagem, precisamos de um cadastro!\n")
        idUser = cadastro()
    destino = input("Para onde deseja ir? ").strip()
    origem = input("Aonde está? ").strip()
    data = input("Quando deseja ir? ").strip()
    qtdePessoas = input("Em quantas pessoas? ").strip()
    if origem and destino and data:
        respConsulta = servidor.consulta(origem, destino, data, 0)
        idCorrida = interesse(data, origem, idUser, destino, qtdePessoas)
        if(not(respConsulta)):
            adicionarALista = input(
                "Não encontrei nada deseja adicionar a sua lista de interesse? 1 - SIM/ 0 - NÃO\n").strip()
            if adicionarALista == '0':
                print('Tudo bem! Nos vemos na próxima\n')
                servidor.cancelarInteresseEmCarona(idCorrida)
        else:
            servidor.cancelarInteresseEmCarona(idCorrida)
            print(respConsulta)

# Registro de interesse em eventos (1,1)
def interesse(data, origem, idUser, destino, qtdePessoas):

    id = servidor.interesseEmCarona(idUser, origem, destino, data, qtdePessoas, signature)
    return id

#cadastro de usuario
def cadastro ():
    print("Novo por aqui? Cadastre-se\n")
    nome = input("Qual seu nome? ").strip().encode()
    telefone = input("Certo! \n Qual seu telefone?").strip().encode()
    encryptor = PKCS1_OAEP.new(key)
    nome = encryptor.encrypt(nome)
    telefone = encryptor.encrypt(telefone)
    if nome and telefone:
        idUser = servidor.cadastroUsuario(nome, telefone, publickey, 0) #O ultimo campo - se 1 motorista, se 0 passageiro
        print(idUser)
    return idUser

#remocao da lista de interesse
def removeInteresse(idUser):
    remover = input("Digite o número da viagem que deseja remover").strip()
    servidor.cancelarInteresseEmCarona(remover)
    print("Feito! Nos vemos na próxima!\n")
#TODO

def main():

    escolha = ''
    idUser = ''
    while escolha != '0':
        escolha = input("\nOlá, o que precisa hoje? \n "
                        "1 - Cadastro \n"
                        " 2 - Buscar viagem \n"
                        " 3 - Remover Viagem \n"
                        " 0 - Sair\n").strip()
        if escolha != '0':
            if escolha == '1':
                idUser = cadastro()
            elif escolha == '2':
                consulta(idUser)
            else:
                removeInteresse(idUser)
    print("Até a próxima!")


if __name__ == "__main__":
    main()