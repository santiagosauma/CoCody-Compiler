import os
import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog
from tkinter import messagebox
from dotenv import load_dotenv
import google.generativeai as genai
import unidecode
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Token
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections.abc import Mapping

load_dotenv()

api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

def traducir_lenguaje_gemini(input_code, language='cpp'):
    prompt = f'Translate the following CoCody code to {language} syntax:\n\n{input_code} without comments and without description just the code'
    respuesta = model.generate_content(prompt)
    respuesta = omitir_primera_ultima_linea(respuesta.text)
    return respuesta

def comentar_lenguaje_gemini(input_code):
    prompt = f'Add comments (in Spanish, UTF-8) to the following CoCody code:\n\n{input_code}'
    respuesta = model.generate_content(prompt)
    respuesta = omitir_primera_ultima_linea(respuesta.text)
    return respuesta

def documentar_lenguaje_gemini(input_code):
    prompt = f'Genera documentación en formato markdown para el siguiente código CoCody en español, sin acentos:\n\n{input_code}'
    respuesta = model.generate_content(prompt)
    respuesta = omitir_primera_ultima_linea(respuesta.text)
    respuesta = unidecode.unidecode(respuesta)
    respuesta += "\n\nPuedes visualizar este documento en un lector de Markdown en linea como [Dillinger](https://dillinger.io/)."
    return respuesta

def limpiar_formato(archivo):
    return archivo.replace('"', '').replace("'", "").replace(" ", "_")

def omitir_primera_ultima_linea(codigo):
    lineas = codigo.split("\n")
    return "\n".join(lineas[1:-1])

def hex_to_rgb(color):
    color = color.lstrip('#')
    if len(color) == 6:
        r, g, b = color[0:2], color[2:4], color[4:6]
    elif len(color) == 3:
        r, g, b = color[0]*2, color[1]*2, color[2]*2
    else:
        return color
    return f'#{r}{g}{b}'

def apply_syntax_highlighting(text_widget, code):
    lexer = PythonLexer()
    style = get_style_by_name('default')
    tokens = lex(code, lexer)
    
    text_widget.config(state=tk.NORMAL)
    text_widget.delete('1.0', tk.END)
    
    defined_tags = set()

    for ttype, value in tokens:
        tag = str(ttype)
        if tag not in defined_tags:
            try:
                color = style.style_for_token(ttype)['color']
                if ttype in Token.Name:  # Variables
                    color = '#1a9469'
                elif ttype in Token.Operator:  # Signos
                    color = '#eacf4f'
                if color:
                    text_widget.tag_configure(tag, foreground=hex_to_rgb(color))
                defined_tags.add(tag)
            except KeyError:
                pass
        text_widget.insert(tk.END, value, tag)

    text_widget.config(state=tk.DISABLED)

