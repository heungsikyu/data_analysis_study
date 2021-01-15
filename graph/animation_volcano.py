from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the data (csv file is hosted on the web)
url = 'https://python-graph-gallery.com/wp-content/uploads/volcano.csv'
data = pd.read_csv(url)

# data.to_csv(BASE_DIR + '/volcano.csv', sep=',', na_rep='NaN')

# Transform it to a long format
df=data.unstack().reset_index()
print(df)

df.columns=["X","Y","Z"]
print(df)


# And transform the old column name in something numeric
df['X']=pd.Categorical(df['X'])
df['X']=df['X'].cat.codes
print(df)


# We are going to do 20 plots, for 20 different angles
for angle in range(80,210,2):
# Make the plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(df['Y'], df['X'], df['Z'], cmap=plt.cm.viridis, linewidth=0.2)

    ax.view_init(30,angle)

    filename=BASE_DIR+'/Volcano_step'+str(angle)+'.png'
    plt.savefig(filename, dpi=96)
    plt.gca()
    
