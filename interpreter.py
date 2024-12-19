import tkinter as tk
import customtkinter as ctk
from tkinter import simpledialog, messagebox
import threading
from queue import Queue

input_request = Queue()
input_response = Queue()


def PL_interpreter(code):
    """
    Interprets and executes PL code with error handling.
    """
    code = ''.join(filter(lambda x: x in ['<', '>', '+', '-', '.', ',', '[', ']'], code))
    if not code:
        raise ValueError("No valid PL code provided.")
    if code.count('[') != code.count(']'):
        raise ValueError("Unmatched brackets in code.")

    tape = [0] * 10000
    ptr = 0
    code_ptr = 0
    output = ''
    loop_stack = []
    max_steps = 10000
    step_count = 0

    while code_ptr < len(code):
        step_count += 1
        #if step_count > max_steps:
            #raise RuntimeError("Maximum execution steps exceeded. Possible infinite loop.")

        command = code[code_ptr]

        if command == '>':
            ptr += 1
            if ptr >= len(tape):
                raise IndexError("Pointer exceeded tape size (ptr > 1000).")
        elif command == '<':
            ptr -= 1
            if ptr < 0:
                raise IndexError("Pointer moved to negative index (ptr < 0).")
        elif command == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif command == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif command == '.':
            output += chr(tape[ptr])
        elif command == ',':
            input_request.put("input")
            user_input = input_response.get()
            if user_input and len(user_input) == 1:
                tape[ptr] = ord(user_input[0]) % 256
            else:
                raise ValueError("Invalid input. Expected a single character.")

        elif command == '[':
            if tape[ptr] == 0:
                open_brackets = 1
                while open_brackets:
                    code_ptr += 1
                    if code_ptr >= len(code):
                        raise ValueError("Unmatched '[' at position {}".format(code_ptr))
                    if code[code_ptr] == '[':
                        open_brackets += 1
                    elif code[code_ptr] == ']':
                        open_brackets -= 1
            else:
                loop_stack.append(code_ptr)
        elif command == ']':
            if not loop_stack:
                raise ValueError("Unmatched ']' at position {}".format(code_ptr))
            if tape[ptr] != 0:
                code_ptr = loop_stack[-1]
            else:
                loop_stack.pop()

        code_ptr += 1

    if loop_stack:
        raise ValueError("Unmatched '[' detected.")

    return output


def request_input():
    """
    Checks if input is requested and shows a dialog in the main thread.
    """
    try:
        input_request.get_nowait()
        user_input = simpledialog.askstring("Input", "Enter a single character:")
        input_response.put(user_input)
    except:
        pass


def run_PL():
    """
    Retrieves the code from the text editor, runs it in a separate thread, and displays the output.
    """
    code = text_editor.get("1.0", tk.END).strip()
    threading.Thread(target=execute_PL, args=(code,), daemon=True).start()


def execute_PL(code):
    """
    Executes the PL code and updates the output display.
    """
    try:
        output = PL_interpreter(code)
        output_display.delete("1.0", tk.END)
        output_display.insert(tk.END, output)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def setup_ui(root):
    """
    Sets up the UI components.
    """
    global text_editor, output_display

    # Configure root window
    root.title("PL Compiler | v1.0 | @quantam")
    root.geometry("800x600")
    root.resizable(False, False)

    # Text editor for PL code
    text_editor = ctk.CTkTextbox(root, width=780, height=300)
    text_editor.pack(pady=20)

    # Placeholder text
    placeholder_text = "Enter your PL code here..."
    text_editor.insert("1.0", placeholder_text)
    text_editor.bind("<FocusIn>", lambda event: on_focus_in(event, placeholder_text))
    text_editor.bind("<FocusOut>", lambda event: on_focus_out(event, placeholder_text))

    # Frame for buttons
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=10)

    # Run button
    run_button = ctk.CTkButton(button_frame, text="Run", command=run_PL)
    run_button.pack(side=tk.LEFT, padx=10)

    # Output display
    output_display = ctk.CTkTextbox(root, width=780, height=200)
    output_display.pack(pady=20)

    # Periodically check for input requests
    root.after(100, check_for_input_requests)


def check_for_input_requests():
    """
    Continuously checks for input requests in the main thread.
    """
    request_input()
    root.after(100, check_for_input_requests)


def on_focus_in(event, placeholder_text):
    """
    Clears the placeholder text when the text editor gains focus.
    """
    if text_editor.get("1.0", tk.END).strip() == placeholder_text:
        text_editor.delete("1.0", tk.END)
        text_editor.config(fg="black")


def on_focus_out(event, placeholder_text):
    """
    Restores the placeholder text if the text editor is empty when it loses focus.
    """
    if not text_editor.get("1.0", tk.END).strip():
        text_editor.insert("1.0", placeholder_text)
        text_editor.config(fg="gray")


if __name__ == "__main__":
    root = ctk.CTk()
    setup_ui(root)
    root.mainloop()
