import numpy as np
import pandas as pd
import scipy as stats
from scipy.stats import chi2



data = {'score': [91, 93, 72, 87, 86, 73, 68, 87, 78, 99, 95, 76, 84, 96, 76, 80, 83, 84, 73, 74],
        'hours': [16, 6, 3, 1, 2, 3, 2, 5, 2, 5, 2, 3, 4, 3, 3, 3, 4, 3, 4, 4],
        'prep': [3, 4, 0, 3, 4, 0, 1, 2, 1, 2, 3, 3, 3, 2, 2, 2, 3, 3, 2, 2],
        'grade': [70, 88, 80, 83, 88, 84, 78, 94, 90, 93, 89, 82, 95, 94, 81, 93, 93, 90, 89, 89]
        }

df = pd.DataFrame(data,columns=['score', 'hours', 'prep','grade'])
print(df.head())

def mahalanobis(x= None, data= None, cov= None):
    x_mu = x - np.mean(data)

    if not cov:
        cov = np.cov(data.values.T)

    inv_covmat = np.linalg.inv(cov)
    left = np.dot(x_mu, inv_covmat)
    mahal = np.dot(left, x_mu.T)
    print(mahal.shape)
    return mahal.diagonal()

df['mahalanobis'] = mahalanobis(x= df, data= df[['score', 'hours', 'prep', 'grade']])

print(df.head())