import tkinter as tk
from tkinter import filedialog, scrolledtext, Toplevel, Text
from Imports import Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
import os

store = {}
def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "KEY HERE"

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory and Chat Application")
        self.chain = self.model_init()
        
        self.directory = None
        self.terms = None
        self.directory_set = False
        self.terms_set = False

        # Configure the grid layout for resizing
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)

        # Button to select directory
        self.select_dir_button = tk.Button(root, text="Select Directory", command=self.select_directory)
        self.select_dir_button.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # Button to enter terms
        self.enter_terms_button = tk.Button(root, text="Enter Terms", command=self.enter_terms)
        self.enter_terms_button.grid(row=0, column=1, sticky='w', padx=10, pady=10)

        # Text area for chat
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', height=10)
        self.chat_area.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Chat input
        self.chat_input = tk.Entry(root)
        self.chat_input.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        self.chat_input.bind("<Return>", self.send_chat)


    @staticmethod
    def model_init():
        model = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.9)
        chain = RunnableWithMessageHistory(model, get_session_history)
        return chain

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory = Imports(directory).getRelativeCode("file4.py")
            self.directory_set = True
            self.display_message("Directory selected.")
            self.check_and_send_initial_context()
        else:
            self.display_message("No directory selected.")

    def enter_terms(self):
        self.show_multiline_input()

    def show_multiline_input(self):
        input_window = Toplevel(self.root)
        input_window.title("Enter Terms")

        text_area = Text(input_window, wrap="word", width=50, height=10)
        text_area.pack(padx=10, pady=10)

        submit_button = tk.Button(input_window, text="Submit", command=lambda: self.process_terms(text_area, input_window))
        submit_button.pack(pady=10)

    def process_terms(self, text_widget, window):
        self.terms = text_widget.get("1.0", tk.END).strip()
        self.terms_set = True
        self.display_message(f"Entered Terms: {self.terms}")
        window.destroy()
        self.check_and_send_initial_context()

    def check_and_send_initial_context(self):
        if self.directory_set and self.terms_set:
            combined_context = f"This is context, do not reply to this\n\nDirectory Content:\n{self.directory}\n\nEntered Terms:\n{self.terms}"
            self.chain(combined_context)
            self.display_message("Initial context sent to API.")

    def send_chat(self, event):
        user_input = self.chat_input.get()
        if user_input:
            self.display_message(f"You: {user_input}")
            self.chat_input.delete(0, tk.END)

            response = self.get_api_response(user_input)
            self.display_message(f"API: {response}")

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def get_api_response(self, user_input):
        return self.chain.invoke(user_input, config={"configurable": {"session_id": "1"}}).content


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
