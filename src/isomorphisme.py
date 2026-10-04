
# Import à l'interieur des fonctions pour éviter des problemes d'import circulaire
def is_isomorphic_naive(graph1: list, graph2: list) -> bool:
    """
    Fonction qui détermine si deux graphes sont isomorphes en comparant leur signature obtenue par la version naive

    Entrée : deux graphes sous forme de liste
    Sortie : True s'ils sont isomorphes, False sinon
    """
    from signature_naive import graph_signature

    return graph_signature(graph1) == graph_signature(graph2)


def is_isomorphic_weinberg(graph1: list, graph2: list) -> bool:
    """
    Fonction qui détermine si deux graphes sont isomorphes en comparant leur signature obtenue par la version Weinberg

    Entrée : deux graphes sous forme de liste
    Sortie : True s'ils sont isomorphes, False sinon
    """    
    from signature_weinberg import graph_signature

    return graph_signature(graph1) == graph_signature(graph2)



def is_isomorphic_by_partition(graph1: list, graph2: list) -> bool:
    """
    Fonction qui détermine si deux graphes sont isomorphes en comparant leur signature obtenue par la version Hopcroft et Tarjan

    Entrée : deux graphes sous forme de liste
    Sortie : True s'ils sont isomorphes, False sinon
    """    
    from signature_partition import partition_signature

    return partition_signature(graph1) == partition_signature(graph2)

    

def is_isomorphic_with_nauty(filename1: str, filename2: str) -> bool:
    """
    Fonction qui détermine si deux graphes sont isomorphes en comparant leur signature obtenue par la version Nauty

    Entrée : deux fichiers.txt
    Sortie : True s'ils sont isomorphes, False sinon
    """
    from nauty import are_isomorphic_with_nauty

    return are_isomorphic_with_nauty(filename1, filename2)
