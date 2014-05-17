# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Analyzing Stop and Frisk Data from NYC (2012)
# 
# For my project I am looking at "Stop and Frisk" data from 2012 to determine the type of people who are getting stopped and frisked. As this issue has become very politicized there are questions about the appropriateness and effectiveness of this approach towards policing. In theory if this was used correctly then it could potentially decrease time. However, in practice it has led to unnecessary harrassment of certain people groups who are being stopped and frisked "on a hunch." 
# 
# ##Some questions to consider##
# 1. What is the breakdown by race and gender of the people being stopped and frisked? Are there any other factors that go into frisks? 
# 2. How "successful" are these frisks if success is defined as stops that lead to arrests? 

# <codecell>

#import packages
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
import pylab as pl

# <markdowncell>

# ##Getting the Data##
# 
# I was able to get 2012 data on **Stop and Frisk** by the NYPD on the [NYCLU website](http://www.nyclu.org/files/stopandfrisk/Stop-and-Frisk-2012.zip).
# 
# Included in the zip file was also a legend with descriptions of all the variables used. The original file includes 532,911 records with 100 variables. 

# <codecell>

#import Stop and Frisk dataset from NYCLU
df = pd.read_csv('../davekoh/DataScience/SNF/SQF2012.csv')
df.shape

# <codecell>

#remove columns which only contains NaNs
#removing columns that have < 500,000 values after dropping NaNs. 
#goes from 532,911 values in 101 columns to 488,299 values and 92 columns

droplist = []
for x in df.columns:
    if len(df[x].dropna()) < 500000:
        droplist.append(x)

for i in droplist:
    df = df.drop(i, axis = 1)

df = df.dropna()
df.shape

# <codecell>

#make dictionaries for race and sex
race_dict = { '1':'Black', 
             '2':'Black Hispanic', 
             '3':'White Hispanic', 
             '4':'White', 
             '5':'Asian', 
             '6':'Am. Indian/Native Alaskan'}

sex_dict = {'1': 'Men', 
            '0': 'Women'}

# <codecell>

#create new labels for race and sex
df['Ethnicity'] = [race_dict[str(int(x))] for x in df['race'].values]
df['Gender'] = [sex_dict[str(int(x))] for x in df['sex'].values]

# <codecell>

%pylab inline 
gender = ['blue', 'red']

#want to show % of people who have been stopped by sex and then by race
stop_stats = (100 * (df.groupby(['Ethnicity', 'Gender']).sex.count() / len(df))).unstack("Gender")
ax = stop_stats.plot(title='Pct. Summary of People Stopped by Race', kind='bar', color=gender, legend=True)
ax.set_ylabel('Pct. Stopped')

# <codecell>

#show % of people who have been frisked by sex and then by race

dffrisk = df[(df.frisked==1)]
frisk_stats = (100 * (dffrisk.groupby(['Ethnicity', 'Gender']).sex.count() / len(dffrisk))).unstack("Gender")
ax = frisk_stats.plot(title='Pct. Summary of People Frisked by Race', kind='bar', color=gender, legend=True)
ax.set_ylabel('Pct. Frisked')

# <codecell>

#want to show pct of people who have been arrested by sex and then by race

dfarst = df[(df.arstmade==1)]
arst_stats = (100 * (dfarst.groupby(['Ethnicity', 'Gender']).sex.count() / len(dfarst))).unstack("Gender")
ax = arst_stats.plot(title='Pct. Summary of People Arrested by Race', kind='bar', color=gender, legend=True)
ax.set_ylabel('Pct. Arrested')

# <codecell>

#Black men age 16-64 from 2010 Census
blackmen = float(564367)

#White men at 16-64 from 2010 Census
whitemen = float(922441)

stop = df.groupby(['Ethnicity', 'Gender']).sex.count()
blmenstop = 100 * (stop['Black']['Men']) / blackmen
whmenstop = 100 * (stop['White']['Men']) / whitemen

frisk = dffrisk.groupby(['Ethnicity', 'Gender']).sex.count()
blmenfrisk = 100 * (frisk['Black']['Men']) / blackmen
whmenfrisk = 100 * (frisk['White']['Men']) / whitemen

arst = dfarst.groupby(['Ethnicity', 'Gender']).sex.count()
blmenarst = 100 * (arst['Black']['Men']) / blackmen
whmenarst = 100 * (arst['White']['Men']) / whitemen

chart = pd.DataFrame(dict(graph=['Stopped', 'Frisked', 'Arrested'],
                           bl=[blmenstop, blmenfrisk, blmenarst], 
                           wh=[whmenstop, whmenfrisk, whmenarst])) 

ind = np.arange(len(chart))
width = 0.4

fig, ax = plt.subplots()
ax.barh(ind, chart.bl, width, color='blue', label='Black Men')
ax.barh(ind + width, chart.wh, width, color='green', label='White Men')

ax.set(title='Pct. Comparison Black Men v. White Men', 
       yticks=ind + width, 
       yticklabels=chart.graph, 
       ylim=[2*width - 1, len(chart)])

ax.legend()

plt.show()

# <codecell>

#Calculate the % of people being stopped who are either Black men or White Hispanic men

