import pandas as pd
from sqlalchemy import create_engine
import urllib
import sys

# --- CONFIGURACIÓN ---
SERVER = 'localhost\\SQLEXPRESS'  # Ajusta según tu configuración
DATABASE = 'NombreBaseDeDatos'

def get_db_connection():
    try:
        # Configuración para Windows Authentication
        params = urllib.parse.quote_plus(
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            r'Trusted_Connection=yes;'
        )
        # Crear el engine 
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
        return engine
    except Exception as e:
        print(f"❌ Error configurando la conexión: {e}")
        sys.exit(1)

# --- 1. EXTRACT (Extracción) ---
def extract():
    print("--- 1. Iniciando Extracción ---")
    # Ajusta las rutas de los archivos 
    base_path = ''  # Si los CSV están en el mismo directorio, dejar vacío
    
    df_juegos = pd.read_csv(base_path + 'juegos.csv', encoding='latin-1')
    df_jugadores = pd.read_csv(base_path + 'jugadores.csv', encoding='latin-1')
    df_sesiones = pd.read_csv(base_path + 'sesiones.csv', encoding='latin-1')
    df_compras = pd.read_csv(base_path + 'compras_en_plataforma.csv', encoding='latin-1')
    df_puntuaciones = pd.read_csv(base_path + 'puntuaciones.csv', encoding='latin-1')

    print(f"   -> Juegos extraídos: {len(df_juegos)}")
    print(f"   -> Jugadores extraídos: {len(df_jugadores)}")

    return df_juegos, df_jugadores, df_sesiones, df_compras, df_puntuaciones

# --- 2. TRANSFORM (Transformación) ---

def transform(df_juegos, df_jugadores, df_sesiones, df_compras, df_puntuaciones):
    print("--- 2. Iniciando Transformación ---")
    
    # 1. Limpieza básica de JUEGOS
    df_juegos['fecha_lanzamiento'] = df_juegos['fecha_lanzamiento'].replace(20.13, 2013)
    df_juegos['fecha_lanzamiento'] = pd.to_numeric(df_juegos['fecha_lanzamiento'], errors='coerce').fillna(0).astype(int)

    # 2. Conversión de Fechas
    df_jugadores['fecha_registro'] = pd.to_datetime(df_jugadores['fecha_registro'], format='%m/%d/%Y', errors='coerce')
    df_sesiones['fecha_inicio'] = pd.to_datetime(df_sesiones['fecha_inicio'], format='%m/%d/%Y %H:%M', errors='coerce')
    df_sesiones['fecha_fin'] = pd.to_datetime(df_sesiones['fecha_fin'], format='%m/%d/%Y %H:%M', errors='coerce')
    df_compras['fecha'] = pd.to_datetime(df_compras['fecha'], format='%m/%d/%Y', errors='coerce')
    df_puntuaciones['fecha'] = pd.to_datetime(df_puntuaciones['fecha'], format='%m/%d/%Y', errors='coerce')

    # 3. Limpieza de Nulos en Puntuaciones
    if 'puntuacion' in df_puntuaciones.columns:
        df_puntuaciones = df_puntuaciones.dropna(subset=['puntuacion'])

    # 4. Limpieza de Nulos en Compras
    n_nulos_monto = df_compras['monto'].isna().sum()
    if n_nulos_monto > 0:
        df_compras = df_compras.dropna(subset=['monto'])
        print(f"      ⚠️ Se eliminaron {n_nulos_monto} compras con monto NULL.")

    # ---------------------------------------------------------
    # 5. DEDUPLICACIÓN DE PUNTUACIONES (EL FIX NUEVO)
    # ---------------------------------------------------------
    print("   -> Gestionando duplicados en Puntuaciones...")
    len_inicial_pts = len(df_puntuaciones)
    
    # keep='last' asume que si aparece dos veces, el último es la corrección del usuario
    df_puntuaciones = df_puntuaciones.drop_duplicates(subset=['id_jugador', 'id_juego', 'fecha'], keep='last')
    
    dupes = len_inicial_pts - len(df_puntuaciones)
    if dupes > 0:
        print(f"      ⚠️ Se eliminaron {dupes} puntuaciones duplicadas (mismo jugador/juego/fecha).")

    # ---------------------------------------------------------
    # 6. VALIDACIÓN DE INTEGRIDAD REFERENCIAL
    # ---------------------------------------------------------
    print("   -> Filtrando registros huérfanos (IDs no existentes)...")
    
    ids_juegos_validos = df_juegos['id_juego'].unique()
    ids_jugadores_validos = df_jugadores['id_jugador'].unique()

    def filtrar_invalidos(df, nombre_df):
        initial_len = len(df)
        if 'id_juego' in df.columns:
            df = df[df['id_juego'].isin(ids_juegos_validos)]
        if 'id_jugador' in df.columns:
            df = df[df['id_jugador'].isin(ids_jugadores_validos)]
        
        removed = initial_len - len(df)
        if removed > 0:
            print(f"      ⚠️ Se eliminaron {removed} registros inválidos de {nombre_df} (ID no encontrado)")
        return df

    df_sesiones = filtrar_invalidos(df_sesiones, "Sesiones")
    df_compras = filtrar_invalidos(df_compras, "Compras")
    df_puntuaciones = filtrar_invalidos(df_puntuaciones, "Puntuaciones")

    return df_juegos, df_jugadores, df_sesiones, df_compras, df_puntuaciones

# --- 3. LOAD (Carga) ---
def load(engine, df_juegos, df_jugadores, df_sesiones, df_compras, df_puntuaciones):
    """
    Carga los DataFrames usando el engine 
    """
    try:
        print("--- 3. Iniciando Carga de Datos ---")
        
        
        # 1. CARGA DE DIMENSIONES (Primero estas para evitar error de FK)
        print("Cargando Juegos...")
        df_juegos.to_sql('juegos', con=engine, if_exists='append', index=False)
        
        print("Cargando Jugadores...")
        df_jugadores.to_sql('jugadores', con=engine, if_exists='append', index=False)
        
        # 2. CARGA DE HECHOS
        print("Cargando Sesiones...")
        df_sesiones.to_sql('sesiones', con=engine, if_exists='append', index=False)
        
        print("Cargando Compras...")
        df_compras.to_sql('compras_en_plataforma', con=engine, if_exists='append', index=False)
        
        print("Cargando Puntuaciones...")
        df_puntuaciones.to_sql('puntuaciones', con=engine, if_exists='append', index=False)
        
        print("✅ ¡Carga completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la carga a SQL: {e}")
       

# --- MAIN ---
if __name__ == "__main__":
    # 1. Conectar (Creamos el objeto engine aquí)
    engine = get_db_connection()
    
    # 2. Flujo ETL
    juegos, jugadores, sesiones, compras, puntos = extract()
    juegos_t, jugadores_t, sesiones_t, compras_t, puntos_t = transform(juegos, jugadores, sesiones, compras, puntos)
    
    # 3. Cargar (Pasamos el objeto engine a la función)
    load(engine, juegos_t, jugadores_t, sesiones_t, compras_t, puntos_t)