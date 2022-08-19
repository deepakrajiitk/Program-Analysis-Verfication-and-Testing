To run the program use the following command:
python symbSubmission -t 'timelimit' -f 'list of two files whose equivalence is to be checked' -d 'dictionary of params' -c 'dictionary of constant params' -e 'output variables'

Ex:
python symbSubmission.py -t 100 -f "['eqtest1.tl','eqtest2.tl']" -d "{':x': 45, ':y': 23}" -c "{':c1': 1, ':c2': 1}" -e "['x','y']"


Working:

1. we run the above command
2. generate the ir of both the files
3. run symbolic execution for both the files and get test data for both of them
4. symbolic execution will cover all the possible paths in given time limit and generate testData dictionary
5. two paths of different program are equal if on giving constraints to z3 solver, we get 'sat'
6. to find values of constparams we will generate constraints by equating the params in 'symbEnc' of first file testdata to the 
corresponding params in 'symbEnc' of second testdata (this is done for each equivalent path pair)
7. we will give those constraints to z3 solver and find the value of constparams :)

Note: in above command, the first file in list must be the file with constants c1,c2.. and second file without constants