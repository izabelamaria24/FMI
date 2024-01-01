class PriorityQueue:
    def __init__(self):
        self.queue = []

    def insert(self, item, priority):
        self.queue.append((item, priority))
        self.queue.sort(key=lambda x: x[1])

    def get_highest_priority(self):
        if not self.queue:
            return None
        return self.queue.pop(0)[0]

    def is_empty(self):
        return len(self.queue) == 0


pq_spectacole = PriorityQueue()
n = int(input())
spectacole = []
for i in range(0, n):
    line = input()
    spectacole.append(line.split('-'))

for i in range(0, n):
    pq_spectacole.insert(spectacole[i], spectacole[i][1])

result = [pq_spectacole.get_highest_priority()]
while not pq_spectacole.is_empty():
    next_spec = pq_spectacole.get_highest_priority()
    curr_spec = result[-1]
    if next_spec[0] >= curr_spec[1]:
        result.append(next_spec)

print(result)
