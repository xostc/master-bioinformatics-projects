
#####1.	Preparación del entorno de trabajo (2 puntos)

# ----------------------------

##En esta primera actividad será necesaria la creación de un ambiente en Conda y la descarga de paquetes adecuados. Indica el comando o comandos necesarios para:
##•	A. Crear un ambiente de Conda que tenga el nombre «actividad1» e instalar en él las librerías de: Pandas, Matplotlib y Seaborn, además del IDE Spyder. (0,8)
# ================

#Usé anaconda prompt ya que tenia instalado esta paltaforma de antes 

#(base) C:\Users\resta>conda create -n actividad1_python310 python=3.10 pandas matplotlib seaborn spyder
#Collecting package metadata (current_repodata.json): done
#Solving environment: done


#==> WARNING: A newer version of conda exists. <==
  #current version: 23.9.0
  #latest version: 25.3.1

#Please update conda by running

    #$ conda update -n base -c defaults conda

#Or to minimize the number of packages updated during conda update use

     #conda install conda=25.3.1

#Instalo esa version para que sea compatible con spyder.Instalo esa version para que sea compatible con spyder.

##•	B. Instala la versión más reciente de Spyder que sea compatible con la versión de Python que tienes en tu entorno de cond
##•	C. Abre una consola. ¿Cómo comprobarías los ambientes creados en Conda? ¿Y las librerías instaladas en el ambiente que acabas de crear? (0,6)
# ================

#(base) C:\Users\resta>conda env list
# conda environments:
#
#base                  *  C:\Users\resta\anaconda3
#actividad1_asignatura_python     C:\Users\resta\anaconda3\envs\actividad1_asignatura_python
#actividad1_python310     C:\Users\resta\anaconda3\envs\actividad1_python310
#bioenv                   C:\Users\resta\anaconda3\envs\bioenv
#nombre_del_entorno       C:\Users\resta\anaconda3\envs\nombre_del_entorno
#rstudio                  C:\Users\resta\anaconda3\envs\rstudio
#rstudio_Xos              C:\Users\resta\anaconda3\envs\rstudio_Xos
#bioenv                   c:\Users\resta\anaconda3\envs\bioenv


#(base) C:\Users\resta>conda activate actividad1_python310


#(actividad1_python310) C:\Users\resta>conda list spyder
# packages in environment at C:\Users\resta\anaconda3\envs\actividad1_python310:
#
# Name                    Version                   Build  Channel
#pyls-spyder               0.4.0              pyhd3eb1b0_0
#spyder                    6.0.3           py310haa95532_0
#spyder-kernels            3.0.3           py310hbc747e5_0


#(actividad1_python310) C:\Users\resta>conda list
# packages in environment at C:\Users\resta\anaconda3\envs\actividad1_python310:
#
# Name                    Version                   Build  Channel
#aiohappyeyeballs          2.4.4           py310haa95532_0
#aiohttp                   3.11.10         py310h827c3e9_0
#aiosignal                 1.2.0              pyhd3eb1b0_0
#alabaster                 0.7.16          py310haa95532_0
#arrow                     1.3.0           py310haa95532_0
#astroid                   3.3.8           py310haa95532_0
#asttokens                 3.0.0           py310haa95532_0
#async-timeout             5.0.1           py310haa95532_0
#asyncssh                  2.17.0          py310haa95532_0
#atomicwrites              1.4.0                      py_0
#......
#spyder                    6.0.3           py310haa95532_0
#spyder-kernels            3.0.3           py310hbc747e5_0
#sqlite                    3.45.3               h2bbff1b_0
#stack_data                0.2.0              pyhd3eb1b0_0
#superqt                   0.7.3           py310hbc747e5_0
#....



#####2. Manipulación de archivos de texto plano (3,5 puntos)

# ----------------------------

###Examina manualmente el archivo con un editor de texto de tu elección (bloc de notas, Notepad, etc.). ¿Cuál es el título descriptivo de esta estructura (TITLE)? ¿Quiénes son los autores de este archivo (AUTHOR)? (0,25)
# ================

#TITLE     TUMOR SUPPRESSOR P53 COMPLEXED WITH DNA   
#AUTHOR    Y.CHO,S.GORINA,P.D.JEFFREY,N.P.PAVLETICH                              

