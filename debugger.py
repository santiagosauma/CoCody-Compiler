import tkinter as tk
from tkinter import ttk

class Debugger:
    def __init__(self, ast, context):
        self.ast = ast
        self.context = context
        self.current_node = None
        self.step_index = 0
        
        self.root = tk.Tk()
        self.root.title("CoCody Debugger")
        
        self.code_text = tk.Text(self.root, height=20, width=50)
        self.code_text.pack(padx=10, pady=10)
        
        self.variable_tree = ttk.Treeview(self.root, columns=('Value',), height=10)
        self.variable_tree.heading('#0', text='Variable')
        self.variable_tree.heading('Value', text='Value')
        self.variable_tree.pack(padx=10, pady=10)
        
        self.step_button = tk.Button(self.root, text="Step", command=self.step)
        self.step_button.pack(pady=10)
        
    def start(self):
        self.update_display()
        self.root.mainloop()
        
    def step(self):
        if self.step_index < len(self.ast):
            self.current_node = self.ast[self.step_index]
            self.current_node.eval(self.context)
            self.step_index += 1
            self.update_display()
        
    def update_display(self):
        self.code_text.delete('1.0', tk.END)
        for i, node in enumerate(self.ast):
            line = f"{i+1}: {node.__class__.__name__}\n"
            self.code_text.insert(tk.END, line)
            if i == self.step_index - 1:
                self.code_text.tag_add("current", f"{i+1}.0", f"{i+1}.end")
                self.code_text.tag_config("current", background="yellow")
        
        self.variable_tree.delete(*self.variable_tree.get_children())
        for var, value in self.context.items():
            if isinstance(value, (int, float, str)):
                self.variable_tree.insert('', 'end', text=var, values=(str(value),))