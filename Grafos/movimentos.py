
import heapq
import matplotlib.pyplot as plt
from networkx import draw, spring_layout, draw_networkx_edge_labels
from algoritmos import minimo_dijkstra, propagar_bsf, peso_total_caminho


def criar_grafo(G, dados):
    G.add_nodes_from(f"V{i}" for i in range(dados['num_vertices']))
    for u, peso, v in dados['arestas']:
        G.add_edge(f"V{u}", f"V{v}", weight=peso)


def mostrar_grafo(G, dados, postos, pontos_agua, equipes, cargas, requisitos):
    plt.ion()
    fig = plt.figure()
    pos = spring_layout(G)
    weights = {e: G.edges[e]['weight'] for e in G.edges}
    color_map = {'verde': 'green', 'vermelho': 'red', 'extinto': 'orange', 'posto': 'yellow', 'agua': 'cyan'}

    cores = {no: 'verde' for no in G.nodes}
    inicio = f"V{dados['fogo']}"
    cores[inicio] = 'vermelho'

    # Inicializa brigadas: cada uma com local, água e caminho a seguir
    brigadas = []
    for i, p in enumerate(postos):
        brigadas.append({
            'id': f'b{i}',
            'local': p,
            'agua': cargas[0],
            'destino': None,
            'caminho': [],
            'relatorio': []
        })

    foco_ativado = [inicio]
    alastramento = [(0, inicio)]
    heapq.heapify(alastramento)
    passo = 0

    while alastramento or foco_ativado:
        # 1) Propagação
        if alastramento:
            tempo, vert = heapq.heappop(alastramento)
            cores = propagar_bsf(G, cores, vert, alastramento, tempo, postos, equipes, foco_ativado)

        # 2) Atribuir focos às brigadas (um foco por brigada)
        focos_disponiveis = foco_ativado.copy()
        for brig in brigadas:
            if not brig['caminho'] and focos_disponiveis:
                alvo = focos_disponiveis.pop(0)
                brig['destino'] = alvo
                brig['caminho'] = minimo_dijkstra(G, brig['local'], alvo)

        # 3) Avanço das brigadas
        for brig in brigadas:
            if brig['caminho']:
                # anda 1 passo no caminho
                brig['local'] = brig['caminho'].pop(0)

                if brig['local'] == brig['destino']:
                    alvo = brig['local']
                    chave = str(alvo) if str(alvo).startswith('V') else f"V{alvo}"
                    reqs = requisitos.get(chave, (0, 0))
                    if isinstance(reqs, tuple):
                        req_agua, req_eq = reqs
                    else:
                        req_agua, req_eq = 0, 0
                    if req_agua > 0 and brig['agua'] >= req_agua and req_eq <= len(equipes):
                        brig['agua'] -= req_agua
                        cores[alvo] = 'extinto'
                        if alvo in foco_ativado:
                            foco_ativado.remove(alvo)
                        brig['relatorio'].append(f"Extinguiu {alvo} com {req_agua}L")
                    else:
                        # Vai reabastecer se sem água
                        nearest = sorted(pontos_agua, key=lambda w: peso_total_caminho(G, minimo_dijkstra(G, brig['local'], w)))[0]
                        brig['destino'] = nearest
                        brig['caminho'] = minimo_dijkstra(G, brig['local'], nearest)
                        brig['relatorio'].append(f"Sem água. Indo para {nearest}")
                elif not brig['caminho']:
                    # caso chegou a ponto de água
                    if brig['local'] in pontos_agua:
                        brig['agua'] = cargas[0]
                        brig['relatorio'].append(f"Reabasteceu em {brig['local']}")

        passo += 1

        # 4) Visualização
        fig.clf()
        node_colors = []
        for n in G.nodes:
            if n in postos:
                node_colors.append(color_map['posto'])
            elif n in pontos_agua:
                node_colors.append(color_map['agua'])
            else:
                node_colors.append(color_map.get(cores[n], 'gray'))
        draw(G, pos, node_color=node_colors)
        draw_networkx_edge_labels(G, pos, edge_labels=weights)
        plt.pause(0.5)

        if not foco_ativado:
            print(f"Fogo contido em {passo} passos.")
            break

    plt.ioff()
    plt.show()

    # 5) Relatório Final
    print("\nRELATÓRIO FINAL DAS BRIGADAS:")
    for brig in brigadas:
        print(f"\nBrigada {brig['id']}:")
        for evento in brig['relatorio']:
            print(" -", evento)
