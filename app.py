import os
import google.generativeai as genai
import streamlit as st
from pdfextractor import text_extractor
from wordextractor import doc_text_extract
from image2text import extract_text_image

# Lets Configure genai model
gemini_key = os.getenv('Google-API-Key3')
genai.configure(api_key= gemini_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite', 
                              generation_config= {'temperature': 0.9})

# Lets create the sidebar

st.sidebar.title('UPLOAD YOUR NOTES:')
st.sidebar.subheader('Only upload Image, PDFs and DOCX')
user_file = st.sidebar.file_uploader('Upload here:', type=['pdf', 'docx',
                                                             'png', 'jpg', 'jpeg',
                                                             'jfif'])

if user_file:
    st.sidebar.success('File Uploaded Successfully')
    if user_file.type == 'application/pdf':
        user_text = text_extractor(user_file)
    elif user_file.type in ['image/png', 'image/jpeg', 'image/jpg',
                            'image/jfif']:
        user_text = extract_text_image(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml':
        user_text = doc_text_extract(user_file)
    else:
        st.sidebar.error('Enter the correct file type')


# lets create the main pages

st.title(':orange[MOM Generator:-] :blue[AI Assisted Minutes of Meeting Generator.]')
st.subheader(':violet[This application creates generalized minutes of meeting from ]')
st.write('''
Follow the steps:
1.Upload the notes in PDF,DOCX or Image format in sidebar.
2.Click "generate" to generate the MOM.''')

if st.button('Generate'):
    with st.spinner("Please Wait....."):
        prompt=f'''
        <Role> You are an expert in writing and formating minutes of meetings.
        <Goal> Create minutes of meetings from the notes that user has provided.
        <Context> The user has provided some rough notes as text..Here are the notes: {user_text}
        <Format> The Output must follow the below format:
        * Title: Assume title of the meeting.
        * Agenda: Assume agenda of the meeting.
        * Attendees: Name of the attendees (If name of the attendees is not there keep it NA)
        * Date and Place: Date and the place of the meeting (If not provided, keep it Online)
        * Body: The body should follow the following sequence of points -
            * Key points discussed.
            * Highlight any decision that has been taken. 
            * Mention Actionable Items.
            * Mention any deadline if discussed. 
            * Mention next meeting date if discussed.
            * Add a 2-3 line of summary.
        
        <Instruction>
        * Do not add any of your own words in the output.
        * Use bullet points and highlight the important keywords by making them bold.
        * Generate the output in docx format.'''

        response = model.generate_content(prompt)
        st.write(response.text)

    if st.download_button(
        label= 'DOWNLOAD',
        data = response.text,
        file_name= 'mom_generated.txt',
        mime = 'text/plain'):
        st.success('Your File Has Been Downloaded')


