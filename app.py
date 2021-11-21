# import basic libraries
import numpy as np
import streamlit as st
import cv2
from deepface import DeepFace as dfc
from PIL import Image
import os

# function to load image
try:
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
except Exception:
    st.write("Error loading cascade classifiers")

@st.cache
def face_detect(img):
    img = np.array(img.convert("RGB"))
    face = face_cascade.detectMultiScale(image=img)

    # draw rectangle around face
    for (x, y, w, h) in face:
        cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
        roi = img[y:y + h, x:x + w]
    return img, face

# analyze image
def analyze_image(img):
    prediction = dfc.analyze(img_path=img)
    return prediction

#function for webcam
def detect_web(image):

    faces = face_cascade.detectMultiScale(
        image=image, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img=image, pt1=(x, y), pt2=(
            x + w, y + h), color=(255, 0, 0), thickness=2)

    return image, faces


def main():
    # Face Analysis Application #
    st.title("Face Detection and Analysis Application")
    activiteis = ["Home", "Analyze Face", "About"]
    choice = st.sidebar.selectbox("Select Activity", activiteis)
    st.sidebar.markdown(
        """ Developed by Vivek     
            Checkout complete project  
            [here] (https://github.com/7Vivek/Face-detection-analysis)""")
    # C0C0C0
    if choice == "Home":
        html_temp_home1 = """<div style="background-color:#6D7B8D;padding:10px">
                                            <h4 style="color:white;text-align:center;">
                                            Face detection and Face feature analysis application using OpenCV, DeepFace and Streamlit.</h4>
                                            </div>
        st.image('https://freepngimg.com/download/keyboard/6-2-keyboard-png-file.png',use_column_width=True)
                                            </br>"""
        st.markdown(html_temp_home1, unsafe_allow_html=True)
        st.write("""
                 The application has two functionalities.
                 
                 1. Face feature analysis such as emotion, gender, age and race.""")
    elif choice == "Analyze Face":
        st.subheader("Analyze facial features such as emotion, age, gender and race.")
        image_file = st.file_uploader("Upload image you want to analyze", type=['jpg', 'png', 'jpeg'])

        if image_file is not None:
            #read image using PIL
            image_loaded = Image.open(image_file)
            #detect faces in image
            result_img, result_face = face_detect(image_loaded)
            st.image(result_img, use_column_width=True)
            st.success("found {} face\n".format(len(result_face)))

            if st.button("Analyze image"):
                # convert image to array
                new_image = np.array(image_loaded.convert('RGB'))
                img = cv2.cvtColor(new_image, 1)
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                #analyze features of face
                result = analyze_image(img)
                # st.write(result)
                st.write("Analysis summary")
                st.write("Face emotion is ", result["dominant_emotion"], "in image.")
                st.write("Gender recognized as", result["gender"], "in image.")
                st.write("Age is", result["age"], "years.")
            else:
                pass
                #st.write("Click on Analyze image ")

    elif choice == "About":
        st.subheader("About this app")
        html_temp_about1= """<div style="background-color:#6D7B8D;padding:10px">
                                    <h4 style="color:white;text-align:center;">
                                    Face detection and Face feature analysis application using OpenCV, DeepFace and Streamlit.</h4>
                                    </div>
                                    </br>"""
        st.markdown(html_temp_about1, unsafe_allow_html=True)

        html_temp4 = """
                             		<div style="background-color:#98AFC7;padding:10px">
                             		<h4 style="color:white;text-align:center;">This Application is developed by Mohammad Juned Khan using Streamlit Framework, Opencv and DeepFace library for demonstration purpose. If you're on LinkedIn and want to connect, just click on the link in sidebar and shoot me a request. If you have any suggestion or wnat to comment just write a mail at Mohammad.juned.z.khan@gmail.com. </h4>
                             		<h4 style="color:white;text-align:center;">Thanks for Visiting</h4>
                             		</div>
                             		<br></br>
                             		<br></br>"""

        st.markdown(html_temp4, unsafe_allow_html=True)

    else:
        pass

if __name__ == '__main__':
    main()
