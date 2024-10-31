import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

# Archivo para almacenar usuarios y contraseñas
FILE_USERS = "usuarios.txt"
# Directorios para almacenar historias clínicas y producción
HISTORIAS_CLINICAS_DIR = "historias_clinicas"
PRODUCCION_DIR = "produccion"

# Crear los directorios si no existen
os.makedirs(HISTORIAS_CLINICAS_DIR, exist_ok=True)
os.makedirs(PRODUCCION_DIR, exist_ok=True)

# Función para registrar un nuevo usuario
def registrar():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if not usuario or not contrasena:
        messagebox.showwarning("Advertencia", "Usuario y contraseña no pueden estar vacíos.")
        return

    # Verificar si el usuario ya existe
    if os.path.exists(FILE_USERS):
        with open(FILE_USERS, "r") as file:
            for linea in file:
                nombre, _ = linea.strip().split(",")
                if nombre == usuario:
                    messagebox.showwarning("Advertencia", "El usuario ya existe. Intente con otro nombre.")
                    return

    # Guardar el nuevo usuario
    with open(FILE_USERS, "a") as file:
        file.write(f"{usuario},{contrasena}\n")
    messagebox.showinfo("Registro", "Usuario registrado con éxito.")
    entry_usuario.delete(0, tk.END)
    entry_contrasena.delete(0, tk.END)

# Función para iniciar sesión
def login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if not usuario or not contrasena:
        messagebox.showwarning("Advertencia", "Usuario y contraseña no pueden estar vacíos.")
        return False

    # Comprobar si el usuario existe y la contraseña es correcta
    if os.path.exists(FILE_USERS):
        with open(FILE_USERS, "r") as file:
            for linea in file:
                nombre, passw = linea.strip().split(",")
                if nombre == usuario and passw == contrasena:
                    messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso.")
                    mostrar_frame(frame_menu_principal)
                    return True
    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    return False

# Función para cambiar entre diferentes secciones (frames)
def mostrar_frame(frame):
    frame.tkraise()

# Función para la historia clínica de la vaca
def historia_clinica():
    nombre_vaca = simpledialog.askstring("Historia Clínica", "Ingrese el nombre o ID de la vaca:")
    if not nombre_vaca:
        return
    global archivo_vaca
    archivo_vaca = os.path.join(HISTORIAS_CLINICAS_DIR, f"{nombre_vaca}.txt")
    label_historia_clinica.config(text=f"--- Historia Clínica de {nombre_vaca} ---")
    mostrar_frame(frame_historia_clinica)
    actualizar_lista_registros_clinicos()

# Función para agregar un registro clínico en el mismo frame
def agregar_registro_clinico():
    fecha = entry_fecha_clinica.get()
    descripcion = text_descripcion_clinica.get("1.0", tk.END).strip()  # Obtener texto del widget Text

    if not fecha or not descripcion:
        messagebox.showwarning("Advertencia", "Fecha y descripción no pueden estar vacíos.")
        return

    with open(archivo_vaca, "a") as file:
        file.write(f"Fecha: {fecha}\nDescripción: {descripcion}\n---\n")
    
    messagebox.showinfo("Registro Clínico", "Registro agregado con éxito.")
    entry_fecha_clinica.delete(0, tk.END)
    text_descripcion_clinica.delete("1.0", tk.END)  # Limpiar el Text
    actualizar_lista_registros_clinicos()

# Función para actualizar la lista de registros clínicos en el frame
def actualizar_lista_registros_clinicos():
    listbox_clinica.delete(0, tk.END)
    if os.path.exists(archivo_vaca):
        with open(archivo_vaca, "r") as file:
            registros = file.readlines()
        registros_completos = ["".join(registros[i:i+3]).strip() for i in range(0, len(registros), 3)]
        for registro in registros_completos:
            listbox_clinica.insert(tk.END, registro)
    else:
        listbox_clinica.insert(tk.END, "No hay registros clínicos.")

# Función para eliminar un registro clínico
def eliminar_registro_clinico():
    seleccion = listbox_clinica.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")
        return

    # Obtener el índice del registro seleccionado
    index = seleccion[0]

    # Leer todos los registros
    with open(archivo_vaca, "r") as file:
        registros = file.readlines()

    # Identificar el inicio y fin del registro seleccionado
    inicio = index * 3
    fin = inicio + 3

    # Eliminar el registro seleccionado
    del registros[inicio:fin]

    # Escribir de nuevo el archivo sin el registro eliminado
    with open(archivo_vaca, "w") as file:
        file.writelines(registros)

    messagebox.showinfo("Eliminar Registro", "Registro eliminado con éxito.")
    actualizar_lista_registros_clinicos()

