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

#Gaston: Cambie los nombre de varias funciones para que sigan la misma logica y se mas facil de leer
def obtener_paises():
#Variable que nos va a permitir que el usuario ingrese paises
    paises = []
    #Gaston: (lo de abajo es para dejarlo de comentario)
    #Si el archivo no esxiste, se crea con encabezado y devuelve lista vacia
    if not os.path.exists(NOMBRE_ARCHIVO): 
        with open(NOMBRE_ARCHIVO, "w", newline= "", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS)
            escritor.writeheader()
        return paises
    
    #Gaston: aca lo mismo(para dejar de coment)
    #Si existe, se lee
    with open(NOMBRE_ARCHIVO, newline="",encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            #ACA ME HICE LIO, SI QUERES REVISARLO MEJOR:  (estaba joya, solo habia que validar que sea >0)
            if ( "nombre" in fila
                and "poblacion" in fila
                and "superficie" in fila
                and "continente" in fila
                and fila["poblacion"].isdigit()
                and fila["superficie"].isdigit()
                #Gaston: aca agregue estas dos lineas para validar que sea > 0
                and int(fila['poblacion']) > 0
                and int(fila['superficie']) > 0
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
#Oriana: Defino la variable fmt para poder formatear números grandes
#CONSULTA: ESTA DEFINICION LA PODEMOS USAR?????

def _fmt_num(n):
    return f"{n: ,}".replace(" ,"," . ")

#Gaston: Esta habria que eliminarla para que no generar conflictos con la funcion modificada por mi mas abajo
# esta entre comillas para que no se ejecute y que vos puedas ir viendo que habia antes  
"""
def agregarPais(pais):
    with open(NOMBRE_ARCHIVO, "a", newline= "", encoding="utf-8") as archivo:
         escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
         escritor.writerow({
            "nombre": pais["nombre"],
            "poblacion": pais["poblacion"],
            "superficie": pais["superficie"],
            "continente": pais["continente"]})
   """      
#Gaston: aca tuve que cambiar el nombre de guardarPais a lo que ves, porque en el menu hace referencia a este nuevo
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
            
    #Gaston: aca modifique el nombre de la funcion con (_) para mantener logica
def pais_ya_existe(nombre_ingresado, paises):
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

    #Gaston: aca solo cambie el nombre con snake case (_) para mantener logica         
def leer_entero_no_negativo(mensaje):
    #la variable debe declarar el umero que se debe ingresar para que sea valida ( un entero mayor o igual a 0)
    while True:
        dato = input(mensaje).strip()
        if dato.isdigit() and int(dato) >= 0:
            return int(dato)
        print("Valor inválido. Ingrese un número entero mayor o igual a 0.")

def validar_entero_no_negaitvo(valor):
    return valor.isdigit() and int(valor) >= 0

#Gaston: defini esta nueva funcion para que sea mas facil el mensaje "no puede estar vacio" cuando preguntamos 
#por nombre de pais o continente
def leer_texto_no_vacio(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("Este campo no puede estar vacio.")

#Gaston: cree nuevamente la funcion agregar_paises para que puedas ver la diferencia llamdando a la funcion 
#que esta aca arriba leer_texto_no_vacio y ademas porque la consigna pide agregar 1 pais, dsp si queres vemos
#y si llegamos modificamos para poder sumar de mas de 1

def agregar_pais(paises):
    print("\n--- Bienvenido! Por favor, ingrese un pais---") 

    #Gaston: pedimos el nombre (llamando a la funcion leer_texto...)
    nombre = leer_texto_no_vacio("Nombre: ")

    #Gaston: verificamos si ya existe para no duplicar la entrada
    if pais_ya_existe(nombre, paises):
        print("Este pais ya existe.")
        return

    #Gaston: Se valida poblacion y superficie
    poblacion = leer_entero_positivo("Poblacion: ")
    superficie = leer_entero_positivo("Superficie (Km2): ")

    #Gaston: Hacemos lo mismo que hicimos con el nombre 
    continente = leer_texto_no_vacio("continente: ")

    #Gaston: Creamos el diccionario
    nuevo = {
        "nombre" : nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }

    #Gaston: lo agregamos a la lsita en memoria
    paises.append(nuevo)

    #Gaston: el guardado definitivo se hace en el menu al salir, no lo hacemos aca
    print(f"El pais {nombre} fue agregado correctamente.")

"""""
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

    print("ERROR // No se completo la carga de nuevos Países")
"""
#Gaston: Ahora tenemos una función que solo se agrega a la lista en memoria. La escritura al CSV se hace 
#una sola vez, cuando elegimos “Guardar y salir”. Es más seguro 

#Gaston: Defino actualizar paises 
def actualizar_pais(paises):
    print("\n--- Actualizar país ---")
    if not paises:
         print("No hay paieses cargados.")
         return
     
    patron = input("Ingrese el nombre del pais o parte del mismo para actualizarlo: ").strip().lower()
    candidatos = [p for p in paises if patron in p['nombre'].lower()]

    if not candidatos:
         print("No se encontraron paises con ese criterio.")
         return
     
    print("Paises encontrados: ")
    for i, p in enumerate(candidatos, start=1):
         print(f"{i}. {p['nombre']}) | Pob: {p['poblacion']} | Sup: {p['superficie']} km2")
        
    indice = leer_entero_positivo("Con numeros, selecione cual quiere actualizar: ")-1
     
    if 0 <= indice < len(candidatos):
         pais = candidatos[indice]
         print(f"Actualizando datos de: {pais['nombre']}")
         pais["poblacion"] = leer_entero_positivo ("Poblacion actualizada: ")
         pais["superficie"] = leer_entero_positivo("Superficie(km2) actualizada: ")
         print("Los datos fueron actualizados correctamente.")
    else:
        print("Opcion invalida.")

 #Gaston: Definimios nuevas funciones para mostrar y listar paises, para usarlas en buscar_pais
def mostrar_pais(p):
    print(
        f"- {p['nombre']} | Población: {p['poblacion']} | "
        f"Superficie: {p['superficie']} km2 | Continente: {p['continente']}")

def listar_paises(paises):
    if not paises:
        print("No hay paises cargados.")
        return
    for p in paises:
        mostrar_pais(p)

#Gaston: Defino funcion para buscar pais
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

#Gaston: Defino funcion para filtrar paises
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
        cont = input("Ingrese el continente: ").strip().lower()
        resultado = [p for p in paises if p["continente"].lower() == cont]

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

#Oriana: Defino punto 5: ordenar países
def ordenar_paises(paises):
    if not paises:
        print("Aún no hay países cargados. ")
        return
    
    print("--ORDENAR PAÍSES--")
    print("Criterios: ")
    print("1. Nombre ")
    print("2. Población ")
    print("3. Supercie")
    crit = input("Elija opción (1,2 o 3): ").strip()

    if crit == "1":
        clave = "nombre"
    elif crit == "2":
        clave = "poblacion"
    elif crit == "3":
        clave = "superficie"
    else:
        print("La opción de criterio no es válida.")
        return
    
    sentido = input("Orden (asc/desc): ").strip().lower()
    reverse =(sentido == "desc")

    if clave == "nombre":
        ordenado = sorted(paises, key=lambda p: p["nombre"].strip().lower(), reverse=reverse)
    else:
        ordenado = sorted(paises, key=lambda p: p[clave], reverse=reverse)
    print(f"\nListado ordenado por {clave} ({'desc' if reverse else 'asc'}):")

    for p in ordenado:
        mostrar_pais(p)

#Oriana: Punto 6. Mostrar Estadisticas 
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
    print(f"• País con MAYOR población : {mayor['nombre']} ({_fmt_num(mayor['poblacion'])})")
    print(f"• País con MENOR población : {menor['nombre']} ({_fmt_num(menor['poblacion'])})")
    print(f"• Promedio de población    : {_fmt_num(int(prom_pob))}")
    print(f"• Promedio de superficie   : {_fmt_num(int(prom_sup))}")

    print("\n• Cantidad de países por continente:")
    for cont, cant in por_continente.items():
        print(f"   - {cont}: {cant}")
    print("")

#Oriana : Punto 7: guardar y salir
#La variable se debe definir para que se guarden los cambios en el csv
def guardar_y_salir(paises):
    print("\n Guardando los cambios en archivo...")
    guardar_paises(paises)
    print("Cambios guardados correctamente. ")
    print("¡Gracias por usar el sistema!. Hasta luego. \n")



 #Oriana: Definimos las variables que va a tener nuestro menu 
    
def mostrar_menu():
    # Carga inicial del CSV
    paises = obtener_paises()
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
                    print(" Opción inválida. Intente nuevamente.")
mostrar_menu ()
