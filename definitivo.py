import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import sys
import customtkinter  # La librería para la interfaz moderna
import fnmatch  # Para la búsqueda con comodines
import re  # <-- AÑADIDO: Necesario para el compilador

# -----------------------------------------------------------------
# PASO 1: El Backend Lógico (Original)
# -----------------------------------------------------------------

class GestorDeArchivos:
    """Contiene toda la lógica para manipular archivos y traducir rutas."""

    def __init__(self):
        ruta_home = os.path.expanduser('~')
        # Hacemos el diccionario sensible a mayúsculas y minúsculas
        self.atajos_ruta = {
            "descargas": os.path.join(ruta_home, "Downloads"),
            "escritorio": os.path.join(ruta_home, "Desktop"),
            "documentos": os.path.join(ruta_home, "Documents"),
            "imágenes": os.path.join(ruta_home, "Pictures"),
            "musica": os.path.join(ruta_home, "Music"),
            "videos": os.path.join(ruta_home, "Videos"),
            ".": os.getcwd(),
        }
        print("Gestor de archivos listo.")
        print(f"Atajos conocidos: {list(self.atajos_ruta.keys())}")

    def traducir_ruta(self, ruta_corta):
        r"""Traduce 'Descargas/a' a C:\Users\TuUser\Downloads\a"""
        if os.path.isabs(ruta_corta):
            return ruta_corta

        ruta_normalizada = ruta_corta.strip().replace("\\", "/")
        partes = ruta_normalizada.split('/')

        if not partes:
            return self.atajos_ruta["."]

        atajo = partes[0].lower()

        if atajo in self.atajos_ruta:
            ruta_base = self.atajos_ruta[atajo]
            sub_ruta = partes[1:]
            ruta_completa = os.path.join(ruta_base, *sub_ruta)
            return ruta_completa

        return ruta_corta

    # --- Funciones de Acción Básicas ---

    def crear_archivo(self, nombre_archivo, ruta_corta):
        try:
            ruta_completa = os.path.join(self.traducir_ruta(ruta_corta), nombre_archivo)
            os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
            with open(ruta_completa, 'w') as f:
                pass
            return f"✅ Archivo creado en: {ruta_completa}"
        except Exception as e:
            return f"❌ Error al crear: {e}"

    def mover_archivo(self, nombre_origen, ruta_origen, nombre_destino, ruta_destino):
        try:
            ruta_completa_origen = os.path.join(self.traducir_ruta(ruta_origen), nombre_origen)
            ruta_completa_destino = os.path.join(self.traducir_ruta(ruta_destino), nombre_destino)
            os.makedirs(os.path.dirname(ruta_completa_destino), exist_ok=True)
            shutil.move(ruta_completa_origen, ruta_completa_destino)
            return f"✅ Archivo movido a: {ruta_completa_destino}"
        except FileNotFoundError:
            return f"❌ Error: No se encontró el archivo de origen."
        except Exception as e:
            return f"❌ Error al mover: {e}"

    def borrar_archivo(self, nombre_archivo, ruta_corta):
        try:
            ruta_completa = os.path.join(self.traducir_ruta(ruta_corta), nombre_archivo)
            os.remove(ruta_completa)
            return f"✅ Archivo borrado: {ruta_completa}"
        except FileNotFoundError:
            return f"❌ Error: No se encontró el archivo."
        except Exception as e:
            return f"❌ Error al borrar: {e}"

    def copiar_archivo(self, nombre_origen, ruta_origen, nombre_destino, ruta_destino):
        try:
            ruta_completa_origen = os.path.join(self.traducir_ruta(ruta_origen), nombre_origen)
            ruta_completa_destino = os.path.join(self.traducir_ruta(ruta_destino), nombre_destino)
            os.makedirs(os.path.dirname(ruta_completa_destino), exist_ok=True)
            shutil.copy(ruta_completa_origen, ruta_completa_destino)
            return f"✅ Archivo copiado a: {ruta_completa_destino}"
        except FileNotFoundError:
            return f"❌ Error: No se encontró el archivo de origen."
        except Exception as e:
            return f"❌ Error al copiar: {e}"

    def renombrar_archivo(self, nombre_original, ruta_corta, nombre_nuevo):
        try:
            ruta = self.traducir_ruta(ruta_corta)
            ruta_original = os.path.join(ruta, nombre_original)
            ruta_nueva = os.path.join(ruta, nombre_nuevo)
            os.rename(ruta_original, ruta_nueva)
            return f"✅ Archivo renombrado a: {nombre_nuevo}"
        except FileNotFoundError:
            return f"❌ Error: No se encontró el archivo."
        except Exception as e:
            return f"❌ Error al renombrar: {e}"

    def crear_carpeta(self, nombre_carpeta, ruta_corta):
        try:
            ruta_completa = os.path.join(self.traducir_ruta(ruta_corta), nombre_carpeta)
            os.makedirs(ruta_completa, exist_ok=True)
            return f"✅ Carpeta creada en: {ruta_completa}"
        except Exception as e:
            return f"❌ Error al crear carpeta: {e}"

    def borrar_carpeta(self, nombre_carpeta, ruta_corta):
        try:
            ruta_completa = os.path.join(self.traducir_ruta(ruta_corta), nombre_carpeta)
            shutil.rmtree(ruta_completa)
            return f"✅ Carpeta borrada: {ruta_completa}"
        except FileNotFoundError:
            return f"❌ Error: No se encontró la carpeta."
        except NotADirectoryError:
            return f"❌ Error: '{nombre_carpeta}' no es una carpeta."
        except Exception as e:
            return f"❌ Error al borrar carpeta: {e}"

    # --- Funciones "Inteligentes" ---

    def organizar_carpeta_por_tipo(self, ruta_corta):
        ruta_completa = self.traducir_ruta(ruta_corta)
        if not os.path.isdir(ruta_completa):
            return f"❌ Error: La ruta '{ruta_completa}' no es un directorio válido."

        MAPEO_TIPOS = {
            "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "Documentos": [".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".csv", ".md"],
            "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Musica": [".mp3", ".wav", ".aac", ".flac"],
            "Videos": [".mp4", ".mov", ".avi", ".mkv"],
            "Programas": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
            "Codigo": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".php"]
        }

        mapa_extensiones = {}
        for carpeta, extensiones in MAPEO_TIPOS.items():
            for ext in extensiones:
                mapa_extensiones[ext.lower()] = carpeta

        otros_dir = "Otros"
        contador = {}

        try:
            for nombre_archivo in os.listdir(ruta_completa):
                ruta_archivo_origen = os.path.join(ruta_completa, nombre_archivo)

                if os.path.isfile(ruta_archivo_origen):
                    _, ext = os.path.splitext(nombre_archivo)
                    ext = ext.lower()

                    carpeta_destino_nombre = mapa_extensiones.get(ext, otros_dir)
                    ruta_carpeta_destino = os.path.join(ruta_completa, carpeta_destino_nombre)

                    os.makedirs(ruta_carpeta_destino, exist_ok=True)

                    ruta_archivo_destino = os.path.join(ruta_carpeta_destino, nombre_archivo)

                    if ruta_archivo_origen == ruta_archivo_destino:
                        continue

                    shutil.move(ruta_archivo_origen, ruta_archivo_destino)

                    contador[carpeta_destino_nombre] = contador.get(carpeta_destino_nombre, 0) + 1

            if not contador:
                return f"ℹ️ No se encontraron archivos para organizar en '{ruta_completa}'."

            resumen = ", ".join([f"{v} {k}" for k, v in contador.items()])
            return f"✅ Organización completa: {resumen}."

        except Exception as e:
            return f"❌ Error durante la organización: {e}"

    def buscar_archivos(self, ruta_corta, nombre_archivo=""):
        """
        Busca archivos recursivamente por nombre y devuelve detalles.
        """
        ruta_completa = self.traducir_ruta(ruta_corta)
        if not os.path.isdir(ruta_completa):
            return [], f"❌ Error: La ruta '{ruta_completa}' no es un directorio válido."

        resultados = []  # Ahora será una lista de diccionarios

        patron_nombre = nombre_archivo.lower() if nombre_archivo else "*"

        try:
            for dirpath, _, filenames in os.walk(ruta_completa):
                for filename in filenames:

                    if not fnmatch.fnmatch(filename.lower(), patron_nombre):
                        continue

                    try:
                        ruta_archivo_completa = os.path.join(dirpath, filename)
                        _, ext = os.path.splitext(filename)
                        tamano_bytes = os.path.getsize(ruta_archivo_completa)
                        tamano_kb = tamano_bytes / 1024

                        resultados.append({
                            'ruta': ruta_archivo_completa,
                            'extension': ext if ext else "Sin Extensión",
                            'tamano_kb': tamano_kb
                        })

                    except OSError:
                        continue

            return resultados, f"✅ Búsqueda finalizada. {len(resultados)} archivos encontrados."

        except Exception as e:
            return [], f"❌ Error durante la búsqueda: {e}"


