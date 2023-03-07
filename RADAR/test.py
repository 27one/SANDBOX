import numpy as np

tt = np.array([1,2,3,4]).reshape(2,-1)
print(tt)
diag = tt.diagonal()
print(diag)