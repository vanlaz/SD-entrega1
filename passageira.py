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
    with open('listaPassageiras.json') as json_file:
        lista_passagerias = json.load(json_file)
    id_user = f"{lista_passagerias[0]['nome']}{lista_passagerias[0]['telefone']}"
    result = [lista_passagerias, id_user]
    print(result)
    return result


# cadastra a carona, verifica a lista de interesse para viagens cadastradas por motoristas,
# inclui a corrida na lista de interesse
def consulta(id_user):
    destino = input("Para onde deseja ir? ").strip()
    origem = input("Aonde está? ").strip()
    data = input("Quando deseja ir? ").strip()
    if origem and destino and data:
        res_consulta = servidor.consulta(destino, origem, data, 0)
        # Registro de interesse em eventos (1,1)
        id_corrida = servidor.interesse_em_carona(destino, origem, data, id_user)
        print(data)
        print(f'passageira id corrida {id_corrida}')
        if not res_consulta:
            adicionar_a_lista = input(
                "Não encontrei nada deseja adicionar a sua lista de interesse? 1 - SIM/ 0 - NÃO\n").strip()
            if adicionar_a_lista == '0':
                print('Tudo bem! Nos vemos na próxima\n')
                servidor.cancelar_interesse_em_carona(id_corrida)
        else:
            servidor.cancelar_interesse_em_carona(id_corrida)
            print(res_consulta)


# remocao da lista de interesse
def remove_interesse(id_user):
    remover = input("Digite o número da viagem que deseja remover").strip()
    servidor.cancelar_interesse_em_carona(remover)
    print("Feito! Nos vemos na próxima!\n")


def main():
    escolha = ''
    id_user = carrega_passageiras()[1]
    while escolha != '0':
        escolha = input("\nOlá passageira, o que precisa hoje? \n"
                        " 1 - Buscar viagem \n"
                        " 2 - Remover Viagem \n"
                        " 0 - Sair\n").strip()
        if escolha != '0':
            if escolha == '1':
                consulta(id_user)
            else:
                remove_interesse(id_user)
    print("Até a próxima!")


if __name__ == "__main__":
    main()
