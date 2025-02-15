import reflex as rx
from presupuesto.states.state import PageState

def balances(data):
    return rx.recharts.composed_chart(

        rx.recharts.area(
            data_key="Ingresos", stroke="green", fill="green"
        ),
        rx.recharts.area(
            data_key="Gastos", stroke="red", fill="red"
        ),
        rx.recharts.brush(
            data_key="Fecha", height=30, stroke="#8884d8"
        ),
        rx.recharts.x_axis(data_key="Fecha"),
        rx.recharts.y_axis(
            label={
                "value": "Euros",
                "angle": -90,
                "position": "left",
            },
        ),
        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
        rx.recharts.graphing_tooltip(),
        data=data,
        height=500,
        width="100%",
    )

"""
rx.recharts.bar(
    data_key="Ingresos Acumulados", bar_size=10, fill="green"
),
rx.recharts.bar(
    data_key="Gastos Acumulados", bar_size=10, fill="red"
),
"""


import reflex as rx

def balances_selector():
    return rx.vstack(
        # Selector de tipo de balance
        rx.segmented_control.root(
            rx.segmented_control.item("Diario", value="diario"),
            rx.segmented_control.item("Mensual", value="mensual"),
            rx.segmented_control.item("Anual", value="anual"),
            on_change=PageState.set_balance_type,  # Estado para cambiar el balance mostrado
            value=PageState.balance_type,
        ),

        # Tarjeta con el gráfico dinámico
        rx.card(
            rx.cond(
                PageState.balance_type == "diario",
                balances(PageState.data_balances),
                rx.cond(
                    PageState.balance_type == "mensual",
                    balances(PageState.data_balances_mensuales),
                    balances(PageState.data_balances_anuales)
                )
            ),
            width="100%",
        ),
    )
