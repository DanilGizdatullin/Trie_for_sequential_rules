__author__ = 'danil.gizdatullin'

from random import randint

from sequence_from_file import SequencesFromFile
from classification import Classification
# from trie import Trie

men_data = SequencesFromFile('/Users/danil.gizdatullin/Documents/folder/Kaggle/new data exp/Men_dataset.csv')
data = men_data.from_file_to_data_list()
men_train_data = data[0]
men_test_data = data[1]
# print len(men_train_data)
# print len(men_test_data)
#
women_data = SequencesFromFile('/Users/danil.gizdatullin/Documents/folder/Kaggle/new data exp/Women_dataset.csv')
data = women_data.from_file_to_data_list()
women_train_data = data[0]
women_test_data = data[1]
# print len(women_train_data)
# print len(women_test_data)
# print women_test_data

from trie import Trie, RulesImportance

# # test_set1 = [[['1'], ['2'], ['3']], [['2'], ['4']], [['1'], ['2'], ['3'], ['5', '6']], [['2'], ['4'], ['5']], [['5'], ['7', '8']]]
# test_set2 = [[['1'], ['2'], ['3']], [['2'], ['5']], [['1'], ['2'], ['3'], ['5']], [['2'], ['4'], ['5']], [['5'], ['7', '8']]]
test_set1 = women_train_data[:]
test_set2 = men_train_data[:]

# men oversampling
number_of_iterations = len(test_set1) - len(test_set2)
test_set_new = []
for _ in xrange(number_of_iterations):
    test_set_new.append(test_set2[randint(0, len(test_set2) - 1)])

test_set2 += test_set_new

print(len(test_set1))
print(len(test_set2))

rules_tree1 = Trie(test_set1)
rules_tree2 = Trie(test_set2)
rules_tree1.trie_for_rules()
rules_tree2.trie_for_rules()
# print(rules_tree.support_t([['5', '6']]))
# print("##############################")
# print rules_tree.node_sequence_dict
# print rules_tree.node_childes_dict
# print rules_tree.node_visits_dict
# print rules_tree.node_full_sequence_dict
# print rules_tree.number_of_objects
imp_rules1 = rules_tree1.important_rules_selection(0.0001)
imp_rules2 = rules_tree2.important_rules_selection(0.0001)

inf1 = RulesImportance(imp_rules1, rules_tree1, rules_tree2, 1.5)
inf2 = RulesImportance(imp_rules2, rules_tree2, rules_tree1, 1.5)
classifier = Classification(inf1, inf2)
print(len(inf1.dict_of_rules))
print(len(inf2.dict_of_rules))

# print(imp_rules1)
# print(imp_rules2)
# print("#######################")
# print(inf1.dict_of_contributions_to_score_class)
# print(inf1.dict_of_rules)
# print("")
# print(inf2.dict_of_contributions_to_score_class)
# print(inf2.dict_of_rules)

# man_data = SequencesFromFile('/Users/danil.gizdatullin/Documents/folder/Kaggle/new data exp/Men_dataset.csv')
# data = man_data.from_file_to_data_list()
# men_train_data = data[0]
# men_test_data = data[1]
#
# trie_man_rules = Trie(men_train_data)
# trie_man_rules.trie_for_rules()
# print(len(trie_man_rules.structure))
results = classifier.classifier(women_train_data, men_train_data)
print(len(women_train_data))
print(len(men_train_data))
t, f, m, w = classifier.classifier_statistics(results)
print t
print f
print m
print w
# print("#######################")
# answer = []
# true = 0
# false = 0
# nc = 0
# for rule in women_test_data:
#     answer.append(classifier.classify_object(rule, women_train_data, men_train_data))
#
# for item in answer:
#     if item == 1:
#         false += 1
#     elif item == 0:
#         true += 1
#     elif item == -1:
#         nc += 1
#
# print true
# print false
# print nc
