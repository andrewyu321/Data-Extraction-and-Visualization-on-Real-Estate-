import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



df = pd.read_csv('real_estate_data')




altered = df.groupby(['area'])

test = altered['prices'].aggregate(np.average)
test = test.reset_index()
test.columns.values[1] = 'prices'


test1 = test.loc[:20, :]

plt.figure(figsize=(30,6))

chart = sns.barplot(x='area', y='prices', data=test)


plt.xticks(rotation=45)
plt.show()


