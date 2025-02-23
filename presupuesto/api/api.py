from presupuesto.database.db import SupabaseAPI

async def obtener_Tabla(user_id: str, banco: str, fecha_inicio: str, fecha_fin: str) -> list:
    DB = SupabaseAPI()
    return DB.obtener_tabla(user_id,banco,fecha_inicio,fecha_fin)


async def obtener_Saldo(user_id: str, banco: str, fecha: str) -> float:
    DB = SupabaseAPI()
    return DB.obtener_saldos(user_id,banco,fecha)