__author__ = 'danil.gizdatullin'

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

        for key in rules_to_delete:
            del self.dict_of_rules[key]