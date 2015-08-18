__author__ = 'danil.gizdatullin'

from trie import Trie, RulesImportance


def _from_rules_list_to_dict(dataset={}, one_object=[],  status=0, free_id=1):
    dataset[free_id] = {}
    dataset[free_id]["data"] = one_object
    dataset[free_id]["status"] = status


def _from_list_to_dataset(dataset={}, datalist=[], status=0, free_id=1):
        free_id = 1
        for rules in datalist:
            _from_rules_list_to_dict(dataset, rules, status, free_id)
            free_id += 1

        return dataset


class Classification:
    def __init__(self, rules_information0, rules_information1):
        self.zero_class_rules = rules_information0
        self.first_class_rules = rules_information1

    # add to this some variants when <bc-d> in <a-bc-d>
    def _classify_object(self, object_to_classification):
        score_for_class0 = 0
        score_for_class1 = 0
        rules_from_class0 = []
        rules_from_class1 = []

        for rule_id, rule in self.zero_class_rules.dict_of_rules.items():
            rule_len = len(rule)
            if rule == object_to_classification[0:rule_len]:
                rules_from_class0.append(rule_id)

        for rule_id, rule in self.first_class_rules.dict_of_rules.items():
            rule_len = len(rule)
            if rule == object_to_classification[0:rule_len]:
                rules_from_class1.append(rule_id)

        for rule in rules_from_class0:
            if rule in self.zero_class_rules.dict_of_contributions_to_score_class:
                score_for_class0 += self.zero_class_rules.dict_of_contributions_to_score_class[rule]

        for rule in rules_from_class1:
            if rule in self.first_class_rules.dict_of_contributions_to_score_class:
                score_for_class1 += self.first_class_rules.dict_of_contributions_to_score_class[rule]

        if (score_for_class0 == score_for_class1) and (score_for_class1 == 0):
            return -1
        elif score_for_class0 >= score_for_class1:
            return 0
        else:
            return 1

    def classifier(self, test_data0, test_data1):
        test_set1 = test_data0
        test_set2 = test_data1
        rules_tree1 = Trie(test_set1)
        rules_tree2 = Trie(test_set2)
        rules_tree1.trie_for_rules()
        rules_tree2.trie_for_rules()
        imp_rules1 = rules_tree1.important_rules_selection(0.0001)
        imp_rules2 = rules_tree2.important_rules_selection(0.0001)

        inf1 = RulesImportance(imp_rules1, rules_tree1, rules_tree2, 1.2)
        inf2 = RulesImportance(imp_rules2, rules_tree2, rules_tree1, 1.2)
        classifier = Classification(inf1, inf2)

        all_data = {}
        temp_object = _from_list_to_dataset(all_data, test_data0, 0, 1)
        n_0 = len(test_data0) + 1
        all_data = _from_list_to_dataset(temp_object, test_data1, 1, n_0)
        results = []

        print("Length Length %f" % len(all_data))
        for id in all_data.iterkeys():
            data = all_data[id]["data"]
            status = all_data[id]["status"]
            results.append((self._classify_object(data), status))

        return results

    def classifier_statistics(self, results):
        true = 0
        false = 0
        all = 0
        true_women = 0
        women = 0
        true_men = 0
        men = 0
        for obs in results:
            if obs[0] == obs[1] == 0:
                true += 1
                all += 1
                true_women += 1
                women += 1
            elif obs[1] == obs[0] == 1:
                true += 1
                all += 1
                true_men += 1
                men += 1
            elif obs[1] == 0:
                false += 1
                all += 1
                men += 1
            elif obs[1] == 1:
                false += 1
                all += 1
                women += 1
            elif obs[1] != -1:
                false += 1
                all += 1

        return true/float(all), false/float(all), true_men/float(men), true_women/float(women)
