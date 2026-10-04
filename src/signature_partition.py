from signature_partition_utils import edge_lambda

# Algorithme inspiré de l'article:
# J. E. HOPCROFT AND R. E. TARJAN, "A V log V Algorithm for Isomorphism 
# of Triconnected Planar Graphs," Computer Science Department, Cornell University, 
# Ithaca, NY, 1972

def first_partitioning(graph: list) -> dict:
    """
    Fonction qui permet de faire le premier partionnement des aretes. 
    Des aretes ayant le meme lambda (i.e meme nombre de degré entrant/sortant 
    et longueur de face droite/gauche) seront mises dans le meme bloc.

    Entrée: Liste représentant les caractéristiques du graphe.
            De la forme: [[n2, n3, n4, n5], [n1, n5, n4, n3], [n1, n2, n4], ....]
    Sortie: Dictionnaire représentant les caractéristiques du bloc suivant des aretes ayant ces propriétés.
            De la forme: {(|face gauche|, |face droite|, degré tail, degré head): [(n1, n2), (n1, n3), (n2, n4)], ...} 
            (avec ni des numéros de noeuds)
    """

    list_edges = []
    # Liste tous les arcs du graphe
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            list_edges.append((i+1, graph[i][j]))

    dico_lambda = dict()

    # On partitionne tous les arcs selon leur lamba
    # Une case de ditionnaire = à un meme lambda
    for edge in list_edges:
        lambda_edge = edge_lambda(edge, graph)

        if lambda_edge in dico_lambda.keys():
            dico_lambda[lambda_edge].append(edge)
        else:
            dico_lambda[lambda_edge] = [edge]

    return dico_lambda



def adjacent_edge(edge: tuple, direction: str, graph: list) -> tuple:
    """
    Fonction qui permet de trouver l'arc directement à droite ou à gauche de l'arc e.

    Entrée: e un tuple représentant un arc de la forme (tail, head)
            D un string prenant la valeur R ou L. 
                L pour trouver l'arc directement à gauche (Left)
                R pour trouver l'arc directement à droite (Right)
    Sortie: tuple de la forme (tail, head)
    """
    tail = edge[0]
    head = edge[1]

    if direction == 'L':
        index = graph[head-1].index(tail)
        new_head = graph[head-1][(index-1)%len(graph[head-1])]
    elif direction == 'R':
        index = graph[head-1].index(tail)
        new_head = graph[head-1][(index+1)%len(graph[head-1])]
    
    edge = (head, new_head)

    return edge


def intersection(first: list, second: list) -> list:
    """
    Fonction qui retourne l'intersection des éléments de 2 listes.

    Utilisation de set dans la fonction pour améliorer la complexité en temps.

    Entrée: l1 et l2 des listes
    Sortie: une liste du resultat de (l1 ∩ l2)
    """

    # Passage sous forme de sets pour améliorer la complexité en temps.
    set_first = set(first)
    set_second = set(second)

    return list(set_first.intersection(set_second))


def find_block(partition: dict, e: tuple) -> tuple:
    """
    Fonction qui retrouve dans quel bloc (clé du dictionnaire) se trouve une arete e.

    Entrée: dico représentant le partionnement en blocs (dict)
            e une arete de la forme (tail, head) (tuple)
    Sortie: la clé du bloc où se trouve e (tuple)
    """

    # Parcours du dictionnaire
    for block, edges in partition.items():
        if e in edges:
            return block


def partition_signature(graph: list) -> dict:
    """
    Fonction mimant le fonctionnement de l'algorithme proposé dans l'article:
    J. E. HOPCROFTANDR. E. TAaJAN,"A V log V AIgorithm for Isomorphism 
    of Triconnected Planar Graphs," Computer Science Department, Cornell University, 
    Ithaca, NY, 1972

    Les noms des variables et constantes proposées dans l'article ont été gardés.

    Entrée: Liste représentant les caractéristiques du graphe.
            De la forme: [[n2, n3, n4, n5], [n1, n5, n4, n3], [n1, n2, n4], ....]
    Sortie: Dictionnaire représentant la signature du graphe.
            De la forme {(caractéritique1): nb d'arcs, (caractéristique2): nb d'arcs, ...}
    """

    blocks = first_partitioning(graph) # Dictionnaire représentant les blocs de partionnement
    # Tri du dictionnaire dans l'ordre croissant
    # Pour que l'algo s'execute tjr dans le meme ordre de partitions
    blocks = dict(sorted(blocks.items()))
    edge_to_block = {
        edge: block_key
        for block_key, block_edges in blocks.items()
        for edge in block_edges
    }

    # STATEMENT A
    process = []
    # Pour chaque lambda (clé) du dictionnaire
    for block_key in blocks:
        process.append((block_key, 'R'))
        process.append((block_key, 'L'))
    
    # Tant que PROCESS est non vide
    while process:
        # STATEMENT C
        # Récupère un élément de PROCESS puis le supprime
        block_key = process[0][0]
        direction = process[0][1]
        del process[0]

        # STATEMENT G
        move = []

        # STATEMENT H
        # Pour chaque arete e du bloc i
        # On ajoute son arc directement à D (droite ou gauche) de lui dans MOVE
        for edge in blocks[block_key]:
            # e est sous la forme d'un tuple (e1, e2)
            move.append(adjacent_edge(edge, direction, graph))

        # initialisation de la liste qui retient quels blocs ont été crées dans le STATEMENT I
        blocks_created = list()

        # STATEMENT I
        # Pour chaque arete de MOVE
        for edge in move:
            block = edge_to_block[edge]
            block_edges = list(blocks[block])

            # STATEMENT J
            common_edges = intersection(block_edges, move)
            common_edges.sort()
            block_edges.sort()

            if common_edges != block_edges:
                # Si le bloc B(j) contient plus d'une arete
                # (i.e. Si on peut split des éléments)
                if len(blocks[block]) > 1:
                    # Création du nom du nouveau bloc B(j')
                    new_block = (block, block_key, direction)

                    # Si B(j') n'est pas encore crée
                    if new_block not in blocks:
                        # Création de B(j') et insertion de e
                        blocks[new_block] = [edge]
                        blocks_created.append((block, new_block))
                    else:
                        # Insertion de e si le bloque était déjà existant
                        blocks[new_block].append(edge)
                    # Suppression de e du bloc B(j)
                    blocks[block].remove(edge)
                    edge_to_block[edge] = new_block
        
        # STATEMENT K
        for elem in blocks_created:
            block = elem[0]
            new_block = elem[1]
            for direction in ("L", "R"):
                if (block, direction) in process:
                    process.append((new_block, direction))
                elif len(blocks[new_block]) <= len(blocks[block]):
                    process.append((new_block, direction))
                else:
                    process.append((block, direction))

    # Standardise la signature pour qu'elle n'est pas de numéro d'arc.
    for key in blocks:
        blocks[key] = len(blocks[key])
        
    return blocks
