import numpy as np
import pandas as pd

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from imblearn.combine import SMOTETomek
from imblearn.pipeline import make_pipeline
from gensim.parsing.porter import PorterStemmer
from constants import ModelsConst

# modelling
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')


class TrainingWorker():
    def __init__(self) -> None:
        df = pd.read_csv('src/datasets/emscad_v1.csv')
        df = df[['description', 'requirements',
                 'benefits', 'fraudulent']].fillna('')
        df["feature"] = df['description'] + " " + \
            df['requirements'] + " " + df['benefits']
        df['feature'] = df['feature'].str.lower()
        # remove html tags and word that start with & and \
        df['feature'] = df['feature'].str.replace(r'<[^>]*>', '')
        df['feature'] = df['feature'].str.replace(r'&[^;]*;', '')
        df['feature'] = df['feature'].str.replace(r'\\[a-z]*', '')
        # remove punctuation
        df['feature'] = df['feature'].str.replace(r'[^\w\s]', '')
        # remove digits
        df['feature'] = df['feature'].str.replace(r'\d+', '')
        # remove whitespace
        df['feature'] = df['feature'].str.replace(r'\s+', ' ')
        df['feature'] = df['feature'].apply(lambda x: word_tokenize(x.lower()))
        df = df[['feature', 'fraudulent']]
        # remove stopwords
        all_stopwords = set(stopwords.words('english'))
        all_stopwords.update(['\\r\\n'])
        df['feature'] = df['feature'].apply(
            lambda x: [word for word in x if word not in all_stopwords])
        # stem words
        df['feature'] = df['feature'].apply(
            lambda x: [PorterStemmer().stem(word) for word in x])
        df['feature'] = df['feature'].apply(
            lambda x: [word for word in x if len(word) >= 3])
        df['feature'] = df['feature'].apply(lambda x: ' '.join(x))
        df = df[df['feature'] != '']
        df['fraudulent'] = df['fraudulent'].apply(
            lambda x: 1 if x == "t" else 0)
        self.df = df

    def train(self, model=ModelsConst.RANDOM_FOREST.value):
        df = self.df
        # make pipeline
        tfidf = TfidfVectorizer()
        svd = TruncatedSVD(n_components=350, random_state=42)
        norm = Normalizer(copy=False)
        smote = SMOTETomek(sampling_strategy='all', random_state=42)
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        pipe = make_pipeline(tfidf, svd, norm, smote, rf)
        x_train, _, y_train, _ = train_test_split(
            df['feature'], df['fraudulent'], test_size=0.2, random_state=42, stratify=df['fraudulent'])
        pipe.fit(x_train, y_train)
        joblib.dump(pipe, f'src/models/{model}.pkl')


if __name__ == "__main__":
    worker = TrainingWorker()
    worker.train()
