import csv
from datetime import datetime
import pandas as pd
import os

ARCHIVO = "visitas.csv"

def main():
    while True:
        try:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Iniciar programa")
            print("2. Salir")

            opcion = int(input("Seleccione una opción (1-2): "))

            if opcion == 1:
                menu_visitas()
            elif opcion == 2:
                print("Saliendo del sistema... 👋")
                break
            else:
                print("Opción no válida. Seleccione 1 o 2.")
        except ValueError:
            print("Entrada inválida. Intente de nuevo.")

def menu_visitas():
    while True:
        try:
            print("\n--- MENÚ DE VISITAS ---")
            print("1. Registrar nueva visita")
            print("2. Consultar todas las visitas")
            print("3. Buscar visita por ID")
            print("4. Volver al menú principal")

            opcion = int(input("Seleccione una opción (1-4): "))

            if opcion == 1:
                registrar_visita()
            elif opcion == 2:
                consultar_visitas(todos=True)
            elif opcion == 3:
                buscar_por_id()
            elif opcion == 4:
                print("Volviendo al menú principal...")
                break
            else:
                print("Opción no válida. Seleccione entre 1 y 4.")
        except ValueError:
            print("Entrada inválida. Intente de nuevo.")

def cargar_visitas():
    """Carga el CSV de visitas de manera segura, ignorando líneas corruptas."""
    if not os.path.exists(ARCHIVO):
        return pd.DataFrame(columns=['id', 'nombre', 'sitio', 'fecha', 'hora'])
    try:
        df = pd.read_csv(ARCHIVO, on_bad_lines='skip')  # Ignora líneas mal formadas
        # Asegurarse de que tenga todas las columnas necesarias
        for col in ['id', 'nombre', 'sitio', 'fecha', 'hora']:
            if col not in df.columns:
                df[col] = ''
        # Limpiar IDs vacíos o inválidos
        df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)
        return df
    except Exception as e:
        print(f"Error al cargar las visitas: {e}")
        return pd.DataFrame(columns=['id', 'nombre', 'sitio', 'fecha', 'hora'])

def registrar_visita():
    try:
        nombre = input("Ingrese el nombre del visitante: ").strip().rstrip(".")
        if not nombre:
            nombre = "Anónimo"

        sitio = input("Ingrese el nombre del sitio web: ").strip().rstrip(".")
        if not sitio:
            sitio = "Sitio desconocido"

        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")

        df = cargar_visitas()
        ultimo_id = df['id'].max() if not df.empty else 0

        visita = {
            "id": int(ultimo_id) + 1,
            "nombre": nombre,
            "sitio": sitio,
            "fecha": fecha,
            "hora": hora
        }

        guardar_visita(visita)
        print(f"✅ Visita registrada correctamente con ID {visita['id']} ({nombre} - {sitio})")
    except Exception as e:
        print(f"Error al registrar la visita: {e}")

def guardar_visita(visita: dict):
    try:
        with open(ARCHIVO, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'nombre', 'sitio', 'fecha', 'hora']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:  # Escribir encabezado si el archivo está vacío
                writer.writeheader()
            writer.writerow(visita)
    except Exception as e:
        print(f"Error al guardar la visita: {e}")

def consultar_visitas(todos=False):
    df = cargar_visitas()
    if df.empty:
        print("No hay visitas registradas.")
        return

    if todos:
        print("\n--- TODOS LOS REGISTROS ---")
        for _, row in df.iterrows():
            print(f"ID: {row['id']}")
            print(f"Nombre: {row['nombre']}")
            print(f"Sitio: {row['sitio']}")
            print(f"Fecha: {row['fecha']}")
            print(f"Hora: {row['hora']}")
            print("-" * 30)

    # Estadísticas generales
    total_visitas = len(df)
    print(f"\n📊 Total de visitas registradas: {total_visitas}")

    # Visitas por sitio
    conteo_sitios = df['sitio'].value_counts()
    print("\n--- VISITAS POR SITIO ---")
    for sitio, cantidad in conteo_sitios.items():
        print(f"{sitio}: {cantidad}")

    # Visitante más frecuente
    visitante_frecuente = df['nombre'].value_counts().idxmax()
    visitas_frecuente = df['nombre'].value_counts().max()
    print(f"\n👤 Visitante más frecuente: {visitante_frecuente} ({visitas_frecuente} visitas)")

def buscar_por_id():
    df = cargar_visitas()
    if df.empty:
        print("No hay visitas registradas.")
        return

    try:
        id_consulta = int(input("Ingrese el ID del registro que desea buscar: "))
        registro = df[df['id'] == id_consulta]
        if registro.empty:
            print(f"No se encontró ningún registro con ID {id_consulta}.")
        else:
            # Mostrar en formato vertical/ficha
            print("\n--- REGISTRO ENCONTRADO ---")
            for _, row in registro.iterrows():
                print(f"ID: {row['id']}")
                print(f"Nombre: {row['nombre']}")
                print(f"Sitio: {row['sitio']}")
                print(f"Fecha: {row['fecha']}")
                print(f"Hora: {row['hora']}")
                print("-" * 30)
    except ValueError:
        print("ID inválido. Debe ser un número entero.")
    except Exception as e:
        print(f"Error al buscar por ID: {e}")

if __name__ == "__main__":
    print("Bienvenido al sistema de registro de visitas a sitios web 🌐")
    main()