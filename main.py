from presupuesto.database.db import SupabaseAPI
import os
os.system('cls' if os.name == 'nt' else 'clear')

DB = SupabaseAPI()

DT=DB.obtener_tabla("Santander","2025-02-01", "2025-02-08","Trabajo")

Saldo_ini = DB.obtener_saldo_inicial("Santander")

