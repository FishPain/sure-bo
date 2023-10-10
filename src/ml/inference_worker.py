import joblib
import numpy as np
import pandas as pd
from lime import lime_text
from typing import List, Tuple, Dict
from constants import ModelsConst
from src.ml.download_helper import download_asset
from src.ml.preprocess_worker import Preprocessor

class InferenceWorker(Preprocessor):
    def __init__(self, data: Dict) -> None:
        self.is_model_downloaded = download_asset()

        df = pd.DataFrame(data, index=[0])
        columns_to_check = ["description", "requirements", "benefits"]
        missing_columns = [col for col in columns_to_check if col not in df.columns]
        for col in missing_columns:
            df[col] = np.nan

        df = df[["description", "requirements", "benefits"]].fillna("")
        super().__init__(df, type="inference")
        self.x_text = df["feature"]

    def predict(self, model: str = ModelsConst.RANDOM_FOREST.value) -> List[int]:
        if self.is_model_downloaded == False:
            raise Exception(f"Model not downloaded, please download it manually from \
                            https://github.com/FishPain/sure-bo/releases/download/v0.1.0/{model}.pkl")

        self.model = joblib.load(f"src/models/{model}.pkl")
        self.pred = self.model.predict(self.x_text)
        return self.pred

    def explain(self) -> List[Tuple]:
        # Create a LIME explainer
        try:
            explainer = lime_text.LimeTextExplainer(class_names=["fraudulent", "not-fraudulent"])
            exp = explainer.explain_instance(self.x_text[0], self.model.predict_proba)
            self.exp = exp.as_list()

        except Exception as e:
            print(f"Unable to generate explainability due to: {e}")

        return self.exp
