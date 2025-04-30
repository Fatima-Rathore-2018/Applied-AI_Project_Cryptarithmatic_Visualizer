import tkinter as tk
from tkinter import ttk, font
import random
from tkinter import messagebox

# class TreeView(tk.Frame):
#     def __init__(self, parent, **kwargs):
#         super().__init__(parent, **kwargs)
#         self.canvas = tk.Canvas(self, bg="#2D3436", highlightthickness=0)
#         self.canvas.pack(fill=tk.BOTH, expand=True)
        
#     def draw_tree(self, word1, word2, result):
#         self.canvas.delete("all")
        
#         # Draw the tree structure
#         # Root node
#         self.canvas.create_oval(300, 50, 400, 100, fill="#F9A826", outline="#E67E22")
#         self.canvas.create_text(350, 75, text=result, font=("Arial", 16, "bold"), fill="#2D3436")
        
#         # Lines to children
#         self.canvas.create_line(325, 100, 200, 150, width=2, fill="#F9A826")
#         self.canvas.create_line(375, 100, 500, 150, width=2, fill="#F9A826")
        
#         # Child nodes
#         self.canvas.create_oval(150, 150, 250, 200, fill="#26C485", outline="#1ABC9C")
#         self.canvas.create_text(200, 175, text=word1, font=("Arial", 16, "bold"), fill="white")
        
#         self.canvas.create_oval(450, 150, 550, 200, fill="#26C485", outline="#1ABC9C")
#         self.canvas.create_text(500, 175, text=word2, font=("Arial", 16, "bold"), fill="white")
        
#         # Add some leaf nodes for visual effect
#         for i in range(3):
#             x_offset = 150 + i * 50
#             self.canvas.create_line(200, 200, x_offset, 250, width=2, fill="#26C485")
#             self.canvas.create_oval(x_offset-25, 250, x_offset+25, 300, fill="#FFF9C4", outline="#26C485")
#             self.canvas.create_text(x_offset, 275, text=word1[i] if i < len(word1) else "?", font=("Arial", 14), fill="#2D3436")
            
#             x_offset = 450 + i * 50
#             self.canvas.create_line(500, 200, x_offset, 250, width=2, fill="#26C485")
#             self.canvas.create_oval(x_offset-25, 250, x_offset+25, 300, fill="#FFF9C4", outline="#26C485")
#             self.canvas.create_text(x_offset, 275, text=word2[i] if i < len(word2) else "?", font=("Arial", 14), fill="#2D3436")

