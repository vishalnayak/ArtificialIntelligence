__author__ = 'vishal'

import math
import timeit
from operator import itemgetter

"""
Main method which extracts the train data from the files, builds the model and uses it predict the samples in test data.
Modifying the threshold in this method, changes the chi-square split stopping criterion.
Three options are provided for threshold: 0.05,0.01,1
"""


def main():
    global in_count
    """
    Training samples containing the feature values
    """
    trainfeat = open('trainfeat.csv', 'r')
    """
    Training samples containing the class attribute values
    """
    trainlabs = open('trainlabs.csv', 'r')
    count = 0
    examples = []
    attributes = []

    """
    Set all the attributes as not split
    """
    for i in range(274):
        attributes.append('1')

    """
    Append the class attribute value to the feature set and build an on-memory version of train data.
    Removing the \n characters present in samples' file.
    """
    for feat_list in trainfeat:
        feat_list = feat_list.replace("\n", "")
        label = trainlabs.readline().replace("\n", "")
        feat_list_split = feat_list.split(" ")
        feat_list_split.extend(label)
        examples.append(feat_list_split)
        count += 1
    trainlabs.close()
    trainfeat.close()

    threshold = 0.0

    """
    Uncomment only one of the following three lines to test different chi-square stopping criterions
    """
    # threshold = 0.05
    # threshold = 0.01
    threshold = 1.0

    """
    Starting timer to calculate running time
    """
    start_time = timeit.default_timer()

    """
    Starting the recursive routine which builds the model which then will be used to predict the class attribute in test samples
    """
    tree = iterative_dichotomiser(examples, attributes, examples, threshold)

    """
    Inorder traversal of the model built. This also counts the number of nodes present in the tree
    """
    inorder(tree)

    tests = []
    t_mismatch = 0.0
    """
    Testing samples containing the feature values
    """
    testfeat = open('testfeat.csv', 'r')
    """
    Testing samples containing the class attribute values
    """
    testlabs = open('testlabs.csv', 'r')
    for feat_list in testfeat:
        feat_list = feat_list.replace("\n", "")
        label = testlabs.readline().replace("\n", "")
        feat_list_split = feat_list.split(" ")
        """
        The class attribute predicted by the model is returned by the lookup method.
        """
        attr_class = lookup(tree, feat_list_split).attr_class
        if (label == '1' and attr_class is 'N') or (label == '0' and attr_class is 'P'):
            t_mismatch += 1
        feat_list_split.extend([attr_class])
        tests.append(feat_list_split)

    testlabs.close()
    testfeat.close()
    time_taken = timeit.default_timer() - start_time
    print 'Threshold:',
    print threshold
    print 'Mismatches:',
    print t_mismatch
    print 'Accuracy:',
    print 100.0 - ((t_mismatch / 25000.0) * 100)
    print 'Tree Nodes Count:',
    print in_count
    print 'Running Time:',
    print time_taken,
    print 'seconds.'


def lookup(node, feat_list):
    """
    Recursive procedure to look for leaf node.
    Based on the splitting value of the attribute present in the nodes of the model, the class attribute of the leaf is searched for.
    """
    if node.attr_index is None and node.attr_split_val is None:
        return node
    if node.attr_split_val <= feat_list[node.attr_index]:
        return lookup(node.left_subtree, feat_list)
    else:
        return lookup(node.right_subtree, feat_list)


class Node(object):
    """
    Tree node to hold information of the decision tree node.
    """
    def __init__(self, attr_index, attr_split_val, attr_class):
        self.attr_index = attr_index
        self.attr_split_val = attr_split_val
        self.left_subtree = None
        self.right_subtree = None
        self.attr_class = attr_class

    def __str__(self):
        """
        Prints the node in desired format
        """
        return '[' + str(self.attr_class) + ', ' + str(self.attr_index) + ', ' + str(self.attr_split_val) + ', ' + str(
            self.left_subtree is not None) + ', ' + str(self.right_subtree is not None) + ']'


