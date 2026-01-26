import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser

wikipedia.set_lang("es")

def hablar(texto):
    engine = pyttsx3.init()
    print(f"Bot dice: {texto}")
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\nCalibrando ruido de fondo... (silencio por favor)")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Para que escuche todo lo que se diga
        recognizer.dynamic_energy_threshold = False 
        
        # Fijamos la sensibilidad. 
        recognizer.energy_threshold = 400 
        
        # Paciencia del bot (cuánto silencio espera antes de cortar)
        recognizer.pause_threshold = 2.0 
        
        print("Escuchando... (Ya puedes hablar)")
        
        try:
            # phrase_time_limit=None Hablar sin limite
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=None)
            
            print("Procesando...")
            comando = recognizer.recognize_google(audio, language='es-ES')
            print(f"Tú: {comando}")
            return comando.lower()
            
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            hablar("No te entendí bien.")
            return ""
        except sr.RequestError:
            hablar("Error de conexión.")
            return ""

# --- CEREBRO DEL CHATBOT ---
def modo_chatbot(consulta):
    """Intenta responder como una persona usando Wikipedia"""
    hablar(f"Déjame pensar sobre {consulta}...")
    
    try:
        # Intenta buscar un resumen directo
        resultado = wikipedia.summary(consulta, sentences=2)
        hablar(resultado)
    except wikipedia.exceptions.DisambiguationError:
        hablar("Hay muchas cosas con ese nombre, sé más específico.")
    except wikipedia.exceptions.PageError:
        hablar("No encontré eso en Wikipedia, abriendo Google.")
        webbrowser.open(f"https://www.google.com/search?q={consulta}")



# --- BUCLE PRINCIPAL ---
def main():
    hablar("Hola, ya estoy listo. Pregúntame algo.")
    
    while True:
        pedido = escuchar()
        
        if not pedido:
            continue 
            
        if "apagar" in pedido or "salir" in pedido or "adiós" in pedido:
            hablar("Nos vemos.")
            break
            
        
        if "busca" in pedido or "buscar" in pedido:
            consulta = pedido.replace("busca", "").strip()
            hablar(f"Abriendo Google para buscar {consulta}")
            webbrowser.open(f"https://www.google.com/search?q={consulta}")
        else:
            # Asume que es una pregunta directa para el chatbot
            modo_chatbot(pedido)

if __name__ == "__main__":
    main()