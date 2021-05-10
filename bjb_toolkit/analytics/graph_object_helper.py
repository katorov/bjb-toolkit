from io import BytesIO

from plotly.graph_objs import Figure


def get_axis_parameters(count_days=None, tickformat=None, dtick=None, title='Дата') -> dict:
    """Получить параметры координатной оси графика"""
    is_special_date_format = bool(count_days and count_days <= 10)
    axis_params = {
        'tickformat': tickformat if not is_special_date_format else "%d %b",
        'dtick': dtick if not is_special_date_format else "D1",
        'title': title
    }
    return axis_params


def set_fig_layout(fig, title_text=None, xaxis=None, yaxis=None, width=1200) -> None:
    """Установить параметры отображения графика"""
    fig.update_layout(
        width=width,
        title_text=title_text,
        titlefont={'color': 'darkblue', 'size': 25},
        margin={'t': 50, 'l': 0},
        xaxis=xaxis,
        yaxis=yaxis,
    )


def get_buffer_image(fig: Figure) -> BytesIO:
    """Получить изображение фигуры plotly в виде in-memory bytes buffer"""
    buffer = BytesIO(initial_bytes=fig.to_image())
    buffer.seek(0)
    return buffer
