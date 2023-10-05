import streamlit as st
import numpy as np
import cv2
from  PIL import Image, ImageEnhance 
from PIL.ImageFilter import *
from io import BytesIO
import streamlit.components.v1 as com

# Adding a header and expander in side bar
st.sidebar.markdown('<h1 class="font" style="text-align: center;">Picaso</h1>', unsafe_allow_html=True)
with st.sidebar.expander("About the App"):
     st.write("""
        Use this simple app to convert your photos to a pencil sketch, a grayscale image, an image with blurring effect and many more..  \n  \n Hope you enjoy!
     """) 
col1, col2 = st.columns( [0.6, 0.4])
with col1:               # To display the header text using css style
   # st.markdown(streamlit_style,unsafe_allow_html=True)
   st.write("""
   <style>
   @import url('https://fonts.googleapis.com/css2?family=Croissant+One&display=swap');
   .big-font {
      font-size: 100px !important;
      font-family: 'Croissant One', cursive;
      color: #FF9633;
      text-align: center;
      
   }
   </style>
   """, unsafe_allow_html=True)
   st.write('<p class="big-font">PICASO</p>', unsafe_allow_html=True)
with col2:               # To display an animation
   com.iframe("https://lottie.host/?file=f0852c29-bd00-4c14-8677-f979ab9d3653/7VAR1qPn30.json")
st.markdown(""" <style> .font {
font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
</style> """, unsafe_allow_html=True)
st.markdown('<p class="font">Play with your images in here......</p>', unsafe_allow_html=True)
st.markdown("---")
uploaded_file = st.file_uploader("Upload your image files here...", type=['png', 'jpeg', 'jpg'])