class VisualizadorDebug:
    def __init__(self, code):
        self.code = code.split('\n')
        self.current_line = 0
        self.variables = {}
        self.call_stack = []
        self.loop_stack = []  # Pila de bucles para manejar los bucles correctamente
        self.history = []  # Historial de estados
        self.output_history = []  # Historial de salida

        self.root = tk.Tk()
        self.root.title("Visualizador de Depuración")

        # Marco principal que contiene el código y la gráfica
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Texto del código
        self.code_text = scrolledtext.ScrolledText(self.main_frame, height=20, width=50, font=("Helvetica", 12))
        self.code_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Panel de gráficos debajo del código
        self.graph_frame = ttk.LabelFrame(self.main_frame, text="Visualización de Datos")
        self.graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Marco de variables
        self.variables_frame = ttk.LabelFrame(self.root, text="Variables")
        self.variables_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Tabla de variables
        self.variables_tree = ttk.Treeview(self.variables_frame, columns=('Variable', 'Valor'), show='headings')
        self.variables_tree.heading('Variable', text='Variable')
        self.variables_tree.heading('Valor', text='Valor')
        self.variables_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de desplazamiento para las variables
        self.variables_scroll = ttk.Scrollbar(self.variables_frame, orient="vertical", command=self.variables_tree.yview)
        self.variables_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.variables_tree.configure(yscrollcommand=self.variables_scroll.set)

        # Marco de pila de llamadas
        self.call_stack_frame = ttk.LabelFrame(self.root, text="Pila de Llamadas")
        self.call_stack_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Lista de pila de llamadas
        self.call_stack_list = tk.Listbox(self.call_stack_frame)
        self.call_stack_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de desplazamiento para la pila de llamadas
        self.call_stack_scroll = ttk.Scrollbar(self.call_stack_frame, orient="vertical", command=self.call_stack_list.yview)
        self.call_stack_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.call_stack_list.configure(yscrollcommand=self.call_stack_scroll.set)

        # Panel de salida
        self.output_frame = ttk.LabelFrame(self.root, text="Salida")
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(self.output_frame, height=10, width=50, font=("Helvetica", 12))
        self.output_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Botones
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.next_button = ttk.Button(self.buttons_frame, text="Siguiente Paso", command=self.next_step)
        self.next_button.pack(fill=tk.X, pady=5)

        self.back_button = ttk.Button(self.buttons_frame, text="Volver Atrás", command=self.back_step)
        self.back_button.pack(fill=tk.X, pady=5)

        self.run_button = ttk.Button(self.buttons_frame, text="Ejecutar hasta breakpoint", command=self.run_to_breakpoint)
        self.run_button.pack(fill=tk.X, pady=5)

        self.restart_button = ttk.Button(self.buttons_frame, text="Volver al Inicio", command=self.restart)
        self.restart_button.pack(fill=tk.X, pady=5)

        self.visualize_button = ttk.Button(self.buttons_frame, text="Visualizar Datos", command=self.visualize_data)
        self.visualize_button.pack(fill=tk.X, pady=5)

        self.breakpoints = set()
        self.load_code()

        self.code_text.bind("<Double-1>", self.toggle_breakpoint)

    def load_code(self):
        code_str = "\n".join(self.code)
        apply_syntax_highlighting(self.code_text, code_str)
        self.code_text.tag_configure("highlight", background="yellow")
        self.code_text.tag_configure("breakpoint", background="red")

    def next_step(self):
        if self.current_line < len(self.code):
            self.save_state()  # Guardar el estado actual en el historial

            self.code_text.tag_remove("highlight", "1.0", tk.END)
            self.code_text.tag_add("highlight", f"{self.current_line+1}.0", f"{self.current_line+1}.end")
            self.code_text.see(f"{self.current_line+1}.0")

            # Simular la ejecución de la línea actual
            current_line = self.code[self.current_line].strip()

            # Guardar el estado anterior de las variables
            previous_variables = self.variables.copy()

            # Manejar la ejecución del código actual
            if '<-' in current_line:
                var, expr = current_line.split('<-')
                var = var.strip()
                expr = expr.strip()
                expr = expr.replace('.', '')  # Transformar la expresión a una sintaxis válida de Python
                value = self.evaluate_expression(expr)
                if '[' in var and ']' in var:
                    # Es una lista con un índice
                    list_var, index = var.split('[')
                    index = index[:-1]  # Remover el ']'
                    list_var = list_var.strip()
                    index = self.evaluate_expression(index)
                    self.variables[list_var][index] = value
                    self.output_history.append(f"{list_var}[{index}] <- {expr} = {self.format_value(value)}\n")
                else:
                    self.variables[var] = value
                    self.output_history.append(f"{var} <- {expr} = {self.format_value(value)}\n")
            elif current_line.startswith("muestra("):
                var = current_line[8:-2].strip()
                value = self.evaluate_expression(var)
                self.output_history.append(f"{var}: {self.format_value(value)}\n")

            # Manejar estructura de control 'si'
            elif current_line.startswith("si"):
                condition = current_line[3:-8].strip()
                if not self.evaluate_condition(condition):
                    # Saltar al fin de la estructura 'si'
                    self.skip_to_end_of_block("FIN_SI")

            # Manejar estructura de control 'ciclo'
            elif current_line.startswith("ciclo"):
                parts = current_line.split()
                var = parts[1]
                start = self.evaluate_expression(parts[3])
                end = self.evaluate_expression(parts[5])
                if self.loop_stack and self.loop_stack[-1]['start_line'] == self.current_line:
                    loop = self.loop_stack[-1]
                    loop['current'] += 1
                    if loop['current'] > end:
                        self.skip_to_end_of_block("fin_ciclo")
                        self.loop_stack.pop()
                        self.call_stack.pop()
                    else:
                        self.variables[loop['var']] = loop['current']
                else:
                    self.variables[var] = start
                    self.loop_stack.append({'start_line': self.current_line, 'end': end, 'current': start, 'var': var})
                    self.call_stack.append(current_line)

            # Resaltar variables que han cambiado
            self.highlight_changes(previous_variables, self.variables)

            # Actualizar pila de llamadas y bucles
            if current_line.startswith('mientras'):
                if self.loop_stack and self.loop_stack[-1]['start_line'] == self.current_line:
                    self.loop_stack[-1]['condition'] = current_line[9:-6].strip().replace('.', '')
                else:
                    self.loop_stack.append({'start_line': self.current_line, 'condition': current_line[9:-6].strip().replace('.', '')})
                self.call_stack.append(current_line)
            elif current_line == 'FIN_SI':
                if self.call_stack and self.call_stack[-1].startswith("si"):
                    self.call_stack.pop()
            elif current_line == 'FIN_MIENTRAS':
                if self.loop_stack:
                    loop = self.loop_stack[-1]
                    if self.evaluate_condition(loop['condition']):
                        self.current_line = loop['start_line']
                    else:
                        self.loop_stack.pop()
                        if self.call_stack:
                            self.call_stack.pop()
                else:
                    if self.call_stack:
                        self.call_stack.pop()
            elif current_line == 'fin_ciclo':
                if self.loop_stack:
                    loop = self.loop_stack[-1]
                    loop['current'] += 1
                    if loop['current'] > loop['end']:
                        self.loop_stack.pop()
                        if self.call_stack:
                            self.call_stack.pop()
                    else:
                        self.variables[loop['var']] = loop['current']
                        self.current_line = loop['start_line']

            # Actualizar la visualización
            self.update_variables(self.variables)
            self.update_call_stack(self.call_stack)
            self.update_output(self.output_history)

            # Verificar si la variable es una lista y actualizar la gráfica
            self.update_graph()

            self.current_line += 1

            # Forzar actualización de la interfaz
            self.root.update_idletasks()

    def skip_to_end_of_block(self, end_marker):
        nested_blocks = 1
        while self.current_line < len(self.code) - 1:
            self.current_line += 1
            current_line = self.code[self.current_line].strip()
            if current_line.startswith("si") or current_line.startswith("ciclo"):
                nested_blocks += 1
            elif current_line == end_marker:
                nested_blocks -= 1
                if nested_blocks == 0:
                    break

    def back_step(self):
        if self.history:
            state = self.history.pop()
            self.restore_state(state)

    def save_state(self):
        state = {
            'current_line': self.current_line,
            'variables': self.variables.copy(),
            'call_stack': self.call_stack.copy(),
            'loop_stack': self.loop_stack.copy(),
            'output_history': self.output_history.copy(),
        }
        self.history.append(state)

    def restore_state(self, state):
        self.current_line = state['current_line']
        self.variables = state['variables']
        self.call_stack = state['call_stack']
        self.loop_stack = state['loop_stack']
        self.output_history = state['output_history']

        self.code_text.tag_remove("highlight", "1.0", tk.END)
        self.code_text.tag_add("highlight", f"{self.current_line+1}.0", f"{self.current_line+1}.end")
        self.code_text.see(f"{self.current_line+1}.0")

        self.update_variables(self.variables)
        self.update_call_stack(self.call_stack)
        self.update_output(self.output_history)

        # Actualizar visualización de datos si es una lista
        self.update_graph()

    def restart(self):
        if self.history:
            initial_state = self.history[0]
            self.restore_state(initial_state)
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete('1.0', tk.END)
            self.output_history = []  # Limpiar el historial de salida
            self.output_text.config(state=tk.DISABLED)
            self.variables = {}  # Limpiar las variables
            self.call_stack = []  # Limpiar la pila de llamadas
            self.loop_stack = []  # Limpiar la pila de bucles
            self.update_variables(self.variables)
            self.update_call_stack(self.call_stack)

    def update_output(self, output_history):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        for line in output_history:
            self.output_text.insert(tk.END, line)
        self.output_text.config(state=tk.DISABLED)

    def highlight_changes(self, previous_variables, current_variables):
        for item in self.variables_tree.get_children():
            self.variables_tree.item(item, tags='')

        for var, value in current_variables.items():
            if var not in previous_variables or previous_variables[var] != value:
                item_id = self.find_variable_item(var)
                if item_id:
                    self.variables_tree.item(item_id, tags=('changed',))
        self.variables_tree.tag_configure('changed', background='yellow')

    def find_variable_item(self, var):
        for item in self.variables_tree.get_children():
            values = self.variables_tree.item(item, 'values')
            if values and values[0] == var:
                return item
        return None

    def evaluate_expression(self, expr):
        # Evaluar la expresión en el contexto de las variables actuales
        try:
            return eval(expr, {}, self.variables)
        except Exception as e:
            return f"Error: {e}"

    def evaluate_condition(self, condition):
        # Evaluar la condición en el contexto de las variables actuales
        try:
            return eval(condition, {}, self.variables)
        except Exception as e:
            return False

    def format_value(self, value):
        if isinstance(value, float):
            return int(value)
        return value

    def run_to_breakpoint(self):
        while self.current_line < len(self.code) and self.current_line not in self.breakpoints:
            self.next_step()

    def toggle_breakpoint(self, event):
        line = int(self.code_text.index(f"@{event.x},{event.y}").split('.')[0])
        if line in self.breakpoints:
            self.breakpoints.remove(line)
            self.code_text.tag_remove("breakpoint", f"{line}.0", f"{line}.end")
        else:
            self.breakpoints.add(line)
            self.code_text.tag_add("breakpoint", f"{line}.0", f"{line}.end")

    def update_variables(self, variables):
        for i in self.variables_tree.get_children():
            self.variables_tree.delete(i)
        for var, value in variables.items():
            if isinstance(value, list):
                for index, item in enumerate(value):
                    self.variables_tree.insert('', 'end', values=(f"{var}[{index}]", item))
            else:
                self.variables_tree.insert('', 'end', values=(var, value))

    def update_call_stack(self, call_stack):
        self.call_stack_list.delete(0, tk.END)
        for call in reversed(call_stack):
            self.call_stack_list.insert(tk.END, call)

    def update_graph(self):
        for var, value in self.variables.items():
            if isinstance(value, list):
                self.visualize_list(value)

    def visualize_data(self):
        var_name = simpledialog.askstring("Variable", "Ingrese el nombre de la variable a visualizar:")
        if var_name and var_name in self.variables:
            value = self.variables[var_name]
            if isinstance(value, (list, tuple)):
                self.visualize_list(value)
            elif isinstance(value, dict):
                self.visualize_dict(value)
            else:
                messagebox.showinfo("Visualización", "La variable no es una lista ni un diccionario.")

    def visualize_list(self, lst):
        self.ax.clear()
        self.ax.bar(range(len(lst)), lst)
        self.ax.set_title("Visualización de Lista")
        self.ax.set_xlabel("Índice")
        self.ax.set_ylabel("Valor")
        self.ax.set_xticks(range(len(lst)))  # Configurar los ticks para mostrar solo los índices
        self.canvas.draw()

    def visualize_dict(self, dct):
        fig, ax = plt.subplots()
        G = nx.DiGraph()
        for key, value in dct.items():
            G.add_node(key)
            if isinstance(value, list):
                for item in value:
                    G.add_edge(key, item)
            else:
                G.add_edge(key, value)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, ax=ax, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
        plt.title("Visualización de Diccionario")
        plt.show()

    def run(self):
        self.root.mainloop()

