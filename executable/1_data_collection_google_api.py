from googleapiclient.discovery import build
import pandas as pd
import json
import time
import csv


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


df = pd.read_excel('MA graduate data.xlsx')
df = df.rename(columns={"Person::NAME_First": "f_name",
                        "Person::NAME_Last": "l_name"})
with open('api.json') as datafile:
    data = json.load(datafile)

my_api_key = data['my_api_key']
my_cse_id = data['my_cse_id']


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def search_result(name, my_api_key, my_cse_id, results):
    result = google_search(
        f'site:linkedin.com/in/ AND {name} AND "University of Chicago"', my_api_key, my_cse_id)
    num_result = int(result['searchInformation']['totalResults'])
    if num_result < 1:
        results[name_space] = ['no result']
        return 0
    else:
        title, url, snippet = result['items'][0]['title'], result['items'][0]['formattedUrl'], result['items'][0]['snippet']
        results[name_space] = [title, url, snippet]
        print(title)
        return 1


def search_multiple_result(name, my_api_key, my_cse_id, results):
    result = google_search(
        f'site:linkedin.com/in/ AND {name} AND "University of Chicago"', my_api_key, my_cse_id)
    num_result = int(result['searchInformation']['totalResults'])
    if num_result < 1:
        results[name_space] = ['no result']
        return 0
    else:
        results[name_space] = []
        for index, item in enumerate(result['items']):
            title, url, snippet = item['title'], item['formattedUrl'], item['snippet']
            results[name_space].append({index: [title, url, snippet]})
        return 1


def gather_results(sample):
    counter = 0
    for row in sample.itertuples():
        counter = counter + 1
        if counter % 100 == 0:
            print(counter)
            time.sleep(65)
        name_space = row.f_name + " " + row.l_name
        name = row.f_name + row.l_name
        results[name_space] = []
        title = ""
        url = ""
        snippet = ''
        result = google_search(
            f'site:linkedin.com/in/ AND {name} AND "University of Chicago"', my_api_key, my_cse_id)
        num_result = int(result['searchInformation']['totalResults'])
        if num_result < 1:
            results[name_space] = ['no result']
        else:
            title, url, snippet = result['items'][0]['title'], result[
                'items'][0]['formattedUrl'], result['items'][0]['snippet']
            results[name_space] = [title, url, snippet]


df_1 = df.iloc[:1000, :]
df_2 = df.iloc[1000:2000]
df_3 = df.iloc[2000:3000]
df_4 = df.iloc[3000:4000]
df_5 = df.iloc[4000:5000]
df_6 = df.iloc[5000:, :]

results = {}

gather_results(df_1)

gather_results(df_2)

gather_results(df_3)

gather_results(df_4)

gather_results(df_5)

gather_results(df_6)


len(results)

sum(df.duplicated(subset=['f_name', 'l_name']))

with open('results_collection.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in results.items():
        writer.writerow([key, value])

count_no_result = 0
for key, values in results.items():
    if values[0] != "no result":
        count_no_result = count_no_result + 1
print("no results: " + str(count_no_result) + "\n" + "have results: " +
      str((len(results) - count_no_result)))
