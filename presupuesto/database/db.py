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
        query = self.supabase.table("Cuentas").select("Saldo_ini") \
            
            
        if banco=="Global":
            pass
        else:
            query=query.eq("Cuenta",banco) \
            
        # Ejecutar la consulta y devolver los resultados
        response = query.execute()

        if response.data:
            return sum([data["Saldo_ini"] for data in response.data])

        return 0.0  # Si no hay datos, retornar 0

    def obtener_tabla(self, banco: str, fecha_inicio: str, fecha_fin: str, Categoria: str | None = None) -> list:
        # Construir la consulta base
        query = self.supabase.table("Movimientos").select("Banco","FECHA", "CONCEPTO", "Categoria", "IMPORTE") \
            .gte("FECHA", fecha_inicio) \
            .lte("FECHA", fecha_fin) \
            .order("FECHA")
        
        if banco=="Global":
            pass
        else:
            query=query.eq("Banco",banco) \

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

    def obtener_saldos(self, banco: str, fecha: str) -> list:
        # Método para obtener los saldo en una fecha
        Saldo_inicial = self.obtener_saldo_inicial(banco)

        # Construir la consulta base
        query = self.supabase.table("Movimientos").select("IMPORTE") \
            .lte("FECHA", fecha) \
            .order("FECHA")

        if banco=="Global":
            pass
        else:
            query=query.eq("Banco",banco) \


        # Ejecutar la consulta y devolver los resultados
        response = query.execute()
        # Si hay datos, los procesamos cambiando los nombres de las claves a minúsculas con la primera en mayúscula
        if response.data:
            transformed_data = [
                {key.capitalize(): value for key, value in row.items()}  # Cambia las claves a formato deseado
                for row in response.data
            ]

            return Saldo_inicial + sum([data["Importe"]  for data in transformed_data])
        return 0.0

