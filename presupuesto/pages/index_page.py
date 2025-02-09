import reflex as rx
from presupuesto.components.calendario import calendar_dialog
from presupuesto.views.table import main_table
from presupuesto.states.state import PageState

@rx.page(on_load=PageState.crear_tabla)
def index() -> rx.Component:
    return rx.box(
        rx.heading("Bienvenido Javi!", size="7"),
        main_table(),
        padding="25px",
        width="100%", 
    )