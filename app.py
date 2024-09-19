import streamlit as st 
from scraper import scrape_product_data

def load_questions(file):
    from io import StringIO
    questions_file = StringIO(file.read().decode("utf-8"))
    questions = questions_file.readlines()
    return [q.strip() for q in questions]

def format_response(section_name, data):
    formatted_response = f"**{section_name}:**\n"
    headings = data.get('Headings', '').split('\n')
    details = data.get('Details', '').split('\n')
    
    if headings[0] == 'Headings not found':
        headings = []
    if details[0] == 'details not found':
        details = []
    
    for i in range(max(len(headings), len(details))):
        heading = headings[i] if i < len(headings) else ""
        detail = details[i] if i < len(details) else ""
        if heading or detail:
            formatted_response += f"- **{heading}**: {detail}\n"
    return formatted_response.strip()

def answers(questions, formatted_data):
    section_map = {
        'controlled remotely': 'Remote Control',
        'scheduling features': 'Scheduling Features',
        'security features': 'Security Features',
        'dimensions': 'Dimensions',
        'design': 'Design Features'
    }
    
    responses = []
    for question in questions:
        response_parts = []
        for key, section in section_map.items():
            if key in question.lower():
                data = formatted_data.get(section, {'Headings': 'Headings not found', 'Details': 'Details not found'})
                response_parts.append(format_response(section, data))
        
        combined_response = "\n".join(response_parts) if response_parts else "Sorry, I don't have relevant information to answer the question."
        responses.append((question, combined_response))
    
    return responses

def main():
    st.title("AI Sales Agent")
    
    url = st.text_input("Enter the product website URL", "https://www.tp-link.com/in/home-networking/smart-plug/hs100/")
    
    uploaded_file = st.file_uploader("Upload the questions text file", type="txt",key="uploaded_file")
    
    if st.button("Scrape Data"):
        if uploaded_file is not None:
            with st.spinner("Scraping data..."):
                try:
                    formatted_data = scrape_product_data(url)
                    st.success("Successfully scraped the product data!")
                    
                    questions = load_questions(uploaded_file)
                    responses = answers(questions, formatted_data)
                    
                    st.subheader("Responses:")
                    for question,response in responses:
                        st.markdown(f'**{question}**')
                        st.markdown(f'{response}')
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload the question file")

if __name__ == "__main__":
    main()