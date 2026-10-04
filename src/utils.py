import random
import re

### ECRITURE/LECTURE DE GRAPHES ###

def write_graph_in_file(graph: list, filename: str) -> None:
    """
    Fonction qui permet à partir d'un graphe, de créer un fichier pour le stocker comme ceux lus depuis plantri web.

    Entrée : un graph sous forme de liste, le nom du fichier sous lequel on le stockera.
    Sortie : - 
    """
    # on garde l'ordre des voisins pour chaque sommet mais on commence par le premier dans l'ordre alphabétique (norme plantri)
    normalized_graph = []
    for neighbors in graph:
        start = neighbors.index(min(neighbors))
        normalized_graph.append(neighbors[start:] + neighbors[:start])

    # on écrit le graphe dans un fichier texte sous la forme s1[s2 s4] s2[s1] s3 [s4 s1] ...   
    with open(filename, "w") as file:
        for vertex, neighbors in enumerate(normalized_graph, start=1):
            string = str(vertex) + '[' + ' '.join(map(str, neighbors)) + ']' + ' '
            file.write(string)


def binary_to_int_list(content):
    """ 
    Fonction qui permet de passer d'une liste format bytes à une liste d'entiers
    
    Entrée : b'\x02\x03\x04\x05\x00\x01\x05\x04\x03\x00\x01\x02\x04\x00\x01\x03\x02\x05\x00\x01\x04\x02\x00'
    Sortie : [[2, 3, 4, 5], [1, 5, 4, 3], [1, 2, 4], [1, 3, 2, 5], [1, 4, 2]]
    """
    
    # le premier élément donne le nombre de sommets, pas intéressant ici
    liste = content[1:]
    # on sépare chaque noeud (avec ses voisins) de ses voisins grâce au binaire 0 qui sépare les sommets et on met dans une liste
    debut = 0
    graph = []
    for i in range(len(liste)):
        if liste[i] == 0 :
            graph.append(liste[debut:i])
            debut = i+1

    # on transforme les éléments de la liste de type bytes en int
    res = []
    for vertex in graph:
        res.append(list(vertex))

    return res



def generate_planar_code(filename: str) -> None:
    """ 
    Fonction qui permet de séparer des graphes issus d'un même fichier bytes généré via le programme Plantri ou web
    dans des fichiers différents.

    Entrée: Fichier bytes
    Résultat: Fichiers textes (.txt) incluant la représentation Plantri d'un graphe web
    """

    ### LECTURE DU FICHIER ###
    
    with open(filename, "rb") as filin:
        # les 15 premiers charactères correspondent à la chaîne ">>planar_code<<"
        filin.read(15)
        data = filin.read()

    graphs_int = []
    # nombre de sommets
    taille = data[0]
        
    # on sépare les graphes : 
    # on connait le nombre de sommet des graphes et apres un binaire zero on change de sommet (ou de graphe)
    debut = 0
    fin = -1
    compteur_sommets = 0
    for i in range(len(data)) :

        # si on lit un zero binaire, on change de sommet
        if data[i] == 0:
            compteur_sommets += 1
        
        # dans le cas où on a n sommets, avec n taille du graphe, on change de graphe
        if compteur_sommets == taille:
            fin = i
            res = binary_to_int_list(data[debut:(fin+1)])
            graphs_int.append(res)

            # re-initialisation des variables 
            compteur_sommets = 0
            debut = fin + 1
    
    ### ENREGISTREMENT DES GRAPHES DANS DES FICHIERS ###
    
    # nombre de graphes à traiter 
    nbr_graphs = len(graphs_int)

    # on se dit que l'on veut 10 graphes au maximum pour chaque taille de graphe
    # si moins de 1O on les prend tous
    if nbr_graphs <= 10 :
        for i in range(nbr_graphs):
            filename = "plantri_graph/ex" + str(taille) + '_' + str(i+1) + '.txt'
            write_graph_in_file(graphs_int[i], filename)
    # si plus de 10 on en prend 10 au hasard
    else:
        # contiendra le numéro des graphes deja choisis pour éviter les doublons
        hasard = []
        compteur = 1
        while compteur < 11 :
            val = random.randint(0, (nbr_graphs-1))
            if val not in hasard:
                hasard.append(val)
                filename = "plantri_graph/ex" + str(taille) + '_' + str(compteur) + '.txt'
                write_graph_in_file(graphs_int[val], filename)
                compteur += 1
            



def read_graph_from_web(content: str) -> list:
    """ 
    Fonction qui permet de mettre un graphe issu d'un fichier texte généré via le programme Plantri version web
    dans une liste où chaque élément de la liste correspond aux arêtes du noeuds dont c'est l'indice. 

    Entrée: chaine de caractère incluant la représentation Plantri d'un graphe
    Sortie: Liste où chaque élément de la liste correspond aux arêtes du noeud dont c'est l'indice 

    Exemple:
        Entrée: "1[2 3 4 5] 2[1 5 4 3] 3[1 2 4] 4[1 3 2 5] 5[1 4 2]"
        Sortie: [[2, 3, 4, 5], [1, 5, 4, 3], [1, 2, 4], [1, 3, 2, 5], [1, 4, 2]]
    """
       
    # Avec une expression régulière on met dans une liste tous les éléments qui sont entre crochets []
    liste = re.findall(r"\[[\d|\s]+\]", content)
    graph = list()

    for vertex in liste :
        vertex = vertex.replace("[", "")
        vertex = vertex.replace("]", "")
        vertex = vertex.split(" ")
        graph.append(vertex) 

    # Tous les éléments de la liste deviennent de type int
    graph = [[int(i) for i in sub_graph] for sub_graph in graph]
        
    return graph    
    