##•	B. Mediante el administrador de contextos with, lee el documento .pdb y extrae solo la secuencia de aminoácidos (SEQRES) de la P53 y guárdalos en una lista. Ten cuidado de no incluir nada no sea un aminoácido en dicha lista. (1,5)
# ================

# Lista para almacenar la secuencia de aminoácidos de p53
p53_seqres = []

#Aquí definp una lista vacía llamada p53_seqres que servirá para almacenar 
#los fragmentos de la secuencia (los residuos) extraídos del archivo PDB.

# Ruta completa al archivo PDB, la defino
ruta_pdb = r"C:\Users\resta\Downloads\mubio07_programacion_python_act1(1)\1tup.pdb"


#Uso with para abrir el archivo de forma segura y una vez que se
#sale del bloque, el archivo se cierra automáticamente, evitando problemas 
#de recursos o errores



# Abro el archivo con el administrador de contextos 'with'
with open(ruta_pdb, "r") as pdb_file:
    for line in pdb_file:
        #Itero línea por línea en el archivo, lo que me permite procesar 
        #cada línea de forma individua
        # Filtro solo las líneas que empiezan con 'SEQRES'
        if line.startswith("SEQRES"):
            partes = line.split()  # Divido la línea en palabras
            cadena = partes[2]     # La tercera palabra es el identificador de cadena
            # Me interesa solo las cadenas de la proteína p53: A, B y C
            if cadena in ["A", "B", "C"]:
                residuos = partes[4:]  # A partir de la quinta palabra están los aminoácidos
                p53_seqres.extend(residuos)


#En el archivo .pdb, la información sobre la secuencia de aminoácidos aparece en 
#las líneas que comienzan con SEQRES (según la información oficial del formato), 
#y en ellas también se indica a qué cadena pertenece cada fragmento de la molécula. 
#En mi caso, me he centrado en extraer la secuencia de la proteína p53, que se encuentra 
#en las cadenas A, B y C, descartando otras como las cadenas E o F, que corresponden a ADN. 
#Aunque en teoría la letra que identifica la cadena está en una posición fija dentro de la 
#línea, en la práctica esto puede variar según el programa que haya generado el archivo o 
#el número de espacios utilizados. Por eso, he considerado más seguro dividir cada línea 
#por espacios usando split() y seleccionar el tercer elemento, que contiene el identificador 
#de la cadena. De esta forma, he podido identificar correctamente qué fragmentos pertenecen 
#a la proteína p53 y extraer únicamente su secuencia de aminoácidos.

# Muestro los resultados
print("Aminoácidos de la proteína p53 (cadenas A, B y C):")
print(p53_seqres)
print(f"Total de aminoácidos encontrados: {len(p53_seqres)}")


##Toma la lista que has creado en el apartado B y crea un programa para contar cuántos 
##aminoácidos hay de cada tipo. Guarda este conteo en un diccionario donde la clave sea el 
##aminoácido y el valor el número de veces que se encuentra repetido. No definas las claves
##del diccionario manualmente. (0,5)
# ================

# Creamos un diccionario vacío para guardar el conteo de aminoácidos
conteo_aminoacidos = {}

# Recorro la lista de aminoácidos extraídos
#uno por uno todos los elementos de la lista p53_seqres, que contiene 
#los nombres de aminoácidos (como GLY, PHE, ARG...).

#Cada uno se guarda momentáneamente en la variable aa. Se crea un diccionario 
#vacío conteo_aminoacidos que se utilizará para almacenar cada aminoácido como 
#clave y el número de apariciones como valor.
for aa in p53_seqres: #Se recorre cada elemento aa (aminoácido) en la lista p53_seqres.
    if aa in conteo_aminoacidos:
        conteo_aminoacidos[aa] += 1  # Si está, sumamos 1
    else:
        conteo_aminoacidos[aa] = 1   # Si no está, lo dejamos como 1
#Itero sobre cada par (clave, valor) en el diccionario y se imprime el 
#nombre del aminoácido junto con su frecuencia. Esto permite ver cuántas veces
#se repite cada tipo de aminoácido en la proteína.


# Muestro el resultado
print("Conteo de aminoácidos en la proteína p53:")
for aa, cantidad in conteo_aminoacidos.items():
    print(f"{aa}: {cantidad}")


