from scipy import stats
import numpy as np
from numbers import Number

# This method computes entropy for information gain
def entropy(class_y):
    # Input:            
    #   class_y         : list of class labels (0's and 1's)
    
    # TODO: Compute the entropy for a list of classes
    #
    # Example:
    #    entropy([0,0,0,1,1,1,1,1,1]) = 0.92
    # if (sum(class_y)==0) or (sum(class_y)==len(class_y)):
    #     return 0.0
    # else : 
    #     fl = float(sum(class_y))/float(len(class_y))
    #     s = 1-fl
    #     entropy = -fl*np.log2(fl)-s*np.log2(s)
    #     return entropy

    array1 = np.array(class_y)
    xu, yc = np.unique(array1, return_counts=True)
    return stats.entropy(yc, base=2)


def partition_classes(X, y, split_attribute, split_val):
    # Inputs:
    #   X               : data containing all attributes
    #   y               : labels
    #   split_attribute : column index of the attribute to split on
    #   split_val       : either a numerical or categorical value to divide the split_attribute
    
    # TODO: Partition the data(X) and labels(y) based on the split value - BINARY SPLIT.
    # 
    # You will have to first check if the split attribute is numerical or categorical    
    # If the split attribute is numeric, split_val should be a numerical value
    # For example, your split_val could be the mean of the values of split_attribute
    # If the split attribute is categorical, split_val should be one of the categories.   
    #
    # You can perform the partition in the following way
    # Numeric Split Attribute:
    #   Split the data X into two lists(X_left and X_right) where the first list has all
    #   the rows where the split attribute is less than or equal to the split value, and the 
    #   second list has all the rows where the split attribute is greater than the split 
    #   value. Also create two lists(y_left and y_right) with the corresponding y labels.
    #
    # Categorical Split Attribute:
    #   Split the data X into two lists(X_left and X_right) where the first list has all 
    #   the rows where the split attribute is equal to the split value, and the second list
    #   has all the rows where the split attribute is not equal to the split value.
    #   Also create two lists(y_left and y_right) with the corresponding y labels.

    '''
    Example:
    
    X = [[3, 'aa', 10],                 y = [1,
         [1, 'bb', 22],                      1,
         [2, 'cc', 28],                      0,
         [5, 'bb', 32],                      0,
         [4, 'cc', 32]]                      1]
    
    Here, columns 0 and 2 represent numeric attributes, while column 1 is a categorical attribute.
    
    Consider the case where we call the function with split_attribute = 0 and split_val = 3 (mean of column 0)
    Then we divide X into two lists - X_left, where column 0 is <= 3  and X_right, where column 0 is > 3.
    
    X_left = [[3, 'aa', 10],                 y_left = [1,
              [1, 'bb', 22],                           1,
              [2, 'cc', 28]]                           0]
              
    X_right = [[5, 'bb', 32],                y_right = [0,
               [4, 'cc', 32]]                           1]
    Consider another case where we call the function with split_attribute = 1 and split_val = 'bb'
    Then we divide X into two lists, one where column 1 is 'bb', and the other where it is not 'bb'.
        
    X_left = [[1, 'bb', 22],                 y_left = [1,
              [5, 'bb', 32]]                           0]
              
    X_right = [[3, 'aa', 10],                y_right = [1,
               [2, 'cc', 28],                           0,
               [4, 'cc', 32]]                           1]
               
    ''' 
    X_left = []
    X_right = []

    y_left = []
    y_right = []
    if isinstance(X[0][split_attribute], Number):
        for index in range(len(X)):
            if X[index][split_attribute] <= split_val:
                X_left.append(X[index])
                y_left.append(y[index])
            else :
                X_right.append(X[index])
                y_right.append(y[index])
    else :
        for index in range(len(X)):
            if X[index][split_attribute] == split_val:
                X_left.append(X[index])
                y_left.append(y[index])
            else :
                X_right.append(X[index])
                y_right.append(y[index])
    return (X_left, X_right, y_left, y_right)

    
def information_gain(previous_y, current_y):
    # Inputs:
    #   previous_y: the distribution of original labels (0's and 1's)
    #   current_y:  the distribution of labels after splitting based on a particular
    #               split attribute and split value
    
    # TODO: Compute and return the information gain from partitioning the previous_y labels
    # into the current_y labels.
    # You will need to use the entropy function above to compute information gain
    # Reference: http://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15381-s06/www/DTs.pdf
    
    """
    Example:
    
    previous_y = [0,0,0,1,1,1]
    current_y = [[0,0], [1,1,1,0]]
    
    info_gain = 0.45915
    """
    en = entropy(previous_y)
    leng = len(previous_y)
    c_y = current_y[0]
    c_y1 = current_y[1]
    l_en = float(len(c_y))/float(leng)*entropy(c_y)
    r_en = float(len(c_y))/float(leng)*entropy(c_y1)
    info_gain = en - l_en - r_en
    return info_gain