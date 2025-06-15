import tkinter as tk
from tkinter import scrolledtext

# -------------------- Chatbot Logic --------------------

def chatbot_response(user_input):
    user_input = user_input.lower()

    # Expanded responses
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"
    elif "order status" in user_input or "track" in user_input:
        return "Please provide your order ID to check the status."
    elif "refund" in user_input:
        return "To initiate a refund, please visit the 'My Orders' section and select the item."
    elif "cancel" in user_input:
        return "You can cancel your order from your account dashboard within 24 hours of purchase."
    elif "support" in user_input or "help" in user_input:
        return "Our support team is available 24/7. Please describe your issue."
    elif "thank you" in user_input or "thanks" in user_input:
        return "You're welcome! I'm here if you need anything else."
    elif "payment failed" in user_input:
        return "If your payment failed, please try again or use a different payment method."
    elif "delivery time" in user_input or "when will i receive" in user_input:
        return "Standard delivery time is 3-5 business days depending on your location."
    elif "change address" in user_input:
        return "You can change your shipping address in your profile settings before the order is shipped."
    elif "working hours" in user_input:
        return "Our support team is available 24/7, including weekends."
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase your question?"

# -------------------- GUI Application --------------------

def send_message():
    user_msg = user_input.get()
    if user_msg.strip() == "":
        return

    chat_area.insert(tk.END, "You: " + user_msg + "\n", "user")
    response = chatbot_response(user_msg)
    chat_area.insert(tk.END, "Bot: " + response + "\n\n", "bot")
    user_input.delete(0, tk.END)
    chat_area.see(tk.END)

# Create main window
window = tk.Tk()
window.title("Customer Support Chatbot")
window.geometry("600x600")
window.config(bg="black")

# Heading
heading_label = tk.Label(window, text="Customer Support", font=("Arial", 24, "bold"), bg="black", fg="cyan")
heading_label.pack(pady=10)

# Create chat display area
chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 13), bg="black", fg="white")
chat_area.place(relx=0.05, rely=0.12, relwidth=0.9, relheight=0.65)
chat_area.config(state='normal')

# Styling chat messages
chat_area.tag_config("user", foreground="lightgreen")
chat_area.tag_config("bot", foreground="cyan")

# Input frame
input_frame = tk.Frame(window, bg="black")
input_frame.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.1)

user_input = tk.Entry(input_frame, font=("Arial", 14))
user_input.place(relwidth=0.75, relheight=1)

send_button = tk.Button(input_frame, text="Send", font=("Arial", 14), bg="#4CAF50", fg="white", command=send_message)
send_button.place(relx=0.77, relwidth=0.22, relheight=1)

window.mainloop()
