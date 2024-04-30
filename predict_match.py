import src.predict_match_outcome as pred
import tkinter as tk

def process_input():
    input_text = entry.get()
    output_text = pred.predict_match_outcome(input_text)
    output_label.config(text=output_text)

# Create the main window
window = tk.Tk()
window.title("CS2 Match Predictor")

# Add a sentence above the entry field
sentence_label = tk.Label(window, text="What is the ID of the match you want to predict?")
sentence_label.pack()

# Set window size and position
window.geometry("400x200")  # width x height
window.resizable(False, False)  # prevent resizing

# Add padding around widgets
window.configure(padx=20, pady=20)

# Create input entry
entry = tk.Entry(window)
entry.pack(pady=10)

# Create a button to trigger the function
button = tk.Button(window, text="Calculate Match Outcome ", command=process_input)
button.pack()

# Create a label to display the output
output_label = tk.Label(window, text="")
output_label.pack(pady=10)

# Run the application
window.mainloop()