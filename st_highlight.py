import json
import pandas as pd
import streamlit as st
import numpy as np

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

highlight_colors = ['green', 'blue', 'red']

answers = {}

with open('answers.json') as ans:
    answers = json.loads(ans.read())

for q in questions:
    st.write(q)

for post in forum.itertuples():
    st.subheader(post.id)
    cur_post = post.message
    cur_ans = answers[str(post.id)]
    
    colors = np.array(['white'] * len(cur_post))

    for answer_idx, ans in enumerate(cur_ans):
        colors[
            ans['start_ind']:
            ans['end_ind']
        ] = highlight_colors[answer_idx]

    message_spans = [
        f'<span style="color: {color};">{cur_post[i]}</span>'
        for i, color in enumerate(colors)
    ]

    st.write('<div style="white-space: pre-wrap;">' + ''.join(message_spans) + '</div>', unsafe_allow_html=True)

    st.write('\n\n\n')
