from presupuesto.database.db import SupabaseAPI

async def obtener_Tabla(banco: str, fecha_inicio: str, fecha_fin: str) -> list:
    DB = SupabaseAPI()
    return DB.obtener_tabla(banco,fecha_inicio,fecha_fin)


async def obtener_Saldo(banco: str, fecha: str) -> float:
    DB = SupabaseAPI()
    return DB.obtener_saldos(banco,fecha)