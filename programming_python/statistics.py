from statistics_calculator import StatisticsCalculator


def print_statistics(input):
    print("Input list: {}".format(input))

    stat = StatisticsCalculator(input)

    print("Mean: {}".format(stat.mean()))
    print("Median: {}".format(stat.median()))
    print("---------------------------")


print_statistics([5, 8, 12, 32, 21, 18, 9, 0, 1])
print_statistics([5, 8, 12, 32, 21, 18, 0, 1])
print_statistics([5, 8])
print_statistics([5])
