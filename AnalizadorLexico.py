from flask import Flask, render_template, request
import re
import time

app = Flask(__name__)

class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"Token({self.tipo}, {self.valor}, {self.linea}, {self.columna})"

class AnalizadorLexico:
    def __init__(self, codigo_fuente, lenguaje='python'):
        self.codigo_fuente = codigo_fuente
        self.linea = 1
        self.columna = 1
        self.tokens = []
        self.errores = []
        self.patrones = self.obtener_patrones(lenguaje)

    def obtener_patrones(self, lenguaje):
        patrones_generales = [
            (r'[a-zA-Z_][a-zA-Z_0-9]*', 'IDENTIFICADOR'),
            (r'\d+\.\d+', 'NUMERO DECIMAL'),  # Números decimales
            (r'\d+', 'NUMERO ENTERO'),         # Números enteros
            (r'\+', 'SUMA'),
            (r'-', 'RESTA'),
            (r'\*', 'MULTIPLICACION'),
            (r'/', 'DIVISION'),
            (r'=', 'ASIGNACION'),
            (r'==', 'IGUALDAD'),
            (r'!=', 'DESIGUALDAD'),
            (r'>', 'MAYOR'),
            (r'<', 'MENOR'),
            (r'>=', 'MAYOR_IGUAL'),
            (r'<=', 'MENOR_IGUAL'),
            (r'{', 'LLAVE_ABIERTA'),
            (r'}', 'LLAVE_CERRADA'),
            (r'\(', 'PARENTESIS_ABIERTO'),
            (r'\)', 'PARENTESIS_CERRADO'),
            (r';', 'PUNTO_Y_COMA: FINAL'),
            (r'//.*', 'COMENTARIO_SIMPLE'),
            (r'/\*[\s\S]*?\*/', 'COMENTARIO_MULTILINEA'),
            (r'"[^"]*"', 'CADENA'),
            (r"\'[^\']*\'", 'CADENA_SIMPLE'),
            (r'[\[\]<>]', 'CARACTER_ESPECIAL'),  # Corchetes y signos de menor/mayor
        ]
        
        # Agregar palabras clave específicas de lenguajes
        if lenguaje == 'python':
            patrones_generales += [(r'\b' + palabra + r'\b', 'PALABRA_CLAVE') for palabra in ['def', 'class', 'if', 'else', 'elif', 'while', 'for', 'return']]
        elif lenguaje == 'java':
            patrones_generales += [(r'\b' + palabra + r'\b', 'PALABRA_CLAVE') for palabra in ['class', 'public', 'private', 'if', 'else', 'for', 'while', 'return', 'int', 'void']]
        elif lenguaje == 'cpp':
            patrones_generales += [(r'\b' + palabra + r'\b', 'PALABRA_CLAVE') for palabra in ['class', 'public', 'private', 'if', 'else', 'for', 'while', 'return', 'int', 'void']]
        
        return patrones_generales

    def eliminar_comentarios(self):
        self.codigo_fuente = re.sub(r'#.*', '', self.codigo_fuente)
        self.codigo_fuente = re.sub(r'/\*.*?\*/', '', self.codigo_fuente, flags=re.DOTALL)

    def eliminar_espacios_en_blanco(self):
        self.codigo_fuente = re.sub(r'\s+', ' ', self.codigo_fuente)

    def analizar(self):
        self.eliminar_comentarios()
        self.eliminar_espacios_en_blanco()

        while self.codigo_fuente:
            encontrado = False
            for patron, tipo in self.patrones:
                match = re.match(patron, self.codigo_fuente)
                if match:
                    token = Token(tipo, match.group(), self.linea, self.columna)
                    self.tokens.append(token)
                    self.codigo_fuente = self.codigo_fuente[match.end():]
                    self.columna += match.end()
                    encontrado = True
                    break 
            if not encontrado:
                self.errores.append(f"Error léxico en la línea {self.linea}, columna {self.columna}")
                self.codigo_fuente = self.codigo_fuente[1:]  # Avanza un carácter si no se encontró ningún patrón
                self.columna += 1  # Aumentar la columna para reflejar el avance

    def tokenizar_caracteres(self):
        caracteres = []
        for token in self.tokens:
            caracteres.extend(list(token.valor))  # Convertir el token en una lista de caracteres
        return caracteres

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

# Proceso de análisis del código
@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        #incializar variables
        codigo_fuente = ""
        lenguaje = 'cpp' #Un Leguaje por defecto 

        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            codigo_fuente = file.read().decode('utf-8')
            # Detectar lenguajes de programación a partir de la extensión de archivos subidos
            extension = file.filename.split('.')[-1]
            if extension == 'cpp':
                lenguaje = 'cpp'
            elif extension == 'py':
                lenguaje = 'python'
            elif extension == 'java':
                lenguaje = 'java'
            else:
                return "Error: Tipo de archivo no soportado"
            
        #Verifica si se ingreso texto en el Textarea
        elif 'codigo_fuente' in request.form and request.form['codigo_fuente'].strip() != '':
            codigo_fuente = request.form['codigo_fuente']
        if not codigo_fuente:
            return "Error: No se recibio codigo fuente ni archivos subidos"
        
        #Crear el analizador lexico 
        analizador = AnalizadorLexico(codigo_fuente, lenguaje=lenguaje)
        #analizar el codigo
        start_time = time.time()
        analizador.analizar()
        caracteres = analizador.tokenizar_caracteres()
        end_time = time.time()

        resultado = '\n'.join(str(token) for token in analizador.tokens)
        resultado_caracteres = ', '.join(caracteres)  # Asegúrate de que esto esté aquí
        tiempo_ejecucion = f"Tiempo de ejecución: {end_time - start_time:.4f} segundos"
        resultado_completo = f"{resultado}\n\nCaracteres: {resultado_caracteres}\n\n{tiempo_ejecucion}"  # Incluye caracteres en la respuesta

        return resultado_completo
    
    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)