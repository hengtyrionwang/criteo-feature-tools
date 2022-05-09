'''
Descripttion: 
version: 
Author: Heng Tyrion Wang
Date: 2022-05-08 17:25:08
LastEditors: Heng Tyrion Wang
Email: hengtyrionwang@gmail.com
LastEditTime: 2022-05-09 08:36:01
'''

from sklearn.model_selection import StratifiedKFold
import csv
import argparse

import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description="Run data split.")
    parser.add_argument('--in_path', nargs='?', default='./dataset/train.csv',help='Input path.')
    parser.add_argument('--out_path', nargs='?', default='./split',help='Output path.')
    parser.add_argument('--split1', nargs='?', default='test_valid',help='first file name.')
    parser.add_argument('--split2', nargs='?', default='train',help='second file name.')
    parser.add_argument('--ratio', type=float, default=0.2,help='ratio of partition.')
    parser.add_argument('--seed', type=int, default=2022, help='random seed.')
    return parser.parse_args()


class Sample_Data(object):
    def __init__(self, args):
        self.inpath = args.in_path
        self.outpath = args.out_path
        self.seed = args.seed
        self.ratio = args.ratio
        self.split1 = args.split1
        self.split2 = args.split2

    def get_index(self):
        X = []
        y = []

        for i, row in enumerate(csv.DictReader(open(self.inpath)), start=1):
            y.append(row['Label'])
            X.append(row['Id'])

        folds = StratifiedKFold(n_splits=10, shuffle=True, random_state=self.seed).split(X, y)

        fold_indexes = []
        for train_id, valid_id in folds:
            fold_indexes.append(valid_id)
        test_index = fold_indexes[0]
        valid_index = fold_indexes[1]
        train_index = np.concatenate(fold_indexes[2:])

        return test_index.tolist(), valid_index.tolist(),train_index.tolist()

    def write_file(self, type, line):
        with open(self.outpath + "/" + type + ".csv", "a+") as f:
            f.write(line)

    def write_header(self):
        header = 'Id,Label,I1,I2,I3,I4,I5,I6,I7,I8,I9,I10,I11,I12,I13,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26\n' 
        self.write_file("train", header)
        self.write_file("valid", header)
        self.write_file("test", header)

    def fit(self):
        self.write_header()
        test_index, valid_index,train_index  = self.get_index()
        index = 0
        i =0
        j =0
        with open(self.inpath, "r") as f:
            line = f.readline()# header
            line = f.readline()
            while line:
                if i < len(test_index) and index == test_index[i]:
                    self.write_file("test", line)
                    i += 1
                elif j < len(valid_index) and index == valid_index[j]:
                    self.write_file("valid", line)
                    j += 1
                else:
                    self.write_file("train", line)
                index += 1
                line = f.readline()


if __name__ == "__main__":
    args = parse_args()
    sp = Sample_Data(args)
    sp.fit()

    

