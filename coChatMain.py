import streamlit as st
from typing import Literal
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from summarization import summarizer
from rag_utils import create_vector_store, load_vector_store, get_relevant_docs
import os

chat = ChatOpenAI(openai_api_key=st.secrets["OPENROUTER_API_KEY"], base_url="https://openrouter.ai/api/v1", model="mistralai/mistral-7b-instruct:free")

# Initialize vector store
db = create_vector_store()
db = load_vector_store()

# Streamlit header
st.set_page_config(page_title="Co:Chat - An LLM-powered chat bot")
st.title("Sheraton-Bot")
st.write("This is a chatbot for a specific Hotel (Knowledge base is limited to Sheraton Hotel and can be customized)")

# laoding styles.css
def load_css():
    with open("static/styles.css", "r")  as f:
        css = f"<style>{f.read()} </style>"
        st.markdown(css, unsafe_allow_html = True)



def initialize_session_state() :
    
    # Initialize a session state to track whether the initial message has been sent
    if "initial_message_sent" not in st.session_state:
        st.session_state.initial_message_sent = False

    # Initialize a session state to store the input field value
    if "customer_prompt" not in st.session_state:
        st.session_state.customer_prompt = ""

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
        prompt = """ You are an AI assistant for Sheraton Grand Bengaluru Whitefield Hotel & Convention Center in Whitefield, Bengaluru, and you will only answer queries related to this hotel using the provided documents under the keyword `documents:`. Your primary goal is to help customers with information and booking assistance: when a user indicates they’d like to book a room, sequentially collect their full name, check-in date, check-out date, number of guests, room type (e.g., Deluxe Room, Executive Room), and any additional services (e.g., airport shuttle, spa, breakfast), asking one question at a time rather than all at once. Once you have all details, summarize the booking in a clear, formatted way and ask for confirmation—if the customer confirms, state that the booking is confirmed; if they decline, cancel the booking and restart the process. If you don’t know the answer to a question, reply “I’m not sure about that,” and if a question falls outside the context of Sheraton Whitefield, respond with “I am tuned to only answer queries related to Sheraton Grand Bengaluru Whitefield.” Stay professional, friendly, and helpful at all times."""

        st.session_state.chat_history.append({"role": "User", "message": prompt})
        st.session_state.chat_history.append({"role": "Chatbot", "message": "Yes understood, I will act accordingly, and will be polite, short and to the point."})


#Callblack function which when activated calls all the other
#functions 

def handle_button_click(prompt_text):
    st.session_state.customer_prompt = prompt_text
    on_click_callback()

def on_click_callback():

    load_css()
    customer_prompt = st.session_state.customer_prompt

    if customer_prompt:
        


        st.session_state.initial_message_sent = True

        with st.spinner('Generating response...'):  
            # Retrieve relevant documents
            retrieved_docs = get_relevant_docs(customer_prompt, db)
            context = "\n".join([doc.page_content for doc in retrieved_docs])

            # Prepare messages for the LLM, including chat history and new prompt
            messages = []
            # Add previous chat history to messages
            for chat_entry in st.session_state.chat_history:
                if chat_entry["role"] == "User":
                    messages.append(HumanMessage(content=chat_entry["message"]))
                elif chat_entry["role"] == "Chatbot":
                    messages.append(AIMessage(content=chat_entry["message"]))
            
            # Add the current context and question
            messages.append(HumanMessage(content=f"Context: {context}\n\nQuestion: {customer_prompt}"))
            llm_response = chat.invoke(messages)
            if "confirm booking" in customer_prompt.lower():
                summary = summarizer(st.session_state.chat_history)
                # print(summary)
                    # Add content to the sidebar
                st.sidebar.title("Summary")
                st.sidebar.write(summary)
                
        st.session_state.chat_history.append({"role": "User", "message": customer_prompt})
        st.session_state.chat_history.append({"role": "Chatbot", "message": llm_response.content})
        st.session_state.customer_prompt = "" # Clear the input box after processing

            

def main():

    initialize_session_state()
    chat_placeholder = st.container()
    prompt_placeholder = st.form("chat-form")

    with chat_placeholder:
        for chat in st.session_state.chat_history[2:]:
            if chat["role"] == "User":
                msg = chat["message"]
            else:
                msg = chat["message"]

            div = f"""
            <div class = "chatRow 
            {'' if chat["role"] == 'Chatbot' else 'rowReverse'}">
                <img class="chatIcon" src = "app/static/{'elsa.png' if chat["role"] == 'Chatbot' else 'admin.png'}" width=32 height=32>
                <div class = "chatBubble {'adminBubble' if chat["role"] == 'Chatbot' else 'humanBubble'}">&#8203; {msg}</div>
            </div>"""
            st.markdown(div, unsafe_allow_html=True)
            
        
    # Quick prompt buttons
    button_cols = st.columns(4)
    with button_cols[0]:
        st.button("Booking", on_click=handle_button_click, args=["I want to book a room."])
    with button_cols[1]:
        st.button("Check-in/Check-out", on_click=handle_button_click, args=["What are the check-in and check-out times?"])
    with button_cols[2]:
        st.button("Dining", on_click=handle_button_click, args=["What dining options are available?"])
    with button_cols[3]:
        st.button("Facilities", on_click=handle_button_click, args=["What facilities does the hotel offer?"])

    with st.form(key="chat_form"):
        cols = st.columns((6, 1))
        
        cols[0].text_input(
            "Chat",
            value=st.session_state.customer_prompt,
            label_visibility="collapsed",
            key="customer_prompt",
            placeholder="Hello, how can I assist you?"
        )
        cols[1].form_submit_button(
            "Ask",
            type="secondary",
            on_click=on_click_callback,
        )





if __name__ == "__main__":
    main()




