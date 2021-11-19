from __future__ import print_function
import sys
import Pyro4.util
import json

sys.excepthook = Pyro4.util.excepthook

servidor = Pyro4.Proxy("PYRONAME:servidor.carona")


def carrega_motoristas():
    with open('listaMotoristas.json') as json_file:
        lista_motoristas = json.load(json_file)
    id_user = f"{lista_motoristas[0]['nome']}{lista_motoristas[0]['telefone']}"
    result = [lista_motoristas, id_user]
    print(result)
    return result


# cadastra a viagem do motorista, verifica a lista de interesse para caronas interessadas,
# inclui a corrida na lista de interesse
def consulta(id_user):
    destino = input("Para onde deseja ir? ").strip()
    origem = input("Aonde está? ").strip()
    data = input("Quando deseja ir? ").strip()
    if origem and destino and data:
        # Sugestão: usar uma constante, que pode ser definida em servidor.py, ao invés do número 1.
        # Exemplo é usar MOTORISTA = 1 e na chamada abaixo simplesmente usar servidor.consulta(origem, destino,
        # data, MOTORISTA)
        res_consulta = servidor.consulta(destino, origem, data, 1)
        # registro de interesse em eventos
        id_corrida = servidor.interesse_em_passageira(destino, origem, data, id_user)
        print(data)
        print(f'motorista id corrida {id_corrida}')
        if not res_consulta:
            adicionar_a_lista = input(
                "Não encontrei nada deseja adicionar a sua lista de interesse? 1 - SIM/ 0 - NÃO\n").strip()
            if adicionar_a_lista == '0':
                print('Tudo bem! Nos vemos na próxima\n')
                servidor.cancelar_interesse_em_passageira(id_corrida)
        else:
            servidor.cancelar_interesse_em_passageira(id_corrida)
            print(res_consulta)


# remocao da lista de interesse
def remove_interesse(id_user):
    remover = input("Digite o número da viagem que deseja remover").strip()
    servidor.cancelar_interesse_em_passageira(remover)
    print("Feito! Nos vemos na próxima!\n")


def main():
    escolha = ''
    id_user = carrega_motoristas()[1]
    while escolha != '0':
        escolha = input("Olá motorista, o que precisa hoje?\n"
                        "1 - Buscar viagem \n"
                        "2 - Remover Viagem \n"
                        "0 - Sair\n").strip()
        if escolha != '0':
            if escolha == '1':
                consulta(id_user)
            else:
                remove_interesse(id_user)
    print("Até a próxima!")


if __name__ == "__main__":
    main()
