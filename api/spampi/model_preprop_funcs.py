import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import string
string.punctuation
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
nltk.download('punkt')
import re

stopwords_english = stopwords.words('english')
stopwords_english.pop( stopwords_english.index('re') ) # Saco 're' de stopwords

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN) # Por default devuelve sustantivo
lemmatizer = WordNetLemmatizer()

def lemmatize(word):
    lemmatized = lemmatizer.lemmatize(word, get_wordnet_pos(word)) # Lemmatizacion flexible (según POS)
    return lemmatized

def remove_basura(mail):
    sin_basura = re.sub('(Subject|[\W_\d])', ' ', mail) # Saco números, puntuación, etc. y la palabra subject
    sin_basura = re.sub(' [a-zA-Z] ', ' ', sin_basura) # Saco letras sueltas (a, s, t...)
    sin_basura = re.sub(' {2,}', ' ', sin_basura) # Saco espaciado de sobra
    sin_basura = re.sub('^\s', '', sin_basura) # Saco el primer espacio de cada oracion
    return sin_basura

def prune_words(mail):
    tokens = nltk.word_tokenize( remove_basura(mail), language='english' ) # Tokenizo (equivale al join de vicky)
    lemmatized_not_stopword = [lemmatize(token.lower()) for token in tokens if token.lower() not in stopwords_english] # OJO que stopwords incluye 're', aca la saque
    return lemmatized_not_stopword