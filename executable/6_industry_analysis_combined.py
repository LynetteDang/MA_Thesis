from collections import Counter
import csv
import nlu
import pandas as pd
import seaborn as sns
import re
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import roc_curve, auc
from sklearn.feature_selection import SelectFromModel
%matplotlib inline

# Self-trained Model
data = pd.read_csv('industry_classification_train_with_label.csv')
final_data = data[['Category', 'Title', 'FullDescription']]
final_data.groupby(by='Category').count()

final_data = pd.concat([final_data[final_data['Category'] == 'Business/Finance'].sample(n=2238),
                        final_data[final_data['Category'] ==
                                   'Charity/Volunteering'].sample(n=2238),
                        final_data[final_data['Category']
                                   == 'Consulting'].sample(n=2238),
                        final_data[final_data['Category'] ==
                                   'Education/Research'].sample(n=2238),
                        final_data[final_data['Category']
                                   == 'Healthcare'].sample(n=2238),
                        final_data[final_data['Category'] ==
                                   'Human Resources'].sample(n=2238),
                        final_data[final_data['Category']
                                   == 'Law'].sample(n=2238),
                        final_data[final_data['Category']
                                   == 'Others'].sample(n=2238),
                        final_data[final_data['Category'] ==
                                   'Policy/Government/Social Work'].sample(n=2238),
                        final_data[final_data['Category'] == 'Technology'].sample(n=2238)]
                       )

final_data.groupby(by='Category').count()
final_data['length'] = final_data['FullDescription'].apply(len)
plt.figure(figsize=(205, 20))
final_data.hist(column='length', by='Category', figsize=(10, 10))
plt.show()


def clean_text(row):

    row = re.sub(r"n\'t", " not", row)
    row = re.sub(r"n\'ll", " will", row)
    row = re.sub(r"n\'ve", " have", row)
    row = re.sub(r"n\'t", " not", row)
    row = re.sub(r"i.e", " ", row)
    row = re.sub(r"n\'s", "", row)
    row = re.sub("[^a-zA-Z]", " ", row)
    white_space = re.compile(r"\s+")
    row = white_space.sub(" ", row).strip()
    return row


final_data['FullDescription'] = (
    final_data['FullDescription']).apply(lambda row: clean_text(row))
final_data['FullDescription'].tail(1)
final_data.reset_index(inplace=True)
final_data["concat_text"] = final_data.FullDescription.astype(
    str) + final_data.Title.astype(str)

stopwords = set(['i', 'l', 'my', 'it', 'off', 'means', 'if', 'you', 'husband', 'do', 'what', 'and', 'a', 'an'
                 'is', 'for', 'this', 'after', 'the', 'so', 'to', 'm', 'that', 'into', 'those', 'were', 'was',
                 'other', 'some', 'are', 'now', 'ry', 'at', 'serv', 't', 's', 'rece',
                 'in', 'don', 'adv', 'word', 'let', 'her', 'him', 'he', 'she', 'them', 'they', 'be', 'been',
                 've', 'some', 'such', 'qu', 'same', 'only', 'up', 'here', 'there', 'do', 'very', 'over',
                 'but', 'via', 'felt', 'who', 'whom', 'whose', 'where', 'how', 'about', 'just', 'most', 'has',
                 'had', 'have', 'way', 'back', 'front', 'let', 'flow', 'sun', 'del', 'your', 'move', 'got', 'air',
                 'breath', 'dude', 'know', 'mean', 'pan', 'means', 'mine', 'both', 'with', 'another', 'bit',
                 'clumps', 'needs', 'room', 'code', 'one', 'ones', 'f', 'em', 'as', 'n', 'cho', 'me', 'descr',
                 'pr', 'compet', 're', 'could', 'would', 'should', 'even', 'r', 'out', 'their', 'n', 'ly', 'down',
                 'from', 'because', 'until', 'unless', 'while', 'its', 'about', 'all', 'any', 'few', 'too',
                 'own', 'itself', 'ppl', 'keep', 'really', 'got', 'AP', 'close'])

