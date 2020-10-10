import pandas as pd
import regex as re
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer

csv_file = pd.read_csv("Large_Sample_Title.csv", engine='python') #Sample_title.csv
sample_titles = csv_file['Employement_Employer_Title']  #Employement_Employer_Title
csv_file2 = pd.read_csv("Occupation_Definitions.csv")
occupation_definitions = csv_file2['specific_onettitle']
ps = PorterStemmer()
sample_titles = sample_titles.dropna()

occupation_id_dict = dict(zip(csv_file2.specific_onettitle, csv_file2.ONETCODEID))

job_title_dict = {}
for item in sample_titles:
    split_item = item.split()
    job_title_dict[item] = split_item
category_title_dict = {}

for item in occupation_definitions:
    job_def = item
    item = re.sub(r'OF|AND', '', item)
    split_item = item.split()
    New_item = []
    for word in split_item:
        word = word.lower()
        word = re.sub(r's\b|ing|\,', '', word)
        if word != 'and':
            New_item.append(word)
        else:
            pass
    category_title_dict[job_def] = New_item


blank_occupation_dict = {}
for i in occupation_definitions:
    blank_occupation_dict[i] = 0


class similarity_score:
    def __init__(self, blank_occupation):
        self.score_dict = blank_occupation

    def add_value(self, occupation, score):
        self.score_dict[occupation] = float(self.score_dict[occupation]) + float(score)

    def get_score_dict(self):
        return self.score_dict


def check(word_val):
    try:
        syn2 = wordnet.synsets(word_val)[0]
        return syn2
    except:
        return 'fail'


def check2(word_val2):
    try:
        syn1 = wordnet.synsets(word_val2)[0]
        return syn1
    except:
        return 'fail'


def check3(syn1_a, syn2_b):
    try:
        similarity_val = syn1_a.wup_similarity(syn2_b)
        return similarity_val
    except:
        return 'fail'


key_list = []
for key, value in job_title_dict.items():
    sim = similarity_score(blank_occupation_dict.copy())
    for word in value:
        list_of_scores = []
        syn1 = check2(word)
        for key2, value2 in category_title_dict.items():
            previous_similarity = 0
            for category_word in value2:
                if ps.stem(category_word) == ps.stem(word):
                    similarity = 1
                else:
                    syn2 = check(category_word)
                    if str(syn2) != 'fail' or None:
                        similarity = check3(syn1, syn2)
                    else:
                        pass
                    if type(similarity) != float:
                        similarity = 0
                    else:
                        pass
                if similarity > previous_similarity:
                    previous_similarity = similarity
                elif similarity == 1:
                    break
                else:
                    pass
            sim.add_value(key2, float(previous_similarity))
    occupation_score_dict = sim.get_score_dict()
    number_of_words = len(value)
    key_score = [key, number_of_words, occupation_score_dict]
    key_list.append(key_score)

def f1():
    v = list(d1.values())
    k = list(d1.keys())
    return k[v.index(max(v))]


list_of_matches = []
for row in key_list:
    row_addition_count = 0
    if row[1] == 1:
        for occupation_title, similarity_value in row[2].items():
            if similarity_value >= 0.8:
                id_code = occupation_id_dict[occupation_title]
                complete_row = [row[0], id_code, occupation_title, similarity_value]
                list_of_matches.append(complete_row)
                row_addition_count += 1
    else:
        word_count = row[1] - 0.5
        for occupation_title, similarity_value in row[2].items():
            if similarity_value >= word_count:
                id_code = occupation_id_dict[occupation_title]
                complete_row = [row[0], id_code, occupation_title, similarity_value]
                list_of_matches.append(complete_row)
                row_addition_count += 1
    if row_addition_count < 1:
        v = list(row[2].values())
        k = list(row[2].keys())
        max_similarity_value = max(v)
        max_occupation = k[v.index(max(v))]
        id_code = occupation_id_dict[max_occupation]
        complete_row = [row[0], id_code, occupation_title, similarity_value]
        list_of_matches.append(complete_row)


column_names = ['Employee_Employer_Job_Title', 'ONETCODEID', 'Occupation_Title', 'Similarity_Score']
final_result = pd.DataFrame(list_of_matches, columns=column_names)
final_result.to_csv("Job_Title_Occupation")

print("Done\n")











