# -*- coding: utf-8 -*-
"""
Created on Sun May 11 22:24:16 2025

Actividad 2 de Python

@author: Xosé Manuel Tomé Castro
"""



# ===========================
# 1)A. DESCARGA DEL ARCHIVO .CIF
# ===========================

#descargo automáticamente archivos .cif (describen cómo es una proteína en 3D) 
#con información de la  base de datos PDB (Protein Data Bank). 
#Cada proteína está identificada por un código, como 1tup, 2xyz, etc.

import os

# Cambio al directorio deseado
os.chdir("C:/Users/resta/Desktop/desktop")

import os
import requests #Bibliotecapara peticiones a la API


#Defino la funcion 
def descargar_cif(lista_ids, carpeta_destino='estructuras_cif'): 
    os.makedirs(carpeta_destino, exist_ok=True) #Creo la carpeta donde se guardarán los archivos descargados
    base_url = "https://files.rcsb.org/download/{}.cif" #'{}' es un marcador de posición que luego se llenará con el ID real
    
    resultados = {} #diccionario vacío para guardar los resultados
    
    for pdb_id in lista_ids: #Recorro uno por uno todos los IDs 
        url = base_url.format(pdb_id.upper()) #format inserta valores
        # Convierto el ID a mayúsculas porque el PDB lo requiere así
        destino = os.path.join(carpeta_destino, f"{pdb_id}.cif")
        try: # el bloque try-except para que, si ocurre un error, el programa no se detenga
            respuesta = requests.get(url) #Solicitud
            if respuesta.status_code == 200: # Si el código de respuesta es 200, significa que todo salió bien
                with open(destino, 'w') as f: #archivo modo escritura
                    f.write(respuesta.text)
                resultados[pdb_id] = 'Descarga correcta'
            else: #Si no se obtuvo un código 200, se registra un error con el código que vino
                resultados[pdb_id] = f'Error HTTP {respuesta.status_code}'
        except Exception as e: # # Si hubo otro tipo de error
            resultados[pdb_id] = f'Error: {str(e)}'
    
    return resultados

# ========= PARTE 1: Obtener ligandos desde archivo CIF =========

# Ejemplo de uso
lista_ids = ['1tup', '2xyz', '3def', '4ogq', '5jkl', '6mno', '7pqr', '8stu', '9vwx', '10yza']
print(descargar_cif(lista_ids))


#Se obtuvo estos resultados en la consola:   
#{'1tup': 'Descarga correcta', '2xyz': 'Descarga correcta', '3def': 'Descarga 
#correcta', '4ogq': 'Descarga correcta', '5jkl': 'Descarga correcta', '6mno': 
#'Descarga correcta', '7pqr': 'Descarga correcta', '8stu': 'Descarga correcta', 
#'9vwx': 'Error HTTP 404', '10yza': 'Error HTTP 400'}







# ===========================
# 1)B. Uniprot y Dataframe
# ===========================


#Primero accedo a https://rest.uniprot.org/uniprotkb/P04637.json como prueba 
#para saber la informacion que hay y si verdaderamente está la info requerida
#y el nombre de las columnas. Y efectivamente está todo bien

import requests
import pandas as pd
from time import sleep

# Función para obtener UniProt ID desde un PDB ID
def obtener_uniprot_id(pdb_id):
    url = "https://rest.uniprot.org/idmapping/run"
    datos = {'from': 'PDB', 
             'to': 'UniProtKB', 
             'ids': pdb_id}
    try: #uso try/except por si no sale bien no se detenga directamente
        respuesta = requests.post(url, data=datos)
        if respuesta.status_code == 200:
            job_id = respuesta.json().get('jobId')
            
            ###Resultado del mapeo
            
            resultado = requests.get(f"https://rest.uniprot.org/idmapping/results/{job_id}", timeout=10).json()
            if 'results' in resultado and resultado['results']:
                return resultado['results'][0]['to']
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    return None

# ========= PARTE 1: Información de uniprot =========

