from os import kill, terminal_size
from pickle import NEWOBJ
import sys
from itertools import islice
from typing import NewType
import graphviz
sys.path.insert(0, '../KachuaCore/ast')
import kachuaAST

class Node:
    def __init__(self, value):
        self.value = value
        self.predecessors = set()
        self.successors = set()

class Graph:
    def __init__(self, graph_dict = None):
        if graph_dict==None:
            graph_dict={}
        self.graph_dict = graph_dict

    def add_vertex(self,vertex):
        if vertex not in self.graph_dict:
            self.graph_dict[vertex]=[]
    
    def add_edges(self,source, dest, source_index, dest_index):
        source.successors.add((dest, dest_index))
        dest.predecessors.add((source, source_index))
        self.graph_dict[source].append(dest)

    def printGraph(self):
        print("\n")
        print('========== CFG ==========')
        print("\n")
        for vertex in self.graph_dict:
            print(vertex.value.__str__(),end="")
            print(" --> ",end="")
            children=[]
            for i in self.graph_dict[vertex]:
                children.append(i.value.__str__())
            print(children)
        print("\n")

def builtGraph(ir):
    graph = Graph()
    nodes = []
    for i in ir:
        node = Node(i[0])
        nodes.append(node)
        graph.add_vertex(node)
    exit_node = Node('exit')
    nodes.append(exit_node)
    graph.add_vertex(exit_node)
    for i in range(len(ir)):
        if(ir[i][0].__str__()!='False'):
            graph.add_edges(nodes[i], nodes[i+1] , i , i+1)

        if ir[i][1]!=1:
            graph.add_edges(nodes[i], nodes[i+ir[i][1]], i , i+ir[i][1])
    
    return graph
    
def genCFG(ir):
    global cfg
    cfg = builtGraph(ir)
    return cfg.graph_dict

def dumpCFG(cfg):
    dot = graphviz.Digraph(comment='CFG')
    index=0 
    for vertex in cfg:
        dot.node(str(vertex), vertex.value.__str__().replace(":",""))
        index+=1
    for vertex in cfg:
        for i in cfg[vertex]:
            dot.edge(str(vertex),str(i))
    dot.render('dot files/testsdf.gv', view=True)


cfg = {}

def optimize(ir):
    global cfg
    ir2 = letsdoit(ir, cfg.graph_dict)
    return ir2

