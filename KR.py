class Nod:
    def __init__(self, informatie, succesori, parinte=None, viz=False):
        self.informatie = informatie
        self.parinte = parinte
        self.succesori = succesori
        self.viz = viz

    def __str__(self):
        drum = self.drumRadacina()
        return f"Din nodul de start {self.informatie} ({('->').join(drum)})"

    def __repr__(self):
        drum = self.drumRadacina()
        return f""

    def drumRadacina(self):
        drum = []
        nodCurent = self
        while nodCurent.parinte is not None:
            drum.append(nodCurent.informatie)
            nodCurent = nodCurent.parinte
        return list(reversed(drum))
    
    def vizitat(self, nod):
        return self.viz

class Graf:
    def __init__(self, nodStart, noduriScop, muchii):
        self.nodStart = nodStart
        self.noduriScop = noduriScop
        self.muchii = muchii

    def scop(self, nod):
        if nod in self.noduriScop:
            return True
        else:
            return False 

    def succesori(self, nod):
        listaSuccesori = []
        for muchie in self.muchii:
            if muchie[0] == nod and not muchie[1].viz: 
                listaSuccesori.append(muchie[1])
                muchie[1].viz = True

        return listaSuccesori


def dfs(n, graf, nodCurent):
    stack = [nodCurent]
    nodCurent.viz = True 
    
    while stack:
        nod = stack.pop() 
        print(nod.informatie)  

        if graf.scop(nod):
            return True  

        succesori = graf.succesori(nod)
        for succes in succesori:
            if not succes.viz:
                succes.viz = True
                stack.append(succes)
    
    return False  


from collections import deque

def bfs(n, graf, nodCurent):
    queue = deque([nodCurent])
    nodCurent.viz = True 
    
    while queue:
        nod = queue.popleft() 
        print(nod.informatie) 

        if graf.scop(nod):
            return True  

        succesori = graf.succesori(nod)
        for succes in succesori:
            if not succes.viz:
                succes.viz = True
                queue.append(succes)
    
    return False 

graf = Graf(0,
            [4, 6],
            [(0, 1, 3), (0, 2, 5), (0, 3, 10), (0, 6, 100),
             (1, 3, 4), (2, 3, 4), (2, 4, 9), (2, 5, 3),
             (3, 1, 3), (3, 4, 2), (5, 4, 4), (6, 2, 3)],
            {1: 1, 2: 6, 3: 2, 4: 0, 5: 3, 6: 0})