vect = TfidfVectorizer(lowercase=True, stop_words={
                       'english'}.update(stopwords), max_df=.8, min_df=3)
X = vect.fit_transform(final_data.concat_text)
y = final_data.Category

# Logistic Regression

lg = LogisticRegression(C=1, penalty="l2", max_iter=1000)
grid = {"C": np.logspace(-3, 3, 7), "penalty": ["l2"]}  # l2 ridge
lg_cv = GridSearchCV(lg, grid, cv=10)
lg_cv.fit(X_train, Y_train)
print("tuned hpyerparameters :(best parameters) ", lg_cv.best_params_)
print("accuracy :", lg_cv.best_score_)
selector = SelectFromModel(lg, max_features=4113)
X_train_selected = selector.fit_transform(X, y)
train_idx, test_idx = train_test_split(np.arange(final_data.shape[0]), test_size=0.4,
                                       shuffle=True, random_state=42)
X_train = X_train_selected[train_idx]
Y_train = y[train_idx]
X_test = X_train_selected[test_idx]
Y_test = y[test_idx]

lg.fit(X_train, Y_train)
y_pred = lg.predict(X_test)

print(classification_report(Y_test, y_pred))


# Naive Bayes
vect = TfidfVectorizer(stop_words={'english'}.update(stopwords))
nb = MultinomialNB()
vect = TfidfVectorizer(lowercase=True, stop_words={
                       'english'}.update(stopwords), max_df=.7, min_df=5)
X = vect.fit_transform(final_data.concat_text)
y = final_data.Category
train_idx, test_idx = train_test_split(np.arange(final_data.shape[0]), test_size=0.4,
                                       shuffle=True, random_state=42)
X_train = X[train_idx]
Y_train = y[train_idx]
X_test = X[test_idx]
Y_test = y[test_idx]
clf = MultinomialNB(alpha=1)
clf.fit(X_train, Y_train)
y_pred = clf.predict(X_test)
print(classification_report(Y_test, y_pred))

# alumni data
small_data = pd.read_csv('result_industry_classification.csv')
small_data = small_data[['description', 'company', 'position', 'industry']]
small_data.dropna(inplace=True)
small_data['description'] = (small_data['description']).apply(
    lambda row: clean_text(row))
small_data["concat_text"] = small_data.description.astype(
    str) + small_data.position.astype(str)


vect = TfidfVectorizer(lowercase=True, stop_words={
                       'english'}.update(stopwords), max_df=.5, min_df=2)
X = vect.fit_transform(small_data.concat_text)
y = small_data.industry
y_pred = lg.predict(X)
print(classification_report(y, y_pred))

nlu_model = nlu.load("en.classify.distilbert_sequence.industry")


def most_common(lst):
    data = Counter(lst)
    return max(lst, key=data.get)


industry_true = small_data[['industry']]

industry = []

for i, row in enumerate(small_data['description']):
    if type(row) == str:
        if type(nlu_model.predict(row)['classified_sequence'][0]) == str:
            lst = []
            ind_pred = nlu_model.predict(row)['classified_sequence']
            for val in ind_pred:
                lst.append(val)
            industry.append(most_common(lst))
        else:
            industry.append('Others')

