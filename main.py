import streamlit as st
from streamlit_option_menu import option_menu
from utils import create,display_user_image,read,update,delete

st.set_page_config(layout="wide",initial_sidebar_state="expanded",
                   page_icon='📝',page_title='Student Application Form')

# Define custom style for the glowing text
glowing_text_style = '''
    <style>
        .glowing-text {
            font-family: 'Arial Black', sans-serif;
            font-size: 40px;
            text-align: center;
            animation: glowing 2s infinite;
        }
        
        @keyframes glowing {
            0% { color: #FF9933; } /* Saffron color */
            20% { color: #FFC300; } /* Yellow color */
            40% { color: #FF5733; } /* Orange color */
            60% { color: #FF33E9; } /* Pink color */
            80% { color: #3369FF; } /* Blue color */
            100% { color: #128807; } /* Green color */
        }
    </style>
'''

# Display the glowing text using st.markdown
st.markdown(glowing_text_style, unsafe_allow_html=True)
st.markdown(f'<p class="glowing-text">📝 Student Application Form 📝</p>', unsafe_allow_html=True)

with st.sidebar:
    selected=option_menu(
        menu_title='App Gallery',
        options=['Create','Read','Update','Delete'],
        default_index=0,
        icons=['patch-plus','binoculars-fill','pencil-fill','trash'],
        menu_icon='view-stacked',
        
        orientation='vertical'
    )
if __name__=="__main__":

    if selected=='Create':
        

      
        create()
    elif selected=='Read':
        
        read()

        pass
    elif selected=='Update':
        update()
        pass
    elif selected=='Delete':
        delete()