def plurality_value(examples):
    """
    Calculate the majority value of the class attribute. In case of ambiguious or pruning nodes, the plurality of the
    node is used to create the leaf node.
    """
    par_p_count, par_n_count = count_classes(examples)
    if par_p_count >= par_n_count:
        return 'P'
    else:
        return 'N'


g_count = 0


def iterative_dichotomiser(examples, attributes, parent_examples, threshold):
    """
    Recursive model builder.
    Calculates the entropy of the state.
    Fetches the attribute which provides maximum information gain.
    Splits the data into two halves.
    Initiates recursive model building in each.
    """
    global g_count
    p_count, n_count = count_classes(examples)
    if p_count + n_count == 0:
        return Node(None, None, plurality_value(parent_examples))
    elif p_count > 0 and n_count == 0:
        return Node(None, None, 'P')
    elif p_count == 0 and n_count > 0:
        return Node(None, None, 'N')
    else:
        entropy = calculate_entropy(examples)
        """
        print 'p_c:',
        print p_count,
        print 'n_c:',
        print n_count
        """
        attr_index, set1, set2, split_val = split_data(entropy, examples, attributes)

        if attr_index == -1:
            return Node(None, None, plurality_value(parent_examples))

        """
        Performing significance test to prune the tree
        """
        if significance_test(examples, set1, set2, threshold) is True:
            print 'Splitting Index:',
            print attr_index,
            g_count += 1
            print 'Count:',
            print g_count

            node = Node(attr_index, split_val, None)
            attributes[attr_index] = '0'
            node.left_subtree = iterative_dichotomiser(set1, attributes, examples, threshold)
            node.right_subtree = iterative_dichotomiser(set2, attributes, examples, threshold)
            return node
        else:
            print 'PRUNING at index:' + str(attr_index)
            return Node(None, None, plurality_value(parent_examples))


def count_classes(examples):
    """
    Counts the number of elements for each class attribute value
    """
    p_count = 0.0
    n_count = 0.0
    for ex in examples:
        if ex[-1] is '1':
            p_count += 1.0
        else:
            n_count += 1.0
    return p_count, n_count


def significance_test(examples, set1, set2, threshold):
    """
    Chi-Square criterion significance value calculator.
    After calculating the s_value, it is compared with the p_value to arrive at a decision.
    p_value depends on the threshold value.
    """
    set1_count = len(set1)
    set2_count = len(set2)

    base_p_count, base_n_count = count_classes(examples)
    base_count = base_n_count + base_p_count

    proj_set1_p_count = (base_p_count / base_count) * set1_count
    proj_set1_n_count = (base_n_count / base_count) * set1_count

    proj_set2_p_count = (base_p_count / base_count) * set2_count
    proj_set2_n_count = (base_n_count / base_count) * set2_count

    act_set1_p_count, act_set1_n_count = count_classes(set1)
    act_set2_p_count, act_set2_n_count = count_classes(set2)

    val_1 = 0.0
    if proj_set1_p_count > 0.0:
        val_1 = (math.pow((proj_set1_p_count - act_set1_p_count), 2) / proj_set1_p_count)

    val_2 = 0.0
    if proj_set1_n_count > 0.0:
        val_2 = (math.pow((proj_set1_n_count - act_set1_n_count), 2) / proj_set1_n_count)

    val_3 = 0.0
    if proj_set2_p_count > 0.0:
        val_3 = (math.pow((proj_set2_p_count - act_set2_p_count), 2) / proj_set2_p_count)

    val_4 = 0.0
    if proj_set2_n_count > 0.0:
        val_4 = (math.pow((proj_set2_n_count - act_set2_n_count), 2) / proj_set2_n_count)

    s_value = val_1 + val_2 + val_3 + val_4

    """
    Different p_value-s based on threshold.
    Use CHIINV in excel to find the value with degrees of freedom as 1, since this is a binary search tree.
    """
    if threshold == 0.05:
        p_value = 3.841459
    elif threshold == 0.01:
        p_value = 6.634897
    else:
        p_value = 0

    if s_value < p_value:
        return False
    else:
        return True