id2label = {'0': 'Advertising',
            '1': 'Aerospace & Defense',
            '2': 'Apparel Retail',
            '3': 'Apparel, Accessories & Luxury Goods',
            '4': 'Application Software',
            '5': 'Asset Management & Custody Banks',
            '6': 'Auto Parts & Equipment',
            '7': 'Biotechnology',
            '8': 'Building Products',
            '9': 'Casinos & Gaming',
            '10': 'Commodity Chemicals',
            '11': 'Communications Equipment',
            '12': 'Construction & Engineering',
            '13': 'Construction Machinery & Heavy Trucks',
            '14': 'Consumer Finance',
            '15': 'Data Processing & Outsourced Services',
            '16': 'Diversified Metals & Mining',
            '17': 'Diversified Support Services',
            '18': 'Electric Utilities',
            '19': 'Electrical Components & Equipment',
            '20': 'Electronic Equipment & Instruments',
            '21': 'Environmental & Facilities Services',
            '22': 'Gold',
            '23': 'Health Care Equipment',
            '24': 'Health Care Facilities',
            '25': 'Health Care Services',
            '26': 'Health Care Supplies',
            '27': 'Health Care Technology',
            '28': 'Homebuilding',
            '29': 'Hotels, Resorts & Cruise Lines',
            '30': 'Human Resource & Employment Services',
            '31': 'IT Consulting & Other Services',
            '32': 'Industrial Machinery',
            '33': 'Integrated Telecommunication Services',
            '34': 'Interactive Media & Services',
            '35': 'Internet & Direct Marketing Retail',
            '36': 'Internet Services & Infrastructure',
            '37': 'Investment Banking & Brokerage',
            '38': 'Leisure Products',
            '39': 'Life Sciences Tools & Services',
            '40': 'Movies & Entertainment',
            '41': 'Oil & Gas Equipment & Services',
            '42': 'Oil & Gas Exploration & Production',
            '43': 'Oil & Gas Refining & Marketing',
            '44': 'Oil & Gas Storage & Transportation',
            '45': 'Packaged Foods & Meats',
            '46': 'Personal Products',
            '47': 'Pharmaceuticals',
            '48': 'Property & Casualty Insurance',
            '49': 'Real Estate Operating Companies',
            '50': 'Regional Banks',
            '51': 'Research & Consulting Services',
            '52': 'Restaurants',
            '53': 'Semiconductors',
            '54': 'Specialty Chemicals',
            '55': 'Specialty Stores',
            '56': 'Steel',
            '57': 'Systems Software',
            '58': 'Technology Distributors',
            '59': 'Technology Hardware, Storage & Peripherals',
            '60': 'Thrifts & Mortgage Finance',
            '61': 'Trading Companies & Distributors'}

for i, ind in enumerate(industry):
    if id2label['4'] in ind or id2label['15'] in ind or id2label['18'] in ind or id2label['19'] in ind or id2label['20'] in ind or id2label['57'] in ind or id2label['58'] in ind or id2label['59'] in ind or id2label['33'] in ind:
        industry[i] = 'Technology'
    elif id2label['30'] in ind:
        industry[i] = 'Human Resources'
    elif id2label['0'] in ind or id2label['2'] in ind or id2label['3'] in ind or id2label['5'] in ind or id2label['8'] in ind or id2label['9'] in ind or id2label['14'] in ind or id2label['29'] in ind or id2label['34'] in ind or id2label['35'] in ind or id2label['36'] in ind or id2label['37'] in ind or id2label['38'] in ind or id2label['40'] in ind or id2label['46'] in ind or id2label['49'] in ind or id2label['50'] in ind or id2label['52'] in ind or id2label['55'] in ind or id2label['60'] in ind or id2label['61'] in ind:
        industry[i] = 'Business/Finance'
    elif id2label['7'] in ind or id2label['23'] in ind or id2label['24'] in ind or id2label['25'] in ind or id2label['26'] in ind or id2label['27'] in ind or id2label['39'] in ind or id2label['47'] in ind:
        industry[i] = 'Healthcare'
    elif id2label['51'] in ind:
        industry[i] = 'Education/Research'
    elif id2label['31'] in ind:
        industry[i] = 'Consulting'
    elif id2label['14'] in ind or id2label['48'] in ind:
        industry[i] = 'Education/Research'
    elif id2label['17'] in ind:
        industry[i] = 'Charity/Volunteering'
    elif id2label['1'] in ind or id2label['21'] in ind or id2label['32'] in ind:
        industry[i] = 'Policy/Government/Social Work'
    else:
        industry[i] = 'Others'

print(classification_report(industry_true, industry))

industry_final = []

for i, ind in enumerate(industry):
    if 'Technology' in ind or 'Healthcare' in ind or 'Charity' in ind or 'Human Resources' in ind or 'Others' in ind:
        industry_final.append(ind)
    else:
        industry_final.append(y_pred[i])

print(classification_report(industry_true, industry_final))
