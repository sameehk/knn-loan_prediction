# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y2XRvjJW5a4kbRgL891-hs9gzhreg1sk
"""

# -*- coding: utf-8 -*-
"""Copy of loan_prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iaIlsnfyx17nHwVNd6hP7YUAQ7iRVVa_
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# Load the loan dataset (assuming it's in a CSV file)
loan_data = pd.read_csv('/content/trainloan.csv')

# Preprocess the data
# Drop irrelevant columns or those with missing values
#loan_data = loan_data.drop(['Loan_ID'], axis=1)
loan_data = loan_data.dropna()
#missing_values = loan_data.isnull().sum()
#print(missing_values)
loan_data.to_csv('trained.csv', index=False)

loan_data = pd.read_csv('/content/trained.csv')
# Convert categorical variables to numerical using label encoding
label_encoder = LabelEncoder()

loan_data['Loan_ID'] = loan_data['Loan_ID'].astype('category').cat.codes.astype(float)


loan_data['Gender'] = label_encoder.fit_transform(loan_data['Gender'])
loan_data['Married'] = label_encoder.fit_transform(loan_data['Married'])
loan_data['Education'] = label_encoder.fit_transform(loan_data['Education'])
loan_data['Self_Employed'] = label_encoder.fit_transform(loan_data['Self_Employed'])
loan_data['Property_Area'] = label_encoder.fit_transform(loan_data['Property_Area'])

# One-hot encode categorical variables
loan_data = pd.get_dummies(loan_data, columns=['Dependents', 'Credit_History'])
loan_data['ApplicantIncome'] = (loan_data['ApplicantIncome'] - loan_data['ApplicantIncome'].mean()) / loan_data['ApplicantIncome'].std()
loan_data['CoapplicantIncome'] = (loan_data['CoapplicantIncome'] - loan_data['CoapplicantIncome'].mean()) / loan_data['CoapplicantIncome'].std()
loan_data['LoanAmount'] = (loan_data['LoanAmount'] - loan_data['LoanAmount'].mean()) / loan_data['LoanAmount'].std()

# Split the dataset into training and testing sets
X = loan_data.drop('Loan_Status', axis=1)
y = loan_data['Loan_Status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the KNN classifier
knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = knn_classifier.predict(X_test)
print(y_pred)

test_data = pd.read_csv('/content/testloan.csv')

# Preprocess the data
# Drop irrelevant columns or those with missing values
#test_data = test_data.drop(['Loan_ID'], axis=1)
#test_data = test_data.dropna()
test_data.to_csv('tested.csv', index=False)

test_data = pd.read_csv('/content/tested.csv')
predicted=test_data['Loan_ID']
missing_values = test_data.isnull().sum()
print(missing_values)



#loan_id_mapping = {index: Loan_ID for index, Loan_ID in enumerate(test_data['Loan_ID'])}
test_data['Loan_ID'] = test_data['Loan_ID'].astype('category').cat.codes.astype(float)
# Convert categorical variables to numerical using label encoding
label_encoder = LabelEncoder()

#test_data['Loan_ID'] = test_data['Loan_ID'].astype('category').cat.codes.astype(float)
#loan_id_mapping = dict(zip(test_data['Loan_ID'], test_data['Loan_ID'].astype(str)))
test_data['Gender'] = label_encoder.fit_transform(test_data['Gender'])
test_data['Married'] = label_encoder.fit_transform(test_data['Married'])
test_data['Education'] = label_encoder.fit_transform(test_data['Education'])
test_data['Self_Employed'] = label_encoder.fit_transform(test_data['Self_Employed'])
test_data['Property_Area'] = label_encoder.fit_transform(test_data['Property_Area'])

# One-hot encode categorical variables
test_data = pd.get_dummies(test_data, columns=['Dependents', 'Credit_History'])
test_data['ApplicantIncome'] = (test_data['ApplicantIncome'] - test_data['ApplicantIncome'].mean()) / loan_data['ApplicantIncome'].std()
test_data['CoapplicantIncome'] = (test_data['CoapplicantIncome'] - test_data['CoapplicantIncome'].mean()) / loan_data['CoapplicantIncome'].std()
test_data['LoanAmount'] = (test_data['LoanAmount'] - test_data['LoanAmount'].mean()) / loan_data['LoanAmount'].std()

imputer = SimpleImputer(strategy='mean')

# Impute missing values with mean
test_data['Gender'] = imputer.fit_transform(test_data[['Gender']])
test_data['Self_Employed'] = imputer.fit_transform(test_data[['Self_Employed']])
test_data['LoanAmount'] = imputer.fit_transform(test_data[['LoanAmount']])
test_data['Loan_Amount_Term'] = imputer.fit_transform(test_data[['Loan_Amount_Term']])

predictions = knn_classifier.predict(test_data)
test_data['Loan_Status'] = predictions
output_data = pd.DataFrame({'Loan_ID': predicted, 'Loan_Status': predictions})
# Save the test data with the predicted values to a new CSV file
output_data.to_csv('output.csv', index=False)
# Print the predictions
print(predictions)