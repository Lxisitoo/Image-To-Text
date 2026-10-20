import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
from PIL import Image
import pytesseract
import google.generativeai as genai

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

genai.configure(api_key="YOUR_API_KEY_HERE") 
modelo = genai.GenerativeModel('gemini-3.7-flash')

def procesar_imagen(ruta_imagen):
    try:
        estado_label.config(text="Estado: Extrayendo texto con OCR...", fg="blue")
        
        # Leer imagen y aplicar OCR
        img = Image.open(ruta_imagen)
        texto_extraido = pytesseract.image_to_string(img, lang='spa', config='--psm 6').strip()
        
        # Mostrar el texto en el primer cuadro
        caja_texto.delete(1.0, tk.END)
        caja_texto.insert(tk.END, texto_extraido if texto_extraido else "No se detectó texto en la imagen.")
        
        if not texto_extraido:
            estado_label.config(text="Estado: Finalizado sin texto.", fg="red")
            return

        # Consultar a Gemini
        estado_label.config(text="Estado: Consultando a Gemini...", fg="blue")
        prompt = f"Responde de forma clara a la siguiente pregunta o texto que extraje de una imagen:\n\n{texto_extraido}"
        respuesta = modelo.generate_content(prompt)
        
        # Mostrar la respuesta en el segundo cuadro
        caja_respuesta.delete(1.0, tk.END)
        caja_respuesta.insert(tk.END, respuesta.text)
        
        estado_label.config(text="Estado: ¡Proceso completado exitosamente!", fg="green")
        
    except Exception as e:
        estado_label.config(text=f"Estado: Error -> {str(e)}", fg="red")

def seleccionar_archivo():
    # Abrir el explorador de archivos (filtramos por PNG y JPG)
    ruta_imagen = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")]
    )
    
    if ruta_imagen:
        # Limpiar las cajas de texto antes de procesar
        caja_texto.delete(1.0, tk.END)
        caja_respuesta.delete(1.0, tk.END)
        
        # Lanzar el proceso en un hilo separado para no congelar la ventana
        hilo = threading.Thread(target=procesar_imagen, args=(ruta_imagen,))
        hilo.start()

# --- 3. INTERFAZ GRÁFICA (Tkinter) ---
ventana = tk.Tk()
ventana.title("Asistente OCR con Gemini")
ventana.geometry("600x700")
ventana.configure(padx=20, pady=20)

# Botón para subir imagen
btn_seleccionar = tk.Button(ventana, text="Subir Imagen", font=("Arial", 12, "bold"), command=seleccionar_archivo, bg="#4CAF50", fg="white", padx=10, pady=5)
btn_seleccionar.pack(pady=10)

# Etiqueta de estado
estado_label = tk.Label(ventana, text="Estado: Esperando imagen...", font=("Arial", 10))
estado_label.pack(pady=5)

# Sección de Texto Extraído
lbl_texto = tk.Label(ventana, text="Texto extraído de la imagen:", font=("Arial", 10, "bold"))
lbl_texto.pack(anchor="w", pady=(10, 0))

caja_texto = scrolledtext.ScrolledText(ventana, height=8, font=("Arial", 10))
caja_texto.pack(fill="x", pady=5)

# Sección de Respuesta de Gemini
lbl_respuesta = tk.Label(ventana, text="Respuesta de Gemini:", font=("Arial", 10, "bold"))
lbl_respuesta.pack(anchor="w", pady=(10, 0))

caja_respuesta = scrolledtext.ScrolledText(ventana, height=15, font=("Arial", 10))
caja_respuesta.pack(fill="both", expand=True, pady=5)

# Iniciar la aplicación
ventana.mainloop()


