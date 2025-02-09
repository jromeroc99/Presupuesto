import reflex as rx
from presupuesto.components.calendario import calendar_dialog
from presupuesto.views.table import main_table,_header_cell
from presupuesto.views.balances import balances_selector
from presupuesto.states.state import PageState

def header(text,icon):
        return rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),


def Selector():
    return rx.vstack(
        # Selector de tipo de balance
        rx.segmented_control.root(
            rx.segmented_control.item(header("Tabla","table-2"), value="Tabla"),
            rx.segmented_control.item(header("Balances","chart-spline"), value="Balances"),
            on_change=PageState.set_mostrado,  # Estado para cambiar el balance mostrado
            value=PageState.Mostrar,
        ),

        # Tarjeta con el gráfico dinámico
        rx.card(
            rx.cond(
                PageState.Mostrar == "Tabla",
                main_table(),
                balances_selector()
            ),
            width="100%",
        ),
    )




@rx.page(on_load=PageState.crear_tabla)
def index() -> rx.Component:
    return rx.box(
        rx.theme_panel(default_open=True),
        rx.heading("Bienvenido Javi!", size="7"),
        Selector(),
        padding="25px",
        width="100%", 
    )