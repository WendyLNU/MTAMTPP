# -*- coding: utf-8 -*-
# @Time    : 2020/7/24 19:29
# @Author  : zxl
# @FileName: data_loader.py

import json
import numpy as np
import pickle
class DataLoader():

    def pro_time_method(self, time_stamp_seq, mask_time):
        timelast_list = [time_stamp_seq[i+1]-time_stamp_seq[i] for i in range(0,len(time_stamp_seq)-1,1)]
        timelast_list.insert(0,0)
        timenow_list = [mask_time-time_stamp_seq[i] for i in range(0,len(time_stamp_seq),1)]

        return [timelast_list,timenow_list]

    def load_save_datasets(self):
        def process_line(line):
            tmp = [0]
            line[0].append(5)
            tmp.append(line[0])
            tmp.append(line[0])
            line[1].append(line[3])
            tmp.append(line[1])
            time_dif = self.pro_time_method(tmp[3], line[3])
            tmp.append(time_dif[0])
            tmp.append(time_dif[1])
            tmp.append([i for i in range(0, len(tmp[1]))])
            tmp.append([line[2],line[2],line[3]])
            tmp.append(line[4]+1)
            return tmp

        train_set = []
        test_set = []
        train_path = '/Users/wendy/Documents/code/TPP_V2/data/training_testing_data/data_hawkes/train.txt'
        test_path = '/Users/wendy/Documents/code/TPP_V2/data/training_testing_data/data_hawkes/test.txt'
        self.dataset_class_train = '/Users/wendy/Documents/code/MTAMTPP/data/training_testing_data/hawkes_time_item_based_unidirection/train_data.txt'
        self.dataset_class_test = '/Users/wendy/Documents/code/MTAMTPP/data/training_testing_data/hawkes_time_item_based_unidirection/test_data.txt'
        self.dataset_class_pkl = '/Users/wendy/Documents/code/MTAMTPP/data/training_testing_data/hawkes_time_item_based_unidirection/parameters.pkl'

        with open(train_path, 'r') as f:
            self.train_set = []
            L = f.readlines()
            for line in L:
                line = eval(line)
                train_set.append(process_line(line))
                if len(train_set) > 50000:
                    break
            # if len(self.train_set) > 10000:
            # self.train_set = random.sample(self.train_set, 10000)

        # load test data
        with open(test_path, 'r') as f:
            self.test_set = []
            L = f.readlines()
            for line in L:
                line = eval(line)
                test_set.append(process_line(line))
                if len(test_set) > 5000:
                    break

        with open(self.dataset_class_pkl, 'wb') as f:
            data_dic = {}
            data_dic["item_count"] = 5
            data_dic["user_count"] = 1
            data_dic["category_count"] = 5
            #data_dic["gap"] = self.gap
            #data_dic["item_category"] = self.item_category_dic
            pickle.dump(data_dic, f, pickle.HIGHEST_PROTOCOL)

        # train text 和 test text 使用文本
        self.save(train_set,self.dataset_class_train)
        self.save(test_set,self.dataset_class_test)

        return train_set, test_set

    def save(self,data_list,file_path):
        fp = open(file_path, 'w+')
        for i in data_list:
            fp.write(str(i) + '\n')
        fp.close()






if __name__ == "__main__":
    loder = DataLoader()
    train_set, test_set = loder.load_save_datasets()