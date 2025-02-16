import reflex as rx

from presupuesto.models.movimiento import Movimiento
from presupuesto.states.state import PageState
from presupuesto.components.calendario import calendar_dialog
from presupuesto.components.item_badges import item_badge

from presupuesto.constants import Colores_Bancos,Colores_Categorias

def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )





def _pagination_view() -> rx.Component:
    return (
        rx.hstack(
            rx.text("Intervalo de fechas: "),
            rx.text(PageState.fecha_ini),
            rx.icon("arrow-right"),
            rx.text(PageState.fecha_fin),
            rx.spacer(),
            rx.badge(PageState.ingresos_filtrado, color_scheme="green"),
            rx.badge(PageState.gastos_filtrado, color_scheme="red"),
            rx.badge(PageState.balance_filtrado, color_scheme="purple"),

            rx.text(
                "Página ",
                rx.code(PageState.page_number),
                f" de {PageState.total_pages}",
                justify="end",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevrons-left", size=18),
                    on_click=PageState.first_page,
                    opacity=rx.cond(PageState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(PageState.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=PageState.prev_page,
                    opacity=rx.cond(PageState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(PageState.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", size=18),
                    on_click=PageState.next_page,
                    opacity=rx.cond(PageState.page_number == PageState.total_pages, 0.6, 1),
                    color_scheme=rx.cond(
                        PageState.page_number == PageState.total_pages, "gray", "accent"
                    ),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevrons-right", size=18),
                    on_click=PageState.last_page,
                    opacity=rx.cond(PageState.page_number == PageState.total_pages, 0.6, 1),
                    color_scheme=rx.cond(
                        PageState.page_number == PageState.total_pages, "gray", "accent"
                    ),
                    variant="soft",
                ),
                align="center",
                spacing="2",
                justify="end",
            ),
            spacing="5",
            margin_top="1em",
            align="center",
            width="100%",
            justify="end",
        ),
    )




def _mostrar_movimiento(mov: Movimiento, index: int) -> rx.Component:
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(mov.Fecha),
        rx.table.cell(item_badge(mov.Banco, Colores_Bancos)),
        rx.table.cell(mov.Concepto),
        rx.table.cell(item_badge(mov.Categoria, Colores_Categorias)),
        rx.table.cell(
            rx.cond(
                mov.Importe>0,
                rx.text(mov.Importe,color_scheme='green'),
                rx.text(mov.Importe,color_scheme='red')
            )
        ),

        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )

def main_table() -> rx.Component:
    return rx.fragment(
        rx.flex(
            rx.heading("Cuenta Seleccionada: "),
            rx.select(
                items=PageState.Bancos,
                value=PageState.banco,
                on_change=PageState.change_bank
            ),
            rx.badge(PageState.Saldo,size="3",variant="outline"),
            rx.spacer(),
            rx.button(
                "Balance",
                on_click=PageState.calcular_balance_tabla,
            ),
            calendar_dialog(),
            rx.cond(
                PageState.sort_reverse,
                rx.icon(
                    "arrow-down-z-a",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=PageState.toggle_sort,
                ),
                rx.icon(
                    "arrow-down-a-z",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=PageState.toggle_sort,
                ),
            ),
            rx.select(
                [
                    "Banco",
                    "Fecha",
                    "Concepto",
                    "Categoria",
                    "Importe",
                ],
                placeholder="Ordenar por...",
                size="3",
                on_change=PageState.set_sort_value,
            ),
            rx.input(
                rx.input.slot(rx.icon("search")),
                rx.input.slot(
                    rx.icon("x"),
                    justify="end",
                    cursor="pointer",
                    on_click=PageState.setvar("search_value", ""),
                    display=rx.cond(PageState.search_value, "flex", "none"),
                ),
                value=PageState.search_value,
                placeholder="Buscar por...",
                size="3",
                max_width="250px",
                width="100%",
                variant="surface",
                color_scheme="gray",
                on_change=PageState.set_search_value,
            ),
            align="center",
            justify="end",
            spacing="3",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Fecha", "calendar-days"),
                    _header_cell("Cuenta", "landmark"),
                    _header_cell("Concepto", "hand-coins"),
                    _header_cell("Categoria", "briefcase-business"),
                    _header_cell("Importe", "euro"),
                ),
            ),
        rx.table.body(
                rx.foreach(
                    PageState.get_current_page,
                    lambda mov, index: _mostrar_movimiento(mov, index),
                )
            ),

            variant="surface",
            size="3",
            width="100%",
        ),
        _pagination_view(),
    )