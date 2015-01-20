
# coding: utf-8

# In[14]:

import os
import re

import pandas as pd
from pandas import DataFrame,Series
import pandas.io.sql 

import numpy as np
import random

from bs4 import BeautifulSoup
import requests

import html5lib
import unicodedata

import pymysql as mdb


# In[48]:

def getReviewURL(review):
# function to get all the urls from the csv files 
    url=[]
    for x in review:
        if -1<x.rfind('('):
            urlStart= x.rfind('(')+1
            urlEnd=x.find(')',urlStart)
            url.append(x[urlStart:urlEnd])
        else: 
             url.append(x)
    return url


# In[46]:

def getReviews(url):
    RSreviews=[]
    for x in url: 
        try:
            html = urllib2.urlopen(x)
            soup = BeautifulSoup(html)
            reviewTags=soup.find(attrs={'class' : 'post-body entry-content'})
            reviewText=reviewTags.text
            endReview=reviewText.rfind('Bulk Buy')
            textOnly=reviewText[:endReview-1]
            textOnly=textOnly.replace('\n',' ')
            textOnly=textOnly.replace('\'','')
            RSreviews.append(textOnly)
        except :
            RSreviews.append('none')

    return RSreviews


# In[134]:

def removeStopWords(reviews):
    reviewNoStops=[]
    allWordsAllRevs=[]
    noStopLine=[]
    for line in reviews:
        line=line.lower()
        print line
        line=re.sub(r'[\W_]+', ' ', line)
        line=re.sub(r'[\d_]+', ' ', line)
        singleLine=[]
        for w in line.split():
            if w.lower() not in stops and 3<len(w)<10:
                w=w.encode('utf-8')
                singleLine.append(w)
                noStopLine.append(w)
        
        allWordsAllRevs.append([singleLine])
        reviewNoStops.append([singleLine])
    
    reviewNoStops=np.unique(noStopLine,False,False).tolist()
    #noStopLine=[x.encode('utf-8') for x in noStopLine]
    
    return noStopLine,reviewNoStops,allWordsAllRevs


# In[ ]:

def getNameVintage(wine):
    name=[re.split(' ',w,1)for w in wine]


# In[6]:

#read in csv file 
reverseSnob= pd.read_csv('ReverseWineSnob.com_Wine_Ranking.csv')
allRevs= pd.read_csv('RSreviews2.csv')


# In[49]:

url=getReviewURL(reverseSnob['Review'])


# In[123]:

# get all reviews... DO NOT RUN AGAIN
RSreviews=getReviews(url)


# In[409]:

RSreviewsTextOnly=[re.split('Overall Rating',line)[0] for line in RSreviews]
allRevs.to_csv('RSreviews2.csv',encoding='utf-8')


# In[124]:

# see how many wines did not have reviews
emptyRevs=[rev for rev in RSreviews if re.search('none',rev)]


# In[125]:

print "Reviews for {0} wines were not found".format(len(emptyRevs))


# In[114]:

reverseSnob= pd.read_csv('ReverseWineSnob.com_Wine_Ranking.csv')

name=[re.split(' ',w,1)for w in reverseSnob['Wine']]
wineName=[n[1] for n in name]
wineVintage=[n[0] for n in name]
reverseSnob['wineName']=wineName
reverseSnob['wineVintage']=wineVintage
reverseSnob['url']=url
reverseSnob['TypeClassifier']=reverseSnob['Type']

replaceWhites=['Rosé','Sparkling','Cider Wine','Box']
for w in replaceWhites:
    reverseSnob['TypeClassifier']=[type.replace(w,'White') for  type in reverseSnob['TypeClassifier']]
    
    
reverseSnob['TypeClassifier']=[type.replace('Dessert','Red') for  type in reverseSnob['TypeClassifier']]


reverseSnobPad=reverseSnob.fillna(value=0)

reverseSnobPad.drop(['Review','Wine','wineName','url'],axis=1, inplace=True)
reverseSnobLongText=reverseSnob


# In[115]:

con = mdb.connect('localhost', 'root', 'cortex', 'cellarTracker') #host, user, password, #database
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS reverseSnobTable")
reverseSnobPad.to_sql(con=con,name='reverseSnobTable', flavor='mysql',if_exists='append',index_label='indx')


# In[97]:

con = mdb.connect('localhost', 'root', 'cortex', 'cellarTracker') #host, user, password, #database
cur = con.cursor()
cur.execute("ALTER TABLE reverseSnobTable ADD (Review MEDIUMTEXT,Wine MEDIUMTEXT,wineName MEDIUMTEXT,url TINYTEXT)")


#cur.execute("CREATE TABLE reverseSnobTable")
#print reverseSnob

                      


# In[112]:

#reverseSnob[['Review','Wine','wineName','url']].to_sql(con=con,name='reverseSnobTable', flavor='mysql',if_exists='append',index_label='indx')



# In[ ]:

with con:
   cur.execute("SELECT * reverseSnobTable")
   rows = cur.fetchall()
   print len(rows)


# In[118]:

allRevs[:2]


# In[113]:




# In[265]:




# In[269]:




# In[329]:

wineNames=np.unique(reverseSnob['Type'])


# In[330]:

cx=reverseSnob.groupby('Type').count()


# In[425]:

bar_width = 0.8
x=range(0,len(cx['Wine']))
plt.bar(x,cx['Wine'],bar_width,color='#990000')
x=np.add(x,0.5)
plt.ylabel('Number of wines')
plt.xticks(x, ['Box', 'Cider', 'Dessert', 'Port', 'Red', 'Rose',
       'Sparkling', 'White'])


# In[120]:

html = urllib2.urlopen(url[1])
soup = BeautifulSoup(html)
reviewTags=soup.find(attrs={'class' : 'post-body entry-content'})
reviewText=reviewTags.text
endReview=reviewText.rfind('Bulk Buy')


# In[119]:

from nltk.corpus import stopwords
stops = set(stopwords.words('english'))


# In[131]:

uniqueWords,trainReviews,allWordsAllRevs=removeStopWords(allRevs[:800])
uniqueWordsSet=set(uniqueWords)


# In[133]:

get_ipython().magic(u'pinfo trainReviews')


# In[415]:

tokenWords=nltk.word_tokenize(str(allWordsInRev))


# In[417]:

fdist = nltk.FreqDist(tokenWords)


# In[418]:

fdist.plot(30,cumulative=True)


# In[421]:

fdist.keys()[1]


# In[303]:

from sklearn.preprocessing import LabelBinarizer
from sklearn.svm  import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB


# In[305]:

vec = CountVectorizer(vocabulary=uniqueWordsSet)


# In[426]:

trainXsparse=vec.fit_transform(reverseSnob['TypeClassifier'][:800])


# In[428]:

get_ipython().magic(u'pinfo trainReviews')


# In[ ]:

clf = MultinomialNB()
clf.fit(trainXsparse,ytrain)

