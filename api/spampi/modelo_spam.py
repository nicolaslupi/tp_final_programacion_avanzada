import pickle

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


class ModeloSpam(object):
    def __init__(self, transform_entrenado, pca_entrenado, svm_entrenado):
        self.tfidf = transform_entrenado
        self.pca = pca_entrenado
        self.svm = svm_entrenado
        
    def predict_email(self, text):
        transf_text = self.tfidf.transform([text])
        transf_dense = transf_text.todense()
        pca_text = self.pca.transform(transf_dense)
        return self.svm.best_estimator_.predict(pca_text)

    def save_spam_model(self, out_path='.', out_name='trained_spam_model'):
        """Save the full model object in a pickle.
        Args:
            out_path (str, optional): Path to save pickled model.
                Defaults to '.'.
            out_name (str, optional): Name to save pickled model.
                Defaults to 'stacked-ensemble'.
        """
        with open(f'{out_path}/{out_name}.pkl', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_spam_model(in_path='.', in_name='trained_spam_model'):
        """Static method to load a previously-saved pickeld model.
        Usage for this is as follow:
        my_new_stacked = StackedEnsembleModel.load_stacker(...)
        Args:
            in_path (str, optional): Path for saved pickled model.
                Defaults to '.'.
            in_name (str, optional): Name for saved pickled model.
                Defaults to 'stacked-ensemble'.
        Returns:
            [type]: [description]
        """
        with open(f'{in_path}/{in_name}.pkl', 'rb') as f:
            return pickle.load(f)