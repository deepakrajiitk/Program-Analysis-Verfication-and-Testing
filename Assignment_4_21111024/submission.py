
import sys
import random
from string import ascii_letters
sys.path.insert(0, "KachuaCore/interfaces/")
from interfaces.fuzzerInterface import *

# make sure dot or xdot works and grapviz is installed.
# Uncomment for Assignment-2
# sys.path.append("KachuaCore/kast")
# import kast.kachuaAST
# import graphviz

class CustomCoverageMetric(CoverageMetricBase):
    # Statements covered is used for 
    # coverage information.
    def __init__(self):
        super().__init__()

    # TODO : Implement this
    def compareCoverage(self, curr_metric, total_metric):
        # must compare curr_metric and total_metric
        # True if Improved Coverage else False
        print("-------------current input coverage-------",curr_metric)
        print("-------------total metric coverage -------",total_metric)
        if len(set(curr_metric) - set(total_metric))>0:
            print("______________________IMPROVED________________________")
            return True
        else:
            return False

    # TODO : Implement this
    def updateTotalCoverage(self, curr_metric, total_metric):
        # Compute the total_metric coverage and return it (list)
        # this changes if new coverage is seen for a 
        # given input.
        temp = set(curr_metric).union(set(total_metric))
        total_metric = list(temp)
        print("------------new updated metric------------",total_metric)
        return total_metric

class CustomMutator(MutatorBase):
    def __init__(self):
        pass

    # TODO : Implement this
    def mutate(self, input_data, coverageInfo, irList):
        # Mutate the input data and return it
        # coverageInfo is of type CoverageMetricBase
        # Don't mutate coverageInfo
        # irList : List of IR Statments (Don't Modify)
        # input_data.data -> type dict() with {key : variable(str), value : int}
        # must return input_data after mutation.

        # possible mutation operators
        # 1. insert - inserting a bit at some random position
        # 2. delete - delelting a bit at some random position
        # 3. flip - flipping a bit at some random position
        mutation_operators = ['insert', 'delete', 'flip']

        # randomly choosing one of the mutation operator
        operator = random.choice(mutation_operators)

        # performing operation on input data based on randomly chosen mutation operator
        for key in input_data.data:
            value = input_data.data[key]
            pos = random.randint(2, len(bin(value))-1)
            if operator == 'flip':
                input_data.data[key] = value ^ (1<<pos)   

            elif operator == 'insert':
                temp = bin(value)
                random_bit = random.choice(['0','1'])
                temp = temp[0:pos] + random_bit + temp[pos:]
                input_data.data[key] = int(temp, 2)

            elif operator == 'delete':
                temp = bin(value)
                temp = temp[0:pos] + temp[pos+1:]
                if temp=='0b':
                    temp = '0b0'
                input_data.data[key] = int(temp, 2)

        print("------------------mutated input is-----------------",input_data.data)
        return input_data

# Reuse code and imports from 
# earlier submissions (if any).
def genCFG(ir):
    # your code here
    cfg = None
    return cfg

def dumpCFG(cfg):
    # dump CFG to a dot file
    pass

def optimize(ir):
    # create optimized ir in ir2
    ir2 = ir # currently no oprimization is enabled
    return ir2