# Función para la producción de la vaca
def produccion():
    nombre_vaca = simpledialog.askstring("Producción", "Ingrese el nombre o ID de la vaca:")
    if not nombre_vaca:
        return
    global archivo_produccion
    archivo_produccion = os.path.join(PRODUCCION_DIR, f"{nombre_vaca}.txt")
    label_produccion.config(text=f"--- Producción de {nombre_vaca} ---")
    mostrar_frame(frame_produccion)
    actualizar_lista_registros_produccion()

# Función para agregar un registro de producción en el mismo frame
def agregar_registro_produccion():
    fecha = entry_fecha_produccion.get()
    cantidad = entry_cantidad_produccion.get()
    tipo_produccion = tipo_produccion_var.get()  # Obtener tipo de producción seleccionado

    if not fecha or not cantidad:
        messagebox.showwarning("Advertencia", "Fecha y cantidad no pueden estar vacíos.")
        return

    # Guardar el registro con el tipo de producción y cantidad
    with open(archivo_produccion, "a") as file:
        file.write(f"Fecha: {fecha}\nTipo: {tipo_produccion} - Cantidad: {cantidad} {unidad_var.get()}\n---\n")

    messagebox.showinfo("Registro de Producción", "Registro de producción agregado con éxito.")
    entry_fecha_produccion.delete(0, tk.END)
    entry_cantidad_produccion.delete(0, tk.END)
    actualizar_lista_registros_produccion()

# Función para actualizar la lista de registros de producción en el frame
def actualizar_lista_registros_produccion():
    listbox_produccion.delete(0, tk.END)
    if os.path.exists(archivo_produccion):
        with open(archivo_produccion, "r") as file:
            registros = file.readlines()
        registros_completos = ["".join(registros[i:i+4]).strip() for i in range(0, len(registros), 4)]
        for registro in registros_completos:
            listbox_produccion.insert(tk.END, registro)
    else:
        listbox_produccion.insert(tk.END, "No hay registros de producción.")

# Función para eliminar un registro de producción
def eliminar_registro_produccion():
    seleccion = listbox_produccion.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")
        return

    # Obtener el índice del registro seleccionado
    index = seleccion[0]

    # Leer todos los registros
    with open(archivo_produccion, "r") as file:
        registros = file.readlines()

    # Identificar el inicio y fin del registro seleccionado
    inicio = index * 4
    fin = inicio + 4

    # Eliminar el registro seleccionado
    del registros[inicio:fin]

    # Escribir de nuevo el archivo sin el registro eliminado
    with open(archivo_produccion, "w") as file:
        file.writelines(registros)

    messagebox.showinfo("Eliminar Registro", "Registro eliminado con éxito.")
    actualizar_lista_registros_produccion()

# Función para actualizar la unidad de medida según el tipo de producción seleccionado
def actualizar_unidad():
    if tipo_produccion_var.get() == "carne":
        unidad_var.set("kg")  # Kilos para carne
    elif tipo_produccion_var.get() == "leche":
        unidad_var.set("litros")  # Litros para leche
    else:
        unidad_var.set("kg")  # Default para doble propósito

# Crear la ventana principal
root = tk.Tk()
root.title("VacaData")
root.geometry("450x650")

# Crear frames para diferentes secciones
frame_login = ttk.Frame(root)
frame_menu_principal = ttk.Frame(root)
frame_historia_clinica = ttk.Frame(root)
frame_produccion = ttk.Frame(root)

# Añadir los frames al grid
for frame in (frame_login, frame_menu_principal, frame_historia_clinica, frame_produccion):
    frame.grid(row=0, column=0, sticky='nsew')

# Configuración de filas y columnas para permitir expansión
frame_central = root
frame_central.rowconfigure(0, weight=1)
frame_central.columnconfigure(0, weight=1)

# --- Frame Login ---
ttk.Label(frame_login, text="Bienvenidos VacaData", font=("Helvetica", 24)).pack(pady=10)

# Campos para usuario y contraseña con mayor ancho y tamaño de letra
ttk.Label(frame_login, text="Usuario:", font=("Helvetica", 14)).pack()
entry_usuario = ttk.Entry(frame_login, width=40, font=("Helvetica", 14))  # Ancho aumentado
entry_usuario.pack(pady=5)

ttk.Label(frame_login, text="Contraseña:", font=("Helvetica", 14)).pack()
entry_contrasena = ttk.Entry(frame_login, show='*', width=40, font=("Helvetica", 14))  # Ancho aumentado
entry_contrasena.pack(pady=5)

# Botones de acción (Iniciar Sesión encima de Registrar)
ttk.Button(frame_login, text="Iniciar Sesión", command=login, padding=10).pack(pady=5)
ttk.Button(frame_login, text="Registrar", command=registrar, padding=10).pack(pady=5)
ttk.Button(frame_login, text="Salir", command=root.quit, padding=10).pack(pady=10)

