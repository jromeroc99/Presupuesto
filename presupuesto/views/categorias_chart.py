import reflex as rx
from presupuesto.states.state import PageState

def bar_double():
    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="Ingresos",
            stroke=rx.color("green", 9),
            fill=rx.color("green", 8),
        ),
        rx.recharts.bar(
            data_key="Gastos",
            stroke=rx.color("red", 9),
            fill=rx.color("red", 8),
        ),
        rx.recharts.x_axis(data_key="Categoria"),
        rx.recharts.y_axis(
            label={
                "value": "Euros",
                "angle": -90,
                "position": "left",
            },
        ),
        rx.recharts.graphing_tooltip(),
        data=PageState.data_categorias,
        width="100%",
        height=250,
    )