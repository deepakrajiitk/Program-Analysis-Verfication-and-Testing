
import sys
import graphviz
sys.path.insert(0, './ast')
from itertools import islice

import kachuaAST

class Graph:
    def __init__(self, graph_dict = None):
        if graph_dict==None:
            graph_dict={}
        self.graph_dict = graph_dict

    def add_vertex(self,vertex):
        if vertex not in self.graph_dict:
            self.graph_dict[vertex]=[]
    
    def add_edges(self,source, dest):
        self.graph_dict[source].append(dest)

    def get_node_in_string_form(self,node):
        node_string=""
        for statement in node.stmts:
                node_string +=statement.__str__().replace(':',"")
                node_string+="\n"
        return node_string
    
    def print_graph(self):
        print("\n")
        print('========== CFG ==========')
        print("\n")
        for vertex in self.graph_dict:
            print([i.__str__() for i in vertex.stmts],end="")
            print(" --> ",end="")
            children=[]
            for i in self.graph_dict[vertex]:
                temp=[]
                for j in i.stmts:
                    temp.append(j.__str__().replace(':',""))
                children.append(temp)
            print(children)
        print("\n")

# a node contain all statements of basic block
class Node:
    def __init__(self, stmts):
        # when node is exit node
        if(len(stmts)==0):
            stmts=['exit']
        self.stmts = stmts

# this function finds the index of all leaders
def find_leaders(ir):
    leaders = {0,len(ir)}
    for idx, item in enumerate(ir):
        if item[1]!=1:
            leaders.add(idx+1)
            leaders.add(idx+item[1])
    return list(leaders)

# this function finds all basic blocks indexes(ex- block0 indexes = [1,2,3], block2 indexes=[4,5])
def find_basic_blocks(ir, leaders):
    leaders.sort()
    blocks={}
    nodes={}
    for i in range(len(leaders)-1):
        blocks[leaders[i]]=list(range(leaders[i],leaders[i+1]))

    # initialising last block(exit block) to an empty list
    blocks[leaders[len(leaders)-1]]=[]
    return blocks

def builtGraph(ir, blocks):
    graph = Graph()

    # temp dictionary is used to identify different nodes based on their leader's index
    temp={}

    # adding nodes to the graphs (vertices to the graph are added as a Node object)
    for key in blocks:
        node = Node([ir[index][0] for index in blocks[key]])
        graph.add_vertex(node)
        temp[key]=node
    
    # adding edges to the graph
    # islice is used because last key of blocks is an exit block which contain empty list, therefore it is used to iterate only till second last key of dictionay
    for key in islice(blocks,len(blocks)-1):

        # edge due to normal jump to next statement(pc = pc+1)
        #if the statement is False then we should not move pc to pc+1
        if(ir[blocks[key][-1]][0].__str__()!='False'):
            edge1 = (key, blocks[key][-1]+1)
            graph.add_edges(temp[edge1[0]],temp[edge1[1]])

        # edge due to jump because of branch statemetn(pc = pc+branch)
        if (ir[blocks[key][-1]][1]!=1):
            edge2 = (key, blocks[key][-1]+ir[blocks[key][-1]][1])
            graph.add_edges(temp[edge2[0]],temp[edge2[1]])

    return graph
    

def genCFG(ir):
    # your code here
    leaders = find_leaders(ir)
    blocks = find_basic_blocks(ir, leaders)
    cfg=builtGraph(ir, blocks)
    cfg.print_graph()
    return cfg

def dumpCFG(cfg):
    # dump CFG to a dot file
    dot = graphviz.Digraph(comment='CFG')

    # iterating over all vertices of graph
    for vertex in cfg.graph_dict:

        # variable a stores string form of node 1 of edge
        a = cfg.get_node_in_string_form(vertex)

        # iterating over all neighbors of vertex 
        for i in cfg.graph_dict[vertex]:

            # variable b stores string form of node 2 of edge
            b = cfg.get_node_in_string_form(i)
            dot.edge(a, b)

    dot.render('dot files/test.gv', view=True)  
