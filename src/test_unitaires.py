import unittest

from utils import create_isomorphism, read_graph
from isomorphisme import (
    is_isomorphic_by_partition,
    is_isomorphic_naive,
    is_isomorphic_weinberg,
)

### TESTS DU MODULE UTILS ###

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.filename1 = "plantri_graph/graph5_1.txt"
        self.filename2 = "plantri_graph/graph5_1ISO.txt"

    
    def test1_create_isomorphism(self):

        create_isomorphism(self.filename1, [[2,5],[1,3]])
        res = [[3, 5, 4], [3, 4, 5], [1, 4, 2, 5], [1, 5, 2, 3], [1, 3, 2, 4]]
        
        self.assertEqual(read_graph(self.filename2), res)

    def test2_create_isomorphism(self):

        create_isomorphism(self.filename1, [[1,3],[2,5]])
        res = [[3, 5, 4], [3, 4, 5], [1, 4, 2, 5], [1, 5, 2, 3], [1, 3, 2, 4]]
        
        self.assertEqual(read_graph(self.filename2), res)


#### TESTS DE LA VERSION NAÏVE ###
    
class TestVersionNaive(unittest.TestCase):
    
    def setUp(self):

        filename1 = "plantri_graph/ex100_9.txt"
        self.graph1 = read_graph(filename1)

        filename1bis = "plantri_graph/ex100_8.txt"
        self.graph1bis = read_graph(filename1bis)

        create_isomorphism(filename1)
        filename1ter = "plantri_graph/ex100_9ISO.txt"
        self.graph1ter = read_graph(filename1ter)


    def test1_isomorphisme(self):
        
        self.assertEqual(is_isomorphic_naive(self.graph1, self.graph1ter), True, 'graphes isomorphes')
        
    def test2_isomorphisme(self):
        
        self.assertEqual(is_isomorphic_naive(self.graph1, self.graph1bis), False, 'graphes non isomorphes')



### TESTS DE LA VERSION HOPCROFT ET TARJAN ###

class TestVersionPartition(unittest.TestCase):
    
    def setUp(self):

        filename1 = "plantri_graph/ex50_1.txt"
        self.graph1 = read_graph(filename1)

        filename1bis = "plantri_graph/ex50_8.txt"
        self.graph1bis = read_graph(filename1bis)

        create_isomorphism(filename1)
        filename1ter = "plantri_graph/ex50_1ISO.txt"
        self.graph1ter = read_graph(filename1ter)


    def test1_isomorphisme(self):
        
        self.assertEqual(is_isomorphic_by_partition(self.graph1, self.graph1ter), True,
                         'graphes isomorphes')
        
    def test2_isomorphisme(self):
    
        self.assertEqual(is_isomorphic_by_partition(self.graph1, self.graph1bis), False, 'graphes non isomorphes')


### TESTS DE LA VERSION WEINBERG ###

class TestVersionWeinberg(unittest.TestCase):
    
    def setUp(self):

        filename1 = "plantri_graph/ex50_1.txt"
        self.graph1 = read_graph(filename1)

        filename1bis = "plantri_graph/ex50_8.txt"
        self.graph1bis = read_graph(filename1bis)

        create_isomorphism(filename1)
        filename1ter = "plantri_graph/ex50_1ISO.txt"
        self.graph1ter = read_graph(filename1ter)


    def test1_isomorphisme(self):
        
        self.assertEqual(is_isomorphic_weinberg(self.graph1, self.graph1ter), True,
                         'graphes isomorphes')
        
    def test2_isomorphisme(self):
    
        self.assertEqual(is_isomorphic_weinberg(self.graph1, self.graph1bis), False, 'graphes non isomorphes')



if __name__ == '__main__':
    unittest.main()
