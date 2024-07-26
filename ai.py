import os
from dotenv import load_dotenv
import google.generativeai as genai
import unidecode

load_dotenv()

genai.configure(api_key=os.getenv('API_KEY'))

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