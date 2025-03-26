import pandas as pd
import csv

path = r"C:\Users\dougl\Documents\DAI\Speedrun\guia4\ejercicio5\file.csv"

# Lee el archivo CSV llamado 'leer_csv.csv' en un DataFrame de pandas
try:
    df = pd.read_csv(path)

    for index, row in df.iterrows():
        nombre = row['nombre']
        apellido = row['apellido']
        fecha_nacimiento = row['fechanacimiento']
        print(f"Nombre: {nombre}, Apellido: {apellido}, Fecha de nacimiento: {fecha_nacimiento}")

except FileNotFoundError:
    print(f"El archivo '{path}' no fue encontrado.")
except KeyError as e:
    print(f"La columna '{e}' no existe en el archivo CSV.")
except Exception as e:
    print(f"Ocurrió un error al leer el archivo CSV: {e}")
