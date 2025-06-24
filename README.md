# Hotel Concierge Bot

## Overview

This project implements a RAG-enabled chatbot tailored for Hotels, leveraging Streamlit for the user interface and OpenRouter for LLM integration. The chatbot provides information, handles inquiries, and assists with booking processes, including conversation summarization.

## Features

- **Retrieval-Augmented Generation (RAG):** Utilizes a custom knowledge base (`hotel_data.txt`) and FAISS vector store for context-aware responses.
- **Conversational Flow:** Guides users through a step-by-step booking process.
- **Conversation Summarization:** Summarizes booking details for confirmation, formatted for billing.
- **Quick Prompt Buttons:** Provides pre-defined buttons for common queries (e.g., "Booking", "Check-in/Check-out", "Dining", "Facilities").
- **Clear Chat Input:** Automatically clears the chat input field after submission for a smoother user experience.
- **LLM Integration:** Configured to use the `mistralai/mistral-7b-instruct:free` model via OpenRouter.

## Project Structure

```
.env
.gitignore
.streamlit/
├── config.toml
└── secrets.toml
README.md
coChatMain.py
faiss_index/
├── index.faiss
└── index.pkl
hotel_data.txt
rag_utils.py
requirements.txt
static/
├── admin.png
├── elsa.png
└── styles.css
summarization.py
```

- **`coChatMain.py`**: The main application file, handling the Streamlit UI, chat logic, and integration with RAG and summarization.
- **`summarization.py`**: Contains the `summarizer` function responsible for generating structured summaries of booking conversations.
- **`rag_utils.py`**: Manages the creation and loading of the FAISS vector store from `hotel_data.txt`.
- **`hotel_data.txt`**: The text file containing the hotel-specific information used to build the knowledge base.
- **`requirements.txt`**: Lists all Python dependencies required for the project.
- **`.streamlit/secrets.toml`**: Stores the OpenRouter API key securely.
- **`static/`**: Contains static assets like CSS and images.

## Getting Started

### Prerequisites

- Python 3.8+
- An OpenRouter API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sujay0610/hotel-concierge-bot.git
   cd sheraton-bot
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ./venv/Scripts/activate  # On Windows
   source venv/bin/activate # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key:**
   Create a `.streamlit` directory in the project root if it doesn't exist.
   Inside `.streamlit`, create a `secrets.toml` file and add your OpenRouter API key:
   ```toml
   OPENROUTER_API_KEY="your_openrouter_api_key_here"
   ```

### Running the Chatbot

To launch the Streamlit application locally, run:

```bash
streamlit run coChatMain.py
```

Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Usage

- Type your queries into the chat input field and press Enter or click the "Ask" button.
- Use the quick prompt buttons above the chatbar for common topics.
- Confirm booking details to see the summarization feature in action.

## Customization

- **Hotel Data:** Modify `hotel_data.txt` to update the hotel information. Remember to rebuild the vector store by running `coChatMain.py`.
- **Prompts:** Adjust the system prompts in `coChatMain.py` to change the chatbot's persona or behavior.
- **LLM Model:** Change the `model` parameter in `ChatOpenAI` initialization in `coChatMain.py` and `summarization.py` to use a different model available on OpenRouter.

## Deployment

This application can be deployed to Streamlit Cloud or other platforms that support Streamlit applications. Ensure your `secrets.toml` is properly configured for the deployment environment.

## Conclusion

This project provides a robust foundation for building intelligent, context-aware chatbots using RAG and Streamlit. Feel free to explore, customize, and extend its functionalities. Contributions and feedback are welcome!

Happy coding!

