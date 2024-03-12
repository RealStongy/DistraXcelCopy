from sklearn import linear_model
from sklearn.linear_model import Ridge

from sklearn.preprocessing import PolynomialFeatures

from sklearn.pipeline import make_pipeline
import numpy

'''
input_data = numpy.array([9, 10, 11, 12, 13, 14, 15, 16]).reshape(8, 1)

output_data = [0, 10, 20, 30, 40, 30, 20, 10]

model = linear_model.LinearRegression()

model.fit(input_data, output_data)

# print(model.predict([[11.5], [15.2]]))
'''

input_data = numpy.array([[1], [2], [3], [4], [5], [6], [7], [8]]).reshape(-1, 1)

output_data = [0, 10, 20, 30, 40, 30, 20, 10]

model = make_pipeline(PolynomialFeatures(2), Ridge())

model.fit(input_data, output_data)

if (model.predict([[7.5]]) <= 0):
    print(0)
else:
    print(model.predict([[7.5]]))