# Función para obtener la información de UniProt
def obtener_info_uniprot(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    try:
        respuesta = requests.get(url)
        return respuesta.json() if respuesta.status_code == 200 else None
    #Si no es exitosa devuelve none, abreviado (if-else)
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    return None

# ========= PARTE 2: Extracción de datos del 1tup=========

# Función para extraer la información relevante del JSON según ejercicio
def extraer_datos(data):
    gen_data = data.get('genes', [{}])[0]
    return {
        'Uniprot_id': data.get('primaryAccession', ''),
        'Fecha_publicacion': data.get('entryAudit', {}).get('firstPublicDate', ''),
        'Fecha_modificacion': data.get('entryAudit', {}).get('lastAnnotationUpdateDate', ''),
        'Revisado': 'Swiss-Prot' if data.get('entryType', '').lower() == 'uniprotkb reviewed (swiss-prot)'.lower() else 'TrEMBL',
        'Nombre_del_gen': gen_data.get('geneName', {}).get('value', ''),
        'Sinónimos': ', '.join([s['value'] for s in gen_data.get('synonyms', [])]) if 'synonyms' in gen_data else '',
        'Organismo': data.get('organism', {}).get('scientificName', ''),
        'PDB_ids': ', '.join([x['id'] for x in data.get('uniProtKBCrossReferences', []) if x.get('database') == 'PDB'])
    }
# ========= PARTE 3: Obtención de ID de 1tup =========

# Función principal que procesa un ID de PDB
def procesar_pdb(pdb_id):
    print(f"Obteniendo datos de UniProt para {pdb_id}...")
    uniprot_id = obtener_uniprot_id(pdb_id)
    if uniprot_id:
        print(f"UniProt ID encontrado: {uniprot_id}")
        info = obtener_info_uniprot(uniprot_id)
        if info:
            return extraer_datos(info)
    print(f" No se pudo encontrar datos para {pdb_id}")
    return None

# ========= PARTE 4: Procesamiento de 1tup =========

# Lista de IDs de PDB a procesar
pdb_ids = ['1tup']  # Añadir más PDB IDs aquí si es necesario

# Obtención de resultados
resultados = []
for pdb_id in pdb_ids:
    print(f"Procesando PDB ID: {pdb_id} → buscando UniProt ID...")
    datos = procesar_pdb(pdb_id)
    if datos:
        resultados.append(datos)
    sleep(5)  # Evita saturar la API


# Crear DataFrame y guardar
df = pd.DataFrame(resultados, columns=[
    'Uniprot_id', 'Fecha_publicacion', 'Fecha_modificacion', 'Revisado',
    'Nombre_del_gen', 'Sinónimos', 'Organismo', 'PDB_ids'
])

# Ahora imprimes el DataFrame y lo guardas como CSV
print(df)
df.to_csv("informacion_uniprot_pdbs.csv", index=False)


##Obtengo un dataframe con los resultados de uniprot y las columns correspondientes
##Obtengo un dataframe con los resultados de uniprot y las columns correspondientes
#UniProt ID encontrado: P04637
 #Uniprot_id  ...                                            PDB_ids
#0     P04637  ...  1A1U, 1AIE, 1C26, 1DT7, 1GZH, 1H26, 1HS5, 1JSP...



# ===========================
# 1)C. Cofactor y Pubchem
# ===========================


#Uso el archivo descargado .cif del apartado A de 1tup. Parseo el archivo para
#obtener el cofactor, que en este acsoo es Zn+2 de manera automática con su CID
#Otra forma es ver en el link:https://rest.uniprot.org/uniprotkb/P04637.json
#en raw data, y buscar cofactor, y poder ver el cofactor manualmente (en este caso
#es factible ya que es solo 1, pero si fueran más parsear sería mejor opción

import os
import requests
import pandas as pd
from Bio.PDB.MMCIFParser import MMCIFParser

# ========= PARTE 1: Parseo el archivo cif  =========

def obtener_ligandos_desde_cif(ruta_cif):
    parser = MMCIFParser(QUIET=True)
    estructura = parser.get_structure("estructura", ruta_cif)

    ligandos = set()
    for modelo in estructura:
        for cadena in modelo:
            for residuo in cadena:
                hetero_flag = residuo.id[0]
                if hetero_flag.startswith("H_"):  # Heteroátomos (cofactores, iones, etc.)
                    ligandos.add(residuo.resname)
    return ligandos

# ========= PARTE 2: Consultar en PubChem =========

def obtener_cid(nombre_compuesto):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{nombre_compuesto}/cids/JSON"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            cids = data.get('IdentifierList', {}).get('CID', [])
            return cids[0] if cids else None
    except Exception as e:
        print(f"❌ Error obteniendo CID para {nombre_compuesto}: {e}")
    return None

def obtener_info_desde_cid(cid):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/MolecularWeight,InChI,InChIKey,IUPACName/JSON"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            props = r.json()['PropertyTable']['Properties'][0]
            return {
                'Pubchem_id': cid,
                'Peso_molecular': props.get('MolecularWeight', ''),
                'Inchi': props.get('InChI', ''),
                'Inchikey': props.get('InChIKey', ''),
                'Iupac_name': props.get('IUPACName', '')
            }
    except Exception as e:
        print(f"❌ Error obteniendo propiedades para CID {cid}: {e}")
    return {
        'Pubchem_id': cid,
        'Peso_molecular': '',
        'Inchi': '',
        'Inchikey': '',
        'Iupac_name': ''
    }

def consultar_pubchem_completo(nombre_compuesto):
    cid = obtener_cid(nombre_compuesto)
    if cid:
        props = obtener_info_desde_cid(cid)
        props['Compuesto'] = nombre_compuesto
        return props
    else:
        print(f"⚠️ No se encontró información para: {nombre_compuesto}")
        return {
            'Compuesto': nombre_compuesto,
            'Pubchem_id': '',
            'Peso_molecular': '',
            'Inchi': '',
            'Inchikey': '',
            'Iupac_name': ''
        }

# ========= PARTE 3: Ejecutar todo con CIF específico =========

# Ruta a tu archivo .cif
ruta_cif = r"C:\Users\resta\Desktop\desktop\estructuras_cif\1tup.cif"
ligandos = obtener_ligandos_desde_cif(ruta_cif)
print(f"Ligandos encontrados: {ligandos}")

# Consultar PubChem para cada ligando directamente
datos_pubchem = []
for lig in ligandos:
    try:
        datos_pubchem.append(consultar_pubchem_completo(lig))
    except Exception as e:
        print(f"No se pudo consultar {lig}: {e}")

# Crear DataFrame
df = pd.DataFrame(datos_pubchem, columns=[
    'Compuesto', 'Pubchem_id', 'Peso_molecular', 'Inchi', 'Inchikey', 'Iupac_name'
])
print(df)

# Guardar CSV
df.to_csv("info_cofactores_pubchem.csv", index=False)


#Ligandos encontrados: {'ZN'}
#Compuesto  Pubchem_id  ...                     Inchikey Iupac_name
#0        ZN       23994  ...  HCHKCACWOHOZIP-UHFFFAOYSA-N       zinc

# ===========================
# 2)A. Parsear mmcifpaser 
# ===========================


from Bio.PDB.MMCIFParser import MMCIFParser

# Importamos una función útil para saber si un residuo es un aminoácido
from Bio.PDB.Polypeptide import is_aa

import os

# Defino la ruta absoluta del archivo mmCIF 4OGQ
file_path = r"C:\Users\resta\Desktop\desktop\estructuras_cif\4ogq.cif"

# Comienzo el parser y parseamos la estructura
parser = MMCIFParser(QUIET=True) # QUIET=True evita que salgan advertencias innecesarias.
structure = parser.get_structure("4ogq", file_path)

# Lista para guardar heteromoléculas (sin incluir agua)
hetero_residues = []

# Recorro los modelos, cadenas y residuos
# Primero por cada modelo
for model in structure:
    # Luego por cada cadena (por ejemplo: cadena A, B, etc.)
    for chain in model:
        # Luego por cada residuo (aminoácido, ligando, ion, agua, etc.)
        for residue in chain:
            hetfield, resseq, icode = residue.id
            ## Cada residuo tiene una ID: (hetfield, resseq, icode)
            
            # Condición para filtrar:
            # 1. Que el residuo sea un heteroátomo (hetfield empieza por "H_") and
            # 2. Que NO sea agua ("HOH")!= , and not
            # 3. Que NO sea un aminoácido estándar (is_aa devuelve False)
            
            if hetfield.startswith("H_") and residue.get_resname() != "HOH" and not is_aa(residue):
                
                # Si cumple, lo añadimos a la lista
                hetero_residues.append(residue)

# Muestro los nombres únicos de las heteromoléculas encontradas
unique_heteros = sorted(set(res.get_resname() for res in hetero_residues))

# Imprimo resultados
print("Heteromoléculas encontradas (sin incluir agua):")
for h in unique_heteros:
    print("-", h)




# ===========================
# 2)B. Parsear MMCIFDICT 
# ===========================

from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import pandas as pd

# Ruta al archivo CIF
file_path = r"C:\Users\resta\Desktop\desktop\estructuras_cif\4ogq.cif"

# Parseo el CIF como diccionario (no como objeto estructural)
mmcif_dict = MMCIF2Dict(file_path)


#Esta clave contiene info sobre moléculas no poliméricas (ligandos, iones, etc.)

# Extraigo identificadores de 3 letras y nombres

compound_ids = mmcif_dict.get('_pdbx_entity_nonpoly.comp_id', []) 

#nombre de cada una de las heteromoléculas,
names = mmcif_dict.get('_pdbx_entity_nonpoly.name', [])

# Creo el DataFrame con esa información
df_nonpoly = pd.DataFrame({
    'Compound_ID': compound_ids,
    'Name': names
})

print(df_nonpoly)


# ===========================
# 2)c. SMILES y SDS archivo 
# ===========================

from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import pandas as pd
import requests

# ========= PARTE 1: Parseo el archivo CIF con MMCIF2Dict  =========

file_path = r"C:\Users\resta\Desktop\desktop\estructuras_cif\4ogq.cif"
mmcif_dict = MMCIF2Dict(file_path)

# Extraigo nombres e identificadores de heteromoléculas (no poliméricas)
names = mmcif_dict.get('_pdbx_entity_nonpoly.name', [])
compound_ids = mmcif_dict.get('_pdbx_entity_nonpoly.comp_id', [])

# Creo DataFrame base
df = pd.DataFrame({
    'Compound_ID': compound_ids,
    'Name': names
})

def get_smiles_from_pubchem(name):
    """
    Consulta PubChem usando el nombre del compuesto para obtener el SMILES canónico.
    """
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/CanonicalSMILES/TXT"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return None
    except:
        return None

# ========= PARTE 2: Añadir columna de SMILES al DataFrame =========

df['SMILES'] = df['Name'].apply(get_smiles_from_pubchem)


print(df)

# Guardo el resultado en CSV ===
df.to_csv("heteromoleculas_con_smiles.csv", index=False)



# ===========================
# 2)d. rdkit y SDS archivo 
# ===========================

from rdkit import Chem
from rdkit.Chem import AllChem

#Nombre del archivo
sdf_path = r"heteromolecules_with_weight.sdf"

def safe_str(val):
    # Convierte un valor a cadena, asegurando que valores nulos no causen errores.
    return str(val) if val is not None else "Unknown"

with Chem.SDWriter(sdf_path) as sdf_writer:
    for index, row in df.iterrows(): # Itera sobre cada fila del DataFrame que contiene los datos moleculares.
        try:
            smiles = row['SMILES'] # Extrae la cadena SMILES de la molécula.
            if pd.isna(smiles): # Verifico si la cadena SMILES está vacía o es NaN.
                print(f"SMILES vacío para {row['Name']}, saltando.")
                continue

            mol = Chem.MolFromSmiles(smiles) # Convierte la cadena SMILES a un objeto Mol de RDKit.
            if mol:
                # Calcular peso molecular
                mol_wt = AllChem.CalcExactMolWt(mol) # Calcula el peso molecular exacto de la molécula.

                # Asignar propiedades seguras
                mol.SetProp("Compound_ID", safe_str(row.get("Compound_ID")))
                mol.SetProp("Name", safe_str(row.get("Name")))
                mol.SetProp("Molecular_weight", str(mol_wt))

                # Escribir al archivo SDF
                sdf_writer.write(mol)
            else:
                print(f"Mol inválido para {row['Name']}")
        except Exception as e:
            print(f"Error procesando {row.get('Name', 'Unknown')}: {e}")

# Leo el archivo SDF generado para verificar las propiedades almacenadas.
supplier = Chem.SDMolSupplier(r"heteromolecules_with_weight.sdf")
for mol in supplier:
    if mol is not None:
        print(mol.GetProp("Name"), "→", mol.GetProp("Molecular_weight"))
