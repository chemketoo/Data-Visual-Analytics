from util import entropy, information_gain, partition_classes
import numpy as np 
import ast
from numbers import Number

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        self.leafsize = 10
        self.depth = 6
        self.tempTree = [] 
        self.tree = []

    def  attribute_selection(ans,X,y):
        neg = - 1.0        
        len_X = len(X[0])
        for index in range(len_X):
            if isinstance(X[0][index], Number):
                values = np.mean([ x[index] for x in X ])
                lx, rx, ly, ry = partition_classes(X,y,index,values)
                tg = information_gain(y,[ly,ry])
                if tg > neg:
                    neg = tg
                    oi =  index
                    ov = values
            else : 
                lv = set([x[index] for x in X])
                for values in lv:
                    lx,rx, ly, ry = partition_classes(X,y,index,values)
                    tg = information_gain(y,[ly,ry])
                    if tg > neg:
                        neg = tg
                        oi =  index
                        ov = values
        return oi, ov

    def construct_tree(ans,att,val):
        ans.depth += ans.depth
        if len(val) < ans.leafsize or ans.depth > 30 or len(set(val)) ==1:
            return [-1, int(round(np.mean(val))), -1, -1]
        split_attribute, split_val = ans.attribute_selection(att,val)
        xl, xr, yl, yr = partition_classes(att, val, split_attribute, split_val)
        tl = ans.construct_tree(xl, yl)
        rl = ans.construct_tree(xr, yr)
        return [split_attribute, split_val, tl, rl]
        

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        #pass

        # we need to add stop conditioin:
        # 1. set the limitation to self.depth
        # 2. set the threshold to the number in the terminal node
        # 3. if all the y values is the same
        # (must avoid the empty list in the partition class)
        self.tree = self.construct_tree(X,y)

    def preliminary_class(att, pre_record):
        if att.tempTree[0]== -1:
            return att.tempTree[1]
        if isinstance(pre_record[att.tempTree[0]], Number):
            if pre_record[att.tempTree[0]] <= att.tempTree[1]:
                att.tempTree = att.tempTree[2]
                return att.preliminary_class(pre_record)
            else :     
                att.tempTree = att.tempTree[3]
                return att.preliminary_class(pre_record)
        else : 
            if pre_record[att.tempTree[0]] ==  att.tempTree[1]:
                att.tempTree = att.tempTree[2]
                return att.preliminary_class(pre_record)
            else :     
                att.tempTree = att.tempTree[3]
                return att.preliminary_class(pre_record)


    def classify(self, record):
        self.tempTree = self.tree
        return self.preliminary_class(record)



