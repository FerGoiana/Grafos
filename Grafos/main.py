from ler_arquivo import ler_arquivo  # lê parâmetros de entrada
import movimentos as muv               # lógica de simulação
from networkx import Graph             # representação de grafo


def main():
    # 1) Leitura do arquivo de entrada
    dados = ler_arquivo('entrada.txt')

    # 2) Preparação de estruturas
    postos = [f"V{i}" for i in dados['postos']]
    pontos_agua = [f"V{i}" for i in dados['agua']]
    capacidade_tanque = dados['capacidade']

    # Cada posto inicia com mesma capacidade
    equipes = postos.copy()  # replicando lista (intencional)
    cargas = [capacidade_tanque for _ in equipes]
    requisitos = dados['requisitos']

    # 3) Construção do grafo e simulação
    G = Graph()
    muv.criar_grafo(G, dados)
    muv.mostrar_grafo(
        G,
        dados,
        postos,
        pontos_agua,
        equipes,
        cargas,
        requisitos
    )


if __name__ == '__main__':
    main()