from collections import namedtuple

Node = namedtuple('Node', ['left', 'right', 'bits', 'rank', 'select', 'string', 'alphabet'])

def add_node(nodes, node):
    nodes.append(node)
    return len(nodes) - 1

def split_alphabet(text):
    uniq_chars = list(set(text))
    split = len(uniq_chars) // 2
    return (uniq_chars[:split], uniq_chars[split:])

def process_node(nodes, node, codes):
    if len(node.alphabet) == 1:
        return []
    left, right = split_alphabet(node.string)

    for l in left:
        if l not in codes:
            codes[l] = []
        codes[l].append(0)

    for r in right:
        if r not in codes:
            codes[r] = []
        codes[r].append(1)

    left_string = ''
    right_string = ''
    for char in node.string:
        if char in left:
            node.bits.append(0)
            left_string += char
        else:
            node.bits.append(1)
            right_string += char

    node.rank.append(0)
    for i in range(1, len(node.bits)+1):
        node.rank.append(node.rank[i - 1] + node.bits[i-1])

    node.select.append([])
    node.select.append([])
    for i in range(len(node.bits)):
        if node.bits[i] == 1:
            node.select[1].append(i)
        else:
            node.select[0].append(i)


    left_node = Node([], [], [], [], [], left_string, set(left_string))
    right_node = Node([], [], [], [], [], right_string, set(right_string))

    left_node_id = add_node(nodes, left_node)
    right_node_id = add_node(nodes, right_node)
    node.left.append(left_node_id)
    node.right.append(right_node_id)

    return [left_node_id, right_node_id]

def access(nodes, i):
    Q = [0]
    last_rank = i
    while len(Q) > 0:
        curr_id = Q.pop(0)
        if len(nodes[curr_id].alphabet) == 1:
            return list(nodes[curr_id].alphabet)[0]

        bit = nodes[curr_id].bits[last_rank]

        if bit == 0:
            Q += nodes[curr_id].left
        else:
            Q += nodes[curr_id].right

        last_rank = node_rank(nodes[curr_id], bit, last_rank)

def print_tree(nodes):
    Q = [(0,0)]
    while len(Q)>0:
        curr_id, level = Q.pop(0)
        prefix = '-' * level
        print(prefix, curr_id, nodes[curr_id])
        if len (nodes[curr_id].left) > 0:
            Q += [(nodes[curr_id].left[0], level + 1)]
        if len (nodes[curr_id].right) > 0:
            Q += [(nodes[curr_id].right[0], level + 1)]

def make_tree(S):
    nodes = []
    codes = {}

    root = Node([], [], [], [], [], S, set(S))
    node_id = add_node(nodes, root)

    Q = [node_id]

    while len(Q) > 0:
        node_id = Q.pop(0)
        new_nodes = process_node(nodes, nodes[node_id], codes)
        Q += new_nodes

    return nodes, codes

def node_rank(node, v, i):
    if v == 1:
        return node.rank[i]
    else:
        return i - node.rank[i]

def node_select(node, v, i):
    if v == 1:
        return node.select[1][i]
    else:
        return node.select[0][i]


def rank(nodes, codes, char, idx):
    curr_node = nodes[0]
    path = codes[char].copy()
    curr_rank = idx


    while len(path) > 0:
        curr_bit = path.pop(0)
        old_rank = curr_rank
        curr_rank = node_rank(curr_node, curr_bit, old_rank)

        if curr_bit == 0:
            curr_node = nodes[curr_node.left[0]]
        else:
            curr_node = nodes[curr_node.right[0]]

    return curr_rank

def select(nodes, codes, char, idx):
    curr_node = nodes[0]
    path = list(codes[char].copy())

    select_nodes = [curr_node]

    for step in path:
        if step == 0:
            curr_node = nodes[curr_node.left[0]]
        else:
            curr_node = nodes[curr_node.right[0]]

        if len(curr_node.alphabet) == 1:
            break

        select_nodes.insert(0, curr_node)

    path.reverse()

    last_select = idx

    for i, bit in enumerate(path):
        last_select = node_select(select_nodes[i], bit, last_select)

    return last_select

def main():
    S = 'abracadabra$'
    nodes, codes = make_tree(S)
    print(sorted(list(set(range(len(S)))-set(nodes[0].select))))
    print(rank(nodes, codes, 'a', 8))

if __name__ == '__main__':
    main()
