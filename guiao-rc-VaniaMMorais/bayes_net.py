# CP = Cara Preocupada
# PA = Precisa de Ajuda
# FR = Frequencia do rato
# SC = Sobrecarga de Trabalho (origina a cara preocupada) 
# CNL = Correio não lido
# PT = Processador de texto (tenderá a PA(presisar de ajuda))
# P(SC)=0.6 P(CP|SC^PA)= 0.02  P(CP|SC^~PA)= 0.01 P(CP|~SC^PA)= 0.011 P(CP|~SC^~PA)= 0.001
# P(CNL|SC)=0.9  P(CNL|~SC)= 0.001
# P(PA|PT) = 0.3  P(PA|~PT) = 0.004  P(PT) = 0.05
# P(FR|PA^PT) = 0.9  P(FR|PA^~PT) = 0.10  P(FR|~PA^PT) = 0.9  P(FR|~PA^~PT) = 0.01 


class BayesNet:

    def __init__(self, ldep=None):  # Why not ldep={}? See footnote 1.
        if not ldep:
            ldep = {}
        self.dependencies = ldep

    # The network data is stored in a dictionary that
    # associates the dependencies to each variable:
    # { v1:deps1, v2:deps2, ... }
    # These dependencies are themselves given
    # by another dictionary that associates conditional
    # probabilities to conjunctions of mother variables:
    # { mothers1:cp1, mothers2:cp2, ... }
    # The conjunctions are frozensets of pairs (mothervar,boolvalue)
    def add(self,var,mothers,prob):
        self.dependencies.setdefault(var,{})[frozenset(mothers)] = prob

    # Joint probability for a given conjunction of
    # all variables of the network
    def jointProb(self,conjunction):
        prob = 1.0
        for (var,val) in conjunction:
            for (mothers,p) in self.dependencies[var].items():
                if mothers.issubset(conjunction):
                    prob*=(p if val else 1-p)
        return prob

    def _list_all_conjunctions(self, variables):
        if len(variables) == 1:
            return [
                [(variables[0], True)],
                [(variables[0], False)]
                ]

        temp=[]
        for conj in self._list_all_conjunctions(variables[1:]):
            temp.append([(variables[0], True)] + conj)
            temp.append([(variables[0], False)] + conj)
        return temp



    def individualProb(self,var,val):
        all_conj = self._list_all_conjunctions(list(self.dependencies.keys()))
        
        #t=0
        #for conj in all_conj:
        #    if (var, val) in conj:
        #        t+=self.jointProb(conj)
        #return t

        return sum([self.jointProb(conj) for conj in all_conj if (var, val) in conj])

import pprint
pprint.pprint(BayesNet()._list_all_conjunctions(['a', 'b']))

# Footnote 1:
# Default arguments are evaluated on function definition,
# not on function evaluation.
# This creates surprising behaviour when the default argument is mutable.
# See:
# http://docs.python-guide.org/en/latest/writing/gotchas/#mutable-default-arguments

