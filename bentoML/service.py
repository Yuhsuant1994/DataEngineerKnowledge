from __future__ import annotations
import numpy as np
import uuid
from typing import Any, AsyncGenerator, Dict, TypedDict, Union
import typing as t

from langchain.chains import LLMChain
from langchain_community.llms import OpenLLM
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

import bentoml
from bentoml.io import NumpyNdarray, Image, PandasDataFrame, JSON, Text

# Define runners for both Iris Classifier and YOLOv5
iris_clf_runner = bentoml.sklearn.get("iris_clf:latest").to_runner()


# Create a single service instance with all runners
svc = bentoml.Service('combined_service', runners=[iris_clf_runner])

# Example input for the Iris Classifier
example_input = np.array([[5.9, 3, 5.1, 1.8]])

# Iris Classifier API
@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def classify(input_series: np.ndarray = example_input) -> np.ndarray:
    result = iris_clf_runner.predict.run(input_series)
    return result
