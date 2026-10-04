def depth_first_edge_walk(graph, edge, visited_edges, walk):
    """
    Fonction récursive qui permet de parcourir en profondeur les arêtes non encore vues d'un graphe. A chaque appel, on met à jour
    l'ensemble des arêtes déjà traitées
    
    Entrée : le graphe sous forme de liste, l'arête que l'on traite, l'ensemble des arêtes déjà traitées dans l'ordre
    Sortie : rien - on met à jour la liste des arêtes visitées 
    """

    #on ajoute l'arête à la liste des arêtes visitées
    visited_edges.add(edge)
    if walk[-1] != edge[0]:
        walk.append(edge[0])
    # on ajoute la tête d'arête (nouveau sommet) à la liste
    walk.append(edge[1])

    # on regarde les voisins et on les prends dans l'ordre à droite de celle d'où l'on vient
    neighbors = graph[edge[1]-1]
    index = neighbors.index(edge[0])
    ordered_neighbors = neighbors[(index+1):] + neighbors[:(index+1)]
    
    # regarder pour chaque voisin de la tête de l'arête, edge[1], si l'arête les reliant a été traité et si non la traiter
    for neighbor in ordered_neighbors:
        if ((neighbor, edge[1]) not in visited_edges) and ((edge[1], neighbor) not in visited_edges):
            depth_first_edge_walk(graph, (edge[1], neighbor), visited_edges, walk)

def edge_walk(graph, starting_edge):
    """
    Fonction qui permet de parcourir le graphe en profondeur sur les arêtes depuis une arête donnée

    Entrée : le graphe sous forme de liste
    Sortie : une liste avec tous les sommets dans l'ordre dans lesquelles on les passe 
    """
    
    # ensemble des arêtes dans l'ordre dans lesquelles on les a passée, mis à jour avec ParcoursProfondeurRecursif
    visited_edges = set()
    walk = [starting_edge[0]]

    # première instance pour le parcours en profondeur 
    depth_first_edge_walk(graph, starting_edge, visited_edges, walk)
    
        
    return walk

def translate_walk(graph, walk):
    """
    Fonction qui renome les sommets de la liste obtenue lors du parcours profondeur en fontion de leur traitement,
    plus on les voit tôt, plus leur numéro est faible

    Entrée : une liste avec tous les sommets dans l'ordre dans lesquelles on les passe
    Sortie : la liste avec les sommets renommés

    Exemple:
        Entrée: [2, 1, 4, 3, 4, 3, 2]
        Sortie: [1, 2, 3, 4, 3, 4, 1]
    """
    
    # initialisation de la liste qui va nous permettre de garder en mémoire les changements de noms 
    traduction =  [-1 for i in range(len(graph))]
    # initialisation du compteur qui nous permettra de renommer les sommets
    k = 1

    res = list()
    
    # pour chaque sommet de la liste d'entrée
    for vertex in walk:
        # si c'est la première fois que l'on rencontre ce sommet
        if traduction[vertex-1] == -1:
            # on ajoute dans le dictionnaire le sommet avec sa nouvelle traduction (k actuel) et on incrémente k pour le prochain cas
            traduction[vertex-1] = k
            k += 1
        res.append(traduction[vertex-1])
    
    return res


def graph_signature(graph):
    """
    Fonction qui permet de générer une signature du graphe en s'appuyant seulement sur sa structure et non pas sur la 
    façon dont il a été nommé. On va générer des sigatures issues de parcours en profondeur depuis chaque arête du graphe et 
    on choisit la plus "petite" (ordre croissant).

    Entrée : le graphe sous forme de liste
    Sortie : la signature
    """
    signatures = list()
    taille = len(graph)

    ### on énumère toutes les arêtes en considérant les deux sens ###
    
    edges = []
    for vertex in range(taille):
        # pour tous les voisins du noeud
        for neighbor in graph[vertex]:
            # on ajoute l'arête (noeud, voisin) à la liste 
            edges.append((vertex+1, neighbor))
        
    ### pour chaque arête, on génère la signature auquelle on applique la traduction (car on ne prend pas compte des noms des sommets) ###
    
    # for edge in edges :
    #     parcours = ParcoursAretes(graph, edge)
    #     signatures.append(Traduction(graph, parcours))

    # on ne traduit que les signatures qui sont de taille plus petite ou égale à celles déjà générées
    taille_parcours_minimum = 10e6                            # initialisation

    for edge in edges:
        walk = edge_walk(graph, edge)
        walk_length = len(walk)

        if walk_length <= taille_parcours_minimum :
            signatures.append(translate_walk(graph, walk))
            taille_parcours_minimum = walk_length

    longueur_min = min(len(liste) for liste in signatures)
    signatures_longueur_min = [liste for liste in signatures if len(liste) == longueur_min]

    return min(signatures_longueur_min)


