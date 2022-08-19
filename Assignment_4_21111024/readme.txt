kachua-v2.3 is used

**Mutate method**
1. create list of possible mutation operations. Ex - ['insert', 'delete', 'flip'......]
2. randomly choose one of the operation from that list
3. now, randomly choose a position in binary form of variable where that particular operation is to be applied
4. apply the operation and return mutated input_data

**compareConverge method**
- if new line is present in current_metric, means coverage is improved therefore return True, else False

**updateTotalConverge**
- take set union of current_metric and total_metric and return total_metric