# -----------------------------------------------------------------
# PASO 1.5: El "Compilador" (Intérprete de Comandos)
# -----------------------------------------------------------------

class MiniCompilador:
    """Traduce texto a comandos del GestorDeArchivos."""
    
    def __init__(self, gestor):
        self.gestor = gestor
        self.comandos = {
            "crear": self.cmd_crear,
            "mover": self.cmd_mover,
            "copiar": self.cmd_copiar,
            "renombrar": self.cmd_renombrar,
            "borrar": self.cmd_borrar,
            "organizar": self.cmd_organizar,
            "buscar": self.cmd_buscar,
        }

    def ejecutar(self, codigo):
        tokens = self.tokenizar(codigo)
        if not tokens:
            return "❌ No se detectaron comandos válidos."
        
        comando_raw = tokens[0]
        comando = comando_raw.lower()
        
        if comando in self.comandos:
            try:
                # Pasamos los tokens originales por si algún argumento
                # necesita ser sensible a may/min (ej. "MiFoto.JPG")
                return self.comandos[comando](tokens)
            except Exception as e:
                return f"❌ Error ejecutando '{comando}': {e}"
        else:
            return f"❌ Comando desconocido: {comando}"

    def tokenizar(self, linea):
        """Divide la línea en tokens, respetando las comillas."""
        patron = r'\"[^\"]+\"|\S+' # "texto entre comillas" O cualquier_no_espacio
        # Quita las comillas de los tokens
        return [t.strip('"') for t in re.findall(patron, linea)]

    # === Comandos (Adaptados al GestorDeArchivos original) ===
    
    def cmd_crear(self, tokens):
        # Uso: crear archivo "nombre.txt" en "descargas/a"
        if len(tokens) < 5 or tokens[1].lower() != "archivo":
            return "❌ Uso: crear archivo \"nombre.txt\" en \"descargas/a\""
        nombre = tokens[2]
        ruta = tokens[4]
        return self.gestor.crear_archivo(nombre, ruta)

    def cmd_mover(self, tokens):
        # Uso: mover "nombre.txt" desde "descargas" hasta "documentos"
        if len(tokens) < 6:
            return "❌ Uso: mover \"nombre.txt\" desde \"descargas\" hasta \"documentos\""
        nombre_origen = tokens[1]
        ruta_origen = tokens[3]
        ruta_destino = tokens[5]
        # El gestor original necesita el nombre de destino.
        # Asumimos que el nombre no cambia en este comando simple.
        return self.gestor.mover_archivo(nombre_origen, ruta_origen, nombre_origen, ruta_destino)

    def cmd_copiar(self, tokens):
        # Uso: copiar "nombre.txt" desde "descargas" hasta "documentos"
        if len(tokens) < 6:
            return "❌ Uso: copiar \"nombre.txt\" desde \"descargas\" hasta \"documentos\""
        nombre_origen = tokens[1]
        ruta_origen = tokens[3]
        ruta_destino = tokens[5]
        # Asumimos que el nombre no cambia
        return self.gestor.copiar_archivo(nombre_origen, ruta_origen, nombre_origen, ruta_destino)

    def cmd_renombrar(self, tokens):
        # Uso: renombrar "a.txt" a "b.txt" en "documentos"
        if len(tokens) < 6:
            return "❌ Uso: renombrar \"a.txt\" a \"b.txt\" en \"documentos\""
        nombre_original = tokens[1]
        nombre_nuevo = tokens[3]
        ruta = tokens[5]
        return self.gestor.renombrar_archivo(nombre_original, ruta, nombre_nuevo)

    def cmd_borrar(self, tokens):
        # Uso: borrar "nombre.txt" en "descargas/a"
        if len(tokens) < 4:
            return "❌ Uso: borrar \"nombre.txt\" en \"descargas/a\""
        nombre = tokens[1]
        ruta = tokens[3]
        return self.gestor.borrar_archivo(nombre, ruta)

    def cmd_organizar(self, tokens):
        # Uso: organizar carpeta "descargas"
        if len(tokens) < 3 or tokens[1].lower() != "carpeta":
            return "❌ Uso: organizar carpeta \"descargas\""
        ruta = tokens[2]
        return self.gestor.organizar_carpeta_por_tipo(ruta)

    def cmd_buscar(self, tokens):
        # Uso: buscar "palabra" en "descargas/a"
        if len(tokens) < 4:
            return "❌ Uso: buscar \"palabra\" en \"descargas/a\""
        palabra_clave = tokens[1]
        ruta = tokens[3]
        
        # El gestor original devuelve (lista, mensaje)
        resultados, mensaje = self.gestor.buscar_archivos(ruta, palabra_clave)
        
        if not resultados:
            return mensaje # Devuelve el mensaje de "No encontrado" o "Error"
            
        # Si hay resultados, los formateamos para la consola
        texto_resultados = [f"Ruta: {res['ruta']} ({res['tamano_kb']:.2f} KB)" for res in resultados]
        
        return f"✅ {mensaje}\n" + "\n".join(texto_resultados)


