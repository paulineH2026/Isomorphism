from utils import read_graph
import signature_naive as naive_signature
import signature_weinberg as weinberg_signature
from signature_partition import partition_signature

import statistics
from math import log
import time
import os 

    
def list_directory_files(directory: str) -> list:
    """ Fonction qui met tous les fichiers d'un répertoire dans une liste """

    files = os.listdir(os.path.abspath(directory))
    # on mets les noms de fichiers sous une forme qui sera prise en compte par nos programmes
    for index in range(len(files)):
        files[index] = directory + "/" + files[index]
    
    return files


#### COMPLEXITE ####

def signature_times(version: str) -> list:
    """
    Fonction qui retourne dans un dictionnaire le temps moyen de calcul 
    de la signature en fonction du nombre de sommets
    """
    supported_versions = {
        "vlogv", "naive", "weinberg",
        "vlogvISO", "naiveISO", "weinbergISO",
    }
    if version not in supported_versions:
        raise ValueError(f"Version de mesure inconnue : {version}")

    from isomorphisme import (
        is_isomorphic_by_partition,
        is_isomorphic_naive,
        is_isomorphic_weinberg,
    )

    files = list_directory_files("plantri_graph")
    
    # pour chaque fichier, on note le nombre de sommets avec le temps d'éxécution associé
    res = {}
    for filename in files:
        if "ISO" not in filename:
            graph = read_graph(filename)
            measures = []
            taille = len(graph)
            if taille <= 220 :

                if version == "vlogv" :
                    # on calcule le temps que met l'algo vlogv pour faire une signature
                    start = time.time()
                    partition_signature(graph)
                    end = time.time()

                elif version == "naive":
                    # on calcule le temps que met l'algo naif pour faire une signature
                    start = time.time()
                    naive_signature.graph_signature(graph)
                    end = time.time()

                elif version == "weinberg":
                    # on calcule le temps que met l'algo naif pour déterminer si deux graphes sont isomorphes
                    start = time.time()
                    weinberg_signature.graph_signature(graph)
                    end = time.time()
                
                elif version == "vlogvISO":
                    # on calcule le temps que met l'algo vlogv pour déterminer si deux graphes sont isomorphes
                    filename2 = filename[:len(filename)-4] + "ISO.txt"
                    graph2 = read_graph(filename2)
                    start = time.time()
                    is_isomorphic_by_partition(graph, graph2)
                    end = time.time()

                elif version == "naiveISO":
                    # on calcule le temps que met l'algo vlogv pour déterminer si deux graphes sont isomorphes
                    filename2 = filename[:len(filename)-4] + "ISO.txt"
                    graph2 = read_graph(filename2)
                    start = time.time()
                    is_isomorphic_naive(graph, graph2)
                    end = time.time()

                elif version == "weinbergISO":
                    # on calcule le temps que met l'algo vlogv pour faire une signature
                    filename2 = filename[:len(filename)-4] + "ISO.txt"
                    graph2 = read_graph(filename2)
                    start = time.time()
                    is_isomorphic_weinberg(graph, graph2)
                    end = time.time()

                measures = (end - start)
                if taille in res:
                    res[taille].append(measures)
                else:
                    res[taille] = [measures]
        
    #on calcule maintenant les moyennes
    for key in res:
        res[key] = statistics.mean(res[key])
        
    #ecart_type = statistics.stdev(measures)

    return {key:res[key] for key in sorted(res)}


def plot_signature_times(version: str, output_filename: str = "filename.png") -> None:
    """
    Fonction qui permet d'afficher le temps de calcul signature 
    algo naif en fontion du nombre de sommets
    """
    
    import matplotlib.pyplot as plt

    data = signature_times(version).items()
    # print(data)
    x, y1 = zip(*data)
    # refaire cette droite
    #y2 = [((i/x[5])**2)*y1[5] for i in x]
    plt.plot(x, y1)
    #plt.plot(x, y2)
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Temps moyen de calcul pour la signature (en secondes)")
    if version == "vlogv":
        plt.title("Algorithme VlogV")
    elif version == "naive":
        plt.title("Algorithme naif")
    elif version == "vlogvISO":
        plt.title("Algorithme d'isomorphisme en VlogV")

    # plt.show()
    plt.savefig(output_filename)


def save_complexity_data(version: str) -> None:
    import pandas as pd

    # génère la moyenne de temps des graphes
    data = signature_times(version).items()

    # Créer un DataFrame pandas à partir des données
    df = pd.DataFrame(data, columns=['Nb Noeuds', 'Moyenne Temps'])

    # Enregistre le Dataframe dans un fichier Excel
    df.to_excel('donnees.xlsx', index=False)
    print("Fichier de données sauvegardé.")


####### REGRESSION LINEAIRE ALGO VLOGV #######

def average_partition_signature_times():

    files = list_directory_files("plantri_graph")
    
    # pour chaque fichier, on note le nombre de sommets avec le temps d'éxécution associé
    res = {}
    for filename in files:
        
        graph = read_graph(filename)
        measures = []
        taille = len(graph)

        # on calcule le temps que met l'algo vlogv pour faire une signature
        start = time.time()
        partition_signature(graph)
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

def plot_vlogv_complexity():
    import matplotlib.pyplot as plt

    data = average_partition_signature_times().items()
    x, y1 = zip(*data)
    x1 = [x*log(x) for x in x]
    print(x)
    plt.plot(x1, y1)
    plt.xlabel("VlogV, V nombre de sommets")
    plt.ylabel("Temps moyen de calcul pour la signature (en secondes)")
    
    plt.title("Algorithme VlogV")

    plt.show()

def export_complexity_data():
    import pandas as pd

    data = average_partition_signature_times().items()
    x, y1 = zip(*data)
    x_log_x = [x*log(x) for x in x]
    x_x = [x*x for x in x]

    table = pd.DataFrame({'v' :x, 'VlogV': x_log_x, 'V*V' : x_x, 't' : y1})
    table.to_excel('data.xlsx', index=False)

if __name__ == "__main__":
    export_complexity_data()
