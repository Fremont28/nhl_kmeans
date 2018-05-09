from sklearn.cluster import KMeans
import numpy as np 
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

nhl=pd.read_csv("skater_stats_2018-04-26 (1).csv")
#subset defenseman
nhl_def=nhl[nhl["Position"]=="D"]
#ice-time per game
nhl_def['ice_time/game']=nhl_def['TOI']/nhl_def['GP'] #15.32
nhl_def['ice_time/game'].median() #15.52
nhl_def['ice_time/game'].describe() 
nhl_def['GP'].describe() 
nhl_def_sub=nhl_def[(nhl_def['ice_time/game']>13.76)&(nhl_def['GP']>35)] #281 players
len(nhl_def_sub) #281 to 181 players
nhl_def_sub.to_csv("coconut_juice1.csv")

dist_columns=['P/60','CF%','Rel CF%','GF%','iP+/-','iCF/60','ixGF/60','PDO',
'iSh%','TOI%','CF% QoT','P1/60','GS/60','G+/-','Rel GF%',
'xGF','xGA','iPEND','iPENT','ZSR','TOI% QoC',
'ice_time/game']
#normalize the data
numbers_nhl1=nhl_def_sub[dist_columns]
norm_def=(numbers_nhl1-numbers_nhl1.mean())/(numbers_nhl1.std())
#compare to a defenseman
doughty=norm_def[nhl_def_sub['Player']=="DREW.DOUGHTY"].iloc[0]
#1. euclidean distance
euc_distance_x=norm_def.apply(lambda x: distance.euclidean(x,doughty),axis=1)
distance_frame1=pd.DataFrame(data={"dist":euc_distance_x,"idx":euc_distance_x.index})
euc_distances2=pd.DataFrame(euc_distance_x)
players_only1=nhl_def_sub[["Team","Player"]]
frames1=[players_only1,euc_distances2] 
result_x=pd.concat(frames1,axis=1)
result_x2=pd.DataFrame(result_x)
result_x.columns=['Team','Player','Distance']
sort_distance=result_x.sort_values(['Distance'])
sort_distance
#to dataframe
sort_distance.to_csv("kings_sim1.csv")



#2. kmeans
k_means_def=norm_def.apply(lambda x: KMeans(n_clusters=4))
k_means_frame=pd.DataFrame(data={"kmeans":k_means_def,"idx":k_means_def.index})
len(norm_def) #181
nhl_def_sub.info() 
kmeans=KMeans(n_clusters=5,random_state=0).fit(norm_def)
means=kmeans.predict(norm_def)
labels=kmeans.labels_ 
kmeans.cluster_centers_
players_array=nhl_def_sub[['Player','Team']].values 
#combine arrays
k_means_players=np.column_stack((players_array,labels))
k_means_players
k_means_players.shape 
k_means_players1=pd.DataFrame(k_means_players)
k_means_players1 
k_means_players1.to_csv("coconut_juice1.csv")

#plot centers 
centers=kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='orange', s=199, alpha=0.5)
plt.show() 

#combine k_means players and regular stats 
type(numbers_nhl1) 
numbers_nhl2=nhl_def_sub.values 
numbers_nhl3=numbers_nhl2[:,4:45]
final_groupings=np.column_stack((k_means_players,numbers_nhl3))
#mean by group
final_groupings1=pd.DataFrame(final_groupings) 
final_groupings1.to_csv("passion_fruit.csv") 

#create matrix X and target y vector
nhl_def_sub.info() 
nhl_def_sub['xGF%'].describe() 
type(nhl_def_sub) 
nhl_def_sub.columns.get_loc("xGF") 
nhl_def_sub['xGF%'].describe() 
low_xg=nhl_def_sub[nhl_def_sub['xGF%']<47.77]
low_xg['Player']
def expected_goals(x):
    if x>52.65:
        return 0
    if x<52.65 or x>50.26:
        return 1
    if x<50.26 or x>47.77:
        return 2
    else:
        return 3 
nhl_def_sub['xg_label']=nhl_def_sub.apply(lambda x:expected_goals(x['xGF%']),axis=1)
nhl_def_sub['xg_label'].value_counts() 
nhl_def_sub.info()
nhl_def_sub1=nhl_def_sub[['Player','Team','CF%','iP+/-','iCF/60','iSh%','PDO','ZSR',
'TOI% QoT','CF% QoT','ice_time/game','xg_label']]
nhl_def_sub2=nhl_def_sub1.values #convert df to np array 
nhl_def_sub2.shape 
#biggest values in columns
big_cf=np.partition(nhl_def_sub2[:,2],3) #corsi for% 
big_cf[:3] 
#
X=np.array(nhl_def_sub2[:,2:11])
y=np.array(nhl_def_sub2[:,11])
y=y.astype('int')
#train and test sets
X_train1,X_test1,y_train1,y_test1=train_test_split(X,y,test_size=0.31,random_state=0)
#KNN classifier
knn=KNeighborsClassifier(n_neighbors=3) 
knn.fit(X_train1,y_train1)
pred_y=knn.predict(X_test1)
accuracy_score(y_test1,pred_y)