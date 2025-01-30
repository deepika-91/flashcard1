import fitz  # PyMuPDF for PDF text extraction
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Global variables for login
users = {"admin": "password123"}  # Example user data

def signup():
    """Signup window."""
    def register():
        username = user_entry.get()
        password = pass_entry.get()
        if username and password:
            users[username] = password
            messagebox.showinfo("Success", "Account created! Please login.")
            signup_window.destroy()
        else:
            messagebox.showerror("Error", "Fields cannot be empty")
    
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry("350x250")
    
    tk.Label(signup_window, text="Username:", font=("Arial", 12)).pack()
    user_entry = tk.Entry(signup_window, font=("Arial", 12))
    user_entry.pack()
    
    tk.Label(signup_window, text="Password:", font=("Arial", 12)).pack()
    pass_entry = tk.Entry(signup_window, show="*", font=("Arial", 12))
    pass_entry.pack()
    
    tk.Button(signup_window, text="Sign Up", font=("Arial", 12), command=register).pack()

def login():
    """Login function."""
    username = user_entry.get()
    password = pass_entry.get()
    if username in users and users[username] == password:
        messagebox.showinfo("Success", "Login successful!")
        root.destroy()
        open_main_app()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def select_pdf():
    file_path = filedialog.askopenfilename(title="Select a PDF", filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        text_box.delete("1.0", tk.END)
        text = extract_text_from_pdf(file_path)
        text_box.insert(tk.END, text)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "".join(page.get_text("text") for page in doc)
    return text

def summarize_text():
    full_text = text_box.get("1.0", tk.END)
    summary = "\n".join(full_text.split("\n")[:15])
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, summary)

def save_flashcards_pdf():
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], title="Save Flashcards PDF")
    if save_path:
        summary = text_box.get("1.0", tk.END)
        create_flashcards_pdf(summary, save_path)
        messagebox.showinfo("Success", f"Flashcards saved to {save_path}")

def create_flashcards_pdf(summary, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    y_position = 750
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Summary:")
    y_position -= 20
    c.setFont("Helvetica", 10)
    for line in summary.split("\n"):
        c.drawString(50, y_position, line[:300])
        y_position -= 20
    c.save()

def open_main_app():
    global text_box
    main_window = tk.Tk()
    main_window.title("PDF Summarizer")
    main_window.geometry("600x600")
    
    # Background Image
    bg_image = Image.open("milky-way-2695569_1280.jpg")
    bg_image = bg_image.resize((600, 600), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(main_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    
    tk.Label(main_window, text="Select a PDF to summarize:", font=("Arial", 14), bg="black", fg="white").pack(pady=10)
    tk.Button(main_window, text="Select PDF", font=("Arial", 12), command=select_pdf).pack(pady=5)
    
    text_box = tk.Text(main_window, height=15, width=60, font=("Arial", 12))
    text_box.pack(pady=10)
    
    tk.Button(main_window, text="Summarize", font=("Arial", 12), command=summarize_text).pack(pady=5)
    tk.Button(main_window, text="Save as Flashcards PDF", font=("Arial", 12), command=save_flashcards_pdf).pack(pady=5)
    
    deviation_label = tk.Label(main_window, text="Deviation from full text: Calculating...", font=("Arial", 12), bg="black", fg="white")
    deviation_label.pack(pady=10)
    
    def calculate_deviation():
        full_text = text_box.get("1.0", tk.END)
        summary_text = text_box.get("1.0", tk.END)
        full_length = len(full_text.split())
        summary_length = len(summary_text.split())
        deviation = ((full_length - summary_length) / full_length) * 100 if full_length > 0 else 0
        deviation_label.config(text=f"Deviation from full text: {deviation:.2f}%")
    
    tk.Button(main_window, text="Calculate Deviation", font=("Arial", 12), command=calculate_deviation).pack(pady=5)
    
    main_window.mainloop()

# Login UI
root = tk.Tk()
root.title("Login")
root.geometry("350x250")

bg_image = Image.open("https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569_1280.jpg")
bg_image = bg_image.resize((350, 250), Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

tk.Label(root, text="Username:", font=("Arial", 12), bg="black", fg="white").pack()
user_entry = tk.Entry(root, font=("Arial", 12))
user_entry.pack()

tk.Label(root, text="Password:", font=("Arial", 12), bg="black", fg="white").pack()
pass_entry = tk.Entry(root, show="*", font=("Arial", 12))
pass_entry.pack()

tk.Button(root, text="Login", font=("Arial", 12), command=login).pack(pady=5)
tk.Button(root, text="Sign Up", font=("Arial", 12), command=signup).pack()

root.mainloop()
