from boolean_formula import *
import os
import random
import time

#####################################################
# CONFIGURATION
#####################################################
log_file_path = r'D:\OneDrive\PythonWorkspace\booleanFormulas\log'
output_directory_path = r'D:\OneDrive\PythonWorkspace\booleanFormulas'
# note that with n=15 there are about 2^65 possible formulas.
number_of_propositions = 3
number_of_formulas = 10
train_data_proportion = 0.95
# dev and test set will share the remainder
depth_of_formulas = -1
# -1 == indifferent. other values makes generation inredibly slow
order = 'pre'
# use 'pre', 'post', or 'normal'
list_of_operators = ['and', 'or', 'imply', 'equiv', 'Nand', 'Nor', 'Nimply', 'Nequiv']
# list of operators involved. please note that negation is encoded in a stupid way

#######################################################
number_of_test = int(number_of_formulas * (1-train_data_proportion))
number_of_train = number_of_formulas - number_of_test
testdata = {}

time_index = time.strftime("%d-%m-%Y-%X", time.localtime()).replace(':','-')


with open(os.path.join(output_directory_path, 'test_input' + '_' + time_index), 'w', encoding='utf-8') as f_test_input,\
        open(os.path.join(output_directory_path, 'test_output' + '_' + time_index), 'w', encoding='utf-8') as f_test_output, \
        open(os.path.join(output_directory_path, 'dev_input' + '_' + time_index), 'w', encoding='utf-8') as f_dev_input,\
        open(os.path.join(output_directory_path, 'dev_output' + '_' + time_index), 'w', encoding='utf-8') as f_dev_output:
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
            if number_of_test % 2 == 0:
                f_test_input.write(' '.join(o) + '\n')
                f_test_output.write(str(evaluate_tree(tree)) + '\n')
            else:
                f_dev_input.write(' '.join(o) + '\n')
                f_dev_output.write(str(evaluate_tree(tree)) + '\n')
            number_of_test -= 1

with open(os.path.join(output_directory_path, 'train_input' + '_' + time_index), 'w', encoding='utf-8') as f_train_input,\
        open(os.path.join(output_directory_path, 'train_output' + '_' + time_index), 'w', encoding='utf-8') as f_train_output:
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

with open(log_file_path, 'a', encoding= 'utf-8') as log_out:
    log_out.write(time_index + '\n')
    log_out.write('#Proporsitions:' + str(number_of_propositions) + '\t' + '# formulas:' + str(number_of_formulas) + '\t'
                  + 'train_data_proportion:' + str(train_data_proportion) + '\t' + 'depth:' + str(depth_of_formulas) + '\t'
                  + 'order:' + order + '\t' + 'operators:' + ','.join(list_of_operators) + '\n')