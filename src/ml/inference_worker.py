import joblib
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lime import lime_text
from typing import List, Tuple, Dict

from constants import ModelsConst
from gensim.parsing.porter import PorterStemmer
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import Normalizer, MultiLabelBinarizer
from sklearn.decomposition import TruncatedSVD
from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')


class SMOTETomekTransformer(TransformerMixin):
    def __init__(self, **kwargs):
        self.smote_tomek = SMOTETomek(**kwargs)

    def fit(self, X, y):
        X_resampled, y_resampled = self.smote_tomek.fit_resample(X, y)
        return self

    def transform(self, X):
        return X


class InferenceWorker():
    def __init__(self, data: Dict) -> pd.DataFrame:
        """ preprocess data and return dataframe with features"""
        df = pd.DataFrame(data, index=[0])

        # Columns to check and add if missing
        columns_to_check = ['description', 'requirements', 'benefits']

        # Check if columns are missing
        missing_columns = [
            col for col in columns_to_check if col not in df.columns]

        # Add missing columns and fill with np.nan
        for col in missing_columns:
            df[col] = np.nan

        df = df[['description', 'requirements', 'benefits']].fillna('')
        df["feature"] = df['description'] + " " + \
            df['requirements'] + " " + df['benefits']
        df = df[['feature']]
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
        # tokenize
        df['feature'] = df['feature'].apply(lambda x: word_tokenize(x.lower()))
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
        self.x_text = df['feature']

    def predict(self, model: str = ModelsConst.RANDOM_FOREST.value) -> List[int]:
        self.model = joblib.load(f'src/models/{model}.pkl')
        self.pred = self.model.predict(self.x_text)
        return self.pred

    def explain(self) -> List[Tuple]:
        # Create a LIME explainer
        explainer = lime_text.LimeTextExplainer(
            class_names=["Non-Scam", "Scam"])

        exp = explainer.explain_instance(
            self.x_text[0], self.model.predict_proba)

        # Print or return the explanation
        self.exp = exp.as_list()
        return self.exp
