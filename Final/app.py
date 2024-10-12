import tkinter as tk
from tkinter import filedialog, scrolledtext, Toplevel, Text

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
# from langchain_google_vertexai import VertexAI
from Imports import Imports


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory and Chat Application")
        self.chain = []#self.model_init()
        self.directory = None

        # Configure the grid layout for resizing
        root.grid_columnconfigure(0, weight=1)  # Column should expand
        root.grid_rowconfigure(1, weight=1)     # Chat area row should expand

        # Button to select directory
        self.select_dir_button = tk.Button(root, text="Select Directory", command=self.select_directory)
        self.select_dir_button.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # Button to enter terms
        self.enter_terms_button = tk.Button(root, text="Enter Terms", command=self.enter_terms)
        self.enter_terms_button.grid(row=0, column=1, sticky='w', padx=10, pady=10)  # Adjust grid position as needed

        # Text area for chat
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', height=10)
        self.chat_area.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Chat input
        self.chat_input = tk.Entry(root)
        self.chat_input.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        self.chat_input.bind("<Return>", self.send_chat)

    # @staticmethod
    # def model_init():
    #     model = VertexAI(model_name="gemini-pro")
    #     memory = ConversationBufferMemory()
    #     chain = ConversationChain(llm=model, memory=memory)
    #     return chain

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            imports = Imports(directory).getRelativeCode("file4.py")
            relative_code = "This is context, do not reply to this\n\n" + imports
            # self.chain(relative_code)
        else:
            self.display_message("No directory selected.")

    def enter_terms(self):
        # Open a custom window for multiline text input
        self.show_multiline_input()

    def show_multiline_input(self):
        # Create a new Toplevel window
        input_window = Toplevel(self.root)
        input_window.title("Enter Terms")

        # Create a Text widget for multiline input
        text_area = Text(input_window, wrap="word", width=50, height=10)
        text_area.pack(padx=10, pady=10)

        # Submit button to process input
        submit_button = tk.Button(input_window, text="Submit", command=lambda: self.process_terms(text_area, input_window))
        submit_button.pack(pady=10)

    def process_terms(self, text_widget, window):
        # Retrieve text from the Text widget
        terms = text_widget.get("1.0", tk.END).strip()  # Get all text, remove trailing spaces/newlines
        if terms:
            self.display_message(f"Entered Terms: {terms}")
            # Send the terms to the chat model
            # self.chain(f"The user entered the following terms: {terms}")
        else:
            self.display_message("No terms were entered.")
        # Close the window after submitting
        window.destroy()

    def send_chat(self, event):
        user_input = self.chat_input.get()
        if user_input:
            self.display_message(f"You: {user_input}")
            self.chat_input.delete(0, tk.END)

            # response = self.get_api_response(user_input)
            self.display_message(f"API: {response}")

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def get_api_response(self, user_input):
        chain = self.chain
        return chain(user_input)['response']


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
