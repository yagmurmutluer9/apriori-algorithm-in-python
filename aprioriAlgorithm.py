from itertools import chain, combinations
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from optparse import OptionParser
import sys


def read_data(file_name):
    with open(file_name) as file:
        for line in file:
            line = line.strip().rstrip(",")
            record = frozenset(line.split(","))
            yield record


def arrange_file(arr):
    file = read(arr)
    sorter = sorted(file, key=itemgetter(0))
    grouper = groupby(sorter, key=itemgetter(0))
    res = {i: list(map(itemgetter(1), j)) for i, j in grouper}
    return res.values()


def read(file):
    customList = []

    with open(file) as file:
        for line in file:
            line = line.strip().rstrip("\t")
            line = line.split()
            customList.append(line)

        return customList


def list_of_transactions(data):
    transaction_list = list()
    item_set = set()
    for record in data:
        transaction = frozenset(record)
        transaction_list.append(transaction)
        for item in transaction:
            item_set.add(frozenset([item]))
    return item_set, transaction_list


def items_greater_than_min_support(set_of_items, transaction_list, min_support, frequent_set):
    _item_set = set()
    local_set = defaultdict(int)

    for item in set_of_items:
        for transaction in transaction_list:
            if item.issubset(transaction):
                frequent_set[item] += 1
                local_set[item] += 1

    for item, count in local_set.items():
        support = float(count / len(transaction_list))
        print(support, item, count, min_support)

        if support >= min_support:
            _item_set.add(item)

    return _item_set


def merge_set(item_set, length):
    return set(
        [i.union(j) for i in item_set for j in item_set if len(i.union(j)) == length]
    )


def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def apriori_algorithm(data, min_support, min_confidence):
    item_set, transaction_list = list_of_transactions(data)

    frequency_set = defaultdict(int)
    original_set = dict()

    assocRules = dict()
    # Dictionary which stores Association Rules

    c1 = items_greater_than_min_support(item_set, transaction_list, min_support, frequency_set)

    current_l_set = c1
    k = 2

    while current_l_set != set([]):
        original_set[k - 1] = current_l_set
        current_l_set = merge_set(current_l_set, k)
        current_c_set = items_greater_than_min_support(
            current_l_set, transaction_list, min_support, frequency_set
        )
        current_l_set = current_c_set
        k = k + 1

    def get_support(item):
        return float(frequency_set[item]) / len(transaction_list)

    to_ret_items = []
    for key, value in original_set.items():
        to_ret_items.extend([(tuple(item), get_support(item)) for item in value])

    to_ret_rules = []
    for key, value in list(original_set.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = get_support(item) / get_support(element)
                    if confidence >= min_confidence:
                        to_ret_rules.append(((tuple(element), tuple(remain)), confidence))
    return to_ret_items, to_ret_rules


def print_result(items, rules):
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s , %.3f" % (str(item), support))

    with open('result2.txt', 'w') as f:
        for rule, confidence in sorted(rules, key=lambda x: x[1]):
            pre, post = rule
            f.write("Rule: %s ==> %s , %.3f \n" % (str(pre), str(post), confidence))


if __name__ == "__main__":

    option_parser = OptionParser()
    option_parser.add_option(
        "-f", "--inputFile", dest="input", help="filename containing csv", default=None
    )
    option_parser.add_option(
        "-s",
        "--minSupport",
        dest="minS",
        help="minimum support value",
        default=0.15,
        type="float",
    )
    option_parser.add_option(
        "-c",
        "--minConfidence",
        dest="minC",
        help="minimum confidence value",
        default=0.6,
        type="float",
    )

    (options, args) = option_parser.parse_args()

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = read_data(options.input)
    else:
        print("No data set filename specified, system with exit\n")
        sys.exit("System will exit")

    minSupport = options.minS
    minConfidence = options.minC

    items, rules = apriori_algorithm(inFile, minSupport, minConfidence)

    print_result(items, rules)
