from sklearn import linear_model
from sklearn import svm
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures, LabelEncoder
from sklearn.pipeline import make_pipeline
import numpy
import pandas as pd

df = pd.read_csv("iris.csv")
inputData = df[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]].values
# inputData = inputData[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]].apply(pd.to_numeric())
print(inputData)

outputData = df["Species"]
# print(outputData)

le = LabelEncoder()
outputEncoded = le.fit_transform(outputData)
# print(outputEncoded)

model = svm.SVC()
model.fit(inputData, outputEncoded)
predicted = model.predict([[6, 3, 1.8, 0.4], [6.4, 2.7, 4.1, 1.5]])
predictedSpecies = le.inverse_transform(predicted)
print(predictedSpecies)
