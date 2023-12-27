import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64
import sqlite3
import cv2
import numpy as np
import os
import io
user_images_folder = "user_images"
os.makedirs(user_images_folder, exist_ok=True)
def create():
    

    with st.form('Student From',clear_on_submit=False):
        roll_no=st.text_input('Enter your roll_no').lower()
        name=st.text_input('Enter your name').lower()
        branch=st.text_input('Enter your branch').lower()
        location=st.text_input('Enter your loaction').lower()
        phone_no=st.text_input('Enter your phone')
        user_img=st.file_uploader('Upload your image',type=['png','jpeg','jpg'])
        st.info(f'''
        When multiple faces are present in the image, the person on the left side is considered. 
        Ensure the image is clear for accurate identification.
        ''')
        submitted=st.form_submit_button('Submit')
        
        if submitted:
            keys_length=prime_length()
            if not roll_no:
                st.warning('Roll number missing!',icon='🚨')
            elif roll_no in keys_length :
                st.warning('Unique Roll Number Required!', icon='🔄')
            elif not phone_no:
                st.warning('Phone number missing!',icon='🚨')
            elif len(phone_no)!=10:
                st.warning(f'''
                Phone number must have 10 digits.
                Ensure a valid 10-digit phone number is provided.
                ''',icon='🚨')
            elif phone_no.isdigit()!=True:
                st.warning("Phone numbers are digits, not alphabets! 📞 No ABCDs here! 😄")
            elif not user_img:
                st.warning('Image is missing',icon='📷')
           
            elif user_img:
              pic2=Image.open(user_img)
              image_np2 = np.array(pic2)
              faces=user_image_checking(image_np2)
              if len(faces)<1:
                st.warning(f'''
                            Oops! No face detected in the image! 
                            🤔 Try uploading a photo with a clear view of the face. 📸
                            ''')
                st.text('Your image')
                st.image(user_img)
              else:
                pic2=Image.open(user_img)
                image_np2 = np.array(pic2)
                faces=user_image_checking(image_np2)
                
                faces=faces[0]
                x, y, w, h = faces
                top_increase = 20
                bottom_increase = 20

                expanded_y = max(0, y - top_increase)
                expanded_h = h + top_increase + bottom_increase

                # Crop and expand the image
                
                
                image_np2 = image_np2[expanded_y:expanded_y + expanded_h, x:x+w]


                # Define the image file path using the roll number
                img_filename = f"{roll_no}.png"
                img_path = os.path.join(user_images_folder, img_filename)

                # Save the image as a PNG file
                Image.fromarray(image_np2).save(img_path)
                with open(f"user_images/{roll_no}.png", "rb") as image_file:
                  # Read the content of the image file
                  image_data = image_file.read()

                image_bytes_io = io.BytesIO(image_data)
                us_img = image_bytes_io.read()
                

                
                col1,col2=st.columns(2)
                with col1:
                  st.text('Your Image')
                  st.image(user_img)
                with col2:
                  st.text('Cropped Image')
                  st.image(image_np2)
                

                   
                
                insert(roll_no,name,branch,location,phone_no,us_img)
                
                


def user_image_checking(img):
  
  gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
  faces = face_cascade.detectMultiScale(gray_img,1.3,5)
  return faces

  pass


def insert(roll_no,name,branch,location,phon_no,user_img):
    conn=sqlite3.connect('vitap.db')
    data=[(roll_no,name,branch,location,phon_no,user_img)]
    query="""
    insert into vitap2 values(?,?,?,?,?,?);
    """
    try:
        c=conn.executemany(query,data)
        st.success('Data Successfully Inserted! 🚀')
        st.balloons()
    except Exception as e:
        st.write(e)
    conn.commit()
    conn.close()

def prime_length():
    conn=sqlite3.connect('vitap.db')
    query='select roll_number from vitap2'
    names_list=[i[0] for i in conn.execute(query)]
    conn.commit()
    conn.close()
    return names_list

def names_list():
    conn=sqlite3.connect('vitap.db')
    query='select name from vitap2'
    roll_list=[i[0] for i in conn.execute(query)]
    conn.commit()
    conn.close()
    return roll_list

def branch_list():
    conn=sqlite3.connect('vitap.db')
    query='select branch from vitap2'
    br_list=[i[0] for i in conn.execute(query)]
    conn.commit()
    conn.close()
    return br_list

def locations_list():
    conn=sqlite3.connect('vitap.db')
    query='select location from vitap2'
    loc_list=[i[0] for i in conn.execute(query)]
    conn.commit()
    conn.close()
    return loc_list

