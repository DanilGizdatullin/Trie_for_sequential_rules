__author__ = 'danil.gizdatullin'

import csv
from random import shuffle


class SequencesFromFile:
    def __init__(self, file_name):
        self.file_name = file_name
        self.coding_dict = {'work': 1,
                            'separation': 2,
                            'partner': 3,
                            'marriage': 4,
                            'children': 5,
                            'parting': 6,
                            'divorce': 7,
                            'education': 8}

    def from_file_to_data_list(self):
        # csvfile = open('/Users/danil.gizdatullin/Documents/folder/Kaggle/new data exp/Men_dataset.csv', 'r')
        csvfile = open(self.file_name, 'r')

        sreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        names = sreader.next()  # stores attributes' names

        data_list = []
        for row in sreader:
            # reads all lines in the csv file
            # and stores them in a dictionary with the value of an attribute

            data_dict = {}
            attr_ind = 0
            if row != ['', '', '', '', '', '', '', '']:
                for cell in row:
                    if cell != '':
                        data_dict[names[attr_ind]] = int(cell)
                    attr_ind += 1
                data_list.append(data_dict)
            # cnt+=1
            # if cnt==20: break

        csvfile.close()

        ds_men = self.data_list_to_sequence_list2(data_list)

        # try oversampling
        # oversampling_cnt = 1767
        # choose_range = len(ds_men)
        # ds_men_oversampling = ds_men[:]
        # for i in xrange(oversampling_cnt):
        #     ds_men_oversampling.append(ds_men[random.randint(0, choose_range-1)])

        number_of_objects = len(ds_men)
        train_size = 0.8
        train_size *= number_of_objects
        train_size = int(train_size)

        ds_men_for_shuffle = ds_men[:]
        shuffle(ds_men_for_shuffle)

        ds_men_train = ds_men_for_shuffle[:train_size]
        ds_men_test = ds_men[train_size:]

        return [ds_men_train, ds_men_test]

    def data_list_to_sequence_list2(self, data_list):
        # maps attributes to a sequence based on sorting them by age in an ascending order
        # taking into account equal ages

        sequence_list = []
        # names=sorted(names)

        for row in data_list:
            temp_serq = sorted(row.keys(), key=row.get)
            sequence = []
            prev_ev = ''
            for ev in temp_serq:
                if prev_ev == '':
                    sequence.append([str(self.coding_dict[ev])])
                    # print row
                elif row[prev_ev] == row[ev]:
                    # print row
                    sequence[-1].append(str(self.coding_dict[ev]))
                else:
                    # print row
                    sequence.append([str(self.coding_dict[ev])])
                prev_ev = ev
            sequence_list.append(sequence)

        return sequence_list
