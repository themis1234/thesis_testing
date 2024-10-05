import tkinter as tk
from tkinter import filedialog, simpledialog, scrolledtext
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain_google_vertexai import VertexAI
from Imports import Imports

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory and Chat Application")
        self.chain = self.model_init()
        self.directory = None

        # Configure the grid layout for resizing
        root.grid_columnconfigure(0, weight=1)  # Column should expand
        root.grid_rowconfigure(1, weight=1)     # Chat area row should expand

        # Button to select directory
        self.select_dir_button = tk.Button(root, text="Select Directory", command=self.select_directory)
        # Place the button without allowing it to stretch horizontally or vertically
        self.select_dir_button.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # Text area for chat
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', height=10)
        # Make the text area expandable
        self.chat_area.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Chat input
        self.chat_input = tk.Entry(root)
        # Make the chat input field expand horizontally
        self.chat_input.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        self.chat_input.bind("<Return>", self.send_chat)

    @staticmethod
    def model_init():
        model = VertexAI(model_name="gemini-pro")
        memory = ConversationBufferMemory()
        chain = ConversationChain(llm=model, memory = memory)
        return chain
    
    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            imports = Imports(directory).getRelativeCode("file4.py")
            relative_code = "This is context, do not reply to this\n\n" + imports
            self.chain(relative_code)
            # Here you can process the directory as needed
        else:
            self.display_message("No directory selected.")

    def send_chat(self, event):
        user_input = self.chat_input.get()
        if user_input:
            # Display user's message in the chat area
            self.display_message(f"You: {user_input}")
            self.chat_input.delete(0, tk.END)

            # Get response from an API or simulate it
            response = self.get_api_response(user_input)
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
