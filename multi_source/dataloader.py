# encoding=utf-8
import numpy as np

train_eval_rate = 0.8


class DataMaster(object):
    def __init__(self):
        self.datasets = np.load('./data/protein_matrix.npy')
        self.dataembs = np.load('./data/protein_emb.npy')
        self.datalabels = np.load('./data/protein_label.npy')

        self.trainsets = self.datasets[
                         :int(train_eval_rate * len(self.datasets))]  # train_X is bootstraped in this dataset
        self.trainembs = self.dataembs[:int(train_eval_rate * len(self.dataembs))]
        self.trainlabels = self.datalabels[:int(train_eval_rate * len(self.datalabels))]

        print("training data numbers(%d%%): %d" % (train_eval_rate * 100, len(self.datalabels)))
        self.pos_idx = (self.trainlabels == 1).reshape(-1)
        self.neg_idx = (self.trainlabels == 0).reshape(-1)
        self.training_size = len(self.trainlabels[self.pos_idx]) * 2
        print("positive data numbers", str(self.training_size // 2))

        self.test_X = self.datasets[int(train_eval_rate * len(self.datasets)):]
        self.test_E = self.dataembs[int(train_eval_rate * len(self.dataembs)):]
        self.test_Y = self.datalabels[int(train_eval_rate * len(self.datalabels)):]
        print("test data numbers", str(len(self.test_Y)))
        self.test_size = len(self.datalabels)

    def shuffle(self):
        mark = list(range(self.training_size // 2))
        np.random.shuffle(mark)
        self.train_X = np.concatenate([self.trainsets[self.pos_idx], self.trainsets[self.neg_idx][mark]])
        self.train_E = np.concatenate([self.trainembs[self.pos_idx], self.trainembs[self.neg_idx][mark]])
        self.train_Y = np.concatenate([self.trainlabels[self.pos_idx], self.trainlabels[self.neg_idx][mark]])
        mark = list(range(self.training_size))
        np.random.shuffle(mark)
        self.train_X = self.train_X[mark]
        self.train_E = self.train_E[mark]
        self.train_Y = self.train_Y[mark]


if __name__ == '__main__':
    DataMaster()
