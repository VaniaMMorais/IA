from tree_search import *
from cidades import *
from blocksworld import *


def func_branching(connections,coordinates):
    #IMPLEMENT HERE
    num_cities= len(coordinates)
    count = 0
    for c in coordinates:
        for (c1, c2, d) in connections:
            if c == c1:
                count += 1
            if c == c2:
                count += 1

    avg=(count/num_cities)-1
    return avg
    

class MyCities(Cidades):
    def __init__(self,connections,coordinates):
        super().__init__(connections,coordinates)
        # ADD CODE HERE IF NEEDED

class MySTRIPS(STRIPS):
    def __init__(self,optimize=False):
        super().__init__(optimize)

    def simulate_plan(self,state,plan):
        #IMPLEMENT HERE
        pass

 
class MyNode(SearchNode):
    def __init__(self,state,parent,cost=0,heuristic=0,depth=0):
        super().__init__(state,parent)
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        #ADD HERE ANY CODE YOU NEED

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',optimize=0,keep=0.25): 
        super().__init__(problem,strategy)
        #ADD HERE ANY CODE YOU NEED
        self.optimize= optimize
        self.keep = keep
        if isinstance(problem,SearchProblem):
            if self.optimize==0:
                self.problem = problem
                root = MyNode(problem.initial, None)
                self.all_nodes = [root]
                self.open_nodes = [0]
            elif self.optimize == 1:
                self.problem = problem
                root = (problem.initial, None, 0, 0, 0)
                self.all_nodes = [root]
                self.open_nodes = [0]
        elif self.optimize == 2:
            self.problem = problem
            root = (problem[1], None, 0, 0, 0)
            self.all_nodes = [root]
            self.open_nodes = [0]
        elif self.optimize == 4:
            self.problem = problem
            root = (problem[1], None, 0, 0, 0)
            self.all_nodes = [root]
            self.open_nodes = [0]
        self.strategy = strategy
        self.solution = None
        self.non_terminals = 0
        self.terminals = 0
    
    def get_path(self,node):
        if self.optimize==0:
            if node.parent == None:
                return [node.state]
            path = self.get_path(self.all_nodes[node.parent])
            path += [node.state]
        elif self.optimize == 1:
            if node[1] == None:
                return [node[0]]
            path = self.get_path(self.all_nodes[node[1]])
            path += [node[0]]
        elif self.optimize == 2:
            if node[1] == None:
                return [node[0]]
            path = self.get_path(self.all_nodes[node[1]])
            path += [node[0]]
        elif self.optimize == 4:
            if node[1] == None:
                return [node[0]]
            path = self.get_path(self.all_nodes[node[1]])
            path += [node[0]]
        
        return(path)

    def astar_add_to_open(self,lnewnodes):
        #IMPLEMENT HERE
        if self.optimize == 0:
            self.open_nodes = sorted(
                    self.open_nodes + lnewnodes, key=lambda node: self.all_nodes[node].cost + self.all_nodes[node].heuristic
                )
        else:
            self.open_nodes = sorted(
                    self.open_nodes + lnewnodes, key=lambda node: self.all_nodes[node][2] + self.all_nodes[node][3]
                )



    # remove a fraction of open (terminal) nodes
    # with lowest evaluation function
    # (used in Incrementally Bounded A*)
    def forget_worst_terminals(self):
        #IMPLEMENT HERE
        pass

    # procurar a solucao
    def search2(self):
        if self.optimize == 0:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem.goal_test(node.state):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state,a)
                    cost_node = self.problem.domain.cost(node.state, a)
                    if newstate not in self.get_path(node):
                        newnode = MyNode(newstate,nodeID, node.cost + cost_node,self.problem.domain.heuristic(newstate, self.problem.goal), node.depth+1)
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            return None
        elif self.optimize == 1:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem.goal_test(node[0]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node[0]):
                    newstate = self.problem.domain.result(node[0],a)
                    cost_node = self.problem.domain.cost(node[0], a)
                    if newstate not in self.get_path(node):
                        newnode = (newstate,nodeID, node[2],self.problem.domain.heuristic(newstate, self.problem.goal), node[4])
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            return None
        elif self.optimize == 2:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem[0][4](node[0], self.problem[2]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem[0][0](node[0]):
                    newstate = self.problem[0][1](node[0],a)
                    cost_node = self.problem[0][2](node[0], a)
                    if newstate not in self.get_path(node):
                        newnode = (newstate,nodeID, node[2],self.problem[0][3](newstate, self.problem[2]), node[4])
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            return None
        elif self.optimize == 4:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem[0][4](node[0], self.problem[2]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem[0][0](node[0]):
                    newstate = self.problem[0][1](node[0],a)
                    cost_node = self.problem[0][2](node[0], a)
                    if newstate not in self.get_path(node):
                        newnode = (newstate,nodeID, node[2],self.problem[0][3](newstate, self.problem[2]), node[4])
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
            return None
        

# If needed, auxiliary functions can be added
#def graph_search(self):
#    
#    new_set = []
#    while self.open_nodes != []:
#        if :
#            return None 
#        




