#encoding: utf8

# YOUR NAME: Vânia Morais
# YOUR NUMBER: 102383

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT:
# - ...
# - ...

from semantic_network import *
from bayes_net import *
from constraintsearch import *


class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def is_object(self,user,obj):
        # IMPLEMENT HERE
        
        for d in self.query_local(user=user):
            if d.relation.name != 'member' and d.relation.name!='subtype' and d.relation.card == None:
                if obj == d.relation.entity1 or obj == d.relation.entity2:
                    return True
            if d.user== user and d.relation.name == 'member':
                if obj == d.relation.entity1:
                    return True

        return False

    def is_type(self,user,type):
        types = set(
            [
                d.relation.entity2
                for d in self.declarations
                if isinstance(d.relation, (Subtype, Member))
            ]
            +
            [
                d.relation.entity2
                for d in self.declarations
                if isinstance(d.relation, Association) and d.relation.card != None
            ]
        )
        for d in self.declarations:
            if d.user == user and type in types:
                return True
        return False



    def infer_type(self,user,obj,xpto='xptoval'):
        # IMPLEMENT HERE
        if self.is_object(user,obj):
            for d in self.query_local(user=user):
                if self.is_type(user,obj):
                    return obj
                elif isinstance(d.relation, (Subtype, Member)):
                    if obj == d.relation.entity1:
                        return d.relation.entity2
                else:
                    return '__unknown__'
        else:
            return None
            

 
    def infer_signature(self,user,assoc,xpto='xptoval'):
        # IMPLEMENT HERE
        for d in self.query_local(user=user, rel=assoc):
            if d.relation.card == 'None':
                return (self.infer_type(user, d.relation.entity1 ), self.infer_type(user, d.relation.entity2 ))
            else:
                return None



class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def markov_blanket(self,var):
        # IMPLEMENT HERE
        #retorna a lista de variáveis que compoe o markov blanket dessa variável
        markov_blanket = set()
        # add parents of var
        if var in self.dependencies:
            for (mt, mf, p) in self.dependencies[var]:
                markov_blanket.update(mt)
            # add children of var
            for dependencies in self.dependencies.values():
                for (mt, mf, p) in dependencies:
                    if var in mt:
                        markov_blanket.add(p)
            # add other parents of children of var
            for dependencies in self.dependencies.values():
                for (mt, mf, p) in dependencies:
                    if p in markov_blanket:
                        markov_blanket.update(mt)
            # return list of variables in the markov blanket
        return [v for v in markov_blanket if isinstance(v, str)]







class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        self.counter = 0
        pass

    def propagate(self,domains,var):
        # IMPLEMENT HERE
        for v1, v2 in self.constraints:
            if v1 == var:
                domains[v2] = [x for x in domains[v2] if self.constraints[(v1, v2)](v1, domains[var][0], v2, x)]
            elif v2 == var:
                domains[v1] = [x for x in domains[v1] if self.constraints[(v1, v2)](v1, x, v2, domains[var][0])]


    def higherorder2binary(self,ho_c_vars,unary_c):
        # create new auxiliary variable
        aux_var = "aux" + str(self.counter)
        self.counter += 1

        # add the auxiliary variable to the domains dictionary
        self.domains[aux_var] = self.domains[ho_c_vars[0]]

        def unary_c(aux, aux_val, var, var_val):
            # modify this function to accept four arguments
            return aux_val == var_val

        # add a new binary constraint involving the auxiliary variable and each variable in ho_c_vars
        for var in ho_c_vars:
            self.constraints[(aux_var,var)] = lambda aux,aux_val,var,var_val: unary_c(aux,aux_val,var,var_val)

