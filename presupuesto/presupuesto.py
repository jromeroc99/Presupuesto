"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

from presupuesto.pages.index_page import index
from presupuesto.api.api import obtener_Tabla, obtener_Saldo




app = rx.App()
app.add_page(index)
app.api.add_api_route("/movimientos/{banco}/{fecha_inicio}/{fecha_fin}", obtener_Tabla)
app.api.add_api_route("/saldo/{banco}/{fecha}/", obtener_Saldo)