# -----------------------------------------------------------------
# PASO 2: La Aplicación Gráfica (Frontend)
# -----------------------------------------------------------------

# --- Definimos colores para los botones ---
COLOR_BOTON_PELIGRO = ("#D32F2F", "#B71C1C") # (normal, hover)
COLOR_BOTON_EXITO = ("#388E3C", "#1B5E20") # (normal, hover)
COLOR_BOTON_BUSCAR = ("#0277BD", "#01579B") # (normal, hover)


class App(customtkinter.CTk): 
    
    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor
        # --- NUEVO: Instanciamos el compilador ---
        self.compilador = MiniCompilador(self.gestor)
        
        self.title("🤖 Gestor Inteligente de Archivos")
        self.geometry("700x550") # <-- Tamaño ajustado para la nueva pestaña

        # --- Definir modo de apariencia (light/dark) ---
        customtkinter.set_appearance_mode("system") 
        customtkinter.set_default_color_theme("blue") 

        # --- Crear las pestañas (la API es diferente) ---
        self.notebook = customtkinter.CTkTabview(self, width=700)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Emojis en las pestañas ---
        self.tab_organizar = self.notebook.add("Organizar 🧠")
        self.tab_buscar = self.notebook.add("Buscar 🔍")
        self.tab_crear = self.notebook.add("Crear 📄")
        self.tab_mover = self.notebook.add("Mover 📦")
        self.tab_copiar = self.notebook.add("Copiar 📋")
        self.tab_renombrar = self.notebook.add("Renombrar 🏷️")
        self.tab_borrar = self.notebook.add("Borrar 🗑️")
        self.tab_carpetas = self.notebook.add("Carpetas 📁")
        # --- NUEVA PESTAÑA ---
        self.tab_compilador = self.notebook.add("Compilador ⚡")

        
        # Cargar los widgets en cada pestaña
        self.crear_widgets_organizar()
        self.crear_widgets_buscar()
        self.crear_widgets_crear()
        self.crear_widgets_mover()
        self.crear_widgets_copiar()
        self.crear_widgets_renombrar()
        self.crear_widgets_borrar()
        self.crear_widgets_carpetas()
        # --- NUEVO WIDGET ---
        self.crear_widgets_compilador()

        
        # --- Barra de Estado con Colores ---
        self.COLOR_EXITO = ("#1B5E20", "#69F0AE") 
        self.COLOR_ERROR = ("#B71C1C", "#FF5252") 
        
        self.status_label = customtkinter.CTkLabel(self, text="Bienvenido. Listo para operar.", 
                                                   height=24, anchor="w",
                                                   font=customtkinter.CTkFont(size=12))
        
        self.COLOR_NORMAL = self.status_label.cget("text_color") 
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

    # --- Nueva Función Helper para la Barra de Estado ---
    def actualizar_estado(self, mensaje, tipo="auto"):
        """Actualiza la barra de estado con texto y color."""
        self.status_label.configure(text=mensaje)
        
        if tipo == "auto":
            if mensaje.startswith("✅"):
                self.status_label.configure(text_color=self.COLOR_EXITO)
            elif mensaje.startswith("❌") or mensaje.startswith("ℹ️"):
                self.status_label.configure(text_color=self.COLOR_ERROR)
            else:
                self.status_label.configure(text_color=self.COLOR_NORMAL)
        elif tipo == "error":
            self.status_label.configure(text_color=self.COLOR_ERROR)
        elif tipo == "normal":
            self.status_label.configure(text_color=self.COLOR_NORMAL)


    # --- Helpers de Selección (para botones "Examinar...") ---
    
    def seleccionar_archivo(self, entry_nombre, entry_ruta):
        """Abre un diálogo para seleccionar UN archivo y rellena los campos."""
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        ruta, nombre = os.path.split(filepath)
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, nombre)
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, ruta)

    def seleccionar_directorio(self, entry_ruta, entry_nombre=None):
        """Abre un diálogo para seleccionar UN directorio."""
        dirpath = filedialog.askdirectory()
        if not dirpath:
            return
        if entry_nombre:
            ruta, nombre = os.path.split(dirpath)
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, nombre)
            entry_ruta.delete(0, tk.END)
            entry_ruta.insert(0, ruta)
        else:
            entry_ruta.delete(0, tk.END)
            entry_ruta.insert(0, dirpath)

    def seleccionar_guardar_archivo(self, entry_nombre, entry_ruta):
        """Abre un diálogo para GUARDAR un archivo y rellena los campos."""
        nombre_inicial = entry_nombre.get() or "nuevo_archivo.txt"
        filepath = filedialog.asksaveasfilename(
            initialfile=nombre_inicial,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return
        ruta, nombre = os.path.split(filepath)
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, nombre)
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, ruta)

    # --- Pestaña CREAR ---
    def crear_widgets_crear(self):
        frame = customtkinter.CTkFrame(self.tab_crear, fg_color="transparent")
        frame.pack(fill="x", expand=True, padx=10, pady=10)
        
        frame.grid_columnconfigure((1), weight=1)

        customtkinter.CTkLabel(frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.crear_nombre = customtkinter.CTkEntry(frame, width=300)
        self.crear_nombre.grid(row=0, column=1, sticky="ew", padx=5)

        customtkinter.CTkLabel(frame, text="Ruta:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.crear_ruta = customtkinter.CTkEntry(frame, width=300)
        self.crear_ruta.grid(row=1, column=1, sticky="ew", padx=5)

        btn_examinar = customtkinter.CTkButton(frame, text="Examinar...", width=100,
                                         command=lambda: self.seleccionar_guardar_archivo(self.crear_nombre, self.crear_ruta))
        btn_examinar.grid(row=0, column=2, rowspan=2, padx=10)
        
        btn_crear = customtkinter.CTkButton(self.tab_crear, text="Crear Archivo", command=self.accion_gui_crear, height=32)
        btn_crear.pack(pady=20, fill='x', padx=10, ipady=5)

    # --- Pestaña MOVER ---
    def crear_widgets_mover(self):
        # Frame Origen
        frame_origen = customtkinter.CTkFrame(self.tab_mover, fg_color="transparent")
        frame_origen.pack(fill="x", expand=True, pady=5)
        frame_origen.grid_columnconfigure((1), weight=1)

        customtkinter.CTkLabel(frame_origen, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.mover_nombre_origen = customtkinter.CTkEntry(frame_origen, width=300)
        self.mover_nombre_origen.grid(row=0, column=1, sticky="ew", padx=5)
        
        customtkinter.CTkLabel(frame_origen, text="Ruta:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.mover_ruta_origen = customtkinter.CTkEntry(frame_origen, width=300)
        self.mover_ruta_origen.grid(row=1, column=1, sticky="ew", padx=5)

        btn_examinar_o = customtkinter.CTkButton(frame_origen, text="Examinar...", width=100, 
                                                command=lambda: self.seleccionar_archivo(self.mover_nombre_origen, self.mover_ruta_origen))
        btn_examinar_o.grid(row=0, column=2, rowspan=2, padx=10)
        
        # Frame Destino
        frame_destino = customtkinter.CTkFrame(self.tab_mover, fg_color="transparent")
        frame_destino.pack(fill="x", expand=True, pady=5)
        frame_destino.grid_columnconfigure((1), weight=1)
        
        customtkinter.CTkLabel(frame_destino, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.mover_nombre_destino = customtkinter.CTkEntry(frame_destino, width=300)
        self.mover_nombre_destino.grid(row=0, column=1, sticky="ew", padx=5)
        
        customtkinter.CTkLabel(frame_destino, text="Ruta:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.mover_ruta_destino = customtkinter.CTkEntry(frame_destino, width=300)
        self.mover_ruta_destino.grid(row=1, column=1, sticky="ew", padx=5)
        
        btn_examinar_d = customtkinter.CTkButton(frame_destino, text="Examinar...", width=100,
                                               command=lambda: self.seleccionar_directorio(self.mover_ruta_destino))
        btn_examinar_d.grid(row=1, column=2, padx=10)

        btn_mover = customtkinter.CTkButton(self.tab_mover, text="Mover Archivo", command=self.accion_gui_mover, height=32)
        btn_mover.pack(pady=10, fill='x', padx=10, ipady=5)
        
    # --- Pestaña COPIAR ---
    def crear_widgets_copiar(self):
        # Frame Origen
        frame_origen = customtkinter.CTkFrame(self.tab_copiar, fg_color="transparent")
        frame_origen.pack(fill="x", expand=True, pady=5)
        frame_origen.grid_columnconfigure((1), weight=1)

        customtkinter.CTkLabel(frame_origen, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.copiar_nombre_origen = customtkinter.CTkEntry(frame_origen, width=300)
        self.copiar_nombre_origen.grid(row=0, column=1, sticky="ew", padx=5)
        
        customtkinter.CTkLabel(frame_origen, text="Ruta:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.copiar_ruta_origen = customtkinter.CTkEntry(frame_origen, width=300)
        self.copiar_ruta_origen.grid(row=1, column=1, sticky="ew", padx=5)

        btn_examinar_o = customtkinter.CTkButton(frame_origen, text="Examinar...", width=100,
                                               command=lambda: self.seleccionar_archivo(self.copiar_nombre_origen, self.copiar_ruta_origen))
        btn_examinar_o.grid(row=0, column=2, rowspan=2, padx=10)
        
        # Frame Destino
        frame_destino = customtkinter.CTkFrame(self.tab_copiar, fg_color="transparent")
        frame_destino.pack(fill="x", expand=True, pady=5)
        frame_destino.grid_columnconfigure((1), weight=1)
        
        customtkinter.CTkLabel(frame_destino, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.copiar_nombre_destino = customtkinter.CTkEntry(frame_destino, width=300)
        self.copiar_nombre_destino.grid(row=0, column=1, sticky="ew", padx=5)
        
        customtkinter.CTkLabel(frame_destino, text="Ruta:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.copiar_ruta_destino = customtkinter.CTkEntry(frame_destino, width=300)
        self.copiar_ruta_destino.grid(row=1, column=1, sticky="ew", padx=5)
        
        btn_examinar_d = customtkinter.CTkButton(frame_destino, text="Examinar...", width=100,
                                               command=lambda: self.seleccionar_directorio(self.copiar_ruta_destino))
        btn_examinar_d.grid(row=1, column=2, padx=10)

        btn_copiar = customtkinter.CTkButton(self.tab_copiar, text="Copiar Archivo", command=self.accion_gui_copiar, height=32)
        btn_copiar.pack(pady=10, fill='x', padx=10, ipady=5)

    # --- Pestaña RENOMBRAR ---
    def crear_widgets_renombrar(self):
        # Frame Origen
        frame_origen = customtkinter.CTkFrame(self.tab_renombrar, fg_color="transparent")
        frame_origen.pack(fill="x", expand=True, pady=5)
        frame_origen.grid_columnconfigure((1), weight=1)
        
        customtkinter.CTkLabel(frame_origen, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.renombrar_nombre_original = customtkinter.CTkEntry(frame_origen, width=300)
        self.renombrar_nombre_original.grid(row=0, column=1, sticky="ew", padx=5)
        
        customtkinter.CTkLabel(frame_origen, text="Ruta:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.renombrar_ruta = customtkinter.CTkEntry(frame_origen, width=300)
        self.renombrar_ruta.grid(row=1, column=1, sticky="ew", padx=5)

        btn_examinar_o = customtkinter.CTkButton(frame_origen, text="Examinar...", width=100, 
                                               command=lambda: self.seleccionar_archivo(self.renombrar_nombre_original, self.renombrar_ruta))
        btn_examinar_o.grid(row=0, column=2, rowspan=2, padx=10)
        
        # Frame Nuevo Nombre
        frame_nuevo = customtkinter.CTkFrame(self.tab_renombrar, fg_color="transparent")
        frame_nuevo.pack(fill="x", expand=True, pady=5)
        frame_nuevo.grid_columnconfigure((1), weight=1)
        
        customtkinter.CTkLabel(frame_nuevo, text="Nuevo Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.renombrar_nombre_nuevo = customtkinter.CTkEntry(frame_nuevo, width=300)
        self.renombrar_nombre_nuevo.grid(row=0, column=1, sticky="ew", padx=5)
        
        btn_renombrar = customtkinter.CTkButton(self.tab_renombrar, text="Renombrar Archivo", command=self.accion_gui_renombrar, height=32)
        btn_renombrar.pack(pady=20, fill='x', padx=10, ipady=5)
        
    # --- Pestaña BORRAR ---
    def crear_widgets_borrar(self):
        frame = customtkinter.CTkFrame(self.tab_borrar, fg_color="transparent")
        frame.pack(fill="x", expand=True, padx=10, pady=10)
        frame.grid_columnconfigure((1), weight=1)

        customtkinter.CTkLabel(frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.borrar_nombre = customtkinter.CTkEntry(frame, width=300)
        self.borrar_nombre.grid(row=0, column=1, sticky="ew", padx=5)
        
        customtkinter.CTkLabel(frame, text="Ruta:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.borrar_ruta = customtkinter.CTkEntry(frame, width=300)
        self.borrar_ruta.grid(row=1, column=1, sticky="ew", padx=5)

        btn_examinar = customtkinter.CTkButton(frame, text="Examinar...", width=100, 
                                               command=lambda: self.seleccionar_archivo(self.borrar_nombre, self.borrar_ruta))
        btn_examinar.grid(row=0, column=2, rowspan=2, padx=10)
        
        btn_borrar = customtkinter.CTkButton(self.tab_borrar, text="Borrar Archivo", 
                                             command=self.accion_gui_borrar, height=32,
                                             fg_color=COLOR_BOTON_PELIGRO[0], 
                                             hover_color=COLOR_BOTON_PELIGRO[1])
        btn_borrar.pack(pady=20, fill='x', padx=10, ipady=5)

    # --- Pestaña CARPETAS ---
    def crear_widgets_carpetas(self):
        # Sección Crear
        frame_crear = customtkinter.CTkFrame(self.tab_carpetas, fg_color="transparent")
        frame_crear.pack(fill="x", expand=True, pady=5)
        frame_crear.grid_columnconfigure((1), weight=1)
        
        customtkinter.CTkLabel(frame_crear, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.carpeta_crear_nombre = customtkinter.CTkEntry(frame_crear, width=300)
        self.carpeta_crear_nombre.grid(row=0, column=1, sticky="ew", padx=5)
        
        customtkinter.CTkLabel(frame_crear, text="Ruta:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.carpeta_crear_ruta = customtkinter.CTkEntry(frame_crear, width=300)
        self.carpeta_crear_ruta.grid(row=1, column=1, sticky="ew", padx=5)

        btn_examinar_c = customtkinter.CTkButton(frame_crear, text="Examinar...", width=100,
                                               command=lambda: self.seleccionar_directorio(self.carpeta_crear_ruta))
        btn_examinar_c.grid(row=1, column=2, padx=10)
        
        btn_crear = customtkinter.CTkButton(frame_crear, text="Crear Carpeta", command=self.accion_gui_crear_carpeta)
        btn_crear.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 5), padx=5)
        
        # Sección Borrar
        frame_borrar = customtkinter.CTkFrame(self.tab_carpetas, fg_color="transparent")
        frame_borrar.pack(fill="x", expand=True, pady=10)
        frame_borrar.grid_columnconfigure((1), weight=1)
        
        customtkinter.CTkLabel(frame_borrar, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.carpeta_borrar_nombre = customtkinter.CTkEntry(frame_borrar, width=300)
        self.carpeta_borrar_nombre.grid(row=0, column=1, sticky="ew", padx=5)
        
        customtkinter.CTkLabel(frame_borrar, text="Ruta:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.carpeta_borrar_ruta = customtkinter.CTkEntry(frame_borrar, width=300)
        self.carpeta_borrar_ruta.grid(row=1, column=1, sticky="ew", padx=5)

        btn_examinar_b = customtkinter.CTkButton(frame_borrar, text="Examinar...", width=100,
                                               command=lambda: self.seleccionar_directorio(self.carpeta_borrar_ruta, self.carpeta_borrar_nombre))
        btn_examinar_b.grid(row=0, column=2, rowspan=2, padx=10)
        
        btn_borrar = customtkinter.CTkButton(frame_borrar, text="Borrar Carpeta", 
                                             command=self.accion_gui_borrar_carpeta,
                                             fg_color=COLOR_BOTON_PELIGRO[0], 
                                             hover_color=COLOR_BOTON_PELIGRO[1])
        btn_borrar.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 5), padx=5)

    # --- Pestaña ORGANIZAR ---
    def crear_widgets_organizar(self):
        frame = customtkinter.CTkFrame(self.tab_organizar, fg_color="transparent")
        frame.pack(fill="x", expand=True, padx=10, pady=10)
        frame.grid_columnconfigure((0), weight=1)

        info_text = "Esta función escaneará la ruta que indiques y moverá los archivos\na subcarpetas (Imagenes, Documentos, etc.) según su tipo."
        customtkinter.CTkLabel(frame, text=info_text, justify=tk.LEFT).grid(row=0, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

        customtkinter.CTkLabel(frame, text="Ruta a organizar:").grid(row=1, column=0, columnspan=2, sticky="w", pady=5, padx=5)
        
        self.organizar_ruta = customtkinter.CTkEntry(frame, width=300)
        self.organizar_ruta.insert(0, "descargas") # Sugerencia por defecto
        self.organizar_ruta.grid(row=2, column=0, sticky="ew", padx=5)
        
        btn_examinar = customtkinter.CTkButton(frame, text="Examinar...", width=100,
                                         command=lambda: self.seleccionar_directorio(self.organizar_ruta))
        btn_examinar.grid(row=2, column=1, padx=(10, 5))
        
        btn_organizar = customtkinter.CTkButton(self.tab_organizar, text="¡Organizar!", 
                                                command=self.accion_gui_organizar, height=32,
                                                fg_color=COLOR_BOTON_EXITO[0],
                                                hover_color=COLOR_BOTON_EXITO[1])
        btn_organizar.pack(pady=20, fill='x', padx=10, ipady=5)

    # --- Pestaña BUSCAR (con botón Limpiar) ---
    def crear_widgets_buscar(self):
        # 1. Frame de Criterios
        frame_criterios = customtkinter.CTkFrame(self.tab_buscar, fg_color="transparent")
        frame_criterios.pack(fill="x", expand=False, padx=10, pady=10)
        frame_criterios.grid_columnconfigure((1), weight=1) # Columna de Entry se expande

        # Ruta
        customtkinter.CTkLabel(frame_criterios, text="Buscar en:").grid(row=0, column=0, sticky="w", padx=5, pady=8)
        self.buscar_ruta = customtkinter.CTkEntry(frame_criterios, placeholder_text="ej: documentos")
        self.buscar_ruta.insert(0, "descargas") # Sugerencia
        self.buscar_ruta.grid(row=0, column=1, sticky="ew", padx=5)
        btn_examinar = customtkinter.CTkButton(frame_criterios, text="Examinar...", width=100,
                                         command=lambda: self.seleccionar_directorio(self.buscar_ruta))
        btn_examinar.grid(row=0, column=2, padx=10)

        # Nombre (Ahora el único filtro)
        customtkinter.CTkLabel(frame_criterios, text="Nombre:").grid(row=1, column=0, sticky="w", padx=5, pady=8)
        self.buscar_nombre = customtkinter.CTkEntry(frame_criterios, placeholder_text="ej: reporte.docx o *.txt (acepta comodines)")
        self.buscar_nombre.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5)

        # 2. Frame de Botones
        frame_botones = customtkinter.CTkFrame(self.tab_buscar, fg_color="transparent")
        frame_botones.pack(pady=10, fill='x', padx=10)

        btn_buscar = customtkinter.CTkButton(frame_botones, text="Buscar Archivos", 
                                             command=self.accion_gui_buscar, height=32,
                                             fg_color=COLOR_BOTON_BUSCAR[0],
                                             hover_color=COLOR_BOTON_BUSCAR[1])
        btn_buscar.pack(side="left", fill='x', expand=True, ipady=5, padx=(0, 5))

        # --- Nuevo Botón Limpiar ---
        btn_limpiar = customtkinter.CTkButton(frame_botones, text="Limpiar", 
                                              command=self.accion_gui_buscar_limpiar, height=32,
                                              width=100, fg_color="gray50", hover_color="gray30")
        btn_limpiar.pack(side="left", ipady=5, padx=(5, 0))

        # 3. Frame de Resultados
        customtkinter.CTkLabel(self.tab_buscar, text="Resultados:").pack(fill="x", padx=10, anchor="w", pady=(5,0))
        self.buscar_resultados_text = customtkinter.CTkTextbox(self.tab_buscar, height=200, state="disabled")
        self.buscar_resultados_text.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    # --- NUEVA PESTAÑA: COMPILADOR ---
    def crear_widgets_compilador(self):
        """Crea los widgets para la nueva pestaña del compilador."""
        # Frame principal que contendrá todo
        frame = customtkinter.CTkFrame(self.tab_compilador, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configurar grid
        frame.grid_rowconfigure(2, weight=1) # El área de salida se expande
        frame.grid_columnconfigure(0, weight=1) # Todo se expande a lo ancho

        # 1. Caja de entrada de texto
        self.compilador_input = customtkinter.CTkTextbox(frame, height=120)
        self.compilador_input.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.compilador_input.insert("1.0", 'crear archivo "prueba.txt" en "descargas"\n' + 
                                            'buscar "prueba.txt" en "descargas"\n' +
                                            'borrar "prueba.txt" en "descargas"')

        # 2. Botón de Ejecutar
        self.compilador_btn = customtkinter.CTkButton(frame, text="Ejecutar Comando", 
                                                      command=self.accion_gui_compilador,
                                                      height=32)
        self.compilador_btn.grid(row=1, column=0, pady=10, padx=5, sticky="ew", ipady=5)

        # 3. Caja de salida de texto (consola)
        self.compilador_output = customtkinter.CTkTextbox(frame, state="disabled")
        self.compilador_output.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # 4. Info de ayuda
        info = "Ayuda: El compilador ejecuta UNA línea a la vez."
        customtkinter.CTkLabel(frame, text=info, font=customtkinter.CTkFont(size=11, slant="italic"))
        self.compilador_output.grid(row=3, column=0, sticky="ew", padx=5, pady=(5,0))


    # --- Acciones de los Botones (Callbacks) ---
    # --- Todas las acciones ahora usan self.actualizar_estado() ---
    
    def accion_gui_crear(self):
        nombre = self.crear_nombre.get()
        ruta = self.crear_ruta.get()
        if not nombre or not ruta:
            self.actualizar_estado("❌ Error: 'Nombre' y 'Ruta' no pueden estar vacíos.")
            return
        resultado = self.gestor.crear_archivo(nombre, ruta)
        self.actualizar_estado(resultado)

    def accion_gui_mover(self):
        n_origen = self.mover_nombre_origen.get()
        r_origen = self.mover_ruta_origen.get()
        n_destino = self.mover_nombre_destino.get() or n_origen # Usar nombre original si está vacío
        r_destino = self.mover_ruta_destino.get()
        if not n_origen or not r_origen or not r_destino:
            self.actualizar_estado("❌ Error: Los campos de origen y la ruta de destino son obligatorios.")
            return
        resultado = self.gestor.mover_archivo(n_origen, r_origen, n_destino, r_destino)
        self.actualizar_estado(resultado)

    def accion_gui_borrar(self):
        nombre = self.borrar_nombre.get()
        ruta = self.borrar_ruta.get()
        if not nombre or not ruta:
            self.actualizar_estado("❌ Error: 'Nombre' y 'Ruta' no pueden estar vacíos.")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres borrar el ARCHIVO '{nombre}' de '{ruta}'?"):
            resultado = self.gestor.borrar_archivo(nombre, ruta)
            self.actualizar_estado(resultado)
        else:
            self.actualizar_estado("ℹ️ Operación de borrado cancelada.", "normal")

    def accion_gui_copiar(self):
        n_origen = self.copiar_nombre_origen.get()
        r_origen = self.copiar_ruta_origen.get()
        n_destino = self.copiar_nombre_destino.get() or n_origen # Usar nombre original si está vacío
        r_destino = self.copiar_ruta_destino.get()
        if not n_origen or not r_origen or not r_destino:
            self.actualizar_estado("❌ Error: Los campos de origen y la ruta de destino son obligatorios.")
            return
        resultado = self.gestor.copiar_archivo(n_origen, r_origen, n_destino, r_destino)
        self.actualizar_estado(resultado)

    def accion_gui_renombrar(self):
        n_original = self.renombrar_nombre_original.get()
        ruta = self.renombrar_ruta.get()
        n_nuevo = self.renombrar_nombre_nuevo.get()
        if not n_original or not ruta or not n_nuevo:
            self.actualizar_estado("❌ Error: Todos los campos son obligatorios.")
            return
        resultado = self.gestor.renombrar_archivo(n_original, ruta, n_nuevo)
        self.actualizar_estado(resultado)

    def accion_gui_crear_carpeta(self):
        nombre = self.carpeta_crear_nombre.get()
        ruta = self.carpeta_crear_ruta.get()
        if not nombre or not ruta:
            self.actualizar_estado("❌ Error: 'Nombre' y 'Ruta' no pueden estar vacíos.")
            return
        resultado = self.gestor.crear_carpeta(nombre, ruta)
        self.actualizar_estado(resultado)

    def accion_gui_borrar_carpeta(self):
        nombre = self.carpeta_borrar_nombre.get()
        ruta = self.carpeta_borrar_ruta.get()
        if not nombre or not ruta:
            self.actualizar_estado("❌ Error: 'Nombre' y 'Ruta' no pueden estar vacíos.")
            return
        
        msg = f"¡PELIGRO!\n\n¿Estás seguro de que quieres borrar la CARPETA '{nombre}' de '{ruta}'?\n\n¡ESTO BORRARÁ TODO SU CONTENIDO!"
        if messagebox.askyesno("CONFIRMACIÓN MUY IMPORTANTE", msg):
            resultado = self.gestor.borrar_carpeta(nombre, ruta)
            self.actualizar_estado(resultado)
        else:
            self.actualizar_estado("ℹ️ Operación de borrado de carpeta cancelada.", "normal")
            
    def accion_gui_organizar(self):
        ruta = self.organizar_ruta.get()
        if not ruta:
            self.actualizar_estado("❌ Error: Debes seleccionar una ruta para organizar.")
            return
        msg = f"¿Estás seguro de que quieres organizar automáticamente la carpeta '{ruta}'?\n\nLos archivos se moverán a subcarpetas por tipo."
        if messagebox.askyesno("Confirmar Organización", msg):
            self.actualizar_estado("Organizando, por favor espera...", "normal")
            self.update() # Forzar actualización de la GUI
            resultado = self.gestor.organizar_carpeta_por_tipo(ruta)
            self.actualizar_estado(resultado)
        else:
            self.actualizar_estado("ℹ️ Organización cancelada.", "normal")

    def accion_gui_buscar(self):
        """Acción de la pestaña BUSCAR (Modificada para nuevos detalles)."""
        self.actualizar_estado("Buscando, por favor espera...", "normal")
        self.update() # Forzar actualización
        
        self.buscar_resultados_text.configure(state="normal")
        self.buscar_resultados_text.delete("1.0", tk.END)

        ruta = self.buscar_ruta.get()
        nombre = self.buscar_nombre.get()
        
        if not ruta:
            self.actualizar_estado("❌ Error: Debes especificar una ruta para 'Buscar en:'.")
            self.buscar_resultados_text.configure(state="disabled")
            return

        resultados, mensaje = self.gestor.buscar_archivos(ruta, nombre)

        self.actualizar_estado(mensaje)
        if resultados:
            texto_resultados = []
            for res in resultados:
                tamano_formateado = f"{res['tamano_kb']:.2f} KB"
                linea = f"Ruta: {res['ruta']}\n\tExt: {res['extension']}  |  Tamaño: {tamano_formateado}\n"
                texto_resultados.append(linea)
            
            self.buscar_resultados_text.insert("1.0", "\n".join(texto_resultados))
            
        else:
            if "0 archivos encontrados" in mensaje:
                self.buscar_resultados_text.insert("1.0", "No se encontraron archivos con esos criterios.")
            else:
                self.buscar_resultados_text.insert("1.0", mensaje)
        
        self.buscar_resultados_text.configure(state="disabled") 

    def accion_gui_buscar_limpiar(self):
        """Limpia los campos y resultados de búsqueda."""
        self.buscar_nombre.delete(0, tk.END)
        self.buscar_resultados_text.configure(state="normal")
        self.buscar_resultados_text.delete("1.0", tk.END)
        self.buscar_resultados_text.configure(state="disabled")
        self.actualizar_estado("Campos de búsqueda limpiados.", "normal")

    # --- NUEVA ACCIÓN: COMPILADOR ---
    def accion_gui_compilador(self):
        """Ejecuta el comando de la pestaña del compilador."""
        # Obtiene solo la línea actual del cursor
        codigo = self.compilador_input.get("insert linestart", "insert lineend").strip()
        
        if not codigo:
            self.actualizar_estado("❌ Escribe un comando en la pestaña del compilador.", "error")
            return
            
        # Ejecuta el comando
        resultado = self.compilador.ejecutar(codigo)
        
        # Muestra el resultado en la consola
        self.compilador_output.configure(state="normal")
        self.compilador_output.insert(tk.END, f">> {codigo}\n")
        self.compilador_output.insert(tk.END, f"{resultado}\n\n")
        self.compilador_output.configure(state="disabled")
        self.compilador_output.see(tk.END) # Auto-scroll
        
        # Actualiza la barra de estado principal
        self.actualizar_estado(f"Comando ejecutado: {resultado.split(' ')[0]}")


# -----------------------------------------------------------------
# PASO 3: Ejecutar la aplicación
# -----------------------------------------------------------------
if __name__ == "__main__":
    gestor_logico = GestorDeArchivos() # 1. Crea el backend
    app = App(gestor_logico)           # 2. Crea el frontend y le pasa el backend
    app.mainloop()                     # 3. Inicia la aplicación