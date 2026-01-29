import tkinter as tk
from tkinter import scrolledtext
import threading
import webbrowser
import logic # Importamos nuestra lógica

class AsistenteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente IA - Proyecto Final")
        self.root.geometry("700x650")

        # --- Variables de estado GUI ---
        self.voz_rate = 145 

        # Métricas del Modelo (Desde logic.py)
        frame_metricas = tk.LabelFrame(root, text="Métricas del Modelo", padx=10, pady=5)
        frame_metricas.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_metricas, text=f"Precisión (Accuracy): {logic.accuracy*100:.2f}% | Ejemplos de entrenamiento: {logic.num_ejemplos}").pack()

        # Configuración
        frame_config = tk.LabelFrame(root, text="Panel de Control", padx=10, pady=5, fg="blue")
        frame_config.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_config, text="Velocidad de Voz:").pack(anchor="w")
        self.scale_velocidad = tk.Scale(frame_config, from_=100, to=300, orient="horizontal", command=self.actualizar_rate)
        self.scale_velocidad.set(self.voz_rate)
        self.scale_velocidad.pack(fill="x")

        tk.Label(frame_config, text="Sensibilidad Micrófono:").pack(anchor="w")
        self.scale_sensibilidad = tk.Scale(frame_config, from_=100, to=1000, orient="horizontal")
        self.scale_sensibilidad.set(400)
        self.scale_sensibilidad.pack(fill="x")

        # Chat Area
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', height=12)
        self.chat_area.pack(padx=10, pady=10, fill="both", expand=True)

        # Botones
        frame_controles = tk.Frame(root)
        frame_controles.pack(pady=5)

        self.btn_hablar = tk.Button(frame_controles, text="🎤 HABLAR", command=self.iniciar_escucha, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=15, height=2)
        self.btn_hablar.pack(side="left", padx=10)

        self.btn_detener = tk.Button(frame_controles, text="⏹ DETENER", command=self.detener_habla, bg="#f44336", fg="white", font=("Arial", 11, "bold"), width=15, height=2)
        self.btn_detener.pack(side="left", padx=10)

        # Input Manual
        frame_input = tk.Frame(root)
        frame_input.pack(fill="x", padx=10, pady=10)
        
        self.entry_texto = tk.Entry(frame_input, font=("Arial", 12))
        self.entry_texto.pack(side="left", fill="x", expand=True, padx=5)
        self.entry_texto.bind("<Return>", self.enviar_texto_hilo)
        
        btn_enviar = tk.Button(frame_input, text="Enviar Texto", command=self.enviar_texto_hilo)
        btn_enviar.pack(side="right")

        self.lbl_estado = tk.Label(root, text="Sistema Listo", fg="gray")
        self.lbl_estado.pack(side="bottom")

    def actualizar_rate(self, valor):
        self.voz_rate = int(valor)

    def detener_habla(self):
        self.actualizar_estado("Silenciando...")
        logic.detener_voz_motor()
        self.actualizar_estado("Silenciado.")

    def actualizar_estado(self, texto):
        self.root.after(0, lambda: self.lbl_estado.config(text=texto))

    def agregar_chat(self, texto):
        self.root.after(0, lambda: self._insertar_chat(texto))

    def _insertar_chat(self, texto):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, texto + "\n\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def iniciar_escucha(self):
        threading.Thread(target=self.proceso_voz).start()

    def enviar_texto_hilo(self, event=None):
        threading.Thread(target=self.procesar_texto_manual).start()

    def procesar_texto_manual(self):
        texto = self.entry_texto.get()
        if texto:
            self.root.after(0, lambda: self.entry_texto.delete(0, tk.END))
            self.ejecutar_accion(texto)

    def proceso_voz(self):
        self.btn_hablar.config(state="disabled")
        umbral = self.scale_sensibilidad.get()
        
        # Pasamos self.actualizar_estado como callback
        comando = logic.escuchar_mic(umbral, callback_status=self.actualizar_estado)
        
        if comando:
            self.ejecutar_accion(comando)
        else:
            self.actualizar_estado("No se escuchó nada.")
            
        self.btn_hablar.config(state="normal")
        self.actualizar_estado("Listo")

    def ejecutar_accion(self, comando):
        if not comando: return

        # Usamos logic para predecir
        intencion = logic.predecir_intencion(comando)
        self.agregar_chat(f"Tú: {comando} (Intención: {intencion})")

        if intencion == "saludo":
            respuesta = logic.consultar_gemini(f"Saluda cortésmente al usuario por la frase '{comando}'")
            self.agregar_chat(f"Gemini: {respuesta}")
            logic.hablar(respuesta, self.voz_rate)

        elif intencion == "despedida":
            respuesta = "Hasta luego, cerrando sistema."
            self.agregar_chat(f"Bot: {respuesta}")
            logic.hablar(respuesta, self.voz_rate)
            self.root.quit()

        elif intencion == "google":
            busqueda = comando.replace("busca en google", "").replace("buscar", "").replace("busca", "").strip()
            respuesta = f"Buscando en Google: {busqueda}"
            self.agregar_chat(f"Bot: {respuesta}")
            logic.hablar(respuesta, self.voz_rate)
            webbrowser.open(f"https://www.google.com/search?q={busqueda}")

        elif intencion == "wiki": 
            self.agregar_chat("Gemini: Pensando...")
            respuesta = logic.consultar_gemini(comando)
            self.agregar_chat(f"Gemini: {respuesta}")
            logic.hablar(respuesta, self.voz_rate)
