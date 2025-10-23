import csv
import pandas as pd
def menu():
    while True:
        try:
            ventas = []
            print('\nmenu de ociones:')
            print('1. registrar ventas')
            print('2. guardar cambios CSV')
            print('3. consutar ventas ')
            print('4. salir')
            opcion = int(input('selecione la opcion: (1-4):'))
            if opcion == 1:
                registrar_ventas(ventas)
            elif opcion == 2:
                print('funcionalidad para guardar cambios CSV aun no implementada')
            elif opcion == 3:
                for venta in ventas:
                    print(venta)
            elif opcion == 4:
                print('saliendo del sistema de gestion de ventas')
                break
            else:
                print('opcion no valida, por favor seleccione una opcion entre 1 y 4')
        except ValueError:
            print('entrada invalida, por favor ingrese un numero entre 1 y 4')

def registrar_ventas(ventas: list):
    while True:
        try:
            producto = input('igrese el nombre del producto')
            cantidad = int(input('ingrese la cantidad vendida: '))
            precio = float(input('ingrese el precio del producto: '))
            fecha = input('ingrese la fecha de venta (AAAA-MM-DD): ')
            cliente = input('ingrese el nombre del cliente: ')


            if cantidad <= 0 or precio < 0:
                print('cantidad y precio deben ser numeros positivos, por favor intente de nuevo')
                continue
            venta = {
            'producto': producto,
            'cantidad': cantidad,
            'precio': precio,
            'fecha': fecha,
            'cliente': cliente
            }
            ventas.append(venta)


            continuar = input('desea registrar otra venta? (s/n): ').lower()
            if continuar != 's':
                    break


        except ValueError:
            print('entrada invalida, por favor intente de nuevo')
            continue


def guardar_ventas_(ventas:list):
    try:
        if not ventas:
            print('no hay ventas para guardar')
            return
        else:
            with open('ventas.csv', mode='w', newline='') as archivo:
                guardar = csv.DictWriter(archivo, fieldnames=['producto', 'cantidad', 'precio', 'fecha', 'cliente'])
                guardar.writeheader()
                guardar.writerows(ventas)
            print('ventas guardadas exitosamente en ventas.csv')
    except Exception as e:
        print(f'error al guardar las ventas: {e}')       

def consultar_ventas():
    try:
        df = pd.read_csv('ventas.csv')
        if df.empty:
            print('no hay ventas registradas')
        else:
            print('\nventas registradas:')
            df['subtotal'] = df['cantidad'] * df['precio']
            total_ventas = df['subtotal'].sum()
            print(f'total de ventas: {total_ventas:.2f}')

            producto_mas_vendido = df.groupby('producto')['cantidad'].sum().idxmax()
            print(f'producto mas vendido: {producto_mas_vendido}')


            tendencia_ventas = df['fecha'].value_counts().idxmax()
            print(f'dia con mayor numero de ventas: {tendencia_ventas}')
    except FileNotFoundError:
        print('el archivo ventas.csv no existe, por favor registre ventas primero')
    except Exception as e:
        print(f'error al consultar las ventas: {e}')

if __name__ == "__main__":
    print('bienvenido al sistema de gestion de ventas')
    menu()