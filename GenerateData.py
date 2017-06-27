from boolean_formula import *
import random

#####################################################
# CONFIGURATION
#####################################################

output_file = r'D:\OneDrive\PythonWorkspace\booleanFormulas\data'

# n=15, depth OFF, 10000 formulas takes approximately 30 seconds on my laptop

# note that with n=15 there are about 2^65 possible formulas.
number_of_propositions = 15

number_of_formulas = 10000

# -1 == indifferent. other values makes generation inredibly slow
depth_of_formulas = -1

# use 'pre', 'post', or 'normal'
order = 'pre'

# list of operators involved. please note that negation is encoded in a stupid way
list_of_operators = ['and', 'or', 'imply', 'equiv', 'Nand', 'Nor', 'Nimply', 'Nequiv']

#######################################################

candidates = enumerate_sequence(number_of_propositions,'')

with open(output_file,'w',encoding='utf-8') as fout:
    while number_of_formulas > 0:
        seq = random.choice(candidates)
        tree = random_specify_tree(build_tree(seq), list_of_operators)
        tree_trim(tree)
        if depth_of_tree(tree) == depth_of_formulas or depth_of_formulas == -1:
            number_of_formulas -= 1
            print(number_of_formulas)
            if order == 'pre':
                o = tree_to_pre_order(tree)
                fout.write(' '.join(o) + '\n' + str(evaluate_tree(tree)) + '\n')
            if order == 'post':
                o = tree_to_post_order(tree)
                fout.write(' '.join(o) + '\n' + str(evaluate_tree(tree)) + '\n')
            if order == 'normal':
                o = tree_to_normal_order(tree)
                fout.write(' '.join(o) + '\n' + str(evaluate_tree(tree)) + '\n')

