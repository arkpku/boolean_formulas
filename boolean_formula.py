import random

# generate sequences representing trees. O = operator; P = propositional letters
def enumerate_sequence(n_proposition, initial_seg):
    nO = initial_seg.count('O')
    nP = initial_seg.count('P')
    if nO >= n_proposition or nP >= n_proposition + 1:
        return []
    if nP == nO + 1:
        if nP == n_proposition:
            return [initial_seg]
        else:
            return []
    else:
        return enumerate_sequence(n_proposition, initial_seg + 'P') + enumerate_sequence(n_proposition, initial_seg + 'O')

def generate_random_sequence(n_propositions):
    if n_propositions == 1:
        return 'P'
    seq = 'O'
    while(len(seq) < 2*n_propositions - 2):
        if seq.count('P') < seq.count('O') and seq.count('O') < n_propositions - 1:
            seq += random.choice(['P','O'])
        elif seq.count('P') == seq.count('O'):
            seq += 'O'
        elif seq.count('O') == n_propositions - 1:
            seq += 'P'
    return seq + 'P'

# get a sub tree sequence from a legal sequence as is generated above
def get_subtree_seq(sequence):
    length = 0
    while sequence[:length].count('P') != sequence[:length].count('O') + 1:
        length += 1
#        if length > len(sequence) + 1:
#            return -1,-1
    return sequence[:length], length

def build_tree(sequence):
    root = {}
    root['operator'] = sequence[0]
    root['children'] = []
    if sequence[0] == 'O':
        lseq, llength = get_subtree_seq(sequence[1:])
        rseq, rlength = get_subtree_seq(sequence[1+llength:])
        lsubtree = build_tree(lseq)
        lsubtree['parent'] = root
        root['children'].append(lsubtree)
        rsubtree = build_tree(rseq)
        rsubtree['parent'] = root
        root['children'].append(rsubtree)
    return root

def random_specify_tree(root, list_of_operators = ['and', 'or', 'imply', 'equiv','Nand','Nor', 'Nimply', 'Nequiv']):
    if root['operator'] == 'P':
        root['operator'] = random.choice([True,False])
    else:
        root['operator'] = random.choice(list_of_operators)
        for child in root['children']:
            random_specify_tree(child, list_of_operators)
    return root

def evaluate_tree(root):
    if root['operator'] in [True,False]:
        return root['operator']
    elif root['operator'] == 'and':
        return evaluate_tree(root['children'][0]) and evaluate_tree(root['children'][1])
    elif root['operator'] == 'or':
        return evaluate_tree(root['children'][0]) or evaluate_tree(root['children'][1])
    elif root['operator'] == 'imply':
        return (not evaluate_tree(root['children'][0])) or evaluate_tree(root['children'][1])
    elif root['operator'] == 'equiv':
        return evaluate_tree(root['children'][0]) == evaluate_tree(root['children'][1])
    elif root['operator'] == 'Nand':
        return not(evaluate_tree(root['children'][0]) and evaluate_tree(root['children'][1]))
    elif root['operator'] == 'Nor':
        return not(evaluate_tree(root['children'][0]) or evaluate_tree(root['children'][1]))
    elif root['operator'] == 'Nimply':
        return not((not evaluate_tree(root['children'][0])) or evaluate_tree(root['children'][1]))
    elif root['operator'] == 'Nequiv':
        return not(evaluate_tree(root['children'][0]) == evaluate_tree(root['children'][1]))
    elif root['operator'] == 'not':
        return not evaluate_tree(root['children'][0])

# expand the negations
def tree_trim(root, list_of_neg_operators = ['Nand','Nor','Nimply','Nequiv']):
    if root['operator'] in [True, False]:
        return
    if root['operator'] in list_of_neg_operators:
        if root['operator'] == 'Nand':
            n_root = root.copy()
            n_root['operator'] = 'and'
            n_root['parent'] = root
            root['operator'] = 'not'
            root['children'] = [n_root]
        elif root['operator'] == 'Nor':
            n_root = root.copy()
            n_root['operator'] = 'or'
            n_root['parent'] = root
            root['operator'] = 'not'
            root['children'] = [n_root]
        elif root['operator'] == 'Nimply':
            n_root = root.copy()
            n_root['operator'] = 'imply'
            n_root['parent'] = root
            root['operator'] = 'not'
            root['children'] = [n_root]
        elif root['operator'] == 'Nequiv':
            n_root = root.copy()
            n_root['operator'] = 'equiv'
            n_root['parent'] = root
            root['operator'] = 'not'
            root['children'] = [n_root]
    for child in root['children']:
        tree_trim(child)

# returns a list
def tree_to_pre_order(root):
    if root['operator'] in [True, False]:
        if root ['operator']:
            return ['True']
        else:
            return['False']
    else:
        r = [root['operator']]
        for child in root['children']:
            r += tree_to_pre_order(child)
        return r

def tree_to_post_order(root):
    if root['operator'] in [True, False]:
        if root ['operator']:
            return ['True']
        else:
            return['False']
    else:
        r = []
        for child in root['children']:
            r += tree_to_post_order(child)
        return r + [root['operator']]

def tree_to_normal_order(root):
    if root['operator'] in [True, False]:
        if root ['operator']:
            return ['True']
        else:
            return['False']
    else:
        if root['operator'] == 'not':
            return ['not'] + tree_to_normal_order(root['children'][0])
        else:
            return ['('] + tree_to_normal_order(root['children'][0]) + [root['operator']] + tree_to_normal_order(root['children'][1]) + [')']

# 'True' should be a boolean value not a string
def pre_order_to_tree(sequence, index, list_of_operators = ['and', 'or', 'imply', 'equiv','Nand','Nor', 'Nimply', 'Nequiv']):
    root = {}
    root['operator'] = sequence[index]
    root['children'] = []
    if sequence[index] in [True,False, 'True', 'False']:
        return root, index + 1
    else:
        lt, il = pre_order_to_tree(sequence, index + 1)
        lt['parent'] = root
        root['children'].append(lt)
        rt, ir = pre_order_to_tree(sequence, il)
        rt['paremt'] = root
        root['children'].append(rt)
    return root, ir

def depth_of_tree(root):
    if len(root['children']) == 0:
        return 1
    else:
        return 1 + max(list(map(lambda x: depth_of_tree(x),root['children'])))