import re
import pandas as pd
import ast
import csv

df1 = pd.read_csv('results_verified_1.csv', header=None)
df2 = pd.read_csv('results_verified_2.csv', header=None)
df3 = pd.read_csv('results_verified_3.csv', header=None)
df4 = pd.read_csv('results_verified_4.csv', header=None)
df5 = pd.read_csv('results_verified_5.csv', header=None)
df__1 = pd.read_csv('results_verified_-1.csv', header=None)
df__2 = pd.read_csv('results_verified_-2.csv', header=None)
df__3 = pd.read_csv('results_verified_-3.csv', header=None)

sample = pd.concat([df1, df2, df3, df4, df5, df__1,
                   df__2, df__3], ignore_index=True)

sample = sample[[0, 1]]

sample.columns = ["Name", "Result"]

sample.to_csv('results_verification.csv')


def edu_or_exp(all_sections):
    educations = []
    experiences = []
    for section in all_sections:
        if 'bachelor' in section or 'master' in section or 'ma, ' in section or 'phd' in section or 'ph.d' in section or 'j.d.' in section or 'juris doctor' in section or 'doctor of medicine' in section or 'mba' in section or 'md' in section or 'high school' in section:
            educations.append(section)
        elif 'show credential\n' in section or 'show project\n' in section or 'show publication\n' in section or '^[0-9]+$ endorsement\n' in section or '^[0-9]+$ endorsements\n' in section or 'recent posts and comments will be displayed here' in section or 'reposted' in section:
            pass
        else:
            experiences.append(section)
    return educations, experiences


def first_break_down(text):
    text = text.split(
        '\n\n\n\n\n\n \n\n \n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n')
    all_sections = []
    delimiters = "\n\n\n\n\n\n \n\n \n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n", '\n\n\n\n\n \n\n \n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n', '\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n'
    regex_pattern = '|'.join(map(re.escape, delimiters))
    for txt in text:
        new_txt = re.split(regex_pattern, txt)
        all_sections.extend(new_txt)
    return all_sections


def further_break_down(sections):
    for section in sections:
        if '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n' in section:
            section_list = section.split(
                '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n')
            sections.remove(section)
            for sec in experience_list:
                if 'mos' in sec or 'yr' in sec:
                    sections.append(sec)


def same_string(test_str):
    regex = f'{test_str[-2:]}{test_str[0:2]}'
    match = re.search(regex, test_str)
    if match is not None:
        return test_str[match.end()-2:]


def edu_list(educations):
    education_list = []
    for education in educations:
        education_dict = {}
        edu_list = section_summary(education)
        for index, edu in enumerate(edu_list):
            if "(" in edu or ")" in edu:
                new_edu = re.sub(r'\([^)]*\)', '', edu)
                edu_list.remove(edu)
                edu_list.insert(index, new_edu)
        if len(edu_list) > 3:
            education_dict['school'] = same_string(edu_list[0])
            education_dict['degree'] = same_string(edu_list[1])
            education_dict['time'] = same_string(edu_list[2])
            education_list.append(education_dict)
    return education_list


def section_summary(section):
    delimiters = '\n\n \n\n', " ¬∑ ", "\n\n\n", " · "
    regex_pattern = '|'.join(map(re.escape, delimiters))
    section_detail = re.split(regex_pattern,  section)
    return section_detail


def exp_list(experiences):
    experience_list = []
    regexp = re.compile(r'^[0-9]+$')
    for experience in experiences:
        if experience != '':
            new_experience = ''
            experience_dict = {}
            if "(" in experience or ")" in experience:
                new_experience = re.sub(r'\([^)]*\)', '', experience)
            else:
                new_experience = experience
            exp_list = section_summary(new_experience)
            while '' in exp_list:
                exp_list.remove('')
            while ' ' in exp_list:
                exp_list.remove(' ')
            while '\n ' in exp_list:
                exp_list.remove('\n ')
            if exp_list != []:
                if len(exp_list) > 4:
                    experience_dict['position'] = same_string(exp_list[0])
                    experience_dict['company'] = same_string(exp_list[1])
                    experience_dict['time'] = exp_list[4]
                    experience_dict['description'] = max(exp_list, key=len)
                    experience_dict['location'] = same_string(exp_list[-1])
                    experience_list.append(experience_dict)
                    if len(experience_list) > 5:
                        break
    return experience_list


data = {}
for index, alum in sample.iterrows():
    try:
        alum_1 = ast.literal_eval(alum[1])
        for s in alum_1:
            if type(s) is bool:
                alum_1.remove(s)
        if alum_1 != ['no result'] and False not in alum_1 and '\n\n\n\n' in max(alum_1, key=len):
            text = max(alum_1, key=len)
            all_sections = first_break_down(text)
            educations, experiences = edu_or_exp(all_sections)
            education_list = edu_list(educations)
            experience_list = exp_list(experiences)
            data[alum[0]] = {"education": education_list,
                             "experience": experience_list}
    except:
        pass


with open('result_preprocessing_initial.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in data.items():
        for category, sections in value.items():
            for section in sections:
                writer.writerow([key, section])

# %%
df = pd.read_csv('result_preprocessing_initial.csv', header=None)


with open('result_preprocessing_final.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['name', 'experience_type', 'school', 'degree',
                    'time', 'position', 'company', 'description', 'location'])
    for index, row in df.iterrows():
        name = row[0]
        details = row[1]
        school = ''
        degree = ''
        time = ''
        position = ''
        company = ''
        description = ''
        location = ''
        experience_type = 'work'
        try:
            school = ast.literal_eval(details)['school']
            experience_type = 'school'
        except:
            pass
        try:
            degree = ast.literal_eval(details)['degree']
        except:
            pass
        try:
            time = ast.literal_eval(details)['time']
        except:
            pass
        try:
            position = ast.literal_eval(details)['position']
        except:
            pass
        try:
            company = ast.literal_eval(details)['company']
        except:
            pass
        try:
            description = ast.literal_eval(details)['description']
        except:
            pass
        try:
            location = ast.literal_eval(details)['location']
        except:
            pass
        writer.writerow([name, experience_type, school, degree,
                        time, position, company, description, location])
