# implementare problema originala
projects = input().split()
projects = [int(x) for x in projects]
projects = [projects[i:i+2] for i in range(0, len(projects), 2)]

projects.sort(key=lambda x: (-x[0], -x[1]))

profit = 0
maxim = max([project[0] for project in projects])

plan = {i: 0 for i in range(1, maxim + 2)}

for project in projects:
    for i in range(project[0], 0, -1):
        if plan[i] == 0:
            plan[i] = project[1]
            profit += project[1]
            break

i = 1
while i < maxim:
    if plan[i] == 0:
        plan[i] = plan[i + 1]
        while plan[i + 1] != 0 and i + 1 <= maxim:
            plan[i + 1] = plan[i + 2]
            i += 1
    i += 1

print(plan)
print(profit)
