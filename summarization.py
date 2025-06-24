import streamlit as st
import os
import requests
import webbrowser
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

chat = ChatOpenAI(openai_api_key=st.secrets["OPENROUTER_API_KEY"], base_url="https://openrouter.ai/api/v1", model="mistralai/mistral-7b-instruct:free")

def formattingForSummarizer(text):
    for each in text :
        if (each == "'") :
            text = text.replace(each, "")
        if(each == "`"):
            text = text.replace(each, "")    
    
    text = text.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
    return text


def summarizer (text):

    CleanText = formattingForSummarizer(str(text))
    summarizer_prompt  = "You are the manager of a hotel and you're task is to summarize the given content: that is the details of booking into the format needed for billing. Please format the summary as follows:\nBooking Details:\nCustomer Name: [Customer Name]\nRoom Type: [Room Type]\nCheck-in Date: [Check-in Date]\nCheck-out Date: [Check-out Date]\nNumber of Guests: [Number of Guests]\nNightly Rate: [Nightly Rate]\nExtras: [Extras]\n"

    messages = [
        HumanMessage(content=summarizer_prompt + CleanText)
    ]

    response = chat.invoke(messages)
    print(response.content)
    return response.content

def generateKBase(largeData):

    rqdFormat =  [
        {
        "title": " ",
        "snippet": " "
        },
    ]
    FormatPrompt = "You should extract the given details text: " + largeData +" into this  \n: "+ " "+ str(rqdFormat) + "\n JSON FORMAT and populate the corresponding values from text : The snippet can contain the large amount of tokens.Don't shortent the content" 
    messages = [
        HumanMessage(content=FormatPrompt)
    ]
    response = chat.invoke(messages)
    print(response.content)
    # sendAPIReg(response.generations[0].text)




def main():
    text = """The customer wants to book a 1-bedroom suite for 2 days
The check-in date is from 13th September
The suite costs ₹12600 and comes with a king bed, executive lounge access, a shower/tub combination, and amenities like high-speed internet and 2 TVs.
Nothing was mentioned about extras."""

    # generateKBase(data)
    # generateDetails(text)

# Add the summary
if __name__ == "__main__":
    main()

