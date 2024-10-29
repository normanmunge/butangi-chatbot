import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st


#### Loading Data and Preprocessing Data

with open('data.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')

# Tokenize the text into sentences
sentences = sent_tokenize(data)


# Define function to preprocess each sentence
def preprocess(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    # Remove stopwords and punctuation
    words = [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation]
    
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    
    words = [lemmatizer.lemmatize(word) for word in words]
    
    return words

# Preprocess each sentence in the text
corpus = [preprocess(sentence) for sentence in sentences]


# Function to find the most relevant sentence in a query
def get_most_relevant_sentence(query):
    # Preprocess the query
    query = preprocess(query)
    
    # Compute the similarity between the query and each sentence in the text
    max_similarity = 0 
    most_relevant_sentence = ''
    
    for sentence in corpus:
        similarity = len(set(query).intersection(sentence)) / float(len(set(query).union(sentence)))
        
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = ' '.join(sentence)
            
    return most_relevant_sentence

def chatbot(question):
    # Find the most relevant sentence in the text
    most_relevant_sentence = get_most_relevant_sentence(question)
    
    # Return the answer
    return most_relevant_sentence


# Create a streamlit app

def main():
    st.title("Chatbot")
    st.write("Hello, I'm Butangi - the M.H.S Alumni chatbot. How can I help you today?")
    
    # Get the user's question
    question = st.text_input("Question:")
    
    # Create a button to submit the question
    if st.button('Ask'):
        response = chatbot(question)
        
        st.write('Chatbot: ' + response)
        

if __name__ == '__main__':
    main()
        