class Traducir:
    def __init__(self, source, target, language):
        self.source = source
        self.target = target
        self.language = language

    def eval(self, context):
        with open(self.source.strip('"'), 'r') as f:
            code = f.read()
        translated_code = traducir_lenguaje_gemini(code, self.language)
        if translated_code:
            sanitized_target = limpiar_formato(self.target)
            target_filename = f"{sanitized_target}"
            with open(target_filename, 'w') as f:
                f.write(translated_code)
            print(f"Archivo {self.source} traducido a {target_filename}")
        else:
            print(f"Error al traducir {self.source} a {self.target}")

class Comentar:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def eval(self, context):
        with open(self.source.strip('"'), 'r') as f:
            code = f.read()
        commented_code = comentar_lenguaje_gemini(code)
        if commented_code:
            sanitized_target = limpiar_formato(self.target)
            target_filename = f"{sanitized_target}"
            with open(target_filename, 'w') as f:
                f.write(commented_code)
            print(f"Archivo {self.source} comentado en {target_filename}")
        else:
            print(f"Error al comentar {self.source}")

class Documentar:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def eval(self, context):
        with open(self.source.strip('"'), 'r') as f:
            code = f.read()
        documentation = documentar_lenguaje_gemini(code)
        if documentation:
            sanitized_target = limpiar_formato(self.target)
            target_filename = f"{sanitized_target}"
            with open(target_filename, 'w') as f:
                f.write(documentation)
            print(f"Archivo {self.source} documentado en {target_filename}")
        else:
            print(f"Error al documentar {self.source}")

