import os
import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

# Set download directory inside Streamlit's persistent storage
nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)

nltk.download("punkt", download_dir=nltk_data_dir)
nltk.download("stopwords", download_dir=nltk_data_dir)

# Tell NLTK to use this directory
nltk.data.path.append(nltk_data_dir)

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = text.split()


    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):

    
    transformed = transform_text(input_sms)
    vector = tfidf.transform([transformed]).toarray()
    result = model.predict(vector)
    st.write("Model output:", result)

    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
