import json
import pandas as pd

from transformers import pipeline

# ------ Data Prep ------ #

# read csv
forum = pd.read_csv('../input/calvin-cs-forum2/forum2.csv')

# only need these columns
needed_columns = ['id', 'userid', 'userfullname', 'message']

# drop all comments and only keep needed columns
forum = forum.loc[forum.get('parent') == 0]

forum.drop(
    columns=forum.columns.difference(needed_columns), 
    axis=1, 
    inplace=True
)

# need to remove unicode characters
forum['message'] = (forum['message']
    .str
    .split()
    .str
    .join(' ')
) 

# ------ Model ------ #

model_name = 'deepset/roberta-base-squad2'

model = pipeline(
    'question-answering', 
    model=model_name, 
    tokenizer=model_name
)

# ------ Predictions ------ #

# hardcode questions for now
questions = [
    'What does Schuurman mean when he says that technology is value-laden?', 
    'Do you agree with what Schuurman says about technology?', 
    'What example is used to illustrate their position on what Schuurman says about technology?'
]

# each post will have a list of answers
answers = {}

# make inferences
for post in forum.itertuples(): # iterate through each post
    post_answers = []
    for question in questions: # then each question
        # model requires question and context
        model_input = {
            'question': question,
            'context': post.message
        }
        
        result = model(model_input)
        
        post_answers.append({
            'answer': result['answer'], # the actual answer itself
            'start_ind': result['start'], # start index of the answer
            'end_ind': result['end'] # end index of the answer
        })

    answers[post.id] = post_answers

# put answer in JSON file
with open('answer.json') as ans:
    ans.write(json.dumps(answers))