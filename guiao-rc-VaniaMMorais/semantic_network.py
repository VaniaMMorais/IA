# Guiao de representacao do conhecimento
# -- Redes semanticas
#
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from time import sleep
from collections import Counter
from statistics import mean


class Relation:
    def __init__(self, e1, rel, e2):
        self.entity1 = e1
        #       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2

    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + str(self.entity2) + ")"

    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)


#   Exemplo:
#   a = Association('socrates','professor','filosofia')

class AssocOne(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self, e1, assoc, e2)



class AssocNum(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self, e1, assoc, float(e2))

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self, sub, super):
        Relation.__init__(self, sub, "subtype", super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self, obj, type):
        Relation.__init__(self, obj, "member", type)


#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self, user, rel):
        self.user = user
        self.relation = rel

    def __str__(self):
        return "decl(" + str(self.user) + "," + str(self.relation) + ")"

    def __repr__(self):
        return str(self)


#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self, ldecl=None):
        self.declarations = [] if ldecl == None else ldecl

    def __str__(self):
        return str(self.declarations)

    def insert(self, decl):
        self.declarations.append(decl)

    def query_local(self, user=None, e1=None, rel=None, e2=None, _type=None):
        self.query_result = [
            d
            for d in self.declarations
            if (user == None or d.user == user)
            and (e1 == None or d.relation.entity1 == e1)
            and (rel == None or d.relation.name == rel)
            and (e2 == None or d.relation.entity2 == e2)
            and (_type == None or isinstance(d.relation, _type))
        ]
        return self.query_result

    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def list_associations(self):
        delc = self.query_local(_type=Association)
        return set([d.relation.name for d in delc])

    def list_objects(self):
        delc = self.query_local(_type=Member)
        return set([d.relation.entity1 for d in delc])

    def list_users(self):
        return set([d.user for d in self.declarations])

    def list_types(self):
        # self.query_local(_type = (Member, Subtype))
        # return set([d.relation.entity1 for d in delc if isinstance(d.relation, Subtype)]+[d.relation.entity2 for d in decl])
        return set(
            [
                d.relation.entity2
                for d in self.declarations
                if isinstance(d.relation, (Subtype, Member))
            ]
            + [
                d.relation.entity1
                for d in self.declarations
                if isinstance(d.relation, Subtype)
            ]
        )

    def list_local_associations(self, entity):
        delc = self.query_local(e1=entity, _type=Association)
        delc += self.query_local(e2=entity, _type=Association)
        return set([d.relation.name for d in delc])

    def list_relations_by_user(self, user):
        delc = self.query_local(user=user)
        return set([d.relation.name for d in delc])

    def associations_by_user(self, user):
        delc = self.query_local(user=user, _type=Association)
        return len(set([d.relation.name for d in delc]))

    def list_local_associations_by_entity(self, entity):
        delc = self.query_local(e1=entity, _type=Association)
        delc += self.query_local(e2=entity, _type=Association)
        return set([(d.relation.name, d.user) for d in delc])

    def predecessor(self, A, B):
        pds = [
            d.relation.entity2 for d in self.query_local(e1=B, _type=(Member, Subtype))
        ]

        if pds == []:
            return False

        for A in pds:
            return True

        return any(self.predecessor(A, p) for p in pds)

    def predecessor_path(self, A, B):
        pds = [
            d.relation.entity2 for d in self.query_local(e1=B, _type=(Member, Subtype))
        ]

        if A in pds:
            return [A, B]

        for p in pds:
            if self.predecessor(A, p):
                return self.predecessor_path(A, p) + [B]

    def query(self, entity, assoc=None):
        pds = [
            d.relation.entity2
            for d in self.query_local(e1=entity, _type=(Member, Subtype))
        ]
        all_assoc = self.query_local(e1=entity, rel=assoc, _type=Association)
        for p in pds:
            all_assoc += self.query(p, assoc)

        return all_assoc

    def query2(self, entity, assoc=None):
        pds = [
            d.relation.entity2
            for d in self.query_local(e1=entity, _type=(Member, Subtype))
        ]
        all_assoc = self.query_local(e1=entity, rel=assoc)
        for p in pds:
            all_assoc += self.query(p, assoc)

        return all_assoc

    def query_cancel(self, entity, assoc):
        pds = [
            d.relation.entity2
            for d in self.query_local(e1=entity, _type=(Member, Subtype))
        ]
        local_assoc = self.query_local(e1=entity, rel=assoc)

        all_assoc = []
        for p in pds:
            all_assoc += [
                d
                for d in self.query_cancel(p, assoc)
                if not d.relation.name in [dd.relation.name for dd in local_assoc]
            ]

        return all_assoc + local_assoc


    def query_down(self, tipo, assoc, first_call = True):
        desc = [d.relation.entity1 for d in self.query_local(e2=tipo, _type=(Member, Subtype))]

        if first_call:
            local_assoc=[]
        else:
            local_assoc = self. query_local(e1=tipo, rel = assoc) + self.query_local(e2= tipo, rel = assoc)

        for d in desc:
            local_assoc += self.query_down(d, assoc, first_call=False)

        return local_assoc

    def query_induce(self, tipo, assoc):
        desc = self.query_down(tipo, assoc)

        c = Counter(d.relation.entity2 for d in desc)

        valor, _ = c.most_common(1)[0]
        return valor
        #desc = [d.relation.entity2 for d in self.query_down(tipo, assoc)]
        #for c, _ in Counter(desc).most_common(1):
        #    return c

    def query_local_assoc(self, tipo, assoc):
        local = self.query_local(e1=tipo, rel= assoc, _type = Association)

        for l in local:
        #if local: (não funciona da mesma maneira)
            count = Counter(d.relation.entity2 for d in local)
            if isinstance(l.relation, AssocOne):
                valor, c = count.most_common(1)[0]
                return valor, c/len(local)

            if isinstance(l.relation, AssocNum):
                return mean(d.relation.entity2 for d in local)

            t= 0
            res=[]
            for v, c in count.most_common():
                res.append((v,c/len(local)))
                t+=c/len(local)
                if t> 0.75:
                    break
            return res
    
    def query_assoc_value(self, E, A):
        local = self.query_local(e1 = E, rel= A)
        c_local= Counter(l.relation.entity2 for l in local)
        if len(c_local) == 1:
            return local[0].relation.entity2
        
        herdados=self.query(E,A)
        c_herdados = Counter(h.relation.entity2 for h in herdados)
        c = c_local + c_herdados
        return c.most_common(1)[0][0] 
        #local_values = [l.relation.entity2 for l in local]
        #if len(set(local_values))==1:
        #    return local_values[0]
        #else:
        #    pred