def split_data(entropy, examples, attributes):
    """
    Splits the data present in 'examples' into two sets.
    Fetches the information gains of each attribute.
    Returns the sets belonging to the attribute with maximum information gain
    """
    information_gains = {}
    set1_list = {}
    set2_list = {}
    split_val_list = {}
    found = 0
    for attr in range(len(attributes)):
        if attributes[attr] is '1':
            found = 1
            """
            Information of each attribute is stored in dictionary.
            Values stored are: Information gain, 2 split sets and the value with which the sets are split
            """
            information_gains[attr], set1_list[attr], set2_list[attr], split_val_list[
                attr] = calculate_information_gain(entropy, examples, attr)

    if found == 0:
        return -1, None, None, None

    max_ig_attr, max_ig_val = max(information_gains.iteritems(), key=itemgetter(1))
    return max_ig_attr, set1_list[max_ig_attr], set2_list[max_ig_attr], split_val_list[max_ig_attr]


def calculate_information_gain(entropy, examples, attr):
    """
    Calculates the information gain of the attribute supplied.
    """
    examples = sorted(examples, key=itemgetter(attr))
    """
    Finding the value with which the splitting is done
    """
    split_value = find_split_value(examples, attr)

    set1 = []
    set1_count = 0.0

    set2 = []
    set2_count = 0.0

    """
    Splitting here
    """
    for ex in examples:
        if ex[attr] <= split_value:
            set1.append(ex)
            set1_count += 1.0
        else:
            set2.append(ex)
            set2_count += 1.0

    total_count = set1_count + set2_count

    """
    Information gain is calculated here.
    """
    ig = entropy - (
        (set1_count / total_count) * calculate_entropy(set1) + (set2_count / total_count) * calculate_entropy(set2))

    return ig, set1, set2, split_value


def find_split_value(examples, attr):
    """
    Finds the split value. Actually split value for continuous attributes has to be calculated using gini indices.
    The attribute value with minimum gini index should be the split value.
    But, for the purposes of this project, the value is based on a different heuristic.
    Finding and counting the attribute values which contains class attribute as positive.
    The value which has the maximum positives of all is used for splitting. This is not proven to be correct, but the result is not very bad.
    """
    picked = {}
    for ex in examples:
        if ex[-1] is '1':
            if not ex[attr] in picked:
                picked[ex[attr]] = 1
            else:
                picked[ex[attr]] += 1

    return max(picked.iteritems(), key=itemgetter(1))[0]


def calculate_entropy(examples):
    """
    Calculates the entropy of the model node samples
    """
    if len(examples) == 0:
        return 0
    p_count = 0.0
    n_count = 0.0
    for ex in examples:
        if ex[-1] is '1':
            p_count += 1
        else:
            n_count += 1
    total = p_count + n_count

    """
    Avoiding divide by zero error
    """
    log_val_p = 0
    if p_count is not 0.0:
        log_val_p = math.log((p_count / total), 2)

    log_val_n = 0
    if n_count is not 0.0:
        log_val_n = math.log((n_count / total), 2)

    """
    Calculating entropy here
    """
    return -1 * ((p_count / total) * log_val_p + (n_count / total) * log_val_n)

"""
Number of nodes in the model built
"""
in_count = 0


def inorder(node):
    """
    Inorder traversal of the decision tree and counting of nummber of nodes in the tree.
    """
    global in_count
    if node is not None:
        inorder(node.left_subtree)
        in_count += 1
        # print str(in_count) + ':' + str(node.attr_class)
        inorder(node.right_subtree)


if __name__ == '__main__':
    main()