# -*- coding: utf-8 -*-
"""Cancer2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NSQ7jRo6z11nnAzbLbQCHLtFI-GK66Bg

1) Setting up Libraries
"""

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

"""2) Mount google drive"""

from google.colab import drive
drive.mount("/content/drive")

cancer = pd.read_csv('/content/drive/MyDrive/cancer_classifications.csv')
cancer.head()

print(cancer.head())
print(cancer.info())

# Step 2: Preprocess the Data
# Split the data into features and target variable
X = cancer.drop('benign_0__mal_1', axis=1)
y = cancer['benign_0__mal_1']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 3: Select and Train Classifiers
classifiers = {
    'Decision Tree': DecisionTreeClassifier(),
    'SVM': SVC(),
    'k-NN': KNeighborsClassifier(),
    'Naive Bayes': GaussianNB()
}

# Train and evaluate each classifier
results = {}
for name, clf in classifiers.items():
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    classification_report_str = classification_report(y_test, y_pred)
    confusion_matrix_array = confusion_matrix(y_test, y_pred)
    results[name] = {
        'accuracy': accuracy,
        'classification_report': classification_report_str,
        'confusion_matrix': confusion_matrix_array
    }
    print(f"{name} Classifier:")
    print("Accuracy:", accuracy)
    print("Classification Report:\n", classification_report_str)
    print("Confusion Matrix:\n", confusion_matrix_array)
    print("\n")

# @title
# Step 5: Evaluate and Compare Classifiers
# Plotting accuracy for each classifier
accuracies = {name: result['accuracy'] for name, result in results.items()}
plt.bar(accuracies.keys(), accuracies.values())
plt.xlabel('Classifiers')
plt.ylabel('Accuracy')
plt.title('Classifier Performance Comparison')
plt.xticks(rotation=45)
plt.show()

new_data = np.array([
    [13.45, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781, 0.1885, 0.05766],
    [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871]
])

# Preprocess the new data using the same scaler
new_data_scaled = scaler.transform(new_data)

# Predict using the best-performing classifier (e.g., SVM)
best_classifier = classifiers['SVM']
prediction = best_classifier.predict(new_data_scaled)

# Output the predictions
prediction_labels = ['Malignant' if pred == 1 else 'Benign' for pred in prediction]
print(f'The predictions for the new data points are: {prediction_labels}')

# Create the scatter plot with color based on species
sns.scatterplot(
    data=cancer,
    x="mean radius",
    y="mean concavity",
    hue="benign_0__mal_1",
    palette="BuPu",  # Choose a color palette from seaborn
)

# Add title and labels
plt.title("Mean Radius vs Mean Concavity by Malignancy")
plt.xlabel("Mean Radius (mm)")
plt.ylabel("Mean Concavity (mm)")

# Show the plot
plt.show()