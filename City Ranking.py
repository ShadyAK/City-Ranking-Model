#!/usr/bin/env python
# coding: utf-8

# ### Importing necessary libraries

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ### Data import and analysis

# In[3]:


data=pd.read_csv("city_ranking.csv")


# In[4]:


data.head()


# ### Let's see some statistical details of the given data

# In[30]:


data.describe()


# ## Points to be noted
# 1. Almost all observation's mean lie around 5.
# 2. Most of the country have a good Access to Contraceptive and Immigration Tolerence score.

# ## Now we will give a quick look to the cities having the best feature score among the dataset

# In[5]:


features=data.columns[2:-1]
countries=[]
for i in range(len(features)):
    indexes=np.where(data.iloc[:,i+2]==max(data.iloc[:,i+2]))
    indexes=indexes[0].tolist()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    print("City/ies with the best score of the feature :",features[i])
    print("|City Name X Country|")
    for j in range(len(indexes)):
        print(data.iloc[indexes[j],0]," ",data.iloc[indexes[j],1],features[i],":",data.iloc[indexes[j],i+2])
        #countries.append(data.iloc[indexes[j],1])
    print("--------------------------------------------------------------------")    


# ## Country wise scores

# In[6]:


grouped_data=data.groupby(["country"])
for i in range(len(features)):
    print("Feature :",features[i])
    series=grouped_data[features[i]].agg(np.mean)
    country_name_max_score=series[series==max(series)].index[0]
    max_score=max(series)
    print("Country with max score :",country_name_max_score,"|| Score: ",max_score)
    print("Number of observations in the country:",len(data[data.iloc[:,1]==country_name_max_score].iloc[:,0]))
    print("------------------------------------------------")


# # Creating Model 

# ## Algorithm
# 1. The algorithm is based on the concept of adding extra values to the ratings of the features wanted by the user in the city
# 2. The results will give more waitage to the user requirements.
# 3. Other features will not be discarded as other features are not important to the user but will serve a better recommendation and experience to the user(practically)
# 4. The bias value is based on practical experimentation and observations , so the model might not give perfect results but is doing the best taking the given time to create the model in consideration.There is definately scope of improvement.
# 5. Due to the lack of the user data the model had to be created from the scratch.

# ## Explanation of Bias Multiplier
# The bias in this model is defined by a function i.e. [10xi/len(features) for i in range(0,len(features)x3,3)] which will result in values [0,30/18,120/18,....]. The bias value for the first priority of the feature user wants in the predictions will be the biggest bias in the list i.e. the bias value at -1 index.
# [10xi/len(features) for i in range(0,len(features)x3,3)] :   range(0,len(features)x3,3) this part of the function makes sure that within the priorities the first priority should always have a greater impact on the final result and the impact of all priorities should be order wise according to the user.
# 

# In[7]:


def model(feature_list):
    biases=[10*i/len(features) for i in range(0,len(features)*3,3)]
    biases.reverse()
    final_scores={}
    for i in range(data.shape[0]):
        row_score=data.iloc[i:i+1,2:-1].sum(axis=1)[i] #Pandas series index will be set as i so extraction of numeric from series we have to specify the index
        for j in range(len(feature_list)):
            bias_add=data.iloc[i,feature_list[j]+2]*biases[j]
            row_score+=bias_add
        final_scores[row_score]=data.iloc[i,0]    
    return final_scores
    #final_scores
     
    


# ## Taking the user input

# In[8]:


print("Enter the numbers respective to the features you want in the city \nNote:Enter them according to the necissity rank i.e. more important first")
for i in range(len(features)):
    print(i,features[i])
print("\n\n\nEnter them as inline order example:'1 4 5 6 3'")    


# In[9]:


while True:
    input_data=input()
    try:
        input_data=list(map(int,input_data.split(" ")))
        break
    except:
        print("---------------------------------")
        print("oops take care of spaces and do not give extra spaces at the end of the input")
        print("Enter input as example below \n6 7 8 9 2 1")
        print("---------------------------------")


# ### Lets assume a person wants to setup a business abroad , his requirements are Startup Score,Employment Score,Transport,Immigration Tollerance
# * Input:1 0 5 11

# In[10]:


scores=model(input_data)
sorted_keys=sorted(scores,reverse=True)
sorted_keys[:5]
suggestions=[]
index=[]
for i in range(5):
    index.append(data[data.iloc[:,0]==scores[sorted_keys[i]]].index.tolist()[0])
    suggestions.append(scores[sorted_keys[i]])
print("Top 5 recommended cities for you")
print(suggestions) 
data.iloc[index,:]    


# In[11]:


def plot_figures(suggestions):
    f, axes = plt.subplots(1, 5, figsize=(18, 5), sharex=True,sharey=True)
    plt.figure(figsize=(12,5))
    for i in range(5):
        col=i
        x=features[input_data].tolist()
        x.append("Overall City Score")
        #print(x)
        y=data.loc[index[i],features[input_data]].tolist()
        y.append(data.iloc[index[i],-1])
        #print(y)
        g=sns.barplot(x=x,y=y,ax=axes[col])
        g.set_xticklabels(labels=x,rotation=90)
        g.set_title(suggestions[i])


# ## Visualizing the recommendations

# In[12]:


plot_figures(suggestions)


# *Now the user can decide on himself what features he can compromise a bit and which city would be best suited by looking at this visual representation of the recommendations. 
