# PapersGPT

1. Upload a PDF, one containing text.
2. An LLM will summarise it for you.
3. Ask questions about it.
4. Enjoy!

## How to use
[Here](https://papers-gpt.riju.tech/)

## Installation
1. Clone the repo
2. Run `poetry install`
3. Run `streamlit run --browser.gatherUsageStats false src/main.py`

## Privacy and Security
TLDR: I don't store anything.

Your PDF file is deleted from the server when you close the app.

None of your data is stored. Your PDF file is not stored, the generated summary is not stored, the questions you ask are not stored, the answers the LLM gives you are not stored.