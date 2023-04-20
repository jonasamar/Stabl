import pandas as pd 
import csv
import numpy as np 
import matplotlib.pyplot as plt 

df = pd.DataFrame(data = [['bonjour', 'Jonas', 'Amar'],[1.,2., 3.],['Test', 'is', 'OK']])

df.to_csv('./df.csv', index=True)

plt.plot(np.linspace(1, 2, 10), np.linspace(1, 2, 10))
plt.title('Plot Test')
plt.show()

