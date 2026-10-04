### SOUS UNIX OU MACOS A CAUSE DE LA LIBRAIRIE PYNauty ###

from pynauty import Graph, isomorphic
from utils import read_graph
from complexite import list_directory_files
import time
import statistics
from complexite import signature_times

def to_nauty_adjacency(filename: str) -> list:
    """
    Fonction qui prend en entrée un fichier de la forme s1[s2 s4] s2[s1] s3[s4 s1] ...
    Et le tranforme en fichier lisible par le programme nauty.
    """
    # par convention les sommets sont numérotés à partir de 0
    graph = read_graph(filename)
    return [[neighbor - 1 for neighbor in neighbors] for neighbors in graph]


def are_isomorphic_with_nauty(filename1: str, filename2: str) -> bool:
    """
    Fonction qui regarde si deux graphes sont isomorphes en utilisant
    l'algorithme nauty.

    Entrée: fichiers textes sous la forme s1[s2 s4] s2[s1] s3 [s4 s1] ...
    Sortie: Vrai si les graphes sont isomorphes Faux sinon
    """
    # lecture des fichiers
    graph1 = to_nauty_adjacency(filename1)
    graph2 = to_nauty_adjacency(filename2)

    # on initialise les objets graphes 
    # Initialisation de la taille des graphes
    graph1_nauty = Graph(len(graph1))
    graph2_nauty = Graph(len(graph2))

    # on mets sous forme de dictionnaire les listes d'adjacence
    adjacency1 = {index: neighbors for index, neighbors in enumerate(graph1)}
    adjacency2 = {index: neighbors for index, neighbors in enumerate(graph2)}

    # Initialisation des arêtes des graphes
    graph1_nauty.set_adjacency_dict(adjacency1)
    graph2_nauty.set_adjacency_dict(adjacency2)

    return isomorphic(graph1_nauty, graph2_nauty)


### ETUDE DE LA COMPLEXITE DE L'ALGORITHME NAUTY ###

def nauty_isomorphism_times() -> dict:
    """
    Fonction qui retourne dans un dictionnaire le temps moyen de calcul 
    pour comparer si deux graphes sont isomorphes par nauty en fonction du nombre de sommets
    """
    files = list_directory_files("plantri_graph")
    res = {}

    for filename1 in files:
        if "ISO" not in filename1:
            measures = []
            graph = read_graph(filename1)
            taille = len(graph)
            # on calcule le temps que met l'algo nauty
            filename2 = filename1[:len(filename1)-4] + "ISO.txt"
            start = time.time()
            are_isomorphic_with_nauty(filename1, filename2)
            end = time.time()

            measures = (end - start)
            if taille in res:
                res[taille].append(measures)
            else:
                res[taille] = [measures]
    
    #on calcule maintenant les moyennes
    for key in res:
       res[key] = statistics.mean(res[key])
    
    return {key:res[key] for key in sorted(res)}


def plot_nauty_isomorphism_times():
    """
    Fonction qui permet d'afficher le temps de calcul de l'algo nauty en fontion du nombre de sommets
    """
    
    import matplotlib.pyplot as plt

    data = nauty_isomorphism_times().items()
    # print(data)
    x, y1 = zip(*data)
    # refaire cette droite
    #y2 = [((i/x[5])**2)*y1[5] for i in x]
    plt.plot(x, y1)
    #plt.plot(x, y2)
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Temps moyen de calcul pour l'isomorphisme (en secondes)")
    plt.title("Algorithme Nauty")

    # plt.show()
    plt.savefig('filename.png')
