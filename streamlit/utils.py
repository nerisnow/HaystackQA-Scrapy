import requests as request
import streamlit as st
import logging as logger
#servicename:portnumber/predict

url = "https://a44bf24d5143.ngrok.io/predict"

def format_request(question):
    """ 
    get the question from front end and changes it to json form.
    in: question of type string.
    out:question in dict form.

    """
    return{'questions':question}

def get_results(response):
    """ 
    get the answer and its context from json respone
    in:json response from api
    out:list containing the dict of answer,context,metadata and probability.

    """
    result = []
    context_check = []
    answers = response['answers']

    for i in range(len(answers)):
        answer = answers[i]['answer']
        if answer:
            context = '...' + answers[i]['context'] + '...'
            meta_name = answers[i]['meta']['title']
            relevance = round(answers[i]['probability']*100,2)
            #checking the context for avoiding duplicate data.
            if context not in context_check:
                result.append({'context':context,'answer':answer,'source':meta_name,'relevance':relevance})
                context_check.append(context)
    context_check.clear()
    #sorting the result in descending order 
    result=sorted(result, key = lambda i: i['relevance'],reverse=True)
    return result


def retrieve_doc(question):
    payload = format_request(question)
    logger.info("Received question.")
    response = request.post(url = url,json = payload)
    logger.info("Received response.")
    st.write(response.status_code)

    if response.status_code != 200:
        st.write("Status code error")
        return None

    response=response.json()
    result = get_results(response)
    return result
