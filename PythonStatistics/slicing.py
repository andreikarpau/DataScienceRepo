base_list = list(range(1, 101))
length = len(base_list)
half_length = int(length/2)

first_10 = base_list[:10]
print("First ten: {}".format(first_10))

last_10 = base_list[-10:]
print("Last ten: {}".format(last_10))

middle_50 = base_list[:half_length][-25:] + base_list[half_length:][:25]
print("Middle 50: {}".format(middle_50))

reversed_middle_50 = middle_50[::-1]
print("Reversed middle 50: {}".format(reversed_middle_50))

every_fifth = base_list[4::5]
print("Every fifth: {}".format(every_fifth))

every_odd_non_border = base_list[2:98:2]
print("Every odd excluding first and last: {}".format(every_odd_non_border))
