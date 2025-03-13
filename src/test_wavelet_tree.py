import unittest
import wavelet_tree

class TestWaveletTree(unittest.TestCase):
    def test_access(self):
        S = 'abracadabra$'
        nodes, codes = wavelet_tree.make_tree(S)
        self.assertEqual(wavelet_tree.access(nodes, 0), 'a')
        self.assertEqual(wavelet_tree.access(nodes, 1), 'b')
        self.assertEqual(wavelet_tree.access(nodes, 2), 'r')
        self.assertEqual(wavelet_tree.access(nodes, 3), 'a')
        self.assertEqual(wavelet_tree.access(nodes, 4), 'c')
        self.assertEqual(wavelet_tree.access(nodes, 5), 'a')
        self.assertEqual(wavelet_tree.access(nodes, 6), 'd')
        self.assertEqual(wavelet_tree.access(nodes, 7), 'a')
        self.assertEqual(wavelet_tree.access(nodes, 8), 'b')
        self.assertEqual(wavelet_tree.access(nodes, 9), 'r')
        self.assertEqual(wavelet_tree.access(nodes, 10), 'a')
        self.assertEqual(wavelet_tree.access(nodes, 11), '$')

    def test_rank(self):
        S = 'abracadabra$'
        nodes, codes = wavelet_tree.make_tree(S)
                 #a  b  r  a  c  a  d  a  b  r  a, $]
        a_rank = [0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5]
        b_rank = [0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
        c_rank = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
        r_rank = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2]
        for i in range(10):
            self.assertEqual(wavelet_tree.rank(nodes, codes, 'a', i), a_rank[i])
            self.assertEqual(wavelet_tree.rank(nodes, codes, 'b', i), b_rank[i])
            self.assertEqual(wavelet_tree.rank(nodes, codes, 'c', i), c_rank[i])
            self.assertEqual(wavelet_tree.rank(nodes, codes, 'r', i), r_rank[i])

    def test_select(self):
        S = 'abracadabra$'
        nodes, codes = wavelet_tree.make_tree(S)

        a_select = [0, 3, 5, 7, 10]

        for i in range(len(a_select)):
            self.assertEqual(wavelet_tree.select(nodes, codes, 'a', i), a_select[i])

        b_select = [1, 8]

        for i in range(len(b_select)):
            self.assertEqual(wavelet_tree.select(nodes, codes, 'b', i), b_select[i])

        c_select = [4]

        for i in range(len(c_select)):
            self.assertEqual(wavelet_tree.select(nodes, codes, 'c', i), c_select[i])

        r_select = [2, 9]

        for i in range(len(r_select)):
            self.assertEqual(wavelet_tree.select(nodes, codes, 'r', i), r_select[i])


if __name__ == '__main__':
    unittest.main()
