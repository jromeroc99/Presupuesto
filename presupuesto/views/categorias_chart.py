import reflex as rx
from presupuesto.states.state import PageState

def pie_double():
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=PageState.data_categorias,
            data_key="Ingresos",
            name_key="Categoria",
            stroke="green",
            fill=rx.color("green",4),
            inner_radius="60%",
            padding_angle=5,
        ),
        rx.recharts.pie(
            data=PageState.data_categorias,
            data_key="Gastos",
            name_key="Categoria",
            stroke="red",
            fill=rx.color("red",4),
            outer_radius="50%",
           
        ),
        rx.recharts.graphing_tooltip(),
        width="100%",
        height=300,
    )
