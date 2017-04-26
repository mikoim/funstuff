import numpy as np
A = np.array([[3,5],[2,7]])
B = np.array([7500,8850])
x = np.dot(np.linalg.inv(A), B)
print(x)  # [  750.  1050.]
