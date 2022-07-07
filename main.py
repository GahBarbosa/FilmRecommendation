import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('white')

column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('historic.data', sep='\t', names=column_names)
movie_titles = pd.read_csv("Movie_Id_Titles")
df = pd.merge(df,movie_titles,on='item_id')

ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())

moviemat = df.pivot_table(index='user_id',columns='title',values='rating')
ratings.sort_values('num of ratings',ascending=False).head(10)


def recommend(name):
    user_ratings = moviemat[name]
    similar = moviemat.corrwith(user_ratings)
    corr_similar = pd.DataFrame(similar,columns=['Correlation'])
    corr_similar.dropna(inplace=True)
    corr_similar = corr_similar.join(ratings['num of ratings'])
    suggestions = corr_similar[corr_similar['num of ratings']>100].sort_values('Correlation',ascending=False).head()
    print(suggestions)
    plt.figure(figsize=(10,4))
    suggestions.hist(bins=70)
    plt.show()
    pass

recommend('Star Wars (1977)')
# recommend('Liar Liar (1997)')
# recommend('Rock, The (1996)')