if uploaded_file:
   image = Image.open(uploaded_file)
   # new_image = img.resize((400, 400))
   # st.image(image)
   converted_img = image
   col1, col2 = st.columns( [0.5, 0.5])
   with col1:
      st.markdown('<p style="text-align: center;">Without Filter</p>',unsafe_allow_html=True)
      st.image(image,width=300)  

   with col2:
      st.markdown('<p style="text-align: center;">With Filter</p>',unsafe_allow_html=True)
      filter = st.sidebar.radio('FILTERS:', ['Original','Gray Image','Black and White', 'Pencil Sketch', 'Blur Effect', 'Edge Enhance', 'Smooth', 'Contour Detection','Viginette Effect'])
      if filter == 'Original':
                  converted_img = image
                  st.image(image,width=300) 
      elif filter == 'Gray Image':
                  img = np.array(image.convert('RGB'))
                  gray_scale = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                  st.image(gray_scale, width=300)
                  converted_img = Image.fromarray(gray_scale)
      elif filter == 'Black and White':
                  converted_img = np.array(image.convert('RGB'))
                  gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                  slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
                  (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
                  converted_img = Image.fromarray(blackAndWhiteImage)
                  st.image(blackAndWhiteImage, width=300)
      elif filter == 'Pencil Sketch':
                  converted_img = np.array(image.convert('RGB')) 
                  gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                  inv_gray = 255 - gray_scale
                  slider = st.sidebar.slider('Adjust the intensity', 25, 255, 125, step=2)
                  blur_image = cv2.GaussianBlur(inv_gray, (slider,slider), 0, 0)
                  sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
                  converted_img = Image.fromarray(sketch)
                  st.image(converted_img, width=300) 
      elif filter == 'Blur Effect':
                  converted_img = np.array(image.convert('RGB'))
                  slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2)
                  converted_img = cv2.cvtColor(converted_img, cv2.COLOR_RGB2BGR)
                  blur_image = cv2.GaussianBlur(converted_img, (slider,slider), 0, 0)
                  converted_img = Image.fromarray(blur_image)
                  st.image(blur_image, channels='BGR', width=300) 
      elif filter == 'Edge Enhance':
                  converted_img = image.filter(EDGE_ENHANCE_MORE)
                  st.image(converted_img, width=300)
      elif filter == 'Smooth':
                  converted_img = image.filter(SMOOTH_MORE)
                  st.image(converted_img, width=300)
      elif filter == 'Contour Detection':
                  converted_img = np.array(image.convert('RGB')) 
                  gray = cv2.cvtColor(converted_img, cv2.COLOR_BGR2GRAY)
                  #Now convert the grayscale image to binary image
                  ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                  #Now detect the contours
                  contours, hierarchy = cv2.findContours(binary, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
                  image_copy = converted_img.copy()
                  image_copy = cv2.drawContours(image_copy, contours, -1, (0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                  converted_img = Image.fromarray(image_copy)
                  st.image(image_copy, width=300)
      elif filter  == 'Viginette Effect':
                  img = np.array(image.convert('RGB')) 
                  rows, cols = img.shape[:2]
                  # radius = 130
                  value = 1
                  mask = np.zeros((int(rows*(value*0.1+1)),int(cols*(value*0.1+1))))
                  radius = st.sidebar.slider('Adjust the Radius', 700, 1500, 900, step=1)
                  value = st.sidebar.slider('Adjust the Focus', 1, 10, 1, step=1)
                  # cv2.namedWindow('Trackbars')
                  # cv2.createTrackbar('Radius', 'Trackbars', 130, 500, changeRadius)
                  # cv2.createTrackbar('Focus', 'Trackbars', 1, 10, changeFocus)
                  kernel_x = cv2.getGaussianKernel(int(cols*(0.1*value+1)),radius)
                  kernel_y = cv2.getGaussianKernel(int(rows*(0.1*value+1)),radius)
                  #rowsXcols
                  kernel = kernel_y * kernel_x.T

                  #Normalizing the kernel
                  kernel = kernel/np.linalg.norm(kernel)

                  #Genrating a mask to image
                  mask = 800 * kernel
                  output = np.copy(img)
                  mask_imposed = mask[int(0.1*value*rows):,int(0.1*value*cols):]
                  # applying the mask to each channel in the input image
                  for i in range(3):
                     output[:,:,i] = output[:,:,i] * mask_imposed
                  converted_img = Image.fromarray(output)
                  st.image(output,width=300)
   st.markdown('<h2 style="text-align: center;">Resizing</h2>',unsafe_allow_html=True)
   width = st.number_input("Width",value = converted_img.width)
   height = st.number_input("Height",value = converted_img.height)
   st.markdown('<h2 style="text-align: center;">Rotation</h2>',unsafe_allow_html=True)
   degree = st.number_input("Degree")
   col1, col2, col3 , col4, col5 = st.columns([0.2,0.2,0.2,0.2,0.2])
   with col1:
      pass
   with col2:
      pass
   with col4:
      pass
   with col5:
      pass
   with col3 :
      s_btn = st.button('Apply Changes')
   if s_btn:
         edited = converted_img.resize((width,height)).rotate(degree)
         st.image(edited)
         buf = BytesIO()
         edited.save(buf, format="JPEG")
         byte_im = buf.getvalue()
         col1, col2, col3 , col4, col5= st.columns([0.2,0.2,0.2,0.2,0.2])
         with col1:
            pass
         with col2:
            pass
         with col4:
            pass
         with col5:
            pass
         with col3 :
            btn = st.download_button(
               label="Download",
               data=byte_im,
               file_name="imagename.jpg",
               mime="image/jpeg",
               )
#Adding a feedback section in the sidebar
st.sidebar.title(' ') #Used to create some space between the filter widget and the comments section
st.sidebar.markdown(' ') #Used to create some space between the filter widget and the comments section
st.sidebar.markdown('<h1 style="text-align: center;">FEEDBACK</h1>', unsafe_allow_html=True)
with st.sidebar.form(key='columns_in_form',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
    rating=st.slider("Please rate the app", min_value=1, max_value=5, value=1,help='Drag the slider to rate the app. This is a 1-5 rating scale where 5 is the highest rating')
    text=st.text_input(label='Please leave your feedback here')
    submitted = st.form_submit_button('Submit')
    if submitted:
      st.write('Thanks for your feedback!')
      st.markdown('Your Rating:')
      st.markdown(rating)
      st.markdown('Your Feedback:')
      st.markdown(text) 
