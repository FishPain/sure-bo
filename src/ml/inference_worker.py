import joblib
import os
import numpy as np
import pandas as pd
from lime import lime_text
from typing import List, Tuple, Dict
from constants import ModelsConst
from src.ml.preprocess_worker import Preprocessor

class InferenceWorker(Preprocessor):
    def __init__(self, data: Dict) -> None:
        df = pd.DataFrame(data, index=[0])
        columns_to_check = ["description", "requirements", "benefits"]
        missing_columns = [col for col in columns_to_check if col not in df.columns]
        for col in missing_columns:
            df[col] = np.nan
    
        df = df[["description", "requirements", "benefits"]].fillna("")
        df["feature"] = df['description'] + " " + \
            df['requirements'] + " " + df['benefits']
        df = df[['feature']]

        super().__init__(df, type="inference")
        self.x_text = self.df["feature"]
    
    def __is_model_exist(self, model=ModelsConst.RANDOM_FOREST.value):

        directory_path = f"src/models/{model}.pkl"

        if os.path.exists(directory_path):
            print(f"The file {model}.pkl exists in the directory {directory_path}.")
            return True
        else:
            print(f"The file {model}.pkl does not exist in the directory {directory_path}.")
            return False


    def predict(self, model: str = ModelsConst.RANDOM_FOREST.value) -> List[int]:
        if self.__is_model_exist() == False:
            raise Exception(f"Model not downloaded, please download it manually from https://github.com/FishPain/sure-bo/releases/download/v0.1.0/{model}.pkl. Or run sure-bo in a docker container by running ./docker-start.sh")
        
        self.model = joblib.load(f"src/models/{model}.pkl", mmap_mode='r')
        self.pred = self.model.predict(self.x_text)
        return self.pred

    def explain(self):
        explainer = lime_text.LimeTextExplainer(class_names=["fraudulent", "not-fraudulent"])
        exp = explainer.explain_instance(self.x_text[0], self.model.predict_proba)
        self.exp = exp.as_list()
        return self.exp, self.raw_text
