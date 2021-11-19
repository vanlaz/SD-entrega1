from __future__ import print_function
import sys
import Pyro4.util
import json

sys.excepthook = Pyro4.util.excepthook

servidor = Pyro4.Proxy("PYRONAME:servidor.carona")

# colocar em contato passageiro e motorista
# um motorista vai fazer uma viagem entre origem e destino e anuncia que tem interesse em aceitar passageiros
# um potencial passageiro tem interesse numa viagem como um carona e se cadastra, anunciando interesse em pegar viagens

# passageiro
def carrega_passageiras():
    with open('listaPassageiras.json.json') as json_file:
        lista_passagerias = json.load(json_file)
    print(lista_passagerias)
    return lista_passagerias

# cadastra a carona, verifica a lista de interesse para viagens cadastradas por motoristas, inclui a corrida na lista de interesse
def consulta(idUser):
    destino = input("Para onde deseja ir? ").strip()
    origem = input("Aonde está? ").strip()
    data = input("Quando deseja ir? ").strip()
    qtdePessoas = input("Em quantas pessoas? ").strip()
    if origem and destino and data:
        respConsulta = servidor.consulta(origem, destino, data, 0)
        idCorrida = interesse(data, origem, idUser, destino, qtdePessoas)
        if (not (respConsulta)):
            adicionarALista = input(
                "Não encontrei nada deseja adicionar a sua lista de interesse? 1 - SIM/ 0 - NÃO\n").strip()
            if adicionarALista == '0':
                print('Tudo bem! Nos vemos na próxima\n')
                servidor.cancelar_interesse_em_carona(idCorrida)
        else:
            servidor.cancelar_interesse_em_carona(idCorrida)
            print(respConsulta)


# Registro de interesse em eventos (1,1)
def interesse(data, origem, idUser, destino, qtdePessoas):
    id = servidor.interesse_em_carona(idUser, origem, destino, data, qtdePessoas)
    return id


# remocao da lista de interesse
def remove_interesse(idUser):
    remover = input("Digite o número da viagem que deseja remover").strip()
    servidor.cancelar_interesse_em_carona(remover)
    print("Feito! Nos vemos na próxima!\n")


# TODO

def main():
    carrega_passageiras()
    escolha = ''
    idUser = ''
    while escolha != '0':
        escolha = input("\nOlá, o que precisa hoje? \n "
                        " 2 - Buscar viagem \n"
                        " 3 - Remover Viagem \n"
                        " 0 - Sair\n").strip()
        if escolha != '0':
            if escolha == '2':
                consulta(idUser)
            else:
                remove_interesse(idUser)
    print("Até a próxima!")


if __name__ == "__main__":
    main()
