import html
from bs4 import BeautifulSoup
from gensim.parsing.porter import PorterStemmer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')


class Preprocessor():
    def __init__(self, df, type=None) -> None:
        if type == "train":
            df['fraudulent'] = df['fraudulent'].apply(
                lambda x: 1 if x == "t" else 0)
            
        df['feature'] = df['feature'].str.lower()
        df['feature'] = df['feature'].apply(self.__remove_html_tags_and_escape_chars)
        self.raw_text = ' '.join(df['feature'].astype(str))
        df['feature'] = df['feature'].apply(self.__remove_non_alpha)
        df['feature'] = df['feature'].apply(lambda x: word_tokenize(x.lower()))
        all_stopwords = set(stopwords.words('english'))
        df['feature'] = df['feature'].apply(
            lambda x: [word for word in x if word not in all_stopwords])
        df['feature'] = df['feature'].apply(
            lambda x: [PorterStemmer().stem(word) for word in x])
        df['feature'] = df['feature'].apply(
            lambda x: [word for word in x if len(word) >= 3])
        df['feature'] = df['feature'].apply(lambda x: ' '.join(x))
        df = df[df['feature'] != '']
        self.df = df
        
    def __remove_html_tags_and_escape_chars(self, input_text):
        # Remove HTML tags
        text_without_html = BeautifulSoup(input_text, 'html.parser').get_text()

        # Unescape HTML characters
        text_without_escape_chars = html.unescape(text_without_html)

        return text_without_escape_chars
    
    def __remove_non_alpha(self, input_text):
        return ''.join(char if char.isalpha() or char.isspace() else ' ' for char in input_text)
