import tkinter as tk
from tkinter import messagebox
import mariadb

db = "prueba"

# Conecta a la base de datos
def conectar_db():
    global conexion
    try:
        conexion = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database=db
        )
    except mariadb.Error as error:
        messagebox.showerror("Error de conexión", str(error))
        return None

# Función para ejecutar una consulta SELECT y obtener un solo resultado
def ejecutar_consulta_fetchone(query):
    try:
        conectar_db()
        cursor = conexion.cursor()
        cursor.execute(query)
        mostrar_resultado(cursor.fetchone())
    except mariadb.Error as error:
        messagebox.showerror("Error de consulta", str(error))   

# Función para ejecutar una consulta SELECT y obtener varios resultados
def ejecutar_consulta_fetchmany(query, num_resultados):
    try:
        conectar_db()
        cursor = conexion.cursor()
        cursor.execute(query)
        mostrar_resultados(cursor.fetchmany(num_resultados))
    except mariadb.Error as error:
        messagebox.showerror("Error de consulta", str(error))

def ejecutar_consulta_fetchall(query):
    try:
        conectar_db()
        cursor = conexion.cursor()
        cursor.execute(query)
        mostrar_resultados(cursor.fetchall())
    except mariadb.Error as error:
        messagebox.showerror("Error de consulta", str(error))

import tkinter as tk

# Función para mostrar un solo resultado en una nueva ventana
def mostrar_resultado(resultado):
    ventana_resultado = tk.Toplevel()
    ventana_resultado.title("Resultado de la consulta")

    if resultado:
        mensaje_resultado = f"Resultado de la consulta:\n\nNombre: {resultado[0]}, Ciudad: {resultado[1]}"
        etiqueta_resultado = tk.Label(ventana_resultado, text=mensaje_resultado)
        etiqueta_resultado.pack()
    else:
        etiqueta_resultado = tk.Label(ventana_resultado, text="No se encontró ningún resultado.")
        etiqueta_resultado.pack()
        
# Función para mostrar varios resultados en una nueva ventana
def mostrar_resultados(resultados):
    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados de la consulta")

    if resultados:
        mensaje_resultados = "Resultados de la consulta:\n\n"
        for resultado in resultados:
            mensaje_resultados += f"Nombre: {resultado[0]}, Ciudad: {resultado[1]}\n"
        etiqueta_resultados = tk.Label(ventana_resultados, text=mensaje_resultados)
        etiqueta_resultados.pack()
    else:
        etiqueta_resultados = tk.Label(ventana_resultados, text="No se encontraron resultados.")
        etiqueta_resultados.pack()

ventana = tk.Tk()
ventana.title("Gestor de Base de Datos")

# Agregar widgets
etiqueta_consulta = tk.Label(ventana, text="Introduce una consulta SQL:")
etiqueta_consulta.pack()

entrada_consulta = tk.Entry(ventana, width=50)
entrada_consulta.pack()                                

# Obtener un solo resultado
def obtener_resultado():
    query = entrada_consulta.get()
    ejecutar_consulta_fetchone(query)

boton_resultado = tk.Button(ventana, text="Obtener un solo resultado", command=obtener_resultado)
boton_resultado.pack()

# Obtener varios resultados
def obtener_resultados():
    query = entrada_consulta.get()
    ejecutar_consulta_fetchmany(query, 2) # Obtener 2 resultados

boton_resultados = tk.Button(ventana, text="Obtener varios resultados", command=obtener_resultados)
boton_resultados.pack()

# Obtener todos los resultados
def obtener_todos_resultados():
    query = entrada_consulta.get()
    ejecutar_consulta_fetchall(query)

boton_todos_resultados = tk.Button(ventana, text="Obtener todos los resultados", command=obtener_todos_resultados)
boton_todos_resultados.pack()

ventana.mainloop()