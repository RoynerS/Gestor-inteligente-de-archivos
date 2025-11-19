# 🤖 Gestor Inteligente de Archivos

Una aplicación de escritorio moderna y completa para gestionar archivos y carpetas de forma intuitiva, con una interfaz gráfica elegante y un sistema de comandos integrado.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación de Clases](#-documentación-de-clases)
- [Comandos del Compilador](#-comandos-del-compilador)
- [Ejemplos](#-ejemplos)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)

## ✨ Características

### Operaciones Básicas
- ✅ **Crear archivos** - Crea archivos nuevos en cualquier ubicación
- 📦 **Mover archivos** - Mueve archivos entre directorios
- 📋 **Copiar archivos** - Duplica archivos manteniendo el original
- 🏷️ **Renombrar archivos** - Cambia el nombre de archivos existentes
- 🗑️ **Borrar archivos** - Elimina archivos de forma segura (con confirmación)
- 📁 **Gestión de carpetas** - Crea y elimina carpetas completas

### Funciones Inteligentes
- 🧠 **Organización automática** - Organiza archivos por tipo en subcarpetas automáticamente
- 🔍 **Búsqueda avanzada** - Busca archivos recursivamente con soporte para comodines
- ⚡ **Compilador de comandos** - Ejecuta comandos escritos en lenguaje natural

### Interfaz de Usuario
- 🎨 Interfaz moderna con CustomTkinter
- 📑 Sistema de pestañas organizadas por funcionalidad
- 🎯 Barra de estado con feedback visual (colores según resultado)
- 🔘 Botones de "Examinar" para selección fácil de archivos/carpetas
- 💬 Confirmaciones para operaciones destructivas

## 📦 Requisitos

- Python 3.7 o superior
- Las siguientes librerías (se instalan automáticamente con pip):
  - `customtkinter` - Interfaz gráfica moderna
  - `tkinter` - Incluido en Python estándar (puede requerir instalación en Linux)

## 🚀 Instalación

1. **Clona o descarga el proyecto**

2. **Instala las dependencias:**
```bash
pip install customtkinter
```

3. **Ejecuta la aplicación:**
```bash
python definitivo.py
```

## 💻 Uso

### Interfaz Gráfica

La aplicación se abre con una ventana principal dividida en pestañas:

1. **Organizar 🧠**: Organiza archivos de una carpeta por tipo
2. **Buscar 🔍**: Busca archivos por nombre (soporta comodines)
3. **Crear 📄**: Crea nuevos archivos
4. **Mover 📦**: Mueve archivos entre ubicaciones
5. **Copiar 📋**: Copia archivos
6. **Renombrar 🏷️**: Renombra archivos
7. **Borrar 🗑️**: Elimina archivos (con confirmación)
8. **Carpetas 📁**: Crea o borra carpetas
9. **Compilador ⚡**: Ejecuta comandos en texto

### Atajos de Rutas

Puedes usar nombres cortos en lugar de rutas completas:

- `descargas` → Carpeta de Descargas del usuario
- `escritorio` → Escritorio del usuario
- `documentos` → Carpeta de Documentos
- `imágenes` → Carpeta de Imágenes
- `musica` → Carpeta de Música
- `videos` → Carpeta de Videos
- `.` → Directorio actual

**Ejemplo:** En lugar de escribir `C:\Users\TuUsuario\Downloads\archivo.txt`, puedes usar `descargas/archivo.txt`

## 📚 Estructura del Proyecto

```
Compilador/
├── definitivo.py    # Código fuente principal
└── README.md        # Este archivo
```

## 📖 Documentación de Clases

### `GestorDeArchivos`

Clase principal que maneja todas las operaciones de archivos y carpetas.

#### Métodos Principales

- `traducir_ruta(ruta_corta)`: Convierte rutas cortas a rutas completas
- `crear_archivo(nombre, ruta)`: Crea un archivo nuevo
- `mover_archivo(nombre_origen, ruta_origen, nombre_destino, ruta_destino)`: Mueve un archivo
- `copiar_archivo(nombre_origen, ruta_origen, nombre_destino, ruta_destino)`: Copia un archivo
- `renombrar_archivo(nombre_original, ruta, nombre_nuevo)`: Renombra un archivo
- `borrar_archivo(nombre, ruta)`: Elimina un archivo
- `crear_carpeta(nombre, ruta)`: Crea una carpeta
- `borrar_carpeta(nombre, ruta)`: Elimina una carpeta y su contenido
- `organizar_carpeta_por_tipo(ruta)`: Organiza archivos por tipo
- `buscar_archivos(ruta, nombre_archivo="")`: Busca archivos recursivamente

### `MiniCompilador`

Intérprete que traduce comandos en texto a operaciones del GestorDeArchivos.

#### Métodos Principales

- `ejecutar(codigo)`: Ejecuta un comando escrito en texto
- `tokenizar(linea)`: Divide una línea en tokens respetando comillas

### `App`

Aplicación gráfica principal construida con CustomTkinter.

#### Métodos Principales

- `actualizar_estado(mensaje, tipo)`: Actualiza la barra de estado
- `seleccionar_archivo(entry_nombre, entry_ruta)`: Abre diálogo de selección de archivo
- `seleccionar_directorio(entry_ruta, entry_nombre)`: Abre diálogo de selección de directorio
- Métodos `accion_gui_*`: Handlers para los botones de cada pestaña

## ⚡ Comandos del Compilador

El compilador permite ejecutar comandos escritos en lenguaje natural. Todos los comandos deben estar en una sola línea.

### Sintaxis de Comandos

#### Crear archivo
```
crear archivo "nombre.txt" en "descargas"
```

#### Mover archivo
```
mover "archivo.txt" desde "descargas" hasta "documentos"
```

#### Copiar archivo
```
copiar "archivo.txt" desde "descargas" hasta "documentos"
```

#### Renombrar archivo
```
renombrar "archivo_viejo.txt" a "archivo_nuevo.txt" en "documentos"
```

#### Borrar archivo
```
borrar "archivo.txt" en "descargas"
```

#### Organizar carpeta
```
organizar carpeta "descargas"
```

#### Buscar archivos
```
buscar "*.txt" en "documentos"
buscar "reporte" en "descargas"
```

### Notas sobre el Compilador

- Los nombres de archivos y rutas con espacios deben ir entre comillas dobles
- El compilador ejecuta UNA línea a la vez (la línea donde está el cursor)
- Los comandos son case-insensitive (no distinguen mayúsculas/minúsculas)
- Soporta todos los atajos de rutas mencionados anteriormente

## 📝 Ejemplos

### Ejemplo 1: Organizar Descargas

1. Abre la pestaña **Organizar 🧠**
2. Escribe `descargas` en el campo de ruta (o usa el botón "Examinar")
3. Haz clic en **¡Organizar!**
4. Los archivos se moverán automáticamente a subcarpetas según su tipo

### Ejemplo 2: Buscar Archivos PDF

1. Abre la pestaña **Buscar 🔍**
2. Escribe `documentos` en "Buscar en:"
3. Escribe `*.pdf` en "Nombre:"
4. Haz clic en **Buscar Archivos**
5. Verás todos los PDFs encontrados con sus rutas y tamaños

### Ejemplo 3: Usar el Compilador

1. Abre la pestaña **Compilador ⚡**
2. Escribe en el área de texto:
   ```
   crear archivo "prueba.txt" en "descargas"
   ```
3. Coloca el cursor en esa línea
4. Haz clic en **Ejecutar Comando**
5. Verás el resultado en la consola de salida

### Ejemplo 4: Mover y Renombrar

1. Abre la pestaña **Mover 📦**
2. Selecciona un archivo de origen usando "Examinar"
3. Selecciona la carpeta de destino
4. Haz clic en **Mover Archivo**
5. Luego usa **Renombrar 🏷️** para cambiarle el nombre si es necesario

## 🛠️ Tecnologías Utilizadas

- **Python 3**: Lenguaje de programación principal
- **CustomTkinter**: Librería para interfaz gráfica moderna
- **Tkinter**: Librería base para GUI (incluida en Python)
- **os**: Módulo estándar para operaciones del sistema operativo
- **shutil**: Módulo estándar para operaciones de archivos avanzadas
- **re**: Módulo estándar para expresiones regulares (tokenización)
- **fnmatch**: Módulo estándar para coincidencia de patrones (búsqueda con comodines)

## 🔒 Seguridad

- ⚠️ Las operaciones de borrado (archivos y carpetas) requieren confirmación
- ⚠️ El borrado de carpetas elimina TODO su contenido de forma permanente
- ✅ Todas las operaciones muestran mensajes de éxito/error claros
- ✅ La barra de estado proporciona feedback visual inmediato

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras un bug o tienes una sugerencia, no dudes en reportarlo.

## 📧 Soporte

Para preguntas o problemas, revisa la documentación de las clases en el código fuente o consulta los ejemplos proporcionados.

---

**Desarrollado con ❤️ usando Python y CustomTkinter**

