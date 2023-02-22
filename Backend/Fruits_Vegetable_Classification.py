import streamlit as st
from PIL import Image
from flask import Flask, request, jsonify
from keras_preprocessing.image.utils import load_img, img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import fruit_data
# fruit_data.data is array of dictory which has "name" key. match that data and retrn whole dictonary  

model = load_model('FV.h5')
labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
          7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
          14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
          26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
          32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple', 'Banana', 'Bello Pepper', 'Chilli Pepper', 'Grapes', 'Jalepeno', 'Kiwi', 'Lemon', 'Mango', 'Orange',
          'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']
vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger',
              'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato',
              'Tomato', 'Turnip']

app = Flask(__name__)
CORS(app)


def processed_img(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()


def getData(name):
    for d in fruit_data.data:
        if(d["name"]==name): 
            return d
        


@app.route('/')
def index():
    return "Hello world"

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    # st.title("Fruits🍍-Vegetable🍅 Classification")
    # img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
    if file is not None:
        print("Non none")
        # img = Image.open(img_file).resize((250, 250))
        # st.image(img, use_column_width=False)
        save_image_path = file.name
        with open(save_image_path, "wb") as f:
            f.write(file.getbuffer())

        # if st.button("Predict"):
        if file is not None:
            print(save_image_path)
            result = processed_img(save_image_path)
            print(result)
            if result in vegetables:
                cat = "Vegetables"
                st.info('**Category : Vegetables**')
            else:
                cat = "Fruit"
                st.info('**Category : Fruit**')
            st.success("**Predicted : " + result + '**')
        return jsonify({'Category': cat, 'Name': result, "data": getData(result)})


if __name__ == '__main__':
    # test(CORSRequestHandler, HTTPServer, port=int(8000))
    app.run(debug=True)
