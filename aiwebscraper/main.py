import streamlit as st
from scrape import scrape_website ,split_dom_content
from llm import deep_seek_ai
#         
st.title("AI Web Scrapper")
url =st.text_input("Enter a Website URL: ")


if st.button("Scrape"):
    st.write("Scraping the website...") 
    result =scrape_website(url)
    st.session_state.dom_content =result
    
    with st.expander("View DOM Content"):
        st.text_area("DOM Content",result, height=300)
        
  
  
parse_description = ""       
#if "DOM Content" in st.session_state:
parse_description = st.text_area("Describe what you want to parse")

if st.button("Parse Content"):
    if parse_description:
        st.write("Parsing the content...")
        # Parse the content with Ollama
        dom_chunks = split_dom_content(st.session_state.dom_content)
        st.write(dom_chunks)
        parsed_result = deep_seek_ai(dom_chunks, parse_description)
        
        st.write(parsed_result)