'''
import numpy as np
a = [1,3,4,5]
b = 2
c = np.array(a)
c = np.reshape(c,(2,2))
d = a,b,c
print(d[2])

'''

import json

json_data = '{"round1":{"type1": "new match", "params1":{"a":1}, "type2": "tick", "params2":{"b":1}, "type3": "tick", "params3":{"b":1}}}'
y = json.loads(json_data)
l = list(y.items())
print(l[0][1])
