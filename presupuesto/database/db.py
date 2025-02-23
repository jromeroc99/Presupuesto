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

    def obtener_saldo_inicial(self, user_id: str,banco: str) -> float:
        # Obtener el saldo inicial restando el importe de la primera transacción
        query = self.supabase.table("Cuentas").select("Saldo_ini") \
        .eq("user_id",user_id)
            
            
        if banco != "Global":
            query=query.eq("Cuenta",banco) \
            
        # Ejecutar la consulta y devolver los resultados
        response = query.execute()

        
        if response.data:
            return sum([data["Saldo_ini"] for data in response.data])

        return 0.0  # Si no hay datos, retornar 0

    def obtener_tabla(self, user_id: str,banco: str, fecha_inicio: str, fecha_fin: str) -> list:
        # Construir la consulta base
        #banco="Efectivo"
        query = self.supabase.table("Movimientos").select("Cuentas!inner(Cuenta)","fecha", "concepto", "Categorias!inner(Nombre)", "importe") \
            .eq("user_id",user_id) \
            .gte("fecha", fecha_inicio) \
            .lte("fecha", fecha_fin) \
            .order("fecha")
        
        if banco=="Global":
            pass
        else:
            query=query.eq("Cuentas.Cuenta",banco) \




        # Ejecutar la consulta y devolver los resultados
        response = query.execute()
        
        # Si hay datos, los procesamos cambiando los nombres de las claves a minúsculas con la primera en mayúscula
        
        if response.data:
            transformed_data = [
                {key.capitalize(): value for key, value in row.items()}  # Cambia las claves a formato deseado
                for row in response.data
            ]
            for row in transformed_data:
                row["Cuentas"] = row["Cuentas"]["Cuenta"]
                row["Categorias"] = row["Categorias"]["Nombre"]

            print(transformed_data)
            return transformed_data
        
        return []

    def obtener_saldos(self, user_id: str,banco: str, fecha: str) -> list:
        # Método para obtener los saldo en una fecha
        Saldo_inicial = self.obtener_saldo_inicial(user_id,banco)

        # Construir la consulta base
        query = self.supabase.table("Movimientos").select("Cuentas!inner(Cuenta)","importe") \
            .eq("user_id",user_id) \
            .lte("fecha", fecha) \
            .order("fecha")

        if banco=="Global":
            pass
        else:
            query=query.eq("Cuentas.Cuenta",banco) \


        # Ejecutar la consulta y devolver los resultados
        response = query.execute()
        # Si hay datos, los procesamos cambiando los nombres de las claves a minúsculas con la primera en mayúscula
        if response.data:
            transformed_data = [
                {key: value for key, value in row.items()}  # Cambia las claves a formato deseado
                for row in response.data
            ]


            return Saldo_inicial + sum([data["importe"]  for data in transformed_data])
        return 0.0

