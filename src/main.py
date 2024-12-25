import os
from tempfile import NamedTemporaryFile
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from loguru import logger
from markitdown import MarkItDown
from langchain_ollama import ChatOllama



def get_ollama_llm(
        model_name: str = "qwen2.5-coder:14b",
        # model_name: str = "gemma2",
        temperature: float = 0.8,
    ):
    llm = ChatOllama(
        model=model_name,
        temperature=temperature,
        base_url=os.getenv('OLLAMA_URL'),  # Set the remote server URL
    )
    return llm


def get_markdown_from_pdf(pdf_file_path):
    md = MarkItDown()
    result = md.convert(pdf_file_path)
    return result.text_content

def ask_llm(llm, query):
    response = llm.stream(f'{query}\nAnswer in 100 words or less.')
    return response

def rm_pdf_4m_sess():
    for key in st.session_state.keys():
        if key in st.session_state:
            del st.session_state[key]


def main():
    st.set_page_config(page_title=os.getenv("APP_NAME"))
    st.title(os.getenv("APP_NAME"))
    def chat_callback():
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        user_input = st.session_state.user_input
        logger.info(f'user_input: {user_input}')
        message = {
            "role": "user",
            "content": user_input,
        }
        st.session_state.messages.append(message)
        response_msg = {
            "role": "assistant",
            "content": ask_llm(
                st.session_state.llm,
                f'{st.session_state.mkdwn_4m_pdf}\nQuestion: {user_input}',
            ),
        }
        st.session_state.messages.append(response_msg)


    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PDF file", type="pdf", on_change=rm_pdf_4m_sess)

    if uploaded_file is None:
        return
    # Read the PDF file
    if 'pdf_file_b' not in st.session_state:
        st.session_state.pdf_file_b = uploaded_file.getvalue()
    pdf_viewer(st.session_state.pdf_file_b, height=900)

    
    with NamedTemporaryFile(prefix=f'{os.getenv("APP_NAME")}_', delete=True) as _tf:
        _tf.write(uploaded_file.getvalue())

        if 'mkdwn_4m_pdf' not in st.session_state:
            logger.debug(f'{_tf.name}')
            st.session_state.mkdwn_4m_pdf = get_markdown_from_pdf(_tf.name)
        
        if 'llm' not in st.session_state:
            st.session_state.llm = get_ollama_llm()
        llm = st.session_state.llm
        
        if 'general_paper_summary' not in st.session_state:
            st.session_state.general_paper_summary = ask_llm(llm, st.session_state.mkdwn_4m_pdf)

        response_placeholder = st.empty()
        if 'gen_ppr_summ' not in st.session_state:
            gen_ppr_summ = ""
            for chunk in st.session_state.general_paper_summary:
                gen_ppr_summ += chunk.content  # Append each chunk to the response text
                response_placeholder.markdown(gen_ppr_summ)
                st.session_state.gen_ppr_summ = gen_ppr_summ
        else:
            response_placeholder.markdown(st.session_state.gen_ppr_summ)



        st.chat_input(
            "Ask a question about the paper",
            on_submit=chat_callback,
            key='user_input',
        )
        if 'messages' not in st.session_state:
            return
        
        for idx, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                # Handle rendering of generator, even tho Streamlit handles it automatically
                # but the string needs to be saved back to the message for continuity
                msg = message["content"]
                # check if msg is a generator
                if isinstance(msg, str):
                    st.write(msg)
                else:
                    ai_res_plchldr = st.empty()
                    ai_response = ""
                    for chunk in msg:
                        ai_response += chunk.content  # Append each chunk to the response text
                        ai_res_plchldr.write(ai_response)
                    st.session_state.messages[idx]["content"] = ai_response



if __name__ == "__main__":
    main()