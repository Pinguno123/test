import mariadb
from tkinter import *
from tkinter import messagebox

# Crear la ventana principal
tk_ventana = Tk()
tk_ventana.title("Gestor de base de datos")

# Inicializar la conexión a la base de datos
conexion_bd = None  

try:
    # Intentar conectar con la base de datos
    conexion_bd = mariadb.connect(
        user="root",
        password="",
        host="localhost",
        database="prueba",
        port=3306
    )
    Label(tk_ventana, text=f"Se conectó correctamente a la base de datos {conexion_bd.database}", fg="green").pack(pady=10)
except mariadb.Error as error:
    messagebox.showerror("Error de conexión", f"Error al conectar con la base de datos: {error}")


def crear_tabla(nombre_tabla, columnas):
    """Crea una tabla en la base de datos con las columnas especificadas."""
    if not conexion_bd:
        messagebox.showerror("Error", "No hay conexión a la base de datos.")
        return

    if not nombre_tabla:
        messagebox.showerror("Error", "Por favor, ingrese un nombre para la tabla.")
        return

    if not columnas or all(not nombre_col for nombre_col, _ in columnas):
        messagebox.showerror("Error", "Por favor, ingrese al menos una columna para la tabla.")
        return

    columnas_sql = []
    for nombre, tipo in columnas:
        if nombre and tipo:
            columnas_sql.append(f"{nombre} {tipo}")

    if not columnas_sql:
        messagebox.showerror("Error", "Por favor, ingrese al menos una columna con nombre y tipo.")
        return

    query = f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({', '.join(columnas_sql)})"

    cursor = conexion_bd.cursor()
    try:
        cursor.execute(query)
        conexion_bd.commit()
        messagebox.showinfo("Éxito", f"Tabla '{nombre_tabla}' creada correctamente.")
    except mariadb.Error as error:
        messagebox.showerror("Error al crear tabla", f"Error al crear la tabla '{nombre_tabla}': {error}")
    finally:
        if cursor:
            cursor.close()


def obtener_datos_tabla():
    """Obtiene los datos ingresados por el usuario para crear la tabla."""
    nombre_tabla = entrada_nombre_tabla.get()
    columnas = []
    for i in range(5):
        nombre_columna = entradas_nombres_columnas[i].get()
        tipo_columna = entradas_tipos_datos[i].get()
        if nombre_columna and tipo_columna:
            columnas.append((nombre_columna, tipo_columna))
    crear_tabla(nombre_tabla, columnas)

# Variables para los campos de entrada
entrada_nombre_tabla = None
entradas_nombres_columnas = []
entradas_tipos_datos = []


def mostrar_formulario_tabla():
    """Muestra el formulario para ingresar el nombre y atributos de la tabla."""
    global entrada_nombre_tabla, entradas_nombres_columnas, entradas_tipos_datos

    Label(tk_ventana, text="Nombre de la tabla :").pack(pady=5)
    entrada_nombre_tabla = Entry(tk_ventana, width=30)
    entrada_nombre_tabla.pack(pady=5)

    Label(tk_ventana, text="Definición de columnas (Nombre / Tipo de dato y extras):").pack(pady=10)

    for i in range(5):
        frame_columna = Frame(tk_ventana)
        frame_columna.pack(pady=2)

        Label(frame_columna, text=f"Columna {i+1}: Nombre").pack(side=LEFT, padx=5)
        entrada_nombre_columna = Entry(frame_columna, width=30)
        entrada_nombre_columna.pack(side=LEFT, padx=5)
        entradas_nombres_columnas.append(entrada_nombre_columna)

        Label(frame_columna, text="Tipo de dato y extras").pack(side=LEFT, padx=5)
        entrada_tipo_dato = Entry(frame_columna, width=50)
        entrada_tipo_dato.pack(side=LEFT, padx=5)
        entradas_tipos_datos.append(entrada_tipo_dato)

    Button(tk_ventana, text="Crear Tabla", command=obtener_datos_tabla).pack(pady=20)

# Mostrar el formulario para ingresar los datos de la tabla
mostrar_formulario_tabla()


def cerrar_bd():
    """Cierra la conexión con la base de datos antes de cerrar la aplicación."""
    if conexion_bd:
        conexion_bd.close()
        print("Conexión a la base de datos cerrada.")
    tk_ventana.destroy()

# Configurar el cierre de la ventana
tk_ventana.protocol("WM_DELETE_WINDOW", cerrar_bd)
tk_ventana.mainloop()