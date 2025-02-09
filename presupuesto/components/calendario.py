import reflex as rx
from reflex_calendar import calendar
from presupuesto.states.state import PageState

def calendario():
    return rx.vstack(

        rx.hstack(
            rx.text(PageState.fecha_ini),
            rx.text(PageState.fecha_fin),
        ),
        calendar(
            locale="es-ES",
            select_range=True,
            return_value="range",
            on_change=PageState.change_range_handler,
        ),
        align="center",
        width="100%",
    )

def calendar_dialog():
    return rx.dialog.root(
    rx.dialog.trigger(rx.link(rx.icon("calendar"))),
    rx.dialog.content(
        rx.dialog.title("Selecciona fechas!"),
        rx.dialog.description(
            "Selecciona el intervalo de fechas donde quieras analizar tus movimientos bancarios.",
        ),
        rx.center(calendario()),
        rx.flex(
            rx.dialog.close(
                rx.button(
                    "Cerrar",
                    color_scheme="gray",
                    variant="soft",
                ),
            ),
            spacing="3",
            margin_top="16px",
            justify="end",
        ),
        
    ),
)