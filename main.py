import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno ocultas
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Inicializar el cliente de Supabase
supabase: Client = create_client(url, key)

def ingestar_datos():
    #print("Cargando CSV en memoria...")
    df = pd.read_csv('./data/ICE_Detention_Trends new.csv')

    # Asegura que la fecha tenga el formato correcto para PostgreSQL
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    # Prevenir errores de JSON reemplazando posibles valores 
    df = df.where(pd.notnull(df), None)

    # Convertir el DataFrame a una lista de diccionarios (formato requerido por la API)
    registros = df.to_dict(orient='records')
    total_registros = len(registros)
    print(f"Preparando {total_registros} registros para subir...")

    # Subir en lotes de 1000 para no exceder los límites de payload de Supabase
    tamaño_lote = 1000
    for i in range(0, total_registros, tamaño_lote):
        lote = registros[i : i + tamaño_lote]
        
        # Usamos upsert: inserta si es nuevo, actualiza si la fecha ya existe
        respuesta = supabase.table('ice_detention_trends').upsert(lote).execute()
        
        print(f"Lote {i // tamaño_lote + 1} subido con éxito.")

    print("Datos subidos en Supabase.")

if __name__ == "__main__":
    ingestar_datos()