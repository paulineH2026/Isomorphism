# Signatures et isomorphismes de graphes planaires

Ce projet compare plusieurs méthodes de calcul de signatures et de détection d'isomorphisme pour des graphes planaires 3-connexes. Les méthodes étudiées comprennent un parcours naïf, l'approche de Weinberg et un raffinement de partition inspiré de Hopcroft et Tarjan. Des comparaisons avec Nauty sont également prévues.

## Utilisation

Depuis la racine du projet, l'interface graphique expérimentale peut être lancée avec :

```bash
python src/main.py
```

L'interface est encore un prototype : les boutons d'action ne sont pas reliés aux algorithmes. Les fonctions de calcul et les tests sont accessibles directement depuis les modules de `src`.

## 🛠️ Manuel technique

### Prérequis 
 - **Système Unix** du fait de l'utilisation de la librairie pynauty.
 - **Python**: 3.11

### Librairies
 - **pynauty**: 2.8.6
 - **pandas**: 2.2.2
 - **networkx**
 - **matplotlib**: 3.8.4

 Pour installer une librairie faire
 ```
pip install <nom librairie>
```

## Organisation des données

- `plantri_graph/` contient des graphes planaires et des graphes isomorphes associés. Les fichiers `ex...` utilisent la représentation lisible issue du code binaire de Plantri; les fichiers `graph...` utilisent le format ASCII.
- `data/` est destiné aux graphiques produits lors des mesures de performance.

Plantri permet de générer des graphes de test. Par exemple, `./plantri -p -a V graphN.txt` produit une sortie ASCII et `./plantri -p V graph.V` une sortie au format binaire. Par convention, plantri génère des graphes 3-connexes. L'ajout de l'option ``-p`` permet de spécifier qu'ils doivent être planaires simples. Plantri ajoute tous les graphes planaires 3-connexes de taille N aux fichiers spécifiés. Il nous a donc fallu les traiter pour obtenir les graphes suivants (un par fichier). Les options exactes sont décrites dans la [documentation de Plantri](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt). 

## Modules Python

Le répertoire source contient les méthodes que nous avons implémentées. 

**Utilitaires**

Le fichier ``utils.py`` comprend les méthodes permettant de lire les fichiers de graphe planaire pour les utiliser par la suite dans nos algorithmes, une méthode permettant de générer des isomorphes à partir d'un graphe, ainsi qu'une méthode permettant de visualiser les graphes. 

**Signature Naïve**

Un algorithme de génération de signatures peu efficace, d'où l'appellation naïve : ``signature_naive.py``. 

**Signature Weinberg**

Il s'agit de l'algorithme de signature imaginé par Weinberg. Il repose sur les parcours eulériens du graphe : ``signature_weinberg.py``. Cette approche est décrite dans l'article «H. Weinberg. A simple and efficient algorithm for determining isomorphism of planar triply connected graphs».

**Signature Tarjan**

Cette version de l'algorithme de signature correspond à celle imaginée par Tarjan, reposant sur le partitionnement des arêtes selon certains critères : ``signature_partition.py`` et ``signature_partition_utils.py``. Cette approche est décrite dans l'article «J. E. Hopcroft et R. E. Tarjan. A V log V algorithm for isomorphism of triconnected planar graphs».

**Nauty**

Un fichier à part, ``nauty.py``, pour gérer la bibliothèque ``pynauty`` accessible seulement depuis une machine Unix. Ce fichier contient les méthodes nous permettant d'effectuer le calcul de signature découvert par Brendan D.McKay sur nos exemples. 

**Isomorphisme**

Pour savoir si deux graphes sont isomorphes, on compare leur signature issue de l'un des algorithmes : ``isomorphisme.py``.

**Complexité**

 ``complexite.py`` permet de générer les graphiques dont on vient de parler dans la section précédente. Pour l'algorithme de partitionnement de Tarjan, la complexité attendue est en $V\log(V)$, où $V$ est le nombre de sommets du graphe. Pour l'algorithme de Weinberg, la complexité attendue est en $V^2$, où $V$ est le nombre d'arêtes du graphe.

**Interface Graphique**

``main.py``

><span style="color:orange">⚠️ Warning</span>
>
> L'interface graphique n'est pas encore utilisable !

