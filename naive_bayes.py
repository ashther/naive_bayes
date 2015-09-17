# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 17:34:23 2015

@author: Administrator
"""
import numpy as np
import random
from sklearn.naive_bayes import GaussianNB
from dataSource import *

#def trainCreate(data, res):
#    num = random.randint(0, len(data)-1)
#    ind = np.hstack((np.arange(num), np.arange(num+1, len(data))))
#    train = np.column_stack((data, res))[ind]
#    test = data[num]
#    result = res[num]
#    return train, test, result
    
def densityProbCaculate(x, miu, sigma):
    return 1 / (np.sqrt(2*np.pi) * sigma * np.exp((x-miu)**2/(2*sigma**2)))

#def continuousBayes(train, test):
#    category = set(train[:, -1])
#    max_prob = 0
#    for ctg in category:
#        data_ctg = train[train[:, -1] == ctg, :-1].astype(float)
#        prob_ctg = float(len(data_ctg)) / float(len(train))
#        prob_feature = reduce(lambda x,y:x*y, 
#                              map(densityProbCaculate, test, 
#                                  data_ctg.mean(axis=0), data_ctg.std(axis=0, ddof=1)))
#        prob = prob_ctg * prob_feature
#        if prob > max_prob:
#            max_prob, result = prob, ctg
#    return result
   
def probCaculate(s, items):
    return ((items == s).sum() + 1.) / len(items)

#def discreteBayes(train, test):
#    category = set(train[:, -1])
#    max_prob = 0
#    for ctg in category:
#        data_ctg = train[train[:, -1] == ctg, :-1]
#        prob_ctg = float(len(data_ctg)) / float(len(train))
#        prob_feature = reduce(lambda x,y:x*y, 
#                              map(probCaculate, test, data_ctg.transpose()))
#        prob = prob_ctg * prob_feature
#        print ctg, prob_ctg, prob_feature, prob
#        if prob > max_prob:
#            max_prob, result = prob, ctg
#    print result
#    return result
    
def naiveBayes(train, test, method):
    category = set(train[:, -1])
    max_prob = 0
    for ctg in category:
        data_ctg = train[train[:, -1] == ctg, :-1]
        prob_ctg = float(len(data_ctg)) / float(len(train))
        if method == 'dis':
            prob_feature = reduce(lambda x,y:x*y, 
                                  map(probCaculate, test, data_ctg.transpose()))
        else:
            data_ctg = data_ctg.astype(float)
            prob_feature = reduce(lambda x,y:x*y, 
                              map(densityProbCaculate, test, 
                                  data_ctg.mean(axis=0), data_ctg.std(axis=0, ddof=1)))
        prob = prob_ctg * prob_feature
        if prob > max_prob:
            max_prob, result = prob, ctg
    return result

#def crossValidation(data, res, k, method):
#    precision = np.zeros(k)
#    for i in range(k):
#        train, test, result = trainCreate(data, res)
#        predict = discreteBayes(train, test) if method == 'dis' else continuousBayes(train, test)
#        if predict == result:
#            precision[i] = 1
#    return precision.mean()
  
def eachTest(data, res, method):
    correct = 0
    for i, da in enumerate(data):
        ind = np.hstack((np.arange(i), np.arange(i+1, len(data))))
        train = np.column_stack((data, res))[ind]
        test = da
        result = res[i]
        predict = naiveBayes(train, test, method)       
        if predict == result:
            correct += 1
    return float(correct) / len(data)

def skTest(data, res):
    correct = 0
    for i, da in enumerate(data):
        ind = np.hstack((np.arange(i), np.arange(i+1, len(data))))
        train = data[ind]
        train_result = res[ind]
        test = da
        result = res[i]
        clf = GaussianNB()     
        clf.fit(train, train_result)
        predict = clf.predict(test)[0]       
        if predict == result:
            correct += 1
    return float(correct) / len(data)



















