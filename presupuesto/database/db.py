from dotenv import load_dotenv
import os
from supabase import create_client, Client
import pandas as pd

load_dotenv()

class SupabaseAPI:

    def __init__(self) -> None:
        # Acceder a las variables de entorno
        self.secret_key: str = os.getenv('SUPABASE_KEY')
        self.database_url: str = os.getenv('SUPABASE_URL')
        self.supabase: Client = create_client(self.database_url, self.secret_key)

    def obtener_saldo_inicial(self, banco: str) -> float:
        # Obtener el saldo inicial restando el importe de la primera transacción
        response = self.supabase.table(banco).select("SALDO", "IMPORTE") \
            .order("FECHA") \
            .limit(1) \
            .execute()

        if response.data:
            saldo, importe = response.data[0]["SALDO"], response.data[0]["IMPORTE"]
            return saldo - importe
        return 0.0  # Si no hay datos, retornar 0

    def obtener_tabla(self, banco: str, fecha_inicio: str, fecha_fin: str, Categoria: str | None = None) -> list:
        # Construir la consulta base
        query = self.supabase.table(banco).select("FECHA", "CONCEPTO", "Categoria", "IMPORTE", "SALDO") \
            .gte("FECHA", fecha_inicio) \
            .lte("FECHA", fecha_fin) \
            .order("FECHA")

        # Filtrar por categoría si es proporcionada
        if Categoria:
            query = query.eq("Categoria", Categoria)

        # Ejecutar la consulta y devolver los resultados
        response = query.execute()
        # Si hay datos, los procesamos cambiando los nombres de las claves a minúsculas con la primera en mayúscula
        if response.data:
            transformed_data = [
                {key.capitalize(): value for key, value in row.items()}  # Cambia las claves a formato deseado
                for row in response.data
            ]
            return transformed_data
        
        return []

    def obtener_saldos(self, banco: str, fecha_inicio: str, fecha_fin: str) -> list:
        # Método para obtener los saldos en un rango de fechas, aún por implementar
        pass
