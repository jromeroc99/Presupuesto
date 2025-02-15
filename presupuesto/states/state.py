import reflex as rx
import pandas as pd
from datetime import datetime
from presupuesto.models.movimiento import Movimiento
from presupuesto.api.api import obtener_Tabla, obtener_Saldo
today = datetime.today()

class PageState(rx.State):
    Bancos: list[str] =["Santander","Revolut","MY Investor","Trade Republic","Efectivo"]
    Tabla: list[Movimiento] = []
    Tabla_filtrada: list[Movimiento] = []
    Saldo: str
    banco: str = "Santander"
    start_date: str = today.replace(month=1, day=1).strftime("%a %b %d %Y")   # Valor por defecto para start_date
    end_date: str = today.strftime("%a %b %d %Y") # Valor por defecto vacío para end_date
    fecha_ini: str = today.replace(month=1, day=1).strftime("%Y-%m-%d")
    fecha_fin: str = today.strftime("%Y-%m-%d")


    data_balances: list[dict] = []
    data_balances_mensuales: list[dict] = []
    data_balances_anuales: list[dict] = []
    data_categorias: list[dict] = []

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page

    Mostrar: str = "Tabla"
    balance_type: str = "diario"  # Estado inicial (Diario)

    ingresos_filtrado: str = ""
    gastos_filtrado: str = ""
    balance_filtrado: str = ""
    
    @rx.event
    async def change_bank(self, var: str):
        self.banco = var
        await self.crear_tabla()


    def set_mostrado(self, var: str|list[str]):
        self.Mostrar = var
        
    # Método para actualizar el tipo de balance seleccionado
    def set_balance_type(self, balance: str|list[str]):
        self.balance_type = balance


    def cambiar_formato(self):
        # Intentar convertir la fecha a un objeto datetime con el formato esperado

        fecha_ini = datetime.strptime(self.start_date, "%a %b %d %Y")
        fecha_fin = datetime.strptime(self.end_date, "%a %b %d %Y")

        # Convertir el objeto datetime a formato "YYYY-MM-DD"
        self.fecha_ini = fecha_ini.strftime("%Y-%m-%d")
        self.fecha_fin = fecha_fin.strftime("%Y-%m-%d")


    async def change_range_handler(self, var: str):
        self.start_date, self.end_date = var
        self.cambiar_formato()
        await self.crear_tabla()


    async def crear_tabla(self):
        movimientos = await obtener_Tabla(self.banco,self.fecha_ini,self.fecha_fin)
        Saldo = await obtener_Saldo(self.banco,self.fecha_fin)
        self.Saldo = f"Saldo: {round(Saldo,2)} €"
        # Verifica el contenido de los movimientos
        # Asegúrate de que las claves del diccionario coinciden con las propiedades del modelo Movimiento
        
        self.Tabla = [Movimiento(**row) for row in movimientos]
        self.Tabla_filtrada = self.Tabla
        self.total_items = len(self.Tabla)
        self.obtener_ingresos_gastos()
        self.obtener_categorias()

        self.ingresos_filtrado = f"Ingresos: {round(sum([mov.Importe for mov in self.Tabla if mov.Importe > 0]),2)} €"
        self.gastos_filtrado = f"Gastos: {round(sum([mov.Importe for mov in self.Tabla if mov.Importe < 0]),2)} €"
        self.balance_filtrado = f"Balance: {round(sum([mov.Importe for mov in self.Tabla]),2)} €"

        


    @rx.var(cache=True)
    def filtered_sorted_movs(self) -> list[Movimiento]:
        movimientos = self.Tabla  # Cambié 'players' por 'movimientos'

        # Filtrar movimientos basado en el valor seleccionado
        if self.sort_value:
            if self.sort_value in ["Saldo", "Importe"]:  # Orrdena los numeros
                movimientos = sorted(
                    movimientos,
                    key=lambda movimiento: float(getattr(movimiento, self.sort_value)),
                    reverse=self.sort_reverse,
                )
            else: # Ordena las letras
                movimientos = sorted(
                    movimientos,
                    key=lambda movimiento: str(getattr(movimiento, self.sort_value)).lower(),
                    reverse=self.sort_reverse,
                )

        # Filtrar movimientos basado en el valor de búsqueda
        if self.search_value:
            search_value = self.search_value.lower()
            movimientos = [
                movimiento
                for movimiento in movimientos
                if any(
                    search_value in str(getattr(movimiento, attr)).lower() #Get attr es como Movimiento.Fecha
                    for attr in [
                        "Fecha",
                        "Concepto",
                        "Categoria",
                        "Importe",
                    ]
                )
            ]

            self.Tabla_filtrada = movimientos
        
        return movimientos
    
    @rx.event
    def calcular_balance_tabla(self):
            movimientos = self.Tabla_filtrada
            self.ingresos_filtrado = f"Ingresos: {round(sum([mov.Importe for mov in movimientos if mov.Importe > 0]),2)} €"
            self.gastos_filtrado = f"Gastos: {round(sum([mov.Importe for mov in movimientos if mov.Importe < 0]),2)} €"
            self.balance_filtrado = f"Balance: {round(sum([mov.Importe for mov in movimientos]),2)} €"
    

    

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 0
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[Movimiento]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_movs[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        #await self.crear_tabla()

    def set_search_value(self,var:str):
        self.search_value = var

    def set_sort_value(self,var:str):
        self.sort_value = var


    def obtener_ingresos_gastos(self):
        movimientos = self.Tabla
        dias = sorted(set([row.Fecha for row in movimientos]))  # Ordenar fechas
        lista = []

        ingresos_acumulados = 0
        gastos_acumulados = 0

        for dia in dias:
            data = {}
            movimientos_diarios = [mov for mov in movimientos if mov.Fecha == dia]

            ingresos_dia = sum([mov.Importe for mov in movimientos_diarios if mov.Importe > 0])
            gastos_dia = sum([mov.Importe for mov in movimientos_diarios if mov.Importe < 0])

            ingresos_acumulados += ingresos_dia
            gastos_acumulados += abs(gastos_dia)  # Gasto como positivo

            data["Fecha"] = dia
            data["Ingresos"] = round(ingresos_dia, 2)
            data["Gastos"] = abs(round(gastos_dia, 2))
            data["Ingresos Acumulados"] = round(ingresos_acumulados, 2)
            data["Gastos Acumulados"] = round(gastos_acumulados, 2)

            lista.append(data)

        self.data_balances = lista
        self.obtener_ingresos_gastos_mensuales()
        self.obtener_ingresos_gastos_anuales()



    def obtener_ingresos_gastos_mensuales(self):
        """Agrupa los ingresos y gastos por mes y calcula acumulados."""
        data_mensual = {}
        
        ingresos_acumulados = 0
        gastos_acumulados = 0

        for item in self.data_balances:
            fecha = datetime.strptime(item["Fecha"], "%Y-%m-%d")
            mes = fecha.strftime("%Y-%m")  # Formato Año-Mes (Ej: "2025-01")

            if mes not in data_mensual:
                data_mensual[mes] = {"Ingresos": 0, "Gastos": 0}

            data_mensual[mes]["Ingresos"] += item["Ingresos"]
            data_mensual[mes]["Gastos"] += item["Gastos"]

        lista_mensual = []
        for mes in sorted(data_mensual.keys()):
            ingresos_acumulados += data_mensual[mes]["Ingresos"]
            gastos_acumulados += data_mensual[mes]["Gastos"]

            lista_mensual.append({
                "Fecha": mes,
                "Ingresos": round(data_mensual[mes]["Ingresos"], 2),
                "Gastos": round(data_mensual[mes]["Gastos"], 2),
                "Ingresos Acumulados": round(ingresos_acumulados, 2),
                "Gastos Acumulados": round(gastos_acumulados, 2)
            })

        self.data_balances_mensuales = lista_mensual

    def obtener_ingresos_gastos_anuales(self):
        """Agrupa los ingresos y gastos por año y calcula acumulados."""
        data_anual = {}

        ingresos_acumulados = 0
        gastos_acumulados = 0

        for item in self.data_balances:
            fecha = datetime.strptime(item["Fecha"], "%Y-%m-%d")
            anio = fecha.strftime("%Y")  # Formato Año (Ej: "2025")

            if anio not in data_anual:
                data_anual[anio] = {"Ingresos": 0, "Gastos": 0}

            data_anual[anio]["Ingresos"] += item["Ingresos"]
            data_anual[anio]["Gastos"] += item["Gastos"]

        lista_anual = []
        for anio in sorted(data_anual.keys()):
            ingresos_acumulados += data_anual[anio]["Ingresos"]
            gastos_acumulados += data_anual[anio]["Gastos"]

            lista_anual.append({
                "Fecha": anio,
                "Ingresos": round(data_anual[anio]["Ingresos"], 2),
                "Gastos": round(data_anual[anio]["Gastos"], 2),
                "Ingresos Acumulados": round(ingresos_acumulados, 2),
                "Gastos Acumulados": round(gastos_acumulados, 2)
            })

        self.data_balances_anuales = lista_anual

   
    def obtener_categorias(self):
        movimientos = self.Tabla
        categorias = sorted(set([row.Categoria for row in movimientos]))  # Ordenar fechas
        lista = []



        for categoria in categorias:
            data = {}
            movimientos_categoricos = [mov for mov in movimientos if mov.Categoria == categoria]

            ingresos = sum([mov.Importe for mov in movimientos_categoricos if mov.Importe > 0])
            gastos = sum([mov.Importe for mov in movimientos_categoricos if mov.Importe < 0])

            tot_ingresos = sum([mov.Importe for mov in movimientos if mov.Importe > 0])
            tot_gastos = sum([mov.Importe for mov in movimientos if mov.Importe < 0])



            data["Categoria"] = f"{categoria}"
            data["Ingresos"] = round(ingresos, 2)
            data["Gastos"] = abs(round(gastos, 2))


            lista.append(data)

        self.data_categorias = lista


    


