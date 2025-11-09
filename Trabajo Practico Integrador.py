#El programa debe ofrecer un menú de opciones en consola que permita: 
#• Agregar un país con todos los datos necesarios para almacenarse (No se 
#permiten campos vacios). 
#• Actualizar los datos de Población y Superfice de un Pais. 
#• Buscar un país por nombre (coincidencia parcial o exacta).  
#• Filtrar países por: 
#o Continente 
#o Rango de población 
#o Rango de superficie  
#• Ordenar países por:  
#o Nombre  
#o Población  
#o Superficie (ascendente o descendente)  
#• Mostrar estadísticas:  
#o País con mayor y menor población 
#o Promedio de población 
#o Promedio de superficie 
#o Cantidad de países por continente  



import csv
import os
NOMBRE_ARCHIVO = "paises.csv"
CAMPOS = ["nombre", "poblacion", "superficie","continente"]

def obtenerPaises():
#Variable que nos va a permitir que el usuario ingrese paises
    paises = []

    if not os.path.exists(NOMBRE_ARCHIVO): 
        with open(NOMBRE_ARCHIVO, "w", newline= "", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS)
            escritor.writeheader()
        return paises
    with open(NOMBRE_ARCHIVO, newline="",encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            #ACA ME HICE LIO, SI QUERES REVISARLO MEJOR
            if ( "nombre" in fila
                and "poblacion" in fila
                and "superficie" in fila
                and "continente" in fila
                and fila["poblacion"].isdigit()
                and fila["superficie"].isdigit()
            ):
                paises.append({
                    "nombre": fila["nombre"].strip(),
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": fila["continente"].strip()
                })
            else:
                print(" Se OMITE una fila con datos inválidos en el CSV.")
    return paises

def agregarPais(pais):
    with open(NOMBRE_ARCHIVO, "a", newline= "", encoding="utf-8") as archivo:
         escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
         escritor.writerow({
            "nombre": pais["nombre"],
            "poblacion": pais["poblacion"],
            "superficie": pais["superficie"],
            "continente": pais["continente"]})
         
def guardarPaises(paises):
    with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        for p in paises:
            escritor.writerow({
                "nombre": p["nombre"],
                "poblacion": p["poblacion"],
                "superficie": p["superficie"],
                "continente": p["continente"]})

def paisYaExiste(nombre_ingresado, paises):
    #Devuelve True si el país ya existe (sin distinguir mayúsculas).
    nombre_ingresado = nombre_ingresado.strip().lower()
    for p in paises:
        if p["nombre"].strip().lower() == nombre_ingresado:
            return True
    return False

#Definicion de las variables numericas

def leer_entero_positivo(mensaje):
    #la variable debe declarar el numero que se debe ingresar para que sea valida, ( un entero mayor o igual a 1)
    while True:
        dato = input(mensaje).strip()
        if dato.isdigit() and int(dato) >= 1:
            return int(dato)
        print("Valor inválido. Ingrese un número entero mayor o igual a 1.")
             
def leerEntero_noNegativo(mensaje):
    #la variable debe declarar el umero que se debe ingresar para que sea valida ( un entero mayor o igual a 0)
    while True:
        dato = input(mensaje).strip()
        if dato.isdigit() and int(dato) >= 0:
            return int(dato)
        print("Valor inválido. Ingrese un número entero mayor o igual a 0.")

def validar_entero_no_negaitvo(valor):
    return valor.isdigit() and int(valor) >= 0


def agregar_paises():
    print(" Bienvenido! Por favor ingrese la cantidad de países que quiere agregar")
    paises = obtenerPaises()
    total = leer_entero_positivo ("¿Cuántos países desea cargar?")

    for i in range(1, total + 1):
        print(f"\nCarga #{i}:")
        while True:
         nombre = input("Nombre del País: ").strip()
         if not nombre:
            print("El nombre no puede estar vacío.")
            continue
         if paisYaExiste(nombre.lower(), paises):
            print("El País ya existe. Por favor ingrese uno diferente.")
            continue
         break
        poblacion = leer_entero_positivo("Población (entero mayor o igual a 1):  ")
    
        superficie = leer_entero_positivo("Supercie en km², ( Ingrese un número entero mayor o igual a 1): ")

        while True: 
            continente = input("Continente: ").strip()
            if not continente:
                print("El continente no puede estar vacío. ")
                continue
            break

        nuevo = {
            "nombre": nombre,
            "poblacion": int(poblacion),
            "superficie": int(superficie),
            "continente": continente}
        
        agregarPais(nuevo)
        paises.append(nuevo)
        cargados_ok += 1
        print(f"País '{nombre}' fue agregado correctamente. ")

    print("ERROR // No se completo la carga de nuevos títulos")




def mostrar_menu():
    # Carga inicial del CSV

    while True:
        print("\n" + "*" * 60)
        print(" SISTEMA DE GESTIÓN DE PAÍSES (TPI - Programación 1) ")
        print("*" * 60)
        print("1) Agregar país")
        print("2) Actualizar datos de un país")
        print("3) Buscar país por nombre")
        print("4) Filtrar países")
        print("5) Ordenar países")
        print("6) Mostrar estadísticas")
        print("7) Guardar y salir")
        print("*" * 60)
        opcion = input("Seleccione una opción: ").strip()


    match opcion:
            case "1":
                agregar_pais()
            case "2":
                actualizar_pais()
            case "3":
                buscar_pais()
            case "4":
                filtrar_paises()
            case "5":
                ordenar_paises()
            case "6":
                mostrar_estadisticas()
            case "7":
                guardar_paises_a_csv()
                print(" Cambios guardados. ¡Hasta luego")
        
            case _:
                print(" Opción inválida. Intente nuevamente.")
mostrar_menu ()