##D. Crea un gráfico de barras con Seaborn con la frecuencia de cada aminoácido. 
##No olvides incluir el título del gráfico, así como el título de los ejes. Asigna a 
##cada uno un color distinto. (1,5)
# ================

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Convierto el diccionario a un DataFrame
df_aminoacidos = pd.DataFrame(list(conteo_aminoacidos.items()), columns=["Aminoácido", "Frecuencia"])

#Convierto el diccionario a un DataFrame con dos columnas: "Aminoácido" y "Frecuencia".

# Ordeno por frecuencia descendente 
df_aminoacidos = df_aminoacidos.sort_values(by="Frecuencia", ascending=False)

# Creo el gráfico de barras
plt.figure(figsize=(12, 6))  # Tamaño del gráfico

# Uso Seaborn para el gráfico
barra = sns.barplot(
    x="Aminoácido",
    y="Frecuencia",
    data=df_aminoacidos,
    palette="husl"  # Paleta de colores con colores distintos por cada barra de aminoacidos
)

# Añado títulos 
plt.title("Frecuencia de Aminoácidos en la Proteína p53 (Cadenas A, B y C)")
plt.xlabel("Aminoácido")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.show()


#####3. Manipulación de conjuntos de datos (4,5 puntos)

# ----------------------------

#A. Lee el archivo «nombre_archivo» y cambia el nombre de las columnas por los siguientes: 
#id, dieta, pulsaciones, tiempo y actividad. (0,25)
# ================

import pandas as pd

# Ruta del archivo
ruta = r"C:\Users\resta\Downloads\mubio07_programacion_python_act1(1)\actividad.csv"

# Leo el archivo con el encabezado original
df = pd.read_csv(ruta, sep=";")

# Cambio los nombres de las columnas
df.columns = ["id", "dieta", "pulsaciones", "tiempo", "actividad"]

# Muestro primeras filas para confirmar
print(df.head())


##•	B. Determina la presencia de celdas vacías con uno de los métodos de la clase 
##DataFrame y elimina dichas filas. (0,5)
# ================

# Ver cuántas celdas vacías hay por columna
print("Celdas vacías por columna:")
print(df.isnull().sum())

# Eliminar filas que tienen al menos una celda vacía
df = df.dropna()

# Confirmar que se eliminaron
print("\nDataFrame después de eliminar filas con celdas vacías:")
print(df.head())

##C. ¿Cuántos niveles hay en la columna «dieta» y cuál es su frecuencia? Lleva 
##a cabo esta tarea con un solo método de la clase DataFrame. (0,25)
# ================

# Obtengo niveles únicos y su frecuencia en la columna "dieta"
frecuencias_dieta = df["dieta"].value_counts()

#El método value_counts() se aplica sobre la columna “dieta” para contar 
#cuántas veces aparece cada nivel (por ejemplo, "low fat", "no fat", etc.).

# Muestro  el resultado
print(frecuencias_dieta)

#Hay dos niveles, low fat y no fat, de las cuales low fat= 45 y no fat=45 bajo
#la etiqueta diet

#D. Ayúdate del método groupby para agrupar los datos por el nivel de actividad. 
#Genera una lista a partir del groupby de forma que puedas observar cómo se ha 
#llevado a cabo la agrupación. Esta lista debería contener tres elementos, ¿por 
#qué tres? ¿Qué contienen cada uno de estos elementos de la lista? (1)
# ================

# Agrupo por la columna "actividad"
grupo_actividad = df.groupby("actividad")

# Convertio el groupby en una lista
lista_agrupada = list(grupo_actividad)

#La conversión a lista con list(grupo_actividad) resulta en una lista de tuplas
#con el nombre del grupo y el dataframe del grupo

# Muestro cuántos elementos tiene la lista
print(f"Número de grupos: {len(lista_agrupada)}\n")

# Muestro cada grupo
for i, grupo in enumerate(lista_agrupada):
    nombre_grupo, datos_grupo = grupo
    print(f"Grupo {i+1} - Actividad: {nombre_grupo}")
    print(datos_grupo.head(), "\n")  # Mostramos las primeras filas de cada grupo

##Al aplicar el método groupby("actividad") sobre el DataFrame y convertirlo con list(...), 
##se genera una lista con 3 elementos. Esto ocurre porque la columna "actividad" tiene 3 niveles 
##distintos: "rest", "walking" y "running"
# ================


