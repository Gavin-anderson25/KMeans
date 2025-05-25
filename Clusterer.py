import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
iris = 'http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
iris = pd.read_csv(iris, sep=',')
columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
iris.columns = columns

#Matrix Initialization#
print("Compare which variables?")
print(columns)
print("X-axis?")
x_specify = input()
print("Y-Axis?")
y_specify = input()
matrix = pd.DataFrame({'x':iris[x_specify], 'y':iris[y_specify], 'species':iris.species, 'cluster':iris.sepal_width})
print(matrix)

#Cluster Generation#
clustersx = []
clustersy = []
print("Enter the number of clusters:")
k = int(input())
x_upper = max(matrix['x'])
y_upper = max(matrix['y'])
x_lower = min(matrix['x'])
y_lower = min(matrix['y'])
for i in range(k):
    if i%2 == 1:
        clustersx.append(x_lower + (i*((x_upper-x_lower)/k)))
        clustersy.append(y_upper)
    elif i%2 == 0:
        clustersx.append(x_lower + (i*((x_upper-x_lower)/k)))
        clustersy.append(y_lower)
clusters = pd.DataFrame({'x':clustersx, 'y':clustersy})
print(clusters)
print("--------------")
r = 0
dist_check = x_upper - x_lower

#Datapoint Assignment#
while r <= 100:
    for i in range(len(matrix)):
        minimum = 10000000000
        iteration = 0
        decision = ()
        dist = ()
        for c in range(len(clusters['x'])):
            dist = np.sqrt(((matrix.loc[i, 'y']-clusters.loc[c, 'y'])**2)+((matrix.loc[i, 'x']-clusters.loc[c, 'x'])**2))
            if dist < minimum:
                minimum = dist
                decision = iteration
            iteration += 1
        matrix.loc[i, 'cluster'] = decision
        
#Cluster Adjustment#
    for i in range(k):
        grouping_x = []
        grouping_y = []
        for c in range(len(matrix)):
            if matrix.loc[c, 'cluster'] == i:
                grouping_x.append(matrix.loc[c, 'x'])
                grouping_y.append(matrix.loc[c, 'y'])
        center_x = sum(grouping_x)/len(grouping_x)
        center_y = sum(grouping_y)/len(grouping_y)
        dist_proxy = np.sqrt(((center_y-clusters.loc[i, 'y'])**2)+((center_x-clusters.loc[i, 'x'])**2))
        
        #print(dist_proxy)
        if dist_proxy > dist_check:
            dist_check = dist_proxy
        clusters.loc[i, 'x'] = center_x
        clusters.loc[i, 'y'] = center_y
    r += 1
    
#Information Display#
clusters.columns = [x_specify, y_specify]

print(clusters)
#Graph Generation#
visual = sns.relplot(data=matrix, x='x', y='y', hue='cluster', palette="Paired", style="species")
visual.ax.set_xlabel(x_specify)
visual.ax.set_ylabel(y_specify)
plt.show()
print("Press any key to exit.")
input()
