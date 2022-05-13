# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 13:51:42 2016
This program is a new evaluation metric for Chinese word segmentation. 
The detailed algorithm can be found in the following paper.

Peng Qian, Xipeng Qiu, Xuanjing Huang, A New Psychometric-inspired 
Evaluation Metric for Chinese Word Segmentation, 
In Proceedings of Annual Meeting of the Association for Computational Linguistics (ACL), 2016.

@author: Peng
"""

"""
How to use this file:
establish a new folder named as 'submissions' under this directory, put the file need to be evaluated into it,
the file should ends with suffix 'close'

while the answer to the test set is absent in this project, if you want to apply for it, please contact us.
"""

import numpy as np



def load_word_weight():
    f = open('nlpcc2016-wordseg-test-ans.weight','r')
    weight = f.readlines()
    weight = [line.strip().split() for line in weight]
    for i in range(len(weight)):
        for j in range(len(weight[i])):
            weight[i][j] = float(weight[i][j])      
    f.close()
    f = open('nlpcc2016-wordseg-test-ans.weight_c','r')
    weight_c = f.readlines()
    weight_c = [line.strip().split() for line in weight_c]
    for i in range(len(weight_c)):
        for j in range(len(weight_c[i])):
            weight_c[i][j] = float(weight_c[i][j])      
    f.close()
    return weight, weight_c    

def sent2features(sent, plan):
    return [word2features(sent, i, plan) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, label in sent]

def sent2tokens(sent):
    return [token for token, label in sent]



def evaluate_word_PRF(y_pred,y):
    c = 0  
    true = 0
    pos = 0
    for i in xrange(len(y)):
        start = 0
        for j in xrange(len(y[i])):
            if y_pred[i][j] == 'E' or y_pred[i][j] == 'S':
                pos += 1
            if y[i][j] == 'E' or y[i][j] == 'S':
                flag = True
                if y_pred[i][j] != y[i][j]:
                    flag = False
                if flag:
                    for k in range(start,j):
                        if y_pred[i][k] != y[i][k]:
                            flag = False
                            break
                    if flag:
                        c += 1
                true += 1
                start = j+1   

    P = c/float(pos)
    R = c/float(true)
    F = 2*P*R/(P+R)    
    return P,R,F




def  evaluate_word_weightedPRF2(y_pred,y,weight,weight_c):
    c = 0  
    pos_true = 0
    true = 0
    pos = 0
    punishment = 0
    punishment_all = 0
    c2 = 0
    true2 = 0
    guess = 0
    guess2 = 0
    earned_weight = []
    for i in xrange(len(y)):
        start = 0
        word_index = 0
        for j in xrange(len(y[i])):
            if y_pred[i][j] == 'E' or y_pred[i][j] == 'S':
                pos += 1
                guess += weight_c[i][j]
                guess2 += 1-weight_c[i][j]
                if y[i][j] == 'B' or y[i][j] == 'M':
                    punishment += (1-weight_c[i][j])
            if y[i][j] == 'E' or y[i][j] == 'S':
                flag = True
                if y_pred[i][j] != y[i][j]:
                    flag = False
                if flag:
                    for k in range(start,j):
                        if y_pred[i][k] != y[i][k]:
                            flag = False
                            break
                    if flag:
                        c += 1*weight[i][word_index]
                        c2 += 1-weight[i][word_index]
                        pos_true += 1
                        earned_weight.append(weight[i][word_index])
                true += 1*weight[i][word_index]
                true2 += 1-weight[i][word_index]
                word_index += 1
                start = j+1   
            else:
                punishment_all += (1-weight_c[i][j])

    R_H = c/float(true)
    R_E = c2/float(true2)

    P_H = c/float(guess) # precision hard
    P_E = c2/float(guess2) # precision easy 
    R = 2*R_H*R_E/(R_H+R_E)  
    P = 2*P_H*P_E/(P_H+P_E)  
    F = 2*P*R/(P+R) 
    return P_H, P_E, R_H, R_E, P,R,F,earned_weight



def BMES2seg(y, path2):
    rs = []
    for i in xrange(len(y)):
        start = 0
        sent = []
        for j in xrange(len(y[i])):
            if y[i][j][1] == u'E' or y[i][j][1] == u'S':
                word = ''.join([w for (w,t) in y[i][start:(j+1)]])
                sent.append(word.encode('utf-8'))
                start = j+1
        rs.append(' '.join(sent))
    f = open(path2,'w')
    for sent in rs:
        f.write(sent)
        f.write('\n')
    f.close()

def seg2BMES(path):
    f = open(path,'r')
    seg = f.readlines()
    f.close()
    seg  =[line.strip().decode('utf-8').split() for line in seg]
    rs = []
    for sent in seg:
        sent_label = []
        for token in sent:
            if len(token)==1:
                sent_label.append('S')
            elif len(token) == 2:
                sent_label += ['B','E']
            else:
                sent_label += ['B']+['M']*(len(token)-2)+['E']
        raw = ''.join(sent)
        rs.append(zip(raw,sent_label))
    return rs

weight, weight_c = load_word_weight()

dataset = 'nlpcc2016test'
test_sents = seg2BMES('nlpcc2016-wordseg-test_ans.dat'.decode('utf-8'))
print dataset,len(test_sents), 'testing samples'

y_test = [sent2labels(s) for s in test_sents]

submissions = ['submission-test']
for sub in submissions:
    pred_sents = seg2BMES('submissions/'.decode('utf-8')+sub+'.close')
    y_pred = [sent2labels(s) for s in pred_sents]
    print 'Participant:',sub
    print 'traditional P:\t%f   R: %f   F: %f' % evaluate_word_PRF(y_pred,y_test)
    P_H, P_E, R_H, R_E, P,R,F,weight_earned = evaluate_word_weightedPRF2(y_pred,y_test,weight,weight_c)
    print 'weighted P_H:\t%f   P_E:\t%f   R_H:\t%f   R_E:\t%f   P:\t%f   R: %f   F: %f' % (P_H, P_E, R_H, R_E, P,R,F)

