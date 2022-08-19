from z3 import *
import argparse
import json
import pickle
import os.path
import sys
sys.path.insert(0, '../KachuaCore/')
from sExecutionInterface import *
from kast.builder import astGenPass
from sExecution import *
import z3solver as zs
from irgen import *
from interpreter import *
import ast

def example(s):
    # To add symbolic variable x to solver
    s.addSymbVar('x')
    s.addSymbVar('y')
    # To add constraint in form of string
    s.addConstraint('x==5+y')
    s.addConstraint('And(x==y,x>5)')
    # s.addConstraint('Implies(x==4,y==x+8')
    # To access solvers directly use s.s.<function of z3>()
    print("constraints added till now",s.s.assertions())
    # To assign z=x+y
    s.addAssignment('z','x+y')
    # To get any variable assigned
    print("variable assignment of z =",s.getVar('z'))

# this function generate the IR of file 
def load_IR(filename):
    parseTree = getParseTree(filename)
    astgen = astGenPass()
    ir = astgen.visitStart(parseTree)
    with open("optimized.kw", 'wb') as f:
        pickle.dump(ir, f)
    f = open("optimized.kw", 'rb')
    ir = pickle.load(f)
    return ir

# this function check if path of first progrom is equivalent to path of second program
def solve(test1, test2, out_params, solver):
    s = zs.z3Solver()
    for param in ast.literal_eval(test1['params']):
        s.addSymbVar(param)
    s.addConstraint(test1['constraints'])
    s.addConstraint(test2['constraints'])
    res = s.s.check()
    # print(res)
    if str(res) == 'sat':
        d1 = ast.literal_eval(test1['symbEnc'])
        d2 = ast.literal_eval(test2['symbEnc'])
        params = ast.literal_eval(test1['params'])
        for i in out_params:
            for j in out_params:
                d1[i] = d1[i].replace(j,str(params[j]))
                d2[i] = d2[i].replace(j,str(params[j]))
        # print(d1)
        # print(d2)
        for i in out_params:
            constraint = d1[i]+"=="+d2[i]
            # print(constraint)
            solver.addConstraint(constraint)



def checkEq(args,ir1,ir2):
    args1 = copy.deepcopy(args)
    args2 = copy.deepcopy(args)
    testData1 = symbolicExecutionMain(ir1,args1.params,args1.constparams,args1.timeout)
    testData2 = symbolicExecutionMain(ir2,args2.params,args2.constparams,args2.timeout)
    print(json.dumps(testData1,indent=4))
    print(json.dumps(testData2,indent=4))
    s = zs.z3Solver()
    for key in testData1:
        for key2 in testData2:
            solve(testData1[key],testData2[key2],args.output,s)
    print(s.s.assertions())
    res = s.s.check()
    if str(res)=='sat':
        print("--------------------------"+str(s.s.model())+"-----------------------------")
    else:
        print("No Solution")



if __name__ == '__main__':
    cmdparser = argparse.ArgumentParser(
        description='symbSubmission for assignment Program Synthesis using Symbolic Execution')
    # cmdparser.add_argument('progfl')
    cmdparser.add_argument('-t', '--timeout', default=10, type=float, 
                            help='Timeout Parameter for Analysis (in secs)')
    cmdparser.add_argument('-f','--progfl',default=list(), type = ast.literal_eval,
                            help='pass two files name whose equivalence is to be checked')
    cmdparser.add_argument('-d', '--params', default=dict(),  type=ast.literal_eval,
                            help="pass variable values to kachua program in python dictionary format")
    cmdparser.add_argument('-c', '--constparams', default=dict(),  type=ast.literal_eval,
                            help="pass variable(for which you have to find values using circuit equivalence) values to kachua program in python dictionary format")
    cmdparser.add_argument('-e', '--output', default=list(), type=ast.literal_eval,
                            help="pass variables to kachua program in python dictionary format")
    args = cmdparser.parse_args()
    # print(type(args.params))
    filename1 = os.path.dirname(__file__) + '/../kachuacore/example/'+args.progfl[0]
    filename2 = os.path.dirname(__file__) + '/../kachuacore/example/'+args.progfl[1]
    # print(filename2)
    ir1 = load_IR(filename1)
    ir2 = load_IR(filename2)
    # print(ir1)
    # print(ir2)
    checkEq(args,ir1,ir2)
    exit()


