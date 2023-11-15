
students_list = [{"name": "Marcel", "group": 151, "credits_list": {"maths": 5, "computer_science": 1, "english": 2}},
                 {"name": "Andrei", "group": 152, "credits_list": {"maths": 5, "computer_science": 0, "english": 2}},
                 {"name": "Ana", "group": 155, "credits_list": {"maths": 5, "computer_science": 1, "english": 0}},
                 {"name": "Bala", "group": 151, "credits_list": {"maths": 5, "computer_science": 1, "english": 2}}]
min_credits = 7


def promoted(stu):
    s = 0
    for cr in stu["credits_list"].items():
        if cr[1] == 0:
            return False
        s += cr[1]
    if s < min_credits:
        return False
    return True


for student in students_list:
    student["promoted"] = promoted(student)


def gen_key_1(stu):  # by group, followed by name
    return stu["group"], stu["name"]


def gen_key_2(stu):   # by promoted, followed by name
    return -stu["promoted"], stu["name"]


def gen_key_3(stu):
    values = [value for key, value in stu["credits_list"].items()]
    return -sum(values), stu["group"], stu["name"]


def gen_key_4(stu):
    values = [value for key, value in stu["credits_list"].items()]
    return stu["group"], -stu["promoted"], -sum(values), stu["name"]


students_list.sort(key=gen_key_4)
print(students_list)
