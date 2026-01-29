import speech_recognition as sr
import pyttsx3
import webbrowser
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Librerías de IA
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Cargar variables de entorno
load_dotenv()
API_KEY_GEMINI = os.getenv("GEMINI_API_KEY")

# --- CONFIGURACIÓN ---
try:
    genai.configure(api_key=API_KEY_GEMINI)
    modelo_gemini = genai.GenerativeModel('gemini-2.5-flash-lite')
except Exception as e:
    print(f"Error configurando Gemini: {e}")
    modelo_gemini = None

# Inicializamos el motor de voz globalmente
engine = pyttsx3.init()

def configurar_voz():
    """Busca y configura una voz en español"""
    voces = engine.getProperty('voices')
    for voz in voces:
        if "spanish" in voz.name.lower() or "español" in voz.name.lower():
            engine.setProperty('voice', voz.id)
            print(f"Voz configurada: {voz.name}")
            return
    print("No se encontró voz en español, usando la predeterminada.")

# Configuramos la voz al inicio
configurar_voz()

# --- ENTRENAMIENTO DEL MODELO ---
datos_entrenamiento = [
    # SALUDOS
    ("hola", "saludo"), ("buenos días", "saludo"), ("buenas tardes", "saludo"),
    ("buenas noches", "saludo"), ("qué tal", "saludo"), ("hey", "saludo"),
    ("hola bot", "saludo"), ("saludos", "saludo"),
    
    # DESPEDIDAS
    ("adiós", "despedida"), ("hasta luego", "despedida"), ("salir", "despedida"),
    ("apagar", "despedida"), ("nos vemos", "despedida"), ("chao", "despedida"),
    ("bye", "despedida"),
    
    # GOOGLE
    ("busca en google", "google"), ("buscar", "google"), ("quiero saber de", "google"),
    ("investiga sobre", "google"), ("necesito información de", "google"),
    ("busca", "google"), ("busca precios de", "google"),

    # GEMINI (WIKI/GENERAL)
    ("que es", "wiki"), ("quien es", "wiki"), ("dime sobre", "wiki"),
    ("resumen de", "wiki"), ("definición de", "wiki"), ("explícame", "wiki"),
    ("biografía de", "wiki"), ("concepto de", "wiki"), ("qué significa", "wiki")
]

X = [x[0] for x in datos_entrenamiento]
y = [x[1] for x in datos_entrenamiento]

modelo = make_pipeline(CountVectorizer(), MultinomialNB())
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
modelo.fit(X_train, y_train)

# Exponemos datos útiles
predicciones = modelo.predict(X_test)
accuracy = metrics.accuracy_score(y_test, predicciones)
num_ejemplos = len(X)

# --- FUNCIONES DE LÓGICA ---
def consultar_gemini(consulta):
    if not modelo_gemini:
        return "Error: Gemini no está configurado."
    try:
        prompt = f"Responde en español, brevemente (máximo 1 párrafo): {consulta}"
        response = modelo_gemini.generate_content(prompt)
        return response.text.replace("*", "")
    except Exception as e:
        print(f"Error Gemini: {e}")
        return "Tuve un problema de conexión con la IA."

def hablar(texto, rate=145):
    """Habla el texto dado. 'rate' puede ser ajustado por la GUI luego."""
    if not texto: return
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    
    if engine._inLoop:
        engine.endLoop()
    engine.say(texto)
    try:
        engine.runAndWait()
    except RuntimeError:
        pass

def detener_voz_motor():
    engine = pyttsx3.init()
    engine.stop()

def escuchar_mic(umbral=400, callback_status=None):
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False 
    recognizer.energy_threshold = umbral 
    recognizer.pause_threshold = 2.0 
    
    with sr.Microphone() as source:
        if callback_status:
            callback_status("Calibrando ruido de fondo... (Silencio por favor)")
            
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        
        if callback_status:
            callback_status("¡Ya puedes hablar!")

        try:
            audio = recognizer.listen(source, timeout=5)
            if callback_status:
                callback_status("Procesando...")
                
            comando = recognizer.recognize_google(audio, language='es-ES')
            return comando.lower()
        except Exception:
            return ""

def predecir_intencion(comando):
    return modelo.predict([comando])[0]
