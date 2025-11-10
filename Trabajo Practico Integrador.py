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
import unicodedata
# ==============================
# 1) Constantes
# ==============================

NOMBRE_ARCHIVO = "paises.csv"
CAMPOS = ["nombre", "poblacion", "superficie","continente"]

# ==============================
# 2) Manejo de archivos (CSV)
# ==============================

def obtener_paises():

    paises = []
    
    #Si el archivo no esxiste, se crea con encabezado y devuelve lista vacia
    if not os.path.exists(NOMBRE_ARCHIVO): 
        with open(NOMBRE_ARCHIVO, "w", newline= "", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS)
            escritor.writeheader()
        return paises
    
    #Si existe, se lee
    with open(NOMBRE_ARCHIVO, newline="",encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            #eliminamos espacios antes de validar
            poblacion_txt = fila["poblacion"].strip()
            superficie_txt = fila["superficie"].strip()

            if ( "nombre" in fila
                and "poblacion" in fila
                and "superficie" in fila
                and "continente" in fila
                and poblacion_txt.isdigit()
                and superficie_txt.isdigit()
                # validar que sea > 0
                and int(poblacion_txt) > 0
                and int(superficie_txt) > 0
            ):
                paises.append({
                    "nombre": fila["nombre"].strip(),
                    "poblacion": int(poblacion_txt),
                    "superficie": int(superficie_txt),
                    "continente": fila["continente"].strip()
                })
            else:
                print(" Se OMITE una fila con datos inválidos en el CSV.")
    return paises

#funcion para escribir la lista completa de paises en el CSV, sobrescribiendo el archivo anterior
def guardar_paises(paises):
    with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        for p in paises:
            escritor.writerow({
                "nombre": p["nombre"],
                "poblacion": p["poblacion"],
                "superficie": p["superficie"],
                "continente": p["continente"]})
            
# ==============================
# 3) Funciones auxiliares 
# ==============================

#funcion para formatear numeros grandes, con punto como separador de miles.
def formatear_num(n):
    #Por ejemplo: 1234567 se transforma en  '1.234.567'
    return f"{n:,}".replace(",", ".")

    
#funcion para normalizar texto
def normalizar(texto):
# Con esta funcion pasamos a minuscula, sacamos espacios extras y reemplazamos las vocales con tilde. 
# Sirve para comparar 'America' con 'América' o 'america' sin problema.
    texto = texto.strip().lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto
def pais_ya_existe(nombre_ingresado, paises):
    #Devuelve True si el país ya existe (sin distinguir mayúsculas).
    nombre_ingresado = nombre_ingresado.strip().lower()
    for p in paises:
        if p["nombre"].strip().lower() == nombre_ingresado:
            return True
    return False

# ==============================
# 4) Validaciones (Utilizadas en operaciones principales)
# ==============================

def leer_entero_positivo(mensaje): #la usamos en agregar_pais 
    #Se pide un numero entero mayor o igual a 1 (>=1), y se repite hasta que el usuario ingrese un valor valido
    while True:
        dato = input(mensaje).strip()
        if dato.isdigit() and int(dato) >= 1:
            return int(dato)
        print("Valor inválido. Ingrese un número entero mayor o igual a 1.")


def leer_entero_no_negativo(mensaje): #la usammos en filrar_paises
    #Se pide un nummero entero mayor o igual a 0 (>=0), y se repide hasta que el usuario ingrese un valor valido
    while True:
        dato = input(mensaje).strip()
        if dato.isdigit() and int(dato) >= 0:
            return int(dato)
        print("Valor inválido. Ingrese un número entero mayor o igual a 0.")

#funcion para que sea mas facil el mensaje "no puede estar vacio" cuando preguntamos 
#por nombre de pais o continente, se repite hasta que el usuario ingrese algo valido 
def leer_texto_no_vacio(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("Este campo no puede estar vacio.")

# ==============================
# 5) Funciones de salida (mostrar datos)
# ==============================

#funciones para mostrar y listar paises, para usarlas en buscar_pais
def mostrar_pais(p):
    print(
        f"- {p['nombre']} | Población: {p['poblacion']} | "
        f"Superficie: {p['superficie']} km2 | Continente: {p['continente']}")
    
#muestra todos los paises cargados 
def listar_paises(paises):
    if not paises:
        print("No hay paises cargados.")
        return
    for p in paises:
        mostrar_pais(p)

# ==============================
# 6) Operaciones principales
# ==============================

def agregar_pais(paises):
    print("\n--- Bienvenido! Por favor, ingrese un pais---") 

    #pedimos el nombre (llamando a la funcion leer_texto...) para validar que no este vacio 
    nombre = leer_texto_no_vacio("Nombre: ")

    #verificamos si ya existe para no duplicar la entrada
    if pais_ya_existe(nombre, paises):
        print("Este pais ya existe.")
        return

    #Se valida poblacion y superficie
    poblacion = leer_entero_positivo("Poblacion: ")
    superficie = leer_entero_positivo("Superficie (Km2): ")

    #Hacemos lo mismo que hicimos con el nombre (Validacion) 
    continente = leer_texto_no_vacio("continente: ")

    #Creamos el diccionario
    nuevo = {
        "nombre" : nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }

    #Se agrega a la lsita en memoria
    paises.append(nuevo)

    #Se impime mensaje, pero el guardado definitivo se hace en el menu al salir, no lo hacemos aca
    print(f"El pais {nombre} fue agregado correctamente.")

#Gaston: Ahora tenemos una función que solo se agrega a la lista en memoria. La escritura al CSV se hace 
#una sola vez, cuando elegimos “Guardar y salir”. Es más seguro 

#actualizar paises 
def actualizar_pais(paises):
    print("\n--- Actualizar país ---")
    if not paises:
         print("No hay países cargados.")
         return
     
    eleccion = input("Ingrese el nombre del pais o parte del mismo para actualizarlo: ").strip().lower()
    candidatos = [p for p in paises if eleccion in p['nombre'].lower()]

    if not candidatos:
         print("No se encontraron países con ese criterio.")
         return
     
    print("Países encontrados: ")
    for i, p in enumerate(candidatos, start=1):
         print(f"{i}. {p['nombre']} | Pob: {p['poblacion']} | Sup: {p['superficie']} km2")
        
    indice = leer_entero_positivo("Con números, seleccione cuál quiere actualizar: ")-1
     
    if 0 <= indice < len(candidatos):
         pais = candidatos[indice]
         print(f"Actualizando datos de: {pais['nombre']}")
         pais["poblacion"] = leer_entero_positivo ("Poblacion actualizada: ")
         pais["superficie"] = leer_entero_positivo("Superficie(km2) actualizada: ")
         print("Los datos fueron actualizados correctamente.")
    else:
        print("Opción inválida.")


#funcion para buscar pais
def buscar_pais(paises):
    print("\n--- Buscar país ---")
    if not paises:
        print("No hay países cargados.")
        return

    patron = input("Ingrese nombre o parte del nombre: ").strip().lower()
    encontrados = [p for p in paises if patron in p["nombre"].lower()]

    if not encontrados:
        print("No se encontraron países.")
    else:
        print(f"Se encontraron {len(encontrados)} país(es):")
        for p in encontrados:
            mostrar_pais(p)             

#filtrar paises
def filtrar_paises(paises):
    print("\n--- Filtrar países ---")
    if not paises:
        print("No hay países cargados.")
        return

    print("1) Por continente")
    print("2) Por rango de población")
    print("3) Por rango de superficie")
    opcion = input("Seleccione una opción: ").strip()

    resultado = []

    if opcion == "1":
        cont = normalizar(input("Ingrese el continente: "))
        resultado = [p for p in paises if normalizar(p["continente"].strip()) == cont]

    elif opcion == "2":
        minimo = leer_entero_no_negativo("Población mínima: ")
        maximo = leer_entero_no_negativo("Población máxima: ")
        if maximo < minimo:
            minimo, maximo = maximo, minimo
        resultado = [p for p in paises if minimo <= p["poblacion"] <= maximo]

    elif opcion == "3":
        minimo = leer_entero_no_negativo("Superficie mínima (km2): ")
        maximo = leer_entero_no_negativo("Superficie máxima (km2): ")
        if maximo < minimo:
            minimo, maximo = maximo, minimo
        resultado = [p for p in paises if minimo <= p["superficie"] <= maximo]

    else:
        print("Opción inválida.")
        return

    if not resultado:
        print("No se encontraron países con ese filtro.")
    else:
        print(f"Se encontraron {len(resultado)} país(es):")
        for p in resultado:
            mostrar_pais(p)

# --- Ordenamos los países ---

def clave_nombre(p):
    return p["nombre"].strip().lower()

def clave_poblacion(p):
    return p["poblacion"]

def clave_superficie(p):
    return p["superficie"]


#ordenar países
def ordenar_paises(paises):
    if not paises:
        print("Aún no hay países cargados. ")
        return
    
    print("--ORDENAR PAÍSES--")
    print("Criterios: ")
    print("1) Nombre ")
    print("2) Población ")
    print("3) Superficie")
    opcion = input("Elija opción (1,2 o 3): ").strip()

    #Llamamos a la funcion clave segun la opcion elegida  

    if opcion == "1":
        clave = "nombre"
        key_func = clave_nombre
    elif opcion == "2":
        clave = "poblacion"
        key_func = clave_poblacion
    elif opcion == "3":
        clave = "superficie"
        key_func = clave_superficie
    else:
        print("La opción de criterio no es válida.")
        return
    
    #pedimos el orden y lo validamos 
    sentido = input("Orden (asc/desc): ").strip().lower()
    if sentido not in ("asc", "desc"):
        print("Orden inválido. Se usará ascendente por defecto.")
        reverse = False
    else:
        reverse = (sentido == "desc")

    # Ordenamos usando la función de clave seleccionada previamente
    ordenado = sorted(paises, key=key_func, reverse=reverse)

    print(f"\nListado ordenado por {clave} ({'desc' if reverse else 'asc'}):")
    for p in ordenado:
        mostrar_pais(p)

# --- Estadísticas ---

def mostrar_estadisticas(paises):
    if not paises:
        print("Aún no hay países cargados.")
        return
    
    mayor = paises[0]
    menor = paises[0]
    total_pob = 0
    total_sup = 0
    por_continente = {}

    for p in paises:
        total_pob += p["poblacion"]
        total_sup += p["superficie"]

        if p["poblacion"] > mayor["poblacion"]:
            mayor = p
        if p["poblacion"] < menor ["poblacion"]:
            menor = p

        cont = p["continente"].strip()
        por_continente[cont] = por_continente.get(cont, 0) + 1

    n = len(paises)
    prom_pob = total_pob / n
    prom_sup = total_sup / n

    print("\n=== ESTADÍSTICAS ===")
    print(f"• País con MAYOR población : {mayor['nombre']} ({formatear_num(mayor['poblacion'])})")
    print(f"• País con MENOR población : {menor['nombre']} ({formatear_num(menor['poblacion'])})")
    print(f"• Promedio de población    : {formatear_num(int(prom_pob))}")
    print(f"• Promedio de superficie   : {formatear_num(int(prom_sup))}")

    print("\n• Cantidad de países por continente:")
    for cont, cant in por_continente.items():
        print(f"   - {cont}: {cant}")
    print("")

# Guardar y salir
# La variable se debe definir para que se guarden los cambios en el csv
def guardar_y_salir(paises):
    print("\n Guardando los cambios en archivo...")
    guardar_paises(paises)
    print("Cambios guardados correctamente. ")
    print("¡Gracias por usar el sistema! Hasta luego. \n")


# ==============================
# 7) Menú y función principal
# =============================
    
def mostrar_menu():
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
        return input("Seleccione una opción: ").strip()

def main():
    paises = obtener_paises()  # Cargamos los datos del CSV una sola vez

    while True:
        opcion = mostrar_menu()

        match opcion:
            case "1":
                agregar_pais(paises)
            case "2":
                actualizar_pais(paises)
            case "3":
                buscar_pais(paises)
            case "4":
                filtrar_paises(paises)
            case "5":
                ordenar_paises(paises)
            case "6":
                mostrar_estadisticas(paises)
            case "7":
                guardar_y_salir(paises)
                break
            case _:
                print("Opción inválida. Intente nuevamente.")
       
if __name__ == "__main__":
    main()
