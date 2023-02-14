from ast import Return
import copy
import sys
import time
import common


class Solver:
    def __init__(self):
        self.search_tree = None
        self.path = None

    def recalcula(self, new_grid):
        new_Map = common.Map(new_grid)
        cars = set(i for i in new_grid.split(" ")[1] if i not in ["x", "o"])
        dict_cars = dict()
        for car in cars:
            coords = new_Map.piece_coordinates(car)
            if coords[0].y == coords[-1].y:
                orientacao= 'H'
            else:
                orientacao=  'V'
            #orientacao = Solver.vehicleType(self, coords)
            dict_cars[car] = orientacao

        self.search_tree = SearchTree(new_Map, dict_cars)
        self.path = self.search_tree.search()
        

    def run(self, new_grid, cursor, selected):
        if self.path is None:
            print("No solution")
            self.recalcula(new_grid)
            return
        
        new_Map = common.Map(new_grid)
        if len(self.path) == 0:
            self.recalcula(new_grid)
        
        
        if self.path is not None:
            piece = new_Map.piece_coordinates(self.path[0][0])[0]
            if selected == "":
                if cursor[0]>piece.x:
                    return "a"
                elif cursor[0]<piece.x:
                    return "d"
                elif cursor[1]>piece.y:
                    return "w"
                elif cursor[1]<piece.y:
                    return "s"
                else:
                    return " "
            if selected == self.path[0][0]:
                return self.path.pop(0)[1]
            else:
                return " "
        else:
            print("No solution")
        

    

class SearchNode:
    def __init__(self, Map, parent, depth, move, cost, heuristic):
        self.Map = Map  
        self.parent: SearchNode = parent 
        self.depth = depth 
        self.move = move  
        self.cost = cost
        self.heuristic = heuristic

    def in_parent(self, Map):
        if self.parent is None:
            return False
        if self.parent.Map.grid == Map.grid:
            return True
        return self.parent.in_parent(Map)

    def __str__(self):
        return "no(" + str(self.Map.grid) + "," + str(self.parent) + ")"

    def __hash__(self) -> int:
        return hash("".join("".join(i) for i in self.Map.grid))

    def __eq__(self, other):
        return hash(self) == hash(other)
        
    def __repr__(self):
        return str(self)


class SearchTree:
    # construtor
    def __init__(self, Map, cars: dict):
        self.Map = Map
        root = SearchNode(Map, None, 0, None, 0,self.heuristicas(Map)) #self.dst_a_parede(Map)+ self.n_carros_frente_ver(Map))
        self.open_nodes = [root]
        self.solution = None
        self.non_terminals = 0
        self.cars = cars
        self.scores = dict()
        self.scores[root] = 0
        
    def get_neighbours(self, node):
        for car, orient in self.cars.items():
            coords0x = node.Map.piece_coordinates(car)[0].x
            coords0y = node.Map.piece_coordinates(car)[0].y
            coords1x = node.Map.piece_coordinates(car)[-1].x
            coords1y = node.Map.piece_coordinates(car)[-1].y
            grid = node.Map.grid
            size = node.Map.grid_size
            Map = node.Map
            if orient == "H":
                if coords0x -1 >= 0 and grid[coords0y][coords0x -1] == "o":
                    # faz a jogada para a esquerda (a)
                    new_Map = copy.deepcopy(Map)
                    new_Map.move(car, common.Coordinates(-1, 0))
                    yield new_Map, (car, "a")
                if coords1x +1 < size and grid[coords1y][coords1x+1] == "o":
                    # faz a jogada para a direita (d)
                    new_Map = copy.deepcopy(Map)
                    new_Map.move(car, common.Coordinates(1, 0))
                    yield new_Map, (car, "d")
            else:
                if coords1y+1 < size and grid[coords1y+1][coords1x] == "o":
                    # faz a jogada para baixo (s)
                    new_Map = copy.deepcopy(Map)
                    new_Map.move(car, common.Coordinates(0, 1))
                    yield new_Map, (car, "s")
                if coords0y -1 >= 0 and grid[coords0y-1][coords0x] == "o":
                    # faz a jogada para cima (w)
                    new_Map = copy.deepcopy(Map)
                    new_Map.move(car, common.Coordinates(0, -1))
                    yield new_Map, (car, "w")

    def search(self):
        while len(self.open_nodes) != 0:
            self.open_nodes.sort(key=lambda x: x.cost + x.heuristic)
            node = self.open_nodes.pop(0)
            #print(len(self.open_nodes))
            
        
            #if node.Map.test_win():
            if node.Map.piece_coordinates('A')[-1].x == node.Map.grid_size-1:
                self.solution = node
                return self.get_path(node)
            self.non_terminals += 1
            lnewnodes = []
            for new_Map, move in self.get_neighbours(node):
                newnode = SearchNode(
                    new_Map,
                    node,
                    node.depth + 1,
                    move,
                    node.cost + 1,
                    self.heuristicas(new_Map)
                )

                if not newnode.in_parent(new_Map) and (newnode not in self.scores or self.scores[newnode] < newnode.cost):
                    lnewnodes.append(newnode)
                    self.scores[newnode] = newnode.cost
            self.open_nodes += lnewnodes
              
        return None
    
    def get_path(self, node):
        if node.parent == None:
            return None
        path= self.get_path(node.parent)
        if path is None:
            path = []
        path.append(node.move)
        return path


    #Heuristicas: distancia do carro A à parede + numero de carros que estao na frente do carro A
    def heuristicas(self, Map):
        n_carros=0
        coordsAx = Map.piece_coordinates('A')[-1].x 
        coordsAy = Map.piece_coordinates('A')[-1].y
        linha = Map.grid[coordsAy]
        for car in linha[coordsAx+1:]:
            if car != "o":
                n_carros+=1
        return n_carros + (Map.grid_size - coordsAx)




