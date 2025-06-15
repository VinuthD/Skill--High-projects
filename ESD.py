import pandas as pd
import numpy as np
import string
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import messagebox

# -------------------- Model Training --------------------

# Load Dataset
url = 'https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv'
data = pd.read_table(url, header=None, names=['label', 'message'])

# Preprocess Text
def preprocess(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    return text

data['cleaned_message'] = data['message'].apply(preprocess)

# Feature Extraction
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['cleaned_message'])
y = data['label'].map({'ham': 0, 'spam': 1})

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# -------------------- GUI Application --------------------

def predict_email():
    email_text = text_input.get("1.0", tk.END)
    processed_text = preprocess(email_text)
    vector = vectorizer.transform([processed_text])
    prediction = model.predict(vector)[0]
    
    if prediction == 1:
        result = "Spam Email"
    else:
        result = "Not Spam Email"
    
    messagebox.showinfo("Prediction Result", result)

window = tk.Tk()
window.title("Spam Email Classifier")
window.geometry("500x400")

label = tk.Label(window, text="Enter Email Text:", font=("Arial", 14))
label.pack(pady=10)

text_input = tk.Text(window, height=10, width=50, font=("Arial", 12))
text_input.pack(pady=10)

predict_button = tk.Button(window, text="Predict", command=predict_email, font=("Arial", 14), bg="lightblue")
predict_button.pack(pady=10)

window.mainloop()