class GenerarEjercicio:
    def __init__(self, nivel, tema):
        self.nivel = nivel
        self.tema = tema

    def eval(self, context):
        prompt = f'In Spanish without accent, generate a {self.nivel} level exercise on {self.tema}. Provide: 1. A brief description of the exercise. 2. The problem statement. 3. An example input and output. 4. Resources to learn the concept.'
        respuesta = model.generate_content(prompt)
        respuesta_text = omitir_primera_ultima_linea(respuesta.text)
        respuesta_text = unidecode.unidecode(respuesta_text)
        respuesta_text += "\n\nPuedes visualizar este documento en un lector de Markdown en linea como [Dillinger](https://dillinger.io/)."
        ejercicio = respuesta_text.strip()
        print(f"Ejercicio generado:\n{ejercicio}")
        
        # Guardar el ejercicio en un archivo .txt en formato markdown
        nombre_archivo = f"ejercicio_{self.nivel}_{self.tema}.txt"
        with open(nombre_archivo, 'w') as file:
            file.write(ejercicio)
        
        print(f"Ejercicio guardado en {nombre_archivo}")

class Visualiza:
    def __init__(self, source):
        self.source = source

    def eval(self, context):
        with open(self.source.strip('"'), 'r') as f:
            code = f.read()
        visualizer = VisualizadorDebug(code)
        visualizer.run()
