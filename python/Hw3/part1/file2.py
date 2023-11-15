def contain_x(x, *lists):
    for current_list in lists:
        if x in current_list:
            print(current_list, end='\n')


def contain_x_gen(x, *lists):
    for current_list in lists:
        if x in current_list:
            yield current_list


value = 1
contain_x(value, [1, 2, 3], [1, 2], [1], [2, 3, 4])

res = contain_x_gen(1, [1, 2, 3], [1, 2], [1], [2, 3, 4])
list_it = next(res, None)

if (list_it is None):
    print(f"{value} is not there")
else:
    while list_it is not None:
        print(list_it)
        list_it = next(res, None)
