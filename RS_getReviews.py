import os
import re
import urllib2
from zipfile import ZipFile
import csv


import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame,Series
import numpy as np
import random

import re
from bs4 import BeautifulSoup

def getReviewURL(review):
# function to get all the urls from the csv files 
	
	for x in review:
		urlStart= x.rfind('(')+1
		urlEnd=x.find(')',urlStart)
		url.append(x[urlStart:urlEnd])
return url

def getReviews(url):
	RSreviews=[]
	for x in url: 
		html = urllib2.urlopen(x)
		soup = BeautifulSoup(html)
		reviewTags=soup.find(attrs={'class' : 'post-body entry-content'})
		reviewText=reviewTags.text
		endReview=reviewText.find('Bulk Buy!')
		textOnly=reviewText[:endReview]
		textOnly=textOnly.replace('\n',' ')
		textOnly=textOnly.replace('\'','')
		RSreviews.append(textOnly)