def ph_list():
    conn=sqlite3.connect('vitap.db')
    query='select phone_no from vitap2'
    phone_list=[i[0] for i in conn.execute(query)]
    conn.commit()
    conn.close()
    return phone_list



def retrieve_user_image():
    conn=sqlite3.connect('vitap.db')
    query='select user_img from vitap2;'
    result=[i[0] for i in conn.execute(query)]
    conn.commit()
    conn.close()
    return result    
    
def display_user_image():
    results=retrieve_user_image()
    #images=[Image.open(BytesIO(byte_data)) for byte_data in results]
    
    return results

    
def read():
    result=checking()
    if result==0:
        st.warning('Database Empty! 🕵️‍♂️✨')
    else:

        roll_numbers=prime_length()
        names=names_list()
        branches_list=branch_list()
        location=locations_list()
        phone=ph_list()
        im_list=display_user_image()
        data={
            'Roll Number':roll_numbers,
            'Name':names,
            'Branch':branches_list,
            'Location':location,
            'Phone Number':phone
            
            
            
        }
        


        st.dataframe(data)
        
        # Allow the user to click on the hyperlink to view the image
        selected_index = st.selectbox("Select an index to view the image", roll_numbers) 
        position=roll_numbers.index(selected_index)
        if st.button("🖼️ View Selected Image"):
            st.text(f"Image for Roll Number: {roll_numbers[position]}")
            st.image(im_list[position])
def checking():
    conn = sqlite3.connect('vitap.db')  # Replace 'your_database.db' with your actual database file
    cursor = conn.cursor()
    query='select count(*) from vitap2'
    cursor.execute(query)
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result[0]

def update():
    choices=['Name','Branch','Location','Phone Number']
    options=st.selectbox('Select the filed to update',choices)
    if options=='Name':
        st.info('Enter your roll number exactly as displayed on the read page! 📝')
        rno=st.text_input('Enter your roll_no').lower()
        keys_length=prime_length()
        bt1=st.button('Submit')
        if st.session_state.get('button') != True:
            st.session_state['button'] = bt1
        if st.session_state['button'] == True:
        
            if rno not in keys_length:
                st.warning('🚨 Roll Number Incorrect! 😱')
            else:
                conn=sqlite3.connect('vitap.db')
                query='select name from vitap2 where roll_number = ?;'
                old_name=[i[0] for i in conn.execute(query,(rno,))]
                conn.commit()
                conn.close()
                st.success('🔑 Roll Number Correct! 🎉')
                new_name=st.text_input('Enter new name')
                if st.button('Update'):
                    st.session_state['button'] = False
                    st.success(updated_new_name_funcion(new_name,rno))
                    st.balloons()
                    st.write('Old Name: {}'.format(old_name[0]))
                    st.write('New Name: {}'.format(new_name))

    elif options=='Branch':
        st.info('Enter your roll number exactly as displayed on the read page! 📝')
        rno=st.text_input('Enter your roll_no').lower()
        keys_length=prime_length()
        bt1=st.button('Submit')
        if st.session_state.get('button') != True:
            st.session_state['button'] = bt1
        if st.session_state['button'] == True:
        
            if rno not in keys_length:
                st.warning('🚨 Roll Number Incorrect! 😱')
            else:
                conn=sqlite3.connect('vitap.db')
                query='select branch from vitap2 where roll_number = ?;'
                old_branch=[i[0] for i in conn.execute(query,(rno,))]
                conn.commit()
                conn.close()
                st.success('🔑 Roll Number Correct! 🎉')
                new_branch=st.text_input('Enter new branch')
                if st.button('Update'):
                    st.session_state['button'] = False
                    st.success(updated_new_branch_funcion(new_branch,rno))
                    st.balloons()
                    st.write('Old branch: {}'.format(old_branch[0]))
                    st.write('New branch: {}'.format(new_branch))

        
    elif options=='Location':
        st.info('Enter your roll number exactly as displayed on the read page! 📝')
        rno=st.text_input('Enter your roll_no').lower()
        keys_length=prime_length()
        bt1=st.button('Submit')
        if st.session_state.get('button') != True:
            st.session_state['button'] = bt1
        if st.session_state['button'] == True:
        
            if rno not in keys_length:
                st.warning('🚨 Roll Number Incorrect! 😱')
            else:
                conn=sqlite3.connect('vitap.db')
                query='select location from vitap2 where roll_number = ?;'
                old_location=[i[0] for i in conn.execute(query,(rno,))]
                conn.commit()
                conn.close()
                st.success('🔑 Roll Number Correct! 🎉')
                new_location=st.text_input('Enter new location')
                if st.button('Update'):
                    st.session_state['button'] = False
                    st.success(updated_new_location_function(new_location,rno))
                    st.balloons()
                    st.write('Old location: {}'.format(old_location[0]))
                    st.write('New location: {}'.format(new_location))
    elif options=='Phone Number':
        st.info('Enter your roll number exactly as displayed on the read page! 📝')
        rno=st.text_input('Enter your roll_no').lower()
        keys_length=prime_length()
        bt1=st.button('Submit')
        if st.session_state.get('button') != True:
            st.session_state['button'] = bt1
        if st.session_state['button'] == True:
        
            if rno not in keys_length:
                st.warning('🚨 Roll Number Incorrect! 😱')
            else:
                conn=sqlite3.connect('vitap.db')
                query='select phone_no from vitap2 where roll_number = ?;'
                old_phone_no=[i[0] for i in conn.execute(query,(rno,))]
                conn.commit()
                conn.close()
                st.success('🔑 Roll Number Correct! 🎉')
               
                new_phone_no=st.text_input('Enter your new  phone number')

                 
                if st.button('Update'):
                  st.session_state['button'] = False
                  st.success(updated_new_phone_no_function(new_phone_no,rno))
                  st.balloons()
                  st.write('Old Phone number: {}'.format(old_phone_no[0]))
                  st.write('New Phone number: {}'.format(new_phone_no))


        
   
    

