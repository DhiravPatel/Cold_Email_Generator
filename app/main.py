import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    user_name = st.text_input("Enter your name:", "Dhirav")
    # st.markdown("Please upload your portfolio CSV containing tech stack and links. This step is optional.")
    # uploaded_file = st.file_uploader("Upload your portfolio CSV (Optional)", type=["csv"])
    url_input = st.text_input("Enter a URL to scrape:")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            # if uploaded_file:
            #     portfolio.load_portfolio(uploaded_file)
            # else:
            #     portfolio.data = None 
            portfolio.data = None
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills) if portfolio.data is not None else []
                email = llm.write_mail(job, links, user_name)
                st.code(email, language='markdown')
                return
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
