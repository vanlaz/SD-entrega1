from __future__ import print_function
import Pyro4
from datetime import datetime


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
#
class Servidor(object):
    def __init__(self):
        self.passageira = []
        self.motorista = []
        self.procura_por_passageira = []
        self.procura_por_carona = []

    # retorna lista de motoristas
    def mostra_a_lista(self):
        return self.Motorista

    # invoca lista de viagens cadastradas conforme o tipo de usuario
    def consulta(self, destino, origem, data, tp_user):
        # se passageiro, procure por motoristas
        if tp_user == 0:
            lista_de_viagens = self.procura_por_passageira
        else:
            lista_de_viagens = self.procura_por_carona
        print(lista_de_viagens)

    def notifica_passageira(self, origem, destino, data, id_user):
        for viagens in self.procura_por_carona:
            if viagens[2] == data and viagens[0] == origem and viagens[1] == destino:
                print(f'passageira, vooê tem uma viagem compativel com a motorista {id_user}')

    def notifica_motorista(self, origem, destino, data, id_user):
        for viagens in self.procura_por_passageira:
            if viagens[2] == data and viagens[0] == origem and viagens[1] == destino:
                print(f'motorista, vooê tem uma viagem compativel a passageira {id_user}')

    # Clientes devem informar seu nome, telefone e chave pública. (0,2)
    # Sugestão: receber uma assinatura digital, que pode ser um texto (challenge)
    # que será encriptado pela pessoa cliente usando sua própria chave privada,
    # e que podemos solicitar que nos seja informado codificado em base 64,
    # para que possamos tratar com texto.
    # Fica assim:
    #  - pessoa se cadastra informado seus dados: ('seiti', '555-5555', 'VARIOSCHARSDAMINHACHAVEPUBLICA')
    #  - pessoa pega um texto qqer (pode ser seu próprio id, digamos '42') e a encripta usando sua chave privada;
    #    Depois a codifica usando base64, obtendo por exemplo '89163501bardt2e3n'
    #  - pessoa quer subscrever interesse: (1, 'São Paulo', 'Rio de Janeiro', '2021-12-25', '89163501bardt2e3n')
    #  - servidor recebe os dados, desencripta o '89163501bardt2e3n' usando a chave pública da própria pessoa
    #    e consegue ler o texto original, que é 42. Bate com o id da própria pessoa, então ela tem a chave privada
    #    e podemos assumir que é a própria pessoa solicitando interesse.
    # cadastra interesse do passageiro em carona
    def interesse_em_carona(self, origem, destino, data, id_user):
        # cria id unica para cada carona e retira caracteres especiais
        id_corrida = str(datetime.now()).replace(":", "").replace("-", "").replace(".", "").replace(" ", "")
        self.procura_por_carona.append([origem, destino, data, id_corrida, id_user])
        self.notifica_motorista(origem, destino, data, id_user)
        return id_corrida

    # Sugestão: ver sugestão acima
    # cadastra interesse do motorista em oferecer carona
    def interesse_em_passageira(self, origem, destino, data, id_user):
        # cria id unica para cada viagem e retira caracteres especiais
        id_corrida = str(datetime.now()).replace(":", "").replace("-", "").replace(".", "").replace(" ", "")
        self.procura_por_passageira.append([origem, destino, data, id_corrida, id_user])
        self.notifica_passageira(origem, destino, data, id_user)
        return id_corrida

    # cancela subscription do motorista para notificacoes de possiveis passageiros
    def cancelar_interesse_em_passageira(self, id_corrida):
        for i in range(0, len(self.procura_por_passageira)):
            if self.procura_por_passageira[i][0] == id_corrida:
                self.procura_por_passageira.pop(i)

    # cancela subscription do passageiro para notificacoes de possiveis viagens
    def cancelar_interesse_em_carona(self, id_corrida):
        for i in range(0, len(self.procura_por_carona)):
            if self.procura_por_carona[i][0] == id_corrida:
                self.procura_por_carona.pop(i)


def main():
    Pyro4.Daemon.serveSimple(
        {
            Servidor: "servidor.carona"
        },
        ns=True)


if __name__ == "__main__":
    main()