# Aseguro que usamos el objeto groupby correcto
grupo_actividad = df.groupby("actividad")

# Aplico el método agg para obtener media y desviación estándar de las pulsaciones
resumen_pulsaciones = grupo_actividad.agg({
    "pulsaciones": ["mean", "std"]
})

#Mediante el método agg, puedo calcular dos estadísticas sobre la columna 
#“pulsaciones”: la media (mean) y la desviación estándar (std), lo que 
#proporciona una idea de la tendencia central y la dispersión de los datos 
#para cada nivel de actividad.


# Muestros el resultado
print(resumen_pulsaciones)


##F. Los pacientes de este estudio, cuyo nombre ha sido sustituido por un ID, 
##provenían de distintas ciudades. Utiliza el método merge para añadir esta información 
##y completar el conjunto de datos. (1)
# ================

import pandas as pd

# Ruta del archivo de ciudades
ruta_ciudades = r"C:\Users\resta\Downloads\mubio07_programacion_python_act1(1)\ciudades.tsv"

# Leo el archivo de ciudades (separado por tabulaciones)
df_ciudades = pd.read_csv(ruta_ciudades, sep="\t")

# Muestro las primeras filas para verificar
print("Contenido de ciudades.tsv:")
print(df_ciudades.head())

# Compruebo las columnas para hacer el merge correctamente
print("\nColumnas del DataFrame de ciudades:", df_ciudades.columns)

# Realizo el merge con el DataFrame original df (por 'id')
df_completo = pd.merge(df, df_ciudades, on="id")

##He hecho la unión mediante la columna "id", que es común a ambos conjuntos.


#Con pd.merge() puedo realizar una unión (merge) entre el DataFrame original df y 
#df_ciudades utilizando la columna “id” como llave. Esto añade información 
#adicional (como la ciudad de cada paciente) al conjunto de datos.



# Muestro las primeras filas del nuevo DataFrame completo
print("\nDataFrame combinado con ciudades:")
print(df_completo.head())


##•	G. Utiliza Matplotlib/Seaborn para hacer un gráfico en el que se pueda ver 
##la relación entre las variables pulsaciones y tiempo según el tipo de actividad 
##y la dieta. No olvides dar un título apropiado al gráfico así como reflejar en 
##cada eje el nombre de la variable correspondiente. Recibirá más puntuación si se 
##consigue hacerlo en una única figura multi-facetada (una faceta por estrato). 
##(0,75) 

import seaborn as sns
import matplotlib.pyplot as plt

# Me aseguro que la columna "tiempo" esté ordenada correctamente
# Si es texto tipo "1 min", "15 min", "30 min", lo convierto a formato numerico
df["tiempo_num"] = df["tiempo"].str.replace(" min", "").astype(int)

#La columna “tiempo” inicialmente contiene valores en formato de cadena 
#. Pero utilizo str.replace(" min", "") para eliminar 
#la parte de texto y luego lo convierto a entero con astype(int), creando una 
#nueva columna tiempo_num que contendrá solo el valor numérico.


# Creo un FacetGrid: una subgráfica por nivel de actividad
g = sns.FacetGrid(
    df,
    col="actividad",          # Una faceta por tipo de actividad
    hue="dieta",              # Colores diferentes por tipo de dieta
    height=4,
    aspect=1.2,
    palette="husl"
)

#El parámetro col="actividad" crea una faceta (subgráfico) por cada nivel 
#presente en la columna “actividad” (por ejemplo, "rest", "walking", "running").

#El parámetro hue="dieta" diferencia los datos dentro de cada faceta mediante 
#colores en función del tipo de dieta.

#Los parámetros height y aspect controlan el tamaño de cada subgráfico y la
#relación del aspecto que selecciono.

# Genero un gráfico de líneas con puntos
g.map(sns.lineplot, "tiempo_num", "pulsaciones", marker="o")

# Añado leyendas, títulos y etiquetas y que quede presentable 
g.add_legend(title="Dieta")
g.set_axis_labels("Tiempo (min)", "Pulsaciones (lpm)")
g.set_titles("Actividad: {col_name}")
plt.subplots_adjust(top=0.85)
g.fig.suptitle("Relación entre Pulsaciones y Tiempo según Actividad y Dieta", fontsize=14)

plt.show()
