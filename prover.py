import sys

class MyLiteral:
    def __init__(self,Name=[],LogValue=[]):
        self.Name=Name
        self.LogValue=LogValue
    
    def __repr__(self):
        return '{}:{}'.format(self.Name, self.LogValue)
    def __eq__(self, other):
        return self.Name==other.Name and self.LogValue==other.LogValue

def read_sentence(line): #receives a clause in CNF, returns list of objects MyLiteral (clause)
    
    cl=[]

    not_test='not'
    line_len=len(line)
    
    if (line_len>1):  #1 literal negated or more than 1 literal
        if line[0]==not_test:  #1 literal negated
            newLit1=MyLiteral(Name=line[1],LogValue=False)
            cl.append(newLit1)
        else: #more than 1 literal
            for i in range(0, line_len):
                if not_test in line[i][0]:
                    newLit1=MyLiteral(Name=line[i][1],LogValue=False) #literal negated
                    cl.append(newLit1)
                else:
                    newLit1=MyLiteral(Name=line[i][0],LogValue=True)
                    cl.append(newLit1)

    else: #1 literal not negated
        newLit1=MyLiteral(Name=line[0],LogValue=True)   
        cl.append(newLit1)         
    
    cl = sorted(cl, key= lambda cl: cl.Name) #sorted by alphabetical order
    return cl


def remove_no_complementary(cl_list): #Applies Simplification 1: remove a clause C if it contains a literal that is not complementary with any other in the remaining clauses
    
    confirmed_lit=[]
    lit_remove=[]
    flag=-1
    num_cl=len(cl_list)

    for i in range(num_cl):
        for literal in cl_list[i]: #pick one literal from one clause
            flag=-1
            if literal.Name in confirmed_lit:  #confirmed_lit=list of literals which have their complementary in another clause
                continue
            for k in range(i+1, num_cl):
                for lit_aux in cl_list[k]: #pick one literal from another clause
                    if lit_aux.Name==literal.Name and literal.LogValue!= lit_aux.LogValue: #check if there is a complementary of the first literal
                        flag=1
                        break
                if flag==1:
                    break
            confirmed_lit.append(literal.Name)
            if flag==-1:
                lit_remove.append(literal) #list with literals to be removed
                
    if lit_remove==[]:
        return False
    for lit in lit_remove:
        for cl in cl_list: 
            if lit in cl:
                cl_list.remove(cl) #remove clauses which have one of the literals to be removed
    return cl_list

def remove_tautologies(cl_list): #Applies Simplification 2: remove tautologies

    num_cl=len(cl_list)
    cl_remove_list=[]

    for i in range(0,num_cl):
        flag=0
        for lit in cl_list[i]:
            for lit_aux in cl_list[i]:
                if lit_aux.Name==lit.Name and lit.LogValue!= lit_aux.LogValue: #check if there is a literal and its complementary in the same clause
                    cl_remove_list.append(cl_list[i])
                    flag=1
                    break
            if flag==1:
                break

    for cl in cl_remove_list:
        cl_list.remove(cl)

    return cl_list
            
def remove_equal(cl_list): #Applies Simplification 3: remove equal clauses
    
    num_cl=len(cl_list)
    cl_remove_list=[]

    for i in range(0,num_cl):
        for k in range(i+1,num_cl):
            if cl_list[i]==cl_list[k]:
                cl_remove_list.append(cl_list[k]) #check if there are two equal clauses

    for cl in cl_remove_list:
        cl_list.remove(cl)

    return cl_list
            
def resolution(first_cl,second_cl,literal,result_list): #receives a first clause, a second clause, a literal from the first clause and the list of clauses 
                                                        #tries to apply resolution; returns the list of clauses, appended with the new clause
    new_cl=[]

    for lit_aux in second_cl:
        if lit_aux.Name==literal.Name and literal.LogValue!= lit_aux.LogValue:
            for lit1 in first_cl:
                if lit1.Name!=literal.Name and lit1 not in new_cl:
                    new_cl.append(lit1)
            for lit2 in second_cl:
                if lit2.Name!=literal.Name and lit2 not in new_cl:
                    new_cl.append(lit2)
            new_cl = sorted(new_cl, key= lambda new_cl: new_cl.Name) #sorted by alphabetical order
            result_list.append(new_cl)
            return True
        else:
            continue
    return False    

def compare_lists(list_M, list_m): #checks if two lists are equal, list_M is the list resulting from resolution: might have one more extra clause than list_m
    not_in_common=[]
    for clause in list_M:
        if clause not in list_m:
            not_in_common.append(clause)
    if not_in_common!=[]:
        return False
    
    return True

def prover(cl_list):
    prov=None
    simplium=None
    cl_list = sorted(cl_list, key= lambda x: len(x))  #list of clauses is sorted by clauses' length

    if cl_list==[]: #if there are no clauses in the clause list
        return cl_list,False

    if cl_list[0]==[]: #if the empty clause is in the list
        return cl_list,True

    num_cl=len(cl_list)

    for i in range(num_cl):
        if i==(num_cl-1):
            return cl_list,False

        for k in range(i+1,num_cl):
            aux=None
            for lit in cl_list[i]:
                cl_list_new=[]
                for cl in cl_list: #create a copy of the original list of clauses
                    cl_list_new.append(cl)
                if resolution(cl_list[i],cl_list[k],lit,cl_list_new)==False:
                    continue
                else:
                    #---simplifications---#
                    remove_tautologies(cl_list_new)
                    remove_equal(cl_list_new)
                    simplium=remove_no_complementary(cl_list_new)
                    while aux!=False:
                        aux=remove_no_complementary(cl_list_new)
                    #---------------------#

                    cl_list_new = sorted(cl_list_new, key= lambda x: len(x))  #list of clauses is sorted by clauses' length
                    if(compare_lists(cl_list_new, cl_list)==False):
                        return cl_list_new,None
                                          
                    else:
                        continue
    return cl_list, False


if __name__=="__main__":
    
    cl_list=[]
    aux=None
    prov=None

    for line in sys.stdin:
       	cl_list.append(read_sentence(eval(line)))

    #---simplifications---#
    remove_tautologies(cl_list)
    remove_equal(cl_list)
    aux=remove_no_complementary(cl_list)
    while aux!=False: 
        aux=remove_no_complementary(cl_list)
    #---------------------#

    prov=None
    while True:
        cl_list, prov =prover(cl_list)
        if prov!=None:
            break
    print(prov)
