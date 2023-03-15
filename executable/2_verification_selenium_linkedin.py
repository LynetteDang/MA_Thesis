import csv
import ast
import jellyfish

reader = csv.reader(open('results_collection.csv', 'r'))
results = {}
for row in reader:
    k, v = row
    results[k] = ast.literal_eval(v)
urls = {}
for key, values in results.items():
    if values[0] != "no result":
        urls[key] = values[1]


def jw_dist(string1, string2):
    return jellyfish.jaro_winkler_similarity(string1, string2) > 0.70


def check_subjects(experiences):
    check_MAPSS = ('social science' in experiences or
                   'social sciences' in experiences or
                   'mapss' in experiences or
                   'history' in experiences or
                   'sociology' in experiences or
                   'economics' in experiences or
                   'committee on social thought' in experiences or
                   'chd' in experiences or
                   'political science' in experiences or
                   'psychology' in experiences or
                   'conceptual and historical studies of science' in experiences or
                   'formation of knowledge' in experiences or
                   'anthropology' in experiences or
                   ('quantitative methods' in experiences and 'social analysis' in experiences) or
                   'qmsa' in experiences or
                   'geographic information science' in experiences)
    check_cir = ('social science' in experiences or
                 'international relations' in experiences or
                 'international security' in experiences or
                 'conflict studies' in experiences or
                 'international political economy' in experiences or
                 'research methods in the social sciences' in experiences or
                 'comparative Studies in political institutions' in experiences)
    check_macss = 'macss' in experiences or 'computational social science' in experiences
    check_cmes = 'middle eastern studies' in experiences or 'cmes' in experiences
    check_subject = check_MAPSS or check_cir or check_macss or check_cmes

    return check_subject


#  Currently alternating among different Linkedin accounts and slowly working through verification:
counter = 0
for name, url in urls.items():
    print(name)
    verified = False
    education_summary = ''
    driver.get(url)
    time.sleep(10)
    try:
        source = BeautifulSoup(driver.page_source, "html.parser")
        info = source.find('div', class_='mt2 relative')
        profile_name = info.find(
            'h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().lower().strip()
        experiences = source.find_all(
            'li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        for experience in experiences:
            education_summary = education_summary + experience.getText()
        education_summary = education_summary.lower()
        check_name = jw_dist(name, profile_name)
        check_school = 'university of chicago' in education_summary
        check_degree = (
            'master' in education_summary or "m.a." in education_summary or "ma" in education_summary)
        check_subject = check_subjects(education_summary)
        if check_name and check_school and check_degree and check_subject:
            verified = True
    except:
        pass
    results[name].append(verified)
    counter = counter + 1
    if counter % 50 == 0:
        time.sleep(1800)
        print(counter)

reader = csv.reader(open('results.csv', 'r'))
results = {}
for row in reader:
    k, v = row
    results[k] = ast.literal_eval(v)