def letsdoit(ir, cfg):
    move_stmts = set()
    forward_stmts = set()
    backward_stmts = set()
    left_stmts = set()
    right_stmts = set()

    # finding all move statements
    index = 0
    for block in cfg:
        if type(block.value) == kachuaAST.MoveCommand:
            move_stmts.add((block.value, index))
        index+=1
    # print(move_stmts)

    # finding all forward, backward, left and right move statements
    for i, j in move_stmts:
        stmt = i.__str__()
        if 'forward' in stmt:
            forward_stmts.add((i, j))
        elif 'backward' in stmt:
            backward_stmts.add((i, j))
        elif 'left' in stmt:
            left_stmts.add((i, j))
        elif 'right' in stmt:
            right_stmts.add((i, j))

    # print(forward_stmts)
    # print(backward_stmts)
    # print(left_stmts)
    # print(right_stmts)

    # initialization part
    IN = [set() for i in cfg]
    OUT = [set() for i in cfg]
    KILL = [set() for i in cfg]
    GEN = [set() for i in cfg]
    IN[0] = set()
    IN[len(cfg)-1] = set()
    OUT[len(cfg)-1] = set()

    # print(IN)
    # print(OUT)
    # print(GEN)
    # print(KILL)

    # finding GEN set
    index = 0
    for block in cfg:
        if type(block.value) == kachuaAST.MoveCommand:
            GEN[index] = {(block.value, index)}
        index+=1
    
    # print(GEN)

    # finding KILL set
    index = 0
    for block in cfg:
        stmt = block.value.__str__()
        stmt_type = type(block.value)
        if stmt_type == kachuaAST.PenCommand:
            KILL[index] = move_stmts.copy()
        elif stmt_type == kachuaAST.MoveCommand:
            if 'forward' in stmt:
                KILL[index] = (left_stmts.union(right_stmts)).union(backward_stmts)
            if 'backward' in stmt:
                KILL[index] = (left_stmts.union(right_stmts)).union(forward_stmts)
            elif 'left' in stmt:
                KILL[index] = (forward_stmts.union(backward_stmts)).union(right_stmts)
            elif 'right' in stmt:
                KILL[index] = (forward_stmts.union(backward_stmts)).union(left_stmts)
        index+=1
    
    # print(KILL)

    # main algo
    iteration_no = 1
    flag = True
    while(flag):
        flag = False
        index = len(cfg)-1

        for block in reversed(cfg):

            # print("----- currently working on ", block.value.__str__())

            NEW_OUT = set()
            successors_indices = [successor[1] for successor in block.successors]
            successors_IN = [IN[i] for i in successors_indices]

            # print("successsors are ",successors_indices)
            # print("IN from successors are")
            # print(successors_IN)


            if len(successors_IN) == 0:
                pass
            elif len(successors_IN) == 1:
                NEW_OUT = successors_IN[0]
            elif len(successors_IN) == 2:
                left_IN = successors_IN[0]
                right_IN = successors_IN[1]

                # print("IN from left is --> ",left_IN)
                # print("IN from right is ---> ",right_IN)

                if len(left_IN) == 0 or len(right_IN) == 0:
                    pass
                else:
                    # (forward and left), (forward and right), (backward, left), etc will never come from same side therefore just check 
                    # one of the element of both side's IN
                    a = list(left_IN)[0][0].__str__()
                    b = list(right_IN)[0][0].__str__()
                    
                    # print("one of the statement from left IN is ---> ", a)
                    # print("one of statement from right IN is --->", b)

                    if 'forward' in a and 'forward' in b:
                        NEW_OUT = left_IN.union(right_IN)
                    
                    elif 'backward' in a and 'backward' in b:
                        NEW_OUT = left_IN.union(right_IN)
                    
                    elif 'left' in a and 'left' in b:
                        NEW_OUT = left_IN.union(right_IN)
                    
                    elif 'right' in a and 'right' in b:
                        NEW_OUT = left_IN.union(right_IN)
                    
                    else:
                        pass
            
            # print("NEW_OUT we got is--> ", NEW_OUT)
            # print("OUT is --> ",OUT[index])

            if OUT[index] != NEW_OUT:
                flag = True
                OUT[index] = NEW_OUT
            IN[index] = GEN[index].union(OUT[index]-KILL[index])

            index-=1
        
        # print("IN and OUT afte ",iteration_no)
        # print("this is the IN")
        # print(IN)
        # print("this is the OUT")
        # print(OUT)

        iteration_no+=1

    # print("----------final IN and OUT are----------")
    # print(IN)
    # print(OUT)

    # Final work!!!!!!!!!! Lets optimize IR now :)
    # we know how many forward statements are available at any program point and what are the indexes of those program, so now we just
    # have to remove and replace few things :)

    ir2 = []
    index = 0
    d = ["0" for i in cfg]
    variable_no = 0
    last_value = "0"
    for stmt in ir:

        if type(stmt[0]) != kachuaAST.MoveCommand:
            ir2.append(stmt)

        else:
            if(len(IN[index])) == 1:
                new_stmt = (kachuaAST.MoveCommand(stmt[0].direction, stmt[0].expr), stmt[1])
                if(d[index]!="0"):
                    new_stmt[0].expr = stmt[0].expr.__str__() + " + " + d[index]
                ir2.append(new_stmt)
                variable_no+=1
                last_value = "0"
            else:
                if(last_value=="0"):
                    rexpr =  stmt[0].expr.__str__()
                else:
                    rexpr = last_value +" + " + stmt[0].expr.__str__()
                new_stmt = (kachuaAST.AssignmentCommand(':x'+str(variable_no),rexpr), stmt[1])
                last_value = new_stmt[0].lvar
                ir2.append(new_stmt)
                for i in IN[index]:
                    if(i[0]!=stmt[0]):
                        d[i[1]] = new_stmt[0].lvar.__str__()
        index+=1

    f = open("Output5.txt",'w')
    print('========== IR ==========\n',file=f)
    pretty_print(ir,f)
    print("\n",file=f)
    print("---------------------OPTIMIZED IR----------------",file=f)
    print("\n",file=f)
    pretty_print(ir2,f)
    return ir2

def pretty_print(ir,f):
    for idx, item in enumerate(ir):
        print(idx, item[0], ' [', item[1], ']',file=f)