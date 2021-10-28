from __future__ import print_function
import Pyro4
from datetime import datetime


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
#
class Servidor(object):
    def __init__(self):
        self.Passageiro = []
        self.Motorista = []
        self.procuraPorPassageiro = []
        self.procuraPorCarona = []

    #retorna lista de motoristas
    def mostraALista(self):
            return self.Motorista

#invoca lista de viagens cadastradas conforme o tipo de usuario
    def consulta(self, origem, destino, data, tpUser):
        if tpUser == 1:         #se motorista, procure por caronas
            listaDeViagens = self.procuraPorCarona
        else:                   #se passageiro, procure por motoristas
            listaDeViagens = self.procuraPorPassageiro
        print(listaDeViagens)
        # [idCorrida, idUser, origem, destino, qtdepassageiros, data]
        
        result = []
        for viagens in listaDeViagens:          #verifica, recursivamente, se ha interseccao entre a viagem desejada e a lista de viagens existentes
            if viagens[4] == data and viagens[2] == origem and viagens[3] == destino:
                #return viagens
                result.append(viagens)
        return result

#Clientes devem informar a origem, destino e a data da viagem desejada. (0,3)
## Sugestão: incluir a chave pública da pessoa que está a se cadastrar, para uso posterior.
    def cadastroUsuario(self, nome, telefone, tpUser):
        if (tpUser == 1):
            idUser = (len(self.Motorista) + 1)          #define a idUser de motorista como o proximo numero disponivel e adiciona no array de motoristas
            self.Motorista.append([idUser, nome, telefone, publicKey])
            return idUser
        else:
            idUser = (len(self.Passageiro) + 1)         #define a idUser de passageiro como o proximo numero disponivel e adiciona no array de passageiros
            self.Passageiro.append([idUser, nome, telefone])
            return idUser

#Clientes devem informar seu nome, telefone e chave pública. (0,2)
## Sugestão: receber uma assinatura digital, que pode ser um texto (challenge)
## que será encriptado pela pessoa cliente usando sua própria chave privada,
## e que podemos solicitar que nos seja informado codificado em base 64, 
## para que possamos tratar com texto.
## Fica assim:
##  - pessoa se cadastra informado seus dados: ('seiti', '555-5555', 'VARIOSCHARSDAMINHACHAVEPUBLICA')
##  - pessoa pega um texto qqer (pode ser seu próprio id, digamos '42') e a encripta usando sua chave privada;
##    Depois a codifica usando base64, obtendo por exemplo '89163501bardt2e3n'
##  - pessoa quer subscrever interesse: (1, 'São Paulo', 'Rio de Janeiro', '2021-12-25', '89163501bardt2e3n')
##  - servidor recebe os dados, desencripta o '89163501bardt2e3n' usando a chave pública da própria pessoa 
##    e consegue ler o texto original, que é 42. Bate com o id da própria pessoa, então ela tem a chave privada 
##    e podemos assumir que é a própria pessoa solicitando interesse.
    def interesseEmCarona(self, idUser, origem, destino, data, qtdepassageiros):         #cadastra interesse do passageiro em carona
        id = datetime.now()         #cria id unica para cada carona e retira caracteres especiais
        id = str(id).replace(":", "")
        id = str(id).replace("-", "")
        id = str(id).replace(".", "")
        idCorrida = str(id).replace(" ", "")
        encoded = str(idUser)

        self.procuraPorCarona.append([idCorrida, idUser, origem, destino, qtdepassageiros, data])
        return idCorrida

## Sugestão: ver sugestão acima    
    def interesseEmPassageiro(self, idUser, origem, destino, data):          #cadastra interesse do motorista em oferecer carona

        id = datetime.now()         #cria id unica para cada viagem e retira caracteres especiais
        id = str(id).replace(":", "")
        id = str(id).replace("-", "")
        id = str(id).replace(".", "")
        idCorrida = str(id).replace(" ", "")
        encoded = str(idUser)
        self.procuraPorPassageiro.append([idCorrida, idUser, origem, destino, data])
        return idCorrida

#cancela subscription do motorista para notificacoes de possiveis passageiros
    def cancelarInteresseEmPassageiro(self, idCorrida):
        for i in range(0, len(self.procuraPorPassageiro)):
            if (self.procuraPorPassageiro[i][0] == idCorrida):
                self.procuraPorPassageiro.pop(i)

#cancela subscription do passageiro para notificacoes de possiveis viagens
    def cancelarInteresseEmCarona(self, idCorrida):
        for i in range(0, len(self.procuraPorCarona)):
            if (self.procuraPorCarona[i][0] == idCorrida):
                self.procuraPorCarona.pop(i)

def main():
    Pyro4.Daemon.serveSimple(
        {
            Servidor: "servidor.carona"
        },
        ns=True)


if __name__ == "__main__":
    main()
