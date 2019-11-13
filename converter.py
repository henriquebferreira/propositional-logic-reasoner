import sys #defines stdin and stdout

''' Functions to test clause type '''
def atom(obj):
    return isinstance(obj, str)
def negation(obj):
    if isinstance(obj, tuple):
        return obj[0]=='not'
    else:
        return False
def conjunction(obj):
    if isinstance(obj, tuple):
        return obj[0]=='and'
    else:
        return False
def disjunction(obj):
    if isinstance(obj, tuple):
        return obj[0]=='or'
    else:
        return False
def implication(obj):
    if isinstance(obj, tuple):
        return obj[0]=='=>'
    else:
        return False
def equivalence(obj):
    if isinstance(obj, tuple):
        return obj[0]=='<=>'
    else:
        return False
def literal(obj):
    if atom(obj):
        return True
    elif negation(obj):
        return atom(obj[1])
    else:
        return False
def pure_disj(obj):
    if not disjunction(obj):
        return False
    elif literal(obj[1]) and literal(obj[2]):
        return True
    elif literal(obj[1]):
        return pure_disj(obj[2])
    elif literal(obj[2]):
        return pure_disj(obj[1])
    else:
        return pure_disj(obj[1]) and pure_disj(obj[1])

''' Function to order a list of literals '''
def order(ll):
    if literal(ll):
        return ll
    l1, l2, l3 = [], [], []
    for lit in ll:
        if len(lit)==1:
            l1.append(lit)
        elif len(lit)==2:
            l2.append(lit)
        else: # Non-literal (should never occur)
            l3.append(lit)
    l1.sort()
    l2.sort()
    l3.sort()
    return l1 + l2 + l3 #first positive literals, then negated

''' Fuction to negate a sentence '''
def negate(sent): # receives and returns only one sentence
    if equivalence(sent):
        sent1 = ('and', negate(sent[1]), sent[2])
        sent2 = ('and', sent[1], negate(sent[2]))
        out = ('or', sent1, sent2 )
    elif implication(sent):
        out = ('and', sent[1], ('not', sent[2]))
    elif conjunction(sent):
        out = ('or', ('not', sent[1]), ('not', sent[2]))
    elif disjunction(sent):
        out = ('and', ('not', sent[1]), ('not', sent[2]))
    elif negation(sent):
        out = sent[1]
    elif atom(sent):
        out = ('not', sent)
    else: # Unknown type (should never occur)
        print("??? I don't know how to negate this...")
        out = ['?']
    return out

''' Convert sentence to list clauses '''
def convert(sent): # receives one sentence and returns a list of clauses
    #print("Input:\t\t",sent)
    if equivalence(sent):
        sent1 = ('=>', sent[1], sent[2]) #simplify equivalence 1
        sent2 = ('=>', sent[2], sent[1]) #simplify equivalence 2
        out = convert(sent1) + convert(sent2) #convert simplification and return concatenation

    elif implication(sent):
        sent1 = ('or', ('not', sent[1]), sent[2]) #simplify implication
        out = convert(sent1) #convert simplification

    elif conjunction(sent):
        out =  convert(sent[1]) + convert(sent[2]) #simplify conjunction and convert simplification

    elif disjunction(sent):
        if pure_disj(sent): # if it is a pure disjunction
            out = [sent] # already a clause
        else:
            aux1 = convert(sent[1])
            aux2 = convert(sent[2])
            out = []
            for sent1 in aux1: # Distributive Property
                for sent2 in aux2:
                    out += [('or', sent1, sent2)]

    elif negation(sent):
        if atom(sent[1]): # if it is a literal
            out = [sent] # already a clause
        else:
            out = convert(negate(sent[1])) # convert negated sentence

    elif atom(sent): # if it is an atomic sentence
        out = [sent] # already a clause

    else: # Unknown type (should never occur)
        print("!!!!!!! Something went wrong...")
        out = ['!']

    #print("Output:\t",out)
    return out

''' Get literals present in a sentence '''
def get_lit (sent): #receives a sentence adn returns list of literals
    if literal(sent):
        out = [sent]
    else:
        lit1 = get_lit(sent[1])
        lit2 = get_lit(sent[2])
        out = lit1 + lit2
    return list(set(out)) # eleminate repeated ones

''' Unify list of clauses '''
def unify(list_sent): #receives list of sentences, returns list of literals
    out=[]
    for s in list_sent:
        if s in out:
            continue
        new = True
        if literal(s):
            lit_s = s
        else:
            lit_s = get_lit(s) # get literals
            for o in out:
                if literal(o):
                    continue
                if set(lit_s) == set(o):
                    new = False
                    break
        if new:
            if len(lit_s)==1: # if only one literal
                lit_s=lit_s[0] # save the literal and not a list of 1 literal
            out.append(lit_s)
    return out

if __name__ == '__main__':

    sent = []
    for line in sys.stdin: # read sentences from stdin
        sent.append(eval(line))

    CNF = []
    for s in sent: # convert each sentence to CNF
        CNF += convert(s)

    CNFu = unify(CNF) # eliminate repeated clauses and get only literals
    for s in CNFu: # print to stdout representation of literals in each clause
        print(repr(s)) # same as sys.stdout.write(str(s)+"\n")