# --- Frame Menú Principal ---
ttk.Label(frame_menu_principal, text="--- Menú Principal ---", font=("Helvetica", 20)).pack(pady=10)
ttk.Button(frame_menu_principal, text="Historia Clínica de la Vaca", command=historia_clinica, padding=10).pack(pady=5)
ttk.Button(frame_menu_principal, text="Producción", command=produccion, padding=10).pack(pady=5)
ttk.Button(frame_menu_principal, text="Cerrar", command=root.quit, padding=10).pack(pady=10)

# --- Frame Historia Clínica ---
label_historia_clinica = ttk.Label(frame_historia_clinica, text="--- Historia Clínica ---", font=("Helvetica", 20))
label_historia_clinica.pack(pady=10)

# Campos para agregar registro clínico
ttk.Label(frame_historia_clinica, text="Fecha (dd/mm/aaaa):", font=("Helvetica", 14)).pack()
entry_fecha_clinica = ttk.Entry(frame_historia_clinica, font=("Helvetica", 14))
entry_fecha_clinica.pack(pady=5)

ttk.Label(frame_historia_clinica, text="Descripción:", font=("Helvetica", 14)).pack()
text_descripcion_clinica = tk.Text(frame_historia_clinica, height=10, width=60, font=("Helvetica", 14))  # Usar Text para mayor espacio
text_descripcion_clinica.pack(pady=5)

ttk.Button(frame_historia_clinica, text="Agregar registro clínico", command=agregar_registro_clinico, padding=10).pack(pady=5)
ttk.Button(frame_historia_clinica, text="Eliminar registro clínico", command=eliminar_registro_clinico, padding=10).pack(pady=5)

# Lista de registros clínicos
listbox_clinica = tk.Listbox(frame_historia_clinica, height=10, width=60, font=("Helvetica", 12))
listbox_clinica.pack(pady=5)

ttk.Button(frame_historia_clinica, text="Volver al Menú Principal", command=lambda: mostrar_frame(frame_menu_principal), padding=10).pack(pady=10)

# --- Frame Producción ---
label_produccion = ttk.Label(frame_produccion, text="--- Producción ---", font=("Helvetica", 20))
label_produccion.pack(pady=10)

# Campos para agregar registro de producción
ttk.Label(frame_produccion, text="Fecha (dd/mm/aaaa):", font=("Helvetica", 14)).pack()
entry_fecha_produccion = ttk.Entry(frame_produccion, font=("Helvetica", 14))
entry_fecha_produccion.pack(pady=5)

# Variables para botones de opción y unidad
tipo_produccion_var = tk.StringVar(value="leche")  # Valor por defecto
unidad_var = tk.StringVar(value="litros")  # Valor por defecto

ttk.Label(frame_produccion, text="Tipo de Producción:", font=("Helvetica", 14)).pack(pady=5)
tipo_produccion_frame = ttk.Frame(frame_produccion)
tipo_produccion_frame.pack(pady=5)

ttk.Radiobutton(tipo_produccion_frame, text="Leche", variable=tipo_produccion_var, value="leche", command=actualizar_unidad).pack(side=tk.LEFT, padx=10)
ttk.Radiobutton(tipo_produccion_frame, text="Carne", variable=tipo_produccion_var, value="carne", command=actualizar_unidad).pack(side=tk.LEFT, padx=10)
ttk.Radiobutton(tipo_produccion_frame, text="Doble Propósito", variable=tipo_produccion_var, value="doble_proposito", command=actualizar_unidad).pack(side=tk.LEFT, padx=10)

ttk.Label(frame_produccion, text="Cantidad:", font=("Helvetica", 14)).pack()
entry_cantidad_produccion = ttk.Entry(frame_produccion, width=40, font=("Helvetica", 14))  # Ajustar el ancho si es necesario
entry_cantidad_produccion.pack(pady=5)

ttk.Button(frame_produccion, text="Agregar registro de producción", command=agregar_registro_produccion, padding=10).pack(pady=5)
ttk.Button(frame_produccion, text="Eliminar registro de producción", command=eliminar_registro_produccion, padding=10).pack(pady=5)

# Lista de registros de producción
listbox_produccion = tk.Listbox(frame_produccion, height=10, width=60, font=("Helvetica", 12))
listbox_produccion.pack(pady=5)

ttk.Button(frame_produccion, text="Volver al Menú Principal", command=lambda: mostrar_frame(frame_menu_principal), padding=10).pack(pady=10)

# Mostrar el frame de inicio de sesión al iniciar
mostrar_frame(frame_login)

root.mainloop()