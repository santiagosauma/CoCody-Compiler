import os
from dotenv import load_dotenv
import google.generativeai as genai

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