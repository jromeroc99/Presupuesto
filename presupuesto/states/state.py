import reflex as rx
import pandas as pd
from datetime import datetime
from presupuesto.models.movimiento import Movimiento
from presupuesto.api.api import obtener_Tabla
today = datetime.today()

class PageState(rx.State):
    Tabla: list[Movimiento] = []
    banco: str = "Santander"
    start_date: str = today.replace(month=1, day=1).strftime("%a %b %d %Y")   # Valor por defecto para start_date
    end_date: str = today.strftime("%a %b %d %Y") # Valor por defecto vacío para end_date
    fecha_ini: str = today.replace(month=1, day=1).strftime("%Y-%m-%d")
    fecha_fin: str = today.strftime("%Y-%m-%d")
    logs: list[str] = []

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page


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
        # Verifica el contenido de los movimientos
        # Asegúrate de que las claves del diccionario coinciden con las propiedades del modelo Movimiento

        self.Tabla = [Movimiento(**row) for row in movimientos]
        self.total_items = len(self.Tabla)


    @rx.var(cache=True)
    def filtered_sorted_movs(self) -> list[Movimiento]:
        movimientos = self.Tabla  # Cambié 'players' por 'movimientos'

        # Filtrar movimientos basado en el valor seleccionado
        if self.sort_value:
            if self.sort_value in ["Saldo", "Importe"]:  # Cambié 'salary' y 'number' por los campos de Movimiento
                movimientos = sorted(
                    movimientos,
                    key=lambda movimiento: float(getattr(movimiento, self.sort_value)),
                    reverse=self.sort_reverse,
                )
            else:
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
                    search_value in str(getattr(movimiento, attr)).lower()
                    for attr in [
                        "Fecha",
                        "Concepto",
                        "Categoria",
                        "Importe",
                        "Saldo",
                    ]
                )
            ]

        return movimientos


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


