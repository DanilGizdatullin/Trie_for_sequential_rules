__author__ = 'danil.gizdatullin'

import numpy as np

INF_VALUE = 100


class Trie:
    def __init__(self, list_of_sequences):
        self.nodes = set([])
        self.node_childes_dict = {}
        self.node_parent_dict = {}
        self.node_sequence_dict = {}
        self.node_visits_dict = {}
        self.node_full_sequence_dict = {}
        self.list_of_sequences = list_of_sequences
        self.number_of_objects = len(list_of_sequences)

    def trie_for_rules(self):
        nodes = set([])
        structure = {}
        dict_seq = {}
        dict_num = {}
        dict_prev = {}
        dict_all_seq = {}

        # len_of_seq = len(self.list_of_sequences)
        free_node = 1
        seq1 = self.list_of_sequences[0]
        nodes.add(0)
        current_node = 0
        dict_all_seq[0] = []

        for i in seq1:
            structure[current_node] = [free_node]
            structure[free_node] = []
            dict_prev[free_node] = current_node

            str_seq = [elem for elem in i]
            dict_all_seq[free_node] = dict_all_seq[current_node][:]
            dict_all_seq[free_node].append(str_seq)

            if type(str_seq) == list:
                dict_seq[free_node] = str_seq
            else:
                dict_seq[free_node] = [str_seq]
            dict_num[free_node] = 1
            current_node = free_node
            free_node += 1

        for seq in self.list_of_sequences[1:]:
            current_node = 0
            for elem in seq:
                str_seq = [i for i in elem]
                if len(structure[current_node]) > 0:
                    temp_seq = [dict_seq[son] for son in structure[current_node]]
                    flag = str_seq in temp_seq
                    if flag:
                        number = 0
                        while temp_seq[number] != str_seq:
                            number += 1
                        current_node = structure[current_node][number]
                        dict_num[current_node] += 1
                    else:
                        structure[current_node].append(free_node)
                        dict_prev[free_node] = current_node
                        dict_all_seq[free_node] = dict_all_seq[current_node][:]
                        dict_all_seq[free_node].append(str_seq)
                        current_node = free_node
                        structure[current_node] = []
                        dict_num[current_node] = 1
                        dict_seq[current_node] = str_seq
                        free_node += 1
                else:
                    structure[current_node].append(free_node)
                    dict_prev[free_node] = current_node
                    dict_all_seq[free_node] = dict_all_seq[current_node][:]
                    dict_all_seq[free_node].append(str_seq)
                    current_node = free_node
                    structure[current_node] = []
                    dict_num[current_node] = 1
                    dict_seq[current_node] = str_seq
                    free_node += 1

        self.nodes = nodes
        self.node_childes_dict = structure
        self.node_sequence_dict = dict_seq
        self.node_visits_dict = dict_num
        self.node_parent_dict = dict_prev
        self.node_full_sequence_dict = dict_all_seq

    def support_t(self, rule):
        dic_all_seq_rev = {str(v): k for k, v in self.node_full_sequence_dict.iteritems()}
        try:
            node = dic_all_seq_rev[str(rule)]
        except KeyError:
            node = -1
        if node == -1:
            sup = 0
        else:
            sup = self.node_visits_dict[node]
        return sup/float(self.number_of_objects)

    def important_rules_selection(self, min_threshold):
        ds_rules = []
        for item in self.node_full_sequence_dict.items():
            rule = item[1]
            if rule:
                if self.support_t(rule) > min_threshold:
                    ds_rules.append(rule)

        return ds_rules


def _growth_rate_t(rule, trie1, trie2):
    support_data_set1 = trie1.support_t(rule)
    support_data_set2 = trie2.support_t(rule)
    if (support_data_set1 == 0) & (support_data_set2 == 0):
        return 0
    elif (support_data_set1 != 0) & (support_data_set2 == 0):
        return INF_VALUE
    else:
        return support_data_set1 / float(support_data_set2)


class RulesImportance:
    def __init__(self, rules, trie1, trie2, threshold):
        self.dict_of_contributions_to_score_class = {}
        self.dict_of_rules = {}

        for i in xrange(len(rules)):
            self.dict_of_rules[str(97 + i)] = rules[i]

        rules_to_delete = []

        for key in self.dict_of_rules.iterkeys():
            gr_ra1 = _growth_rate_t(self.dict_of_rules[key], trie1, trie2)
            if gr_ra1 > threshold:
                if gr_ra1 == INF_VALUE:
                    self.dict_of_contributions_to_score_class[key] = trie1.support_t(self.dict_of_rules[key])
                else:
                    self.dict_of_contributions_to_score_class[key] = (gr_ra1 / (1 + gr_ra1)) * \
                                                                     (trie1.support_t(self.dict_of_rules[key]))
            else:
                rules_to_delete.append(key)

        contributions = self.dict_of_contributions_to_score_class.values()
        contributions = np.array(contributions)
        median = np.median(contributions)
        # median = len(contributions)
        print("Median = %f" % median)

        for key, value in self.dict_of_contributions_to_score_class.items():
            self.dict_of_contributions_to_score_class[key] = value / float(median)

        for key in rules_to_delete:
            del self.dict_of_rules[key]
