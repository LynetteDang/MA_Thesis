
import pandas as pd
import numpy as np
import re

work_exp = pd.read_excel("results_experience-only_no_label.xlsx")
work_exp.head()

work_exp = work_exp[['description', 'company', 'position']]
work_exp = work_exp.dropna()

for index, row in work_exp.iterrows():
    if type(row['description']) == str and ('sustainab' in row['description'] or 'congress' in row['description'] or 'justice' in row['description'] or 'policy' in row['description'] or 'district of' in row['description'] or 'research' in row['description'] or 'campaign' in row['description']):
        row['industry'] = 'Policy/Government/Social Work'
    if (type(row['description']) == str and 'consult' in row['description']) or (type(row['company']) == str and 'consult' in row['company']):
        row['industry'] = 'Consulting'
    if (type(row['description']) == str and ('school' in row['description'] or 'graduate' in row['description'] or 'universit' in row['description'])) or (type(row['company']) == str and ('school' in row['company'] or 'educa' in row['company'] or 'college' in row['company'] or 'university' in row['company'] or 'institute' in row['company'])) or (type(row['position']) == str and ('faculty' in row['position'] or 'tutor' in row['position'] or 'school' in row['position'])):
        row['industry'] = 'Education/Research'
    if type(row['company']) == str and ('pharma' in row['company'] or 'lab' in row['company'] or 'bio' in row['company'] or 'health' in row['company'] or 'hospital' in row['company']):
        row['industry'] = 'Healthcare'
    if type(row['description']) == str and (type(row['description']) == str and ('market' in row['description'] or 'trad' in row['description'] or 'venture' in row['description'] or 'corporate' in row['description'] or 'invest' in row['description'] or 'financ' in row['description'] or 'business' in row['description'] or 'report' in row['description']) or 'banking' in row['description']) or (type(row['company']) == str and ('realty' in row['company'] or 'bank' in row['company'])):
        row['industry'] = 'Business/Finance'
    if (type(row['position']) == str and ('law' in row['position'] or 'legal' in row['position'] or 'attorney' in row['position'] or 'judic' in row['position'])) or (type(row['description']) == str and ('legal' in row['description'] or 'attorney' in row['description'] or 'judic' in row['description'] or 'law' in row['description'])):
        row['industry'] = 'Law'
    if (type(row['description']) == str and ('volunt' in row['description'] or 'nonprofit' in row['description'] or 'community' in row['description'])) or (type(row['company']) == str and ('peace corp' in row['company'] or 'foundation' in row['company'])):
        row['industry'] = 'Charity/Volunteering'
    if (type(row['company']) == str and ('tech' in row['company'])) or (type(row['description']) == str and ('quantum' in row['description'] or 'comput' in row['description'] or 'data' in row['description'] or 'developer' in row['description'] or 'software' in row['description'])):
        row['industry'] = 'Technology'
    if (type(row['position']) == str and ('recruit' in row['position'])) or (type(row['description']) == str and ('recruit' in row['description'] or 'human resource' in row['description'])):
        row['industry'] = 'Human Resources'

work_exp['industry'] = pd.Series(['Others']*len(work_exp))
work_exp['industry'] = work_exp['industry'].fillna('Others')

work_exp_new = pd.read_excel("experience-only_no_label.xlsx")
work_exp_new = work_exp_new[[
    'name', 'experience_type', 'school', 'degree', 'time', 'location']]
work_exp_total = pd.concat([work_exp_new, work_exp], axis=1)
work_exp_total.to_csv('result_industry_classification.csv')


# Process Training data for model
train_df = pd.read_csv('industry_classification_train.csv')
train_df['Category'] = train_df['Category'].replace(
    'Engineering Jobs', 'Technology')
train_df['Category'] = train_df['Category'].replace('IT Jobs', 'Technology')
train_df['Category'] = train_df['Category'].replace(
    'Accounting & Finance Jobs', 'Business/Finance')
train_df['Category'] = train_df['Category'].replace(
    'Customer Services Jobs', 'Business/Finance')
train_df['Category'] = train_df['Category'].replace(
    'Trade & Construction Jobs', 'Business/Finance')
train_df['Category'] = train_df['Category'].replace(
    'Sales Jobs', 'Business/Finance')
train_df['Category'] = train_df['Category'].replace(
    'Property Jobs', 'Business/Finance')
