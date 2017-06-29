from boolean_formula import *
import os
import random

#####################################################
# CONFIGURATION
#####################################################

output_path = r'D:\OneDrive\PythonWorkspace\booleanFormulas'
# note that with n=15 there are about 2^65 possible formulas.
number_of_propositions = 10
number_of_formulas = 10000
train_data_proportion = 0.95
# -1 == indifferent. other values makes generation inredibly slow
depth_of_formulas = -1
# use 'pre', 'post', or 'normal'
order = 'pre'
# list of operators involved. please note that negation is encoded in a stupid way
list_of_operators = ['and', 'or', 'imply', 'equiv', 'Nand', 'Nor', 'Nimply', 'Nequiv']

#######################################################
iterator = number_of_formulas

number_of_test = int(number_of_formulas * (1-train_data_proportion))
number_of_train = number_of_formulas - number_of_test
testdata = {}

with open(os.path.join(output_path,'test_input'),'w',encoding='utf-8') as f_test_input,\
        open(os.path.join(output_path,'test_output'),'w',encoding='utf-8') as f_test_output:
    while number_of_test > 0:
        proto_form = generate_random_sequence(number_of_propositions)
        tree = random_specify_tree(build_tree(proto_form), list_of_operators)
        tree_trim(tree)
        pre = tree_to_pre_order(tree)
        prestr = ' '.join(pre)
        if prestr not in testdata:
            testdata[prestr] = 0
            if order == 'pre':
                o = tree_to_pre_order(tree)
            elif order == 'post':
                o = tree_to_post_order(tree)
            elif order == 'normal':
                o = tree_to_normal_order(tree)
            f_test_input.write(' '.join(o) + '\n')
            f_test_output.write(str(evaluate_tree(tree)) + '\n')
            number_of_test -= 1

with open(os.path.join(output_path,'train_input'),'w',encoding='utf-8') as f_train_input,\
        open(os.path.join(output_path,'train_output'),'w',encoding='utf-8') as f_train_output:
    while number_of_train > 0:
        proto_form = generate_random_sequence(number_of_propositions)
        tree = random_specify_tree(build_tree(proto_form), list_of_operators)
        tree_trim(tree)
        pre = tree_to_pre_order(tree)
        prestr = ' '.join(pre)
        if prestr not in testdata:
            if order == 'pre':
                o = tree_to_pre_order(tree)
            elif order == 'post':
                o = tree_to_post_order(tree)
            elif order == 'normal':
                o = tree_to_normal_order(tree)
            f_train_input.write(' '.join(o) + '\n')
            f_train_output.write(str(evaluate_tree(tree)) + '\n')
            number_of_train -= 1