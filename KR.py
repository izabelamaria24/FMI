# class Nod:
#     def __init__(self, informatie, succesori, parinte=None, viz=False):
#         self.informatie = informatie
#         self.parinte = parinte
#         self.succesori = succesori
#         self.viz = viz

#     def __str__(self):
#         drum = self.drumRadacina()
#         return f"Din nodul de start {self.informatie} ({('->').join(drum)})"

#     def __repr__(self):
#         drum = self.drumRadacina()
#         return f""

#     def drumRadacina(self):
#         drum = []
#         nodCurent = self
#         while nodCurent.parinte is not None:
#             drum.append(nodCurent.informatie)
#             nodCurent = nodCurent.parinte
#         return list(reversed(drum))
    
#     def vizitat(self, nod):
#         return self.viz

# class Graf:
#     def __init__(self, nodStart, noduriScop, muchii):
#         self.nodStart = nodStart
#         self.noduriScop = noduriScop
#         self.muchii = muchii

#     def scop(self, nod):
#         if nod in self.noduriScop:
#             return True
#         else:
#             return False 

#     def succesori(self, nod):
#         listaSuccesori = []
#         for muchie in self.muchii:
#             if muchie[0] == nod and not muchie[1].viz: 
#                 listaSuccesori.append(muchie[1])
#                 muchie[1].viz = True

#         return listaSuccesori


# def dfs(n, graf, nodCurent):
#     stack = [nodCurent]
#     nodCurent.viz = True 
    
#     while stack:
#         nod = stack.pop() 
#         print(nod.informatie)  

#         if graf.scop(nod):
#             return True  

#         succesori = graf.succesori(nod)
#         for succes in succesori:
#             if not succes.viz:
#                 succes.viz = True
#                 stack.append(succes)
    
#     return False  


# from collections import deque

# def bfs(n, graf, nodCurent):
#     queue = deque([nodCurent])
#     nodCurent.viz = True 
    
#     while queue:
#         nod = queue.popleft() 
#         print(nod.informatie) 

#         if graf.scop(nod):
#             return True  

#         succesori = graf.succesori(nod)
#         for succes in succesori:
#             if not succes.viz:
#                 succes.viz = True
#                 queue.append(succes)
    
#     return False 

# graf = Graf(0,
#             [4, 6],
#             [(0, 1, 3), (0, 2, 5), (0, 3, 10), (0, 6, 100),
#              (1, 3, 4), (2, 3, 4), (2, 4, 9), (2, 5, 3),
#              (3, 1, 3), (3, 4, 2), (5, 4, 4), (6, 2, 3)],
#             {1: 1, 2: 6, 3: 2, 4: 0, 5: 3, 6: 0})



# class Node:
#     def __init__(self, info, parent=None, g=0, h=0):
#         self.info = info
#         self.parent = parent
#         self.g = g
#         self.h = h
#         self.f = g + h
#         self.successors = []

#     def visited(self):
#         node = self.parent
#         while node:
#             if node.info == self.info:
#                 return True
#             node = node.parent
#         return False

#     def __lt__(self, other):
#         return self.f < other.f

#     def __repr__(self):
#         return f"Node({self.info}, g={self.g}, h={self.h}, f={self.f})"

import heapq

class Graph:
    def __init__(self, startNode, scopeNodes, edges, estimates):
        self.startNodeInfo = startNode
        self.scopeNodes = set(scopeNodes)
        self.edges = edges
        self.estimates = estimates
        self.startNode = Node(startNode, g=0, h=self.estimate_h(startNode))

    def scope(self, nodeInfo):
        return nodeInfo in self.scopeNodes

    def estimate_h(self, nodeInfo):
        return self.estimates.get(nodeInfo, 0)

    def successors(self, node):
        successors = []
        for node1, node2, cost in self.edges:
            if node1 == node.info:
                new_g = node.g + cost 
                new_h = self.estimate_h(node2) 
                newNode = Node(node2, parent=node, g=new_g, h=new_h)

                if not newNode.visited():
                    successors.append(newNode)

        return successors

    def a_star(self):
      open_set = []  # min-heap
      heapq.heappush(open_set, self.startNode)
      closed_set = set()  # visited nodes

      while open_set:
          current_node = heapq.heappop(open_set) 

          if self.scope(current_node.info):
              return self.reconstruct_path(current_node)

          closed_set.add(current_node.info)

          for successor in self.successors(current_node):
              if successor.info in closed_set:
                  continue
              heapq.heappush(open_set, successor)

      return None

    def ida_star(self):
        def search(node, threshold):
            f_cost = node.g + node.h
            if f_cost > threshold:
                return f_cost, None  

            if node.info in self.scopeNodes:
                return None, node.get_path()  

            min_cost = float('inf')
            for successor in self.successors(node):
                result, path = search(successor, threshold)
                if path:
                    return None, path  
                if result is not None:
                    min_cost = min(min_cost, result)

            return min_cost, None

    def reconstruct_path(self, node):
        path = []
        while node:
            path.append(node.info)
            node = node.parent
        return path[::-1] 

    def __repr__(self):
        return (f"Graph(startNode={self.startNodeInfo}, "
                f"scopeNodes={list(self.scopeNodes)}, "
                f"edges={self.edges}, "
                f"estimates={self.estimates})")



graf = Graph(0,
             [4, 6],
             [(0, 1, 3), (0, 2, 5), (0, 3, 10), (0, 6, 100),
              (1, 3, 4), (2, 3, 4), (2, 4, 9), (2, 5, 3),
              (3, 1, 3), (3, 4, 2), (5, 4, 4), (6, 2, 3)],
             {1: 1, 2: 6, 3: 2, 4: 0, 5: 3, 6: 0})

path = graf.a_star()
path2 = graf.ida_star()
print("Optimal Path:", path)
print("Optimal IDA Path:", path2)
