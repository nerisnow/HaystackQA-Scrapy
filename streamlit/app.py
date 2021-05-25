import streamlit as st

from utils import retrieve_doc
from annotated_text import annotated_text


def annotate_answer(answer,context):
    start_idx = context.find(answer)
    end_idx = start_idx+len(answer)
    annotated_text(context[:start_idx],(answer,"ANSWER","#8ef"),context[end_idx:])

st.write('# Haystack demo')
question = st.text_input("Please provide your query:",value="Who can be vaccinated ?")
run_query = st.button("Run")

if run_query:
    # results,raw_json = retrieve_doc(question)
    results = retrieve_doc(question)
    if results != None:
        st.write("## Retrieved answers:")
        for result in results:
            annotate_answer(result['answer'],result['context'])
            '**Relevance:** ', result['relevance'] , '**Source:** ' , result['source']
        