def updated_new_name_funcion(new_name,rno):
    conn=sqlite3.connect('vitap.db')
    query='update vitap2 set name = ? where roll_number = ?;'
    conn.execute(query,(new_name,rno))
    conn.commit()
    conn.close()
    return f'📝 Record Updated! 💻'

def updated_new_branch_funcion(new_branch,rno):
    conn=sqlite3.connect('vitap.db')
    query='update vitap2 set branch = ? where roll_number = ?;'
    conn.execute(query,(new_branch,rno))
    conn.commit()
    conn.close()
    return f'📝 Record Updated! 💻'

def updated_new_location_function(new_location,rno):
    conn=sqlite3.connect('vitap.db')
    query='update vitap2 set location = ? where roll_number = ?;'
    conn.execute(query,(new_location,rno))
    conn.commit()
    conn.close()
    return f'📝 Record Updated! 💻'

def updated_new_phone_no_function(new_phone_no,rno):
    conn=sqlite3.connect('vitap.db')
    query='update vitap2 set phone_no = ? where roll_number = ?;'
    conn.execute(query,(new_phone_no,rno))
    conn.commit()
    conn.close()
    return f'📝 Record Updated! 💻'

def delete():
    choices=['Location','Phone Number']
    options=st.selectbox('Select the feild to delete',choices)
    if options=='Location':
        st.info('Enter your roll number exactly as displayed on the read page! 📝')
        rno=st.text_input('Enter your roll_no').lower()
        keys_length=prime_length()
        bt1=st.button('Submit')
        if st.session_state.get('button') != True:
            st.session_state['button'] = bt1
        if st.session_state['button'] == True:
        
            if rno not in keys_length:
                st.warning('🚨 Roll Number Incorrect! 😱')
            else:
                conn=sqlite3.connect('vitap.db')
                
                st.success('🔑 Roll Number Correct! 🎉')
                if st.button('Delete'):
                    st.session_state['button'] = False
                    removed_item=''
                    
                    st.success(delete_location_function(removed_item,rno))
                    st.balloons()

    elif options=='Phone Number':
        st.info('Enter your roll number exactly as displayed on the read page! 📝')
        rno=st.text_input('Enter your roll_no').lower()
        keys_length=prime_length()
        bt1=st.button('Submit')
        if st.session_state.get('button') != True:
            st.session_state['button'] = bt1
        if st.session_state['button'] == True:
        
            if rno not in keys_length:
                st.warning('🚨 Roll Number Incorrect! 😱')
            else:
                conn=sqlite3.connect('vitap.db')
                
                st.success('🔑 Roll Number Correct! 🎉')
                if st.button('Delete'):
                    st.session_state['button'] = False
                    removed_item=''
                    
                    st.success(delete_phone_function(removed_item,rno))
                    st.balloons()



    


def delete_location_function(removed_item,rno):
    conn=sqlite3.connect('vitap.db')
    query='update vitap2 set location = ? where roll_number = ?;'
    d=conn.execute(query,(removed_item,rno))
    conn.commit()
    conn.close()
    return f'🗑️ Record Deleted! 💣'


def delete_phone_function(removed_item,rno):
    conn=sqlite3.connect('vitap.db')
    query='update vitap2 set phone_no = ? where roll_number = ?;'
    d=conn.execute(query,(removed_item,rno))
    conn.commit()
    conn.close()
    return f'🗑️ Record Deleted! 💣'