# ON NE PEUT UTILISER LE PROGRAMME PLANTRI QUE SUR DES MACHINES UNIX
# ./plantri 5 -a test.txt (un graphe planaire à 5 sommets)

def read_graph_from_plantri_ascii(content: str) -> list:
    """ 
    Fonction qui permet de mettre un graphe issu d'un fichier texte généré via le programme Plantri
    dans une liste où chaque élément de la liste correspond aux arêtes du noeuds dont c'est l'indice. 
    ATTENTION ON NE PEUT GENERER QUE DES GRAPHES DE 30 SOMMETS MAXIMUM AVEC LA METHODE ASCII

    Entrée: Fichier texte (.txt) incluant la représentation Plantri d'un graphe
    Sortie: Liste où chaque élément de la liste correspond aux arêtes du noeud dont c'est l'indice 

    Exemple:
        Entrée: 5 bcde,aedc,abd,acbe,adb
        Sortie: [[2, 3, 4, 5], [1, 5, 4, 3], [1, 2, 4], [1, 3, 2, 5], [1, 4, 2]]
    """

    # on sépare la ligne entre le nombre de noeuds et le reste
    liste = content.split(" ")
    # on sépare chaque noeud (avec ses voisins) de ses voisins
    liste = liste[1].split(",") 
    graph = list()

    for vertex in liste :
        # la fonction ord permet de passer d'un caractère ascii à un entier (-96 car on veut des noms de noeuds qui commencent à 1)
        vertex = [ord(vertex[i]) - 96 for i in range(len(vertex))]
        # indice de la liste correspond au nom du noeud 
        graph.append(vertex) 

    return graph


def read_graph(filename: str) -> list:
    """ 
    Fonction qui permet de mettre un graphe issu d'un fichier texte généré via le programme Plantri
    dans une liste où chaque élément de la liste correspond aux arêtes du noeuds dont c'est l'indice. 

    Entrée: Fichier texte (.txt) incluant la représentation Plantri d'un graphe ou web
    Sortie: Liste où chaque élément de la liste correspond aux arêtes du noeud dont c'est l'indice 

    Exemple:
        Entrée: 5 bcde,aedc,abd,acbe,adb
        Sortie: [[2, 3, 4, 5], [1, 5, 4, 3], [1, 2, 4], [1, 3, 2, 5], [1, 4, 2]]
    """
    with open(filename, "r") as filin:
        line = filin.readline()
        # cas où on est dans une représentation générée par le programme Plantri
        if "a" in line:
            return read_graph_from_plantri_ascii(line)
        # cas où on est dans une représentation générée par le web
        else:
            return read_graph_from_web(line)


















### REPRESENTATION DES GRAPHES ###


def draw_graph(graph: list) -> None:
    """
    Fonction qui permet d'afficher le graphe sous forme planaire.

    Entrée : graphe sous forme de liste
    Sortie : -
    """
    import matplotlib.pyplot as plt
    import networkx as nx

    g = nx.Graph()
    # génération de toutes les arêtes du graphe
    edges = []
    for vertex, neighbors in enumerate(graph, start=1):
        for neighbor in neighbors:
            edges.append((vertex, neighbor))
    # on ajoute les arêtes au dessin
    g.add_edges_from(edges)
        
    # représentation planaire du graphe
    try:
        pos = nx.planar_layout(g)
    except ValueError as err:
        print(err.args)
            
    nx.draw(g, pos=pos, with_labels=True)
    plt.show()
















### GENERATION  D'ISOMORPHISME ###


def create_isomorphism(filename: str, positions: list | None = None) -> list:
    """
    Fonction qui créée un graphe isomorphe à celui passé en argument. 
    Par défaut, échange des noms de noeuds 1 et 3. 

    Entrée: chemin du fichier contenant la liste du graphe, liste des positions à échanger:
    Sortie: graphe isomorphe
    """

    if positions is None:
        positions = [[1, 3]]

    graph = read_graph(filename)
    # nom du fichier contenant le nouveau graphe isomorphe
    new_filename = filename.split('.')[0] + 'ISO' + '.txt'

    # Inversion des voisins des sommets à échanger
    for first, second in positions:
        graph[first - 1], graph[second - 1] = graph[second - 1], graph[first - 1]

    # on crée un dictionnaire de correspondance entre les anciens et les nouveaux noms de sommets
    relabeling = {
        old: new
        for first, second in positions
        for old, new in ((first, second), (second, first))
    }

    # on renomme les voisins des sommets échangés pour que le graphe soit isomorphe
    iso = [
        [relabeling.get(neighbor, neighbor) for neighbor in neighbors]
        for neighbors in graph
    ]
    
    write_graph_in_file(iso, new_filename)
    return iso
