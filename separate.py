import numpy as np  # works in 1.10.1
import pandas as pd  # works in 0.13.1
import sys
import json
import gc
import os
from datetime import datetime
import csv
import shutil

import math

print(f'Number of arguments:{len(sys.argv)}')

file = sys.argv[1]
classifications = sys.argv[2]
print(classifications)
workflow_version = sys.argv[3]

if file == [] or classifications == [] or workflow_version ==[]:
    print("Include a file name and workflow version please")



CHILDREN_TEXT_TASKS = ['T1','T7','T12','T17','T22','T27','T32','T42','T47','T52','T57','T62']
TAGS = 'T9'
OTHER_TEXT = 'T8'


def extract_subject(id, subject, volume, number, divider):
    column_titles = subject.loc[s['task'] == 'T0']['data.consensus_text'].to_list()
    column_titles_string = column_titles[0].split(divider)
    lines_transcribed = 0
    ongoing_consensus = 0
    original_path = f'ntranscripts/{volume}/{number}.csv'

    with open(original_path, 'w') as file:
        writer = csv.writer(file)

        # add column titles to csv
        writer.writerow(column_titles_string)
        # writer.writerow('\n')

        for task in CHILDREN_TEXT_TASKS:
            score = float(subject.loc[s['task'] == task]['data.consensus_score'])
            child = subject.loc[s['task'] == task]['data.consensus_text'].to_list()
            if isinstance(child[0], str):
                child_text_array = child[0].split(divider)
                # Add child text to csv
                writer.writerow(child_text_array)
                lines_transcribed = lines_transcribed + 1
                ongoing_consensus = ongoing_consensus + score
                
        # Add any other text to file
        other_text = subject.loc[s['task'] == OTHER_TEXT]['data.consensus_text'].to_list()[0]
        if str(other_text) == True:
            other_text_string = other_text.split(divider)
            writer.writerow(other_text_string)

        # Add any keywords to file
        tags = subject.loc[s['task'] == TAGS]['data.consensus_text'].to_list()[0]
        if str(tags) == True:
            writer.writerow(tags.split(divider))
            
    # if consesnsus score is low - move file 
    if ongoing_consensus < (lines_transcribed * 1.5):
        # lots of issues
        new_path = path = f'ntranscripts/{volume}/low/{number}.csv'
        shutil.move(original_path,new_path)  
    elif ongoing_consensus < (lines_transcribed * 2):
        # a fair few issues
        new_path = path = f'ntranscripts/{volume}/medium/{number}.csv'
        shutil.move(original_path,new_path)

# Only nessecary for the fucking idiots who used forwad spaces
def clean_string(string):
    string = string.replace('/unclear', "\\unclear").replace('/deletion', "\\deletion").replace('/insertion', "\\insertion")
    return string

 

# --------------------------------------------------------------------------
# Program is run from here

# file = ('text_reducer_first-attempt-text.csv')
data = pd.read_csv(file)

subjects = data.subject_id.unique()
all_classifications = pd.read_csv(classifications)

for classification_id in subjects:
    print(classification_id)
    

    # Create dataframe with only specific subject
    s = data.loc[data['subject_id'] == classification_id]

    # find the mutherfudging volume and id
    entry = all_classifications.loc[all_classifications['subject_ids'] == classification_id].iloc[0]
    subject = json.loads(entry['subject_data'])
    
    volume = subject[str(classification_id)].get('volume')
    number = subject[str(classification_id)].get('subject number')

    # test registers don't have a volumne
    if volume == None:
        volume = "test"

    if number == None:
        number = classification_id

    import code; code.interact(local=dict(globals(), **locals()))

    # Create the main column names from text
    column_titles = s.loc[s['task'] == 'T0']['data.consensus_text'].to_list()
    column_titles_string = column_titles[0].split('\\')

    if (classification_id == 53253694):
            import code; code.interact(local=dict(globals(), **locals()))

    if len(column_titles_string) == 1:
        print('idiot used forward slashes')
        extract_subject(classification_id, s, volume, number, '/')
    else :
        extract_subject(classification_id, s, volume, number, '\\')



        