train_df['Category'] = train_df['Category'].replace(
    'Retail Jobs', 'Business/Finance')
train_df['Category'] = train_df['Category'].replace(
    'PR, Advertising & Marketing Jobs', 'Business/Finance')
train_df['Category'] = train_df['Category'].replace('Legal Jobs', 'Law')
train_df['Category'] = train_df['Category'].replace(
    'Consultancy Jobs', 'Consulting')
train_df['Category'] = train_df['Category'].replace(
    'Consultancy Jobs', 'Charity/Volunteering')
train_df['Category'] = train_df['Category'].replace(
    'Scientific & QA Jobs', 'Education/Research')
train_df['Category'] = train_df['Category'].replace(
    'Teaching Jobs', 'Education/Research')
train_df['Category'] = train_df['Category'].replace(
    'Charity & Voluntary Jobs', 'Charity/Volunteering')
train_df['Category'] = train_df['Category'].replace(
    'Social work Jobs', 'Policy/Government/Social Work')
train_df['Category'] = train_df['Category'].replace(
    'HR & Recruitment Jobs', 'Human Resources')
train_df['Category'] = train_df['Category'].replace(
    'Healthcare & Nursing Jobs', 'Healthcare')
train_df['Category'] = train_df['Category'].replace(
    'Hospitality & Catering Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace(
    'Other/General Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace(
    'Hospitality & Catering Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace(
    'Manufacturing Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace('Travel Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace(
    'Creative & Design Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace('Admin Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace(
    'Energy, Oil & Gas Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace(
    'Logistics & Warehouse Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace(
    'Maintenance Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace(
    'Domestic help & Cleaning Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace('Graduate Jobs', 'Others')
train_df['Category'] = train_df['Category'].replace('Part time Jobs', 'Others')

train_df.to_csv("industry_classification_train_with_label.csv")

id2label = {
    "0": "Advertising",
    "1": "Aerospace & Defense",
    "2": "Apparel Retail",
    "3": "Apparel, Accessories & Luxury Goods",
    "4": "Application Software",
    "5": "Asset Management & Custody Banks",
    "6": "Auto Parts & Equipment",
    "7": "Biotechnology",
    "8": "Building Products",
    "9": "Casinos & Gaming",
    "10": "Commodity Chemicals",
    "11": "Communications Equipment",
    "12": "Construction & Engineering",
    "13": "Construction Machinery & Heavy Trucks",
    "14": "Consumer Finance",
    "15": "Data Processing & Outsourced Services",
    "16": "Diversified Metals & Mining",
    "17": "Diversified Support Services",
    "18": "Electric Utilities",
    "19": "Electrical Components & Equipment",
    "20": "Electronic Equipment & Instruments",
    "21": "Environmental & Facilities Services",
    "22": "Gold",
    "23": "Health Care Equipment",
    "24": "Health Care Facilities",
    "25": "Health Care Services",
    "26": "Health Care Supplies",
    "27": "Health Care Technology",
    "28": "Homebuilding",
    "29": "Hotels, Resorts & Cruise Lines",
    "30": "Human Resource & Employment Services",
    "31": "IT Consulting & Other Services",
    "32": "Industrial Machinery",
    "33": "Integrated Telecommunication Services",
    "34": "Interactive Media & Services",
    "35": "Internet & Direct Marketing Retail",
    "36": "Internet Services & Infrastructure",
    "37": "Investment Banking & Brokerage",
    "38": "Leisure Products",
    "39": "Life Sciences Tools & Services",
    "40": "Movies & Entertainment",
    "41": "Oil & Gas Equipment & Services",
    "42": "Oil & Gas Exploration & Production",
    "43": "Oil & Gas Refining & Marketing",
    "44": "Oil & Gas Storage & Transportation",
    "45": "Packaged Foods & Meats",
    "46": "Personal Products",
    "47": "Pharmaceuticals",
    "48": "Property & Casualty Insurance",
    "49": "Real Estate Operating Companies",
    "50": "Regional Banks",
    "51": "Research & Consulting Services",
    "52": "Restaurants",
    "53": "Semiconductors",
    "54": "Specialty Chemicals",
    "55": "Specialty Stores",
    "56": "Steel",
    "57": "Systems Software",
    "58": "Technology Distributors",
    "59": "Technology Hardware, Storage & Peripherals",
    "60": "Thrifts & Mortgage Finance",
    "61": "Trading Companies & Distributors"
},
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
