from list_statistics import ListStatistics


def print_statistics(input_list):
    print("Input list: {}".format(input_list))

    stat = ListStatistics(input_list)

    print("Mean: {}".format(stat.mean()))
    print("Median: {}".format(stat.median()))
    print("Variance: {}".format(stat.variance()))
    print("Standard deviation: {}".format(stat.std()))
    print("---------------------------")


print_statistics([5, 8, 12, 32, 21, 18, 9, 0, 1])
print_statistics([5, 8, 12, 32, 21, 18, 0, 1])
print_statistics([5, 8])
