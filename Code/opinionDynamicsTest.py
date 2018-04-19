import numpy as np
import scipy as sp
import pandas
import random

Pv = [
    [0.00025, 0, 0, 0.00025],
    [0.0005, -0.0005, -0.0005, 0],
    [0.0005, 0, -0.0005, 0],
    [0. , 0, -0.0005, 0.0005],
    [0, -0.00025, -0.00025, 0]]
#print( pandas.DataFrame(Pv) )

Pe = [
    [ ['AA', 1], ['AC', 1], ['AC', 0.12], ['AA', 1] ],
    [ ['AA', 1], ['AC', 1], ['AC', 1], ['AA', 0.87] ],
    [ ['NC', 1], ['NC', 1], ['NC', 1], ['NC', 1] ],
    [ ['BC', 1], ['BA', 0.87], ['BA', 1], ['BC', 1] ],
    [ ['BC', 0.12], ['BA', 1], ['BA', 1], ['BC', 1] ]
    ]
print( pandas.DataFrame(Pe) )

infoCodes = {'GA':0, 'BA':1, 'GB':2, 'BB':3}
partyCodes = {'AA':0, 'AC':1, 'NC':2, 'BC':3, 'BA':4}

info = ['GA', 'BA', 'GB', 'BB']

p1 = ['AA', 0.55, 'I']
p2 = ['AC', 0.48, 'I']
p3 = ['NC', 0.47, 'I']
p4 = ['BC', 0.5, 'I']
p5 = ['BA', 0.52, 'I']


people = [p1, p2, p3, p4, p5]

#for i in info :
    #print(i)
"""for person in people :
    rowIndex = partyCodes[ person[0] ]
    colIndex = infoCodes[ info[0] ]
    #print( Pv[rowIndex][colIndex] )
    person[1] += Pv[rowIndex][colIndex]"""

print( pandas.DataFrame(people) )

#for i in info :
#print(i)
for person in people :
    rowIndex = partyCodes[ person[0] ]
    colIndex = infoCodes[ info[3] ]
    newState = Pe[rowIndex][colIndex]
    val = random.uniform(0,1)
    print(val, newState[1])
    if val <= newState[1] :
        person[0] = newState[0]
        #print(person[0])
print( pandas.DataFrame(people) )
