import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from imblearn.combine import SMOTETomek
from imblearn.pipeline import make_pipeline
from constants import ModelsConst

# modelling
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from src.ml.preprocess_worker import Preprocessor


class TrainingWorker(Preprocessor):
    def __init__(self) -> None:
        df = pd.read_csv('src/datasets/emscad_v1.csv')
        df = df[['description', 'requirements',
                'benefits', 'fraudulent']].fillna('')
        df["feature"] = df['description'] + " " + \
            df['requirements'] + " " + df['benefits']
        df = df[['feature', 'fraudulent']]
        super().__init__(df, type="train")

    def train(self, model=ModelsConst.RANDOM_FOREST.value):
        df = self.df
        # make pipeline
        tfidf = TfidfVectorizer()
        svd = TruncatedSVD(n_components=350, random_state=42)
        norm = Normalizer(copy=False)
        smote = SMOTETomek(sampling_strategy='all', random_state=42)
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        pipe = make_pipeline(tfidf, svd, smote, norm, rf)
        x_train, _, y_train, _ = train_test_split(
            df['feature'], df['fraudulent'], test_size=0.2, random_state=42, stratify=df['fraudulent'])
        pipe.fit(x_train, y_train)
        joblib.dump(pipe, f'src/models/{model}.pkl')


if __name__ == "__main__":
    worker = TrainingWorker()
    worker.train()
