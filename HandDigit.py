import numpy as np
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageDraw, ImageOps
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
import os

# -------------------- Step 1: Train CNN Model --------------------
def train_model():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255
    x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    model = Sequential([
        Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.1)
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print(f'Test accuracy: {test_acc:.4f}')
    model.save('digit_cnn_model.h5')
    print('Model trained and saved successfully.')

if not os.path.exists('digit_cnn_model.h5'):
    train_model()

model = load_model('digit_cnn_model.h5')

# -------------------- Step 2: GUI with Drawing Canvas --------------------
class DigitRecognizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Draw a Digit to Recognize")
        master.geometry("400x500")

        self.label = Label(master, text="Draw a Digit Below", font=("Arial", 16))
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(master, width=280, height=280, bg='white')
        self.canvas.pack()

        self.image = Image.new("L", (280, 280), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind('<B1-Motion>', self.draw_lines)

        self.predict_button = Button(master, text="Predict Digit", command=self.predict_digit, font=("Arial", 14))
        self.predict_button.pack(pady=10)

        self.clear_button = Button(master, text="Clear", command=self.clear_canvas, font=("Arial", 14))
        self.clear_button.pack(pady=5)

        self.result_label = Label(master, text="", font=("Arial", 20))
        self.result_label.pack(pady=20)

    def draw_lines(self, event):
        x, y = event.x, event.y
        r = 8  # Brush size
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black', outline='black')
        self.draw.ellipse([x - r, y - r, x + r, y + r], fill='black')

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, 280, 280], fill='white')
        self.result_label.config(text="")

    def predict_digit(self):
        img = self.image.resize((28, 28))
        img = ImageOps.invert(img)
        img_array = np.array(img)

        # Blank check: if all pixels are white (inverted -> black)
        if np.sum(img_array) == 0:
            self.result_label.config(text="Please draw any digit...")
            return

        img_array = img_array.astype('float32') / 255
        img_array = img_array.reshape(1, 28, 28, 1)

        prediction = model.predict(img_array)
        digit = np.argmax(prediction)

        self.result_label.config(text=f"Predicted Digit: {digit}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = DigitRecognizerApp(root)
    root.mainloop()
