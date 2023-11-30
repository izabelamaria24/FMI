my_list = []

def citire():
    global my_list
    my_list = [int(x) for x in input().split()]


def afisare(list):
    for x in list:
        print(x, end=" ")
    print(end="\n")


def valpoz():
    global my_list
    return [x for x in my_list if x > 0]


def semn():
    global my_list
    my_list =  [-x for x in my_list]