class WordDisplay(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.text_area = tk.Text(self, bg="#3D4446", fg="#FFFFFF", font=("Arial", 18), wrap=tk.WORD, height=10)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.config(state=tk.DISABLED)  # Make it read-only


    def update_display(self, word1, word2):
        unique_letters = set(word1 + word2)
        
        # Clear previous text and tags
        self.text_area.config(state=tk.NORMAL)  # Enable editing to update text
        self.text_area.delete(1.0, tk.END)  # Clear previous text
        
        # Insert blank lines for padding
        self.text_area.insert(tk.END, "\n\n")  # Add a blank line for padding
        self.text_area.insert(tk.END, "\t\t\t\t Selected Words:\n ", "header")  # Insert header with tag
        self.text_area.insert(tk.END, "\n")  # Add another blank line for padding

        # Insert the display text with tags
        self.text_area.insert(tk.END, "\t\t\t\t WORD1:\n", "word1_label")
        self.text_area.insert(tk.END, f"\t\t\t\t\t {word1}\n", "word1")
        self.text_area.insert(tk.END, "\t\t\t\t WORD2:\n", "word2_label")
        self.text_area.insert(tk.END, f"\t\t\t\t\t {word2}\n\n", "word2")
        self.text_area.insert(tk.END, "\t\t\t\t Unique Letters: ", "uniqueLable")
        self.text_area.insert(tk.END, "\n \t\t\t\t\t", "unique_letters")  
        self.text_area.insert(tk.END, ', '.join(sorted(unique_letters)), "unique_letters")  
        
        self.text_area.config(state=tk.DISABLED)  # Make it read-only again

        # Define tags with colors
        self.text_area.tag_config("header", foreground="#85CFCB", font=("Arial", 16, "bold"))
        self.text_area.tag_config("word1_label", foreground="#85CFCB", font=("Arial", 14, "bold"))
        self.text_area.tag_config("word1", foreground="#EEE4B1", font=("Arial", 12))
        self.text_area.tag_config("word2_label", foreground="#85CFCB", font=("Arial", 14, "bold"))
        self.text_area.tag_config("word2", foreground="#EEE4B1", font=("Arial", 12))
        self.text_area.tag_config("uniqueLable", foreground="#85CFCB", font=("Arial", 14, "bold"))
        self.text_area.tag_config("unique_letters", foreground="#EEE4B1", font=("Arial", 12)) 
    

class VisualCryptaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VISUAL CRYPTA")
        self.root.configure(bg="#1C1C1C")  # Dark background
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#1C1C1C", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="VISUAL CRYPTA", 
                                font=("Arial", 28, "bold"), bg="#1C1C1C", fg="#F9A826")
        title_label.pack(pady=(5, 20))
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg="#1C1C1C")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Controls
        left_frame = tk.Frame(content_frame, bg="#1C1C1C", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Example frame
        example_frame = tk.LabelFrame(left_frame, text="Examples", 
                                       font=("Arial", 16, "bold"), bg="#1C1C1C", fg="#F9A826")
        example_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Example text
        example_text = tk.Label(example_frame, 
                                 text="BASE + BALL = GAMES\nCLUE + ONE = TWO",
                                 font=("Arial", 12), bg="#1C1C1C", fg="#FFFFFF")
        example_text.pack(anchor=tk.W)
        
        # Method selection
        method_frame = tk.LabelFrame(left_frame, text="Method", 
                                      font=("Arial", 16, "bold"), bg="#1C1C1C", fg="#F9A826")
        method_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Radio buttons for method
        self.method_var = tk.StringVar(value="step")
        step_radio = tk.Radiobutton(method_frame, text="STEP BY STEP", 
                                     variable=self.method_var, value="step",
                                     font=("Arial", 12), bg="#1C1C1C", fg="#FFFFFF")
        step_radio.pack(anchor=tk.W)
        
        direct_radio = tk.Radiobutton(method_frame, text="DIRECT (QUICK)", 
                                       variable=self.method_var, value="direct",
                                       font=("Arial", 12), bg="#1C1C1C", fg="#FFFFFF")
        direct_radio.pack(anchor=tk.W)
        
        # Start button
        start_button = tk.Button(left_frame, text="START", 
                                 command=self.process_words,
                                 font=("Arial", 14, "bold"), bg="#F9A826", fg="#1C1C1C")
        start_button.pack(fill=tk.X, pady=(20, 0), padx=10)
        
        # Right column - Word inputs and visualization
        right_frame = tk.Frame(content_frame, bg="#1C1C1C", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Word inputs
        words_frame = tk.Frame(right_frame, bg="#1C1C1C")
        words_frame.pack(side=tk.TOP, pady=(30, 20))
        
        # WORD1
        word1_label = tk.Label(words_frame, text="WORD1", 
                               font=("Arial", 16, "bold"), bg="#1C1C1C", fg="#F9A826")
        word1_label.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky=tk.EW)
        
        self.word1_entry = tk.Entry(words_frame, font=("Arial", 12), width=20, 
                                     bg="#3D4446", fg="#FFFFFF", justify='center')
        self.word1_entry.grid(row=0, column=1, padx=(0, 10), pady=(0, 20), sticky=tk.EW)
        self.word1_entry.bind('<Return>', lambda event: self.focus_next_entry(self.word2_entry))
        
        # WORD2
        word2_label = tk.Label(words_frame, text="WORD2", 
                               font=("Arial", 16, "bold"), bg="#1C1C1C", fg="#F9A826")
        word2_label.grid(row=1, column=0, padx=(0, 5), pady=(0, 5), sticky=tk.EW)
        
        self.word2_entry = tk.Entry(words_frame, font=("Arial", 12), width=20, 
                                     bg="#3D4446", fg="#FFFFFF", justify='center')
        self.word2_entry.grid(row=1, column=1, padx=(0, 10), pady=(0, 20), sticky=tk.EW)
        self.word2_entry.bind('<Return>', lambda event: self.focus_next_entry(self.word3_entry))
        
        # WORD3 (Result)
        word3_label = tk.Label(words_frame, text="WORD3", 
                               font=("Arial", 16, "bold"), bg="#1C1C1C", fg="#F9A826")
        word3_label.grid(row=2, column=0, padx=(0, 5), pady=(0, 5), sticky=tk.EW)
        
        self.word3_entry = tk.Entry(words_frame, font=("Arial", 12), width=20, 
                                     bg="#3D4446", fg="#FFFFFF", justify='center')
        self.word3_entry.grid(row=2, column=1, padx=(0, 10), pady=(0, 20), sticky=tk.EW)
        
        # Word display area
        self.word_display = WordDisplay(right_frame, bg="#1C1C1C")
        self.word_display.pack(fill=tk.BOTH, expand=True)
        
    def focus_next_entry(self, current_entry):
        current_entry.focus_set()

    def process_words(self):
        word1 = self.word1_entry.get().upper()
        word2 = self.word2_entry.get().upper()
        
        if not word1 or not word2:
            messagebox.showerror("Error", "Please enter both WORD1 and WORD2")
            return
        
        # Update the display with selected words and unique letters
        self.word_display.update_display(word1, word2)

        # If word3 is empty, calculate it
        word3 = self.word3_entry.get().upper()
        if not word3:
            # Simple algorithm: add characters and take modulo 26
            result = ""
            for i in range(max(len(word1), len(word2))):
                char1 = ord(word1[i % len(word1)]) - ord('A') if i < len(word1) else 0
                char2 = ord(word2[i % len(word2)]) - ord('A') if i < len(word2) else 0
                new_char = chr(((char1 + char2) % 26) + ord('A'))
                result += new_char
            
            self.word3_entry.delete(0, tk.END)
            self.word3_entry.insert(0, result)
            word3 = result

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')  # Maximize the window
    app = VisualCryptaApp(root)
    root.mainloop()