bl_stops = float(stop['Black']['Men'])/ len(df)
hi_stops = float(stop['White Hispanic']['Men']) / len(df)

# make a square figure and axes
figure(1, figsize=(6,6))
ax = axes([0.1, 0.1, 0.8, 0.8])

# The slices will be ordered and plotted counter-clockwise.
labels = 'Black Men', 'White Hispanic Men', 'Others'
fracs = [bl_stops, hi_stops, (1 - bl_stops - hi_stops)]

pie(fracs, labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=90)
           

title('Stops in NYC 2012', bbox={'facecolor':'0.8', 'pad':5})

show()

# <markdowncell>

# #Black Men are targeted for stops 1/2 the time
# The main takeaway here is that 74% of the people stopped in NYC are either Black Men or White Hispanic Men. There is a clear pattern of targeting Black people, specifically Black men, but the question is why? 
# 
# **Do stops of Black men actually lead to arrests?** 
# 
# For comparison I have done a horizontal bar plot for Black Men and White Men which shows how many people are stopped, frisked, and eventually arrested. I have normalized the figures by taking the raw counts and dividing them by the total number of Black Men and White Men aged 16-64 respectively. 
# 
# As shown on the charts the chances of a Black Man being stopped and frisked are significantly higher than a White Man. 

# <codecell>

#keep columns for variables that aren't explicitly related to people who have been frisked.
cols_to_keep = ['pct',
            'datestop', 
            'timestop',
            'sex',
            'dob',
            'age',
            'height',
            'weight',
            'perobs',
            'cs_objcs',
            'cs_descr',
            'cs_casng',
            'cs_lkout',
            'cs_cloth',
            'cs_drgtr',
            'cs_furtv',
            'cs_vcrim',
            'cs_bulge',
            'cs_other',
            'inout',
            'offunif',
            'offverb',
            'officrid',
            'offshld']

#create dummy columns for categorical variables
dummy_city = pd.get_dummies(df['city'], prefix='city')
dummy_race = pd.get_dummies(df['race'], prefix='race')
dummy_build = pd.get_dummies(df['build'], prefix='build')
dummy_hair = pd.get_dummies(df['haircolr'], prefix='hair')
dummy_eye = pd.get_dummies(df['eyecolor'], prefix='eye')
dummy_trhs = pd.get_dummies(df['trhsloc'], prefix='trhs')

#join the dataframe with the dummy columns
data = df[cols_to_keep].join(dummy_city.ix[:,:])
data = data.join(dummy_race.ix[:,:])
data = data.join(dummy_build.ix[:,:])
data = data.join(dummy_hair.ix[:,:])
data = data.join(dummy_eye.ix[:,:])
data = data.join(dummy_trhs.ix[:,:])
data.shape

# <codecell>

#Random Forest Classifier without PCA

clf1 = RandomForestClassifier(n_jobs=2)
y, _ = pd.factorize(df['frisked'])
clf1.fit(data,y)

# <codecell>

#Get score on Random Forest Classifier without PCA
clf1.score(data,y)

# <codecell>

#Perform 5-fold cross validation on Random Forest Classifier without PCA
scores = cross_val_score(clf1, data, y, scoring='accuracy', cv=5)
print scores
print scores.mean()

# <markdowncell>

# Running Random Forest with 59 features gives a pretty high accuracy of 72%. As we already know that race, sex, and age are important in determining who is stopped, how accurate is it in determining who is frisked?

# <codecell>

data.info()

# <codecell>

cols_to_keep2 = ['sex', 'age', 'race_1.0', 'race_2.0', 'race_3.0', 'race_4.0', 'race_5.0', 'race_6.0']
data2 = data[cols_to_keep2]

# <codecell>

#Random Forest Classifier without PCA on data subset with race, sex, age
clf2 = RandomForestClassifier(n_jobs=2)
clf2.fit(data2,y)

# <codecell>

#Perform 5-fold cross validation on Random Forest Classifier without PCA on smaller data subset
scores = cross_val_score(clf2, data2, y, scoring='accuracy', cv=5)
print scores
print scores.mean()

# <codecell>

#Random Forest Classifier with PCA

clf3 = RandomForestClassifier(n_jobs=2)
pca = PCA(n_components=15)
X1 = pca.fit_transform(data)
clf3.fit(X1, y)

# <codecell>

#Perform 5-fold cross validation on Random Forest Classifier with PCA
scores = cross_val_score(clf3, X1, y, scoring='accuracy', cv=5)
print scores
print scores.mean()

# <codecell>

#Logistic Regression with PCA

clf4 = LogisticRegression()
clf4.fit(X1, y)
clf4.score(X1, y)

# <codecell>

#Perform 5-fold cross validation on Logistic Regression with PCA
scores = cross_val_score(clf2, X1, y, scoring='accuracy', cv=5)
print scores
print scores.mean()

# <codecell>

#Logistic Regression without PCA

clf5 = LogisticRegression()
clf5.fit(data, y)
clf5.score(data, y)

# <codecell>

#Perform 5-fold cross validation on Logistic Regression without PCA
scores = cross_val_score(clf5, data, y, scoring='accuracy', cv=5)
print scores
print scores.mean()

# <codecell>


