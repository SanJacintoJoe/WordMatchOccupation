import pandas as pd
import nltk
import regex as re
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
import csv
#nltk.download('wordnet')

csv_file = pd.read_csv("Large_Sample_Title.csv", engine='python') #Sample_title.csv
sample_titles = csv_file['Employement_Employer_Title']  #Employee_Title
csv_file2 = pd.read_csv("Occupation_Definitions.csv")
occupation_definitons = csv_file2['specific_onettitle']
ps = PorterStemmer()

sample_titles = sample_titles.dropna()

Row_list = []
for index, rows in csv_file2.iterrows():
    my_list = [rows.ONETCODEID, rows.specific_onettitle]
    Row_list.append(my_list)

job_title_dict = {}
for item in sample_titles:
    split_item = item.split()
    job_title_dict[item] = split_item
category_title_dict = {}

for item in occupation_definitons:
    job_def = item
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


def check(word):
    try:
        syn2 = wordnet.synsets(word)[0]
        return syn2
    except:
        return 'fail'

def check2(word):
    try:
        syn1 = wordnet.synsets(word)[0]
        return syn1
    except:
        return 'fail'

def check3(syn1, syn2):
    try:
        similarity = syn1.wup_similarity(syn2)
        return similarity
    except:
        return 'fail'

key_list = []
occupation_dict = {}


for key, value in job_title_dict.items():
    key_score = [key]
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
            result = [key2, previous_similarity]
            list_of_scores.append(result)
        org_scores = [word, list_of_scores]
        key_score.append(org_scores)
    key_score = [key_score]
    key_list.append(key_score)


print("Done\n")

size = len(key_list)
number_of_categories = len(key_list[1][0][1][1])
Categories_to_jobs = []

final_Output = []
for i in range(size - 1):
    number_of_words = len(key_list[i][0])
    #we divided the words

    if number_of_words == 3:
        final_score = ['empty', 0]
        three_fourth_match = []
        for x in range(number_of_categories - 1):
            word1 = key_list[i][0][1][1][x][1]
            word2 = key_list[i][0][2][1][x][1]
            category_score = word1 + word2
            if category_score >= 1.7:
                #three_fourth_match = [key_list[i][0][2][1][x][0], category_score]
                test6 = [key_list[i][0][2][1][x][0], category_score]
                three_fourth_match.append(test6)
            elif category_score > final_score[1] and category_score < 1.7:
                final_score = [key_list[i][0][2][1][x][0], category_score]
            else:
                pass

        match2 = three_fourth_match+[final_score]
        output1 = [key_list[i][0][0], match2]
        final_Output.append(output1)
        print(output1)

    if number_of_words == 2:
        final_score2 = ['empty', 0]
        full_match = []
        for x in range(number_of_categories - 1):
            word1 = key_list[i][0][1][1][x][1]
            if word1 == 1:
                full_match.append([key_list[i][0][1][1][x][0], word1])
            if word1 > final_score2[1] and word1 < 1:
                final_score2 = [key_list[i][0][1][1][x][0], word1]
            else:
                pass
        matches = full_match+[final_score2]
        output2 = [key_list[i][0][0], matches]
        final_Output.append(output2)
        print(output2)



#test_dict = {}
series_list = []
data_list = []
for num in range(len(final_Output)):
    for item in final_Output[num][1]:
        for i in Row_list:
            if i[1] == str(item[0]):
                ide = str(i[0])
        row_line = [ide, str(final_Output[num][0]), str(item[0]), str(item[1])]
        data_list.append(row_line)
    #series_item = pd.Series(final_Output[num][1], name=str(final_Output[num][0]))
    #series_list.append(series_item)
    #test_dict[str(final_Output[num])] = final_Output[num][1]
#final_result = pd.concat(series_list, axis=1)
#print(data_list)
column_names = ['ONETCODEID', 'Employement_Employer_Title', 'Occupation', 'Score']
final_result = pd.DataFrame(data_list, columns=column_names)
final_result.to_csv("Reformatted_Occupation_Dataframe.csv")

#print(pd.DataFrame.from_dict(test_dict))


file = open('Job_Match_Output.csv', "w", newline="")
writer = csv.writer(file)
for item in final_Output:
    writer.writerow([item])
file.close()
