import json
import pandas as pd
import streamlit as st

# ------ Data Prep ------ #

# read csv
forum = pd.read_csv('forum2.csv')

# only need these columns
needed_columns = ['id', 'userid', 'userfullname', 'message']

# drop all comments and only keep needed columns
forum = forum.loc[forum.get('parent') == 0]

forum.drop(
    columns=forum.columns.difference(needed_columns), 
    axis=1, 
    inplace=True
)

forum['message'] = forum['message'].str.split().str.join(' ') # need to remove unicode characters

questions = [ # questions hardcoded
    'What does Schuurman mean when he says that technology is value-laden?', 
    'Do you agree with what Schuurman says about technology?',
    'What example is used to illustrate their position on what Schuurman says about technology?'
]

answers = {}

with open('answers.json') as ans:
    answers = json.loads(ans.read())

for q in questions:
    st.write(q)

for post in forum.itertuples():
    cur_ans = answers[str(post.id)]
    
    answer_inds = []

    for a in cur_ans:
        answer_inds.append(a['start_ind'])
        answer_inds.append(a['end_ind'])

    highlighting = False

    message_spans = []

    for i in range(len(post.message)):
        color = 'white'

        if i in answer_inds and answer_inds.index(i) % 2 == 0: # if it is a start of an answer
            highlighting = True
        
        if highlighting:
            color = 'red'
        
        message_spans.append(
            f'<span style="color: {color}; white-space: pre-wrap;">{post.message[i]}</span>'
        )

        if i in answer_inds and not answer_inds.index(i) % 2 == 0: # if it is an end of an answer
            highlighting = False


    st.write(''.join(message_spans), unsafe_allow_html=True)

    st.write('\n\n\n')
