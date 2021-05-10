import plotly.graph_objects as go

from ..analytics.graph_object_helper import get_axis_parameters, set_fig_layout
from ..datetime import utc_to_local, hh_mm_printer

MILK, WATER, NUTRITION = 'м', 'в', 'п'
FOOD_TYPE_CHOICES = {
    MILK: 'Молоко',
    WATER: 'Вода',
    NUTRITION: 'Пища',
}


def get_food_analytics(records, timezone: str, period_name='период') -> tuple:
    """Получить аналитический график и его описание по записям журнала питания"""
    event_category = 'Питание'
    days = {utc_to_local(r.dt, timezone).date(): 0 for r in records}
    milk_days = {utc_to_local(r.dt, timezone).date(): 0 for r in records}
    water_days = {utc_to_local(r.dt, timezone).date(): 0 for r in records}
    another_food_days = {utc_to_local(r.dt, timezone).date(): 0 for r in records}
    counter = dict(milk=[0, 0, 0], water=[0, 0, 0], another_food=[0, 0, 0])

    for r in records:
        day = utc_to_local(r.dt, timezone).date()
        category = r.category
        days[day] += r.quantity

        if category == MILK:
            milk_days[day] += r.quantity
            counter['milk'][0] += 1
            counter['milk'][1] += r.quantity
        elif category == WATER:
            water_days[day] += r.quantity
            counter['water'][0] += 1
            counter['water'][1] += r.quantity
        else:
            another_food_days[day] += r.quantity
            counter['another_food'][0] += 1
            counter['another_food'][1] += r.quantity

    for key in counter:
        if counter[key][0] != 0:
            counter[key][2] = round(counter[key][1] / counter[key][0])
        else:
            counter[key][2] = 0

    x0, y0 = list(days.keys()), list(days.values())
    x1, y1 = list(milk_days.keys()), list(milk_days.values())
    x2, y2 = list(water_days.keys()), list(water_days.values())
    x3, y3 = list(another_food_days.keys()), list(another_food_days.values())

    title = f'{event_category} [Аналитика за {period_name}]'
    caption = f'📊 {title}\n\n'
    caption += f'<b>Всего за период:</b> {len(records)} раз\n\n'
    caption += "<b>{} 🍼\n</b>{} раз \nвсего {} мл \nв среднем за день {} мл\n\n".format(
        FOOD_TYPE_CHOICES[MILK],
        counter['milk'][0],
        counter['milk'][1],
        counter['milk'][2])
    caption += "<b>{} 🚰\n</b>{} раз \nвсего {} мл \nв среднем за день {} мл\n\n".format(
        FOOD_TYPE_CHOICES[WATER],
        counter['water'][0],
        counter['water'][1],
        counter['water'][2])
    caption += "<b>{} 🍽\n</b>{} раз \nвсего {} мл \nв среднем за день {} мл\n\n".format(
        FOOD_TYPE_CHOICES[NUTRITION],
        counter['another_food'][0],
        counter['another_food'][1],
        counter['another_food'][2])

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x1, y=y1, name=FOOD_TYPE_CHOICES[MILK], text=y1, textposition='auto'))
    fig.add_trace(go.Bar(x=x2, y=y2, name=FOOD_TYPE_CHOICES[WATER], text=y2, textposition='auto'))
    fig.add_trace(go.Bar(x=x3, y=y3, name=FOOD_TYPE_CHOICES[NUTRITION], text=y3,
                         textposition='auto'))
    fig.add_trace(go.Scatter(x=x0, y=y0, name='ВСЕГО', mode='lines+markers'))

    xaxis = get_axis_parameters(count_days=len(days))
    yaxis = get_axis_parameters(title='Количество, грамм')
    set_fig_layout(fig, title_text=title, xaxis=xaxis, yaxis=yaxis)
    return fig, caption


def get_gymnastics_analytics(records, timezone: str, period_name='период') -> tuple:
    """Получить аналитический график и его описание по записям журнала гимнастики"""
    event_category = 'Гимнастика'
    days = {utc_to_local(r.dt, timezone).date(): 0 for r in records}
    for r in records:
        day = utc_to_local(r.dt, timezone).date()
        days[day] += r.duration

    x = list(days.keys())
    y = list(days.values())

    title = f'{event_category} [Аналитика за {period_name}]'
    caption = f'📊 {title}\n\n'
    caption += f'<b>Всего за период:</b> {len(records)} раз\n'
    caption += '<b>Среднее значение за день:</b>'
    caption += f'{hh_mm_printer(round(sum(days.values()) / len(records)))}\n'

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y))

    xaxis = get_axis_parameters(count_days=len(days))
    yaxis = get_axis_parameters(title='Продолжительность, мин')
    set_fig_layout(fig, title_text=title, xaxis=xaxis, yaxis=yaxis)
    return fig, caption


def get_sleep_analytics(records, timezone: str, period_name='период') -> tuple:
    """Получить аналитический график и его описание по записям журнала сна"""
    event_category = 'Сон'
    days = {utc_to_local(r.dt, timezone).date(): 0 for r in records}
    for r in records:
        day = utc_to_local(r.dt, timezone).date()
        days[day] += r.duration

    x = list(days.keys())
    y = list(days.values())

    title = f'{event_category} [Аналитика за {period_name}]'
    caption = f'📊 {title}\n\n'
    caption += f'<b>Всего за период:</b> {len(records)} раз\n'
    caption += '<b>Среднее значение за день:</b>'
    caption += f'{hh_mm_printer(round(sum(days.values()) / len(records)))}\n'

    # Преобразовать минуты в часы
    y = [round(minutes_count / 60, 1) for minutes_count in y]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y))

    xaxis = get_axis_parameters(count_days=len(days))
    yaxis = get_axis_parameters(title='Продолжительность, час')
    set_fig_layout(fig, title_text=title, xaxis=xaxis, yaxis=yaxis)
    return fig, caption


def get_walk_analytics(records, timezone: str, period_name='период') -> tuple:
    """Получить аналитический график и его описание по записям журнала прогулок"""
    event_category = 'Прогулки'
    days = {utc_to_local(r.dt, timezone).date(): 0 for r in records}
    for r in records:
        day = utc_to_local(r.dt, timezone).date()
        days[day] += r.duration

    x = list(days.keys())
    y = list(days.values())

    title = f'{event_category} [Аналитика за {period_name}]'
    caption = f'📊 {title}\n\n'
    caption += f'<b>Всего за период:</b> {len(records)} раз\n'
    caption += '<b>Среднее значение за день:</b>'
    caption += f'{hh_mm_printer(round(sum(days.values()) / len(records)))}\n'

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y))

    xaxis = get_axis_parameters(count_days=len(days))
    yaxis = get_axis_parameters(title='Продолжительность, мин')
    set_fig_layout(fig, title_text=title, xaxis=xaxis, yaxis=yaxis)
    return fig, caption


def get_toilet_analytics(records, timezone: str, period_name='период') -> tuple:
    """Получить аналитический график и его описание по записям журнала туалета"""
    event_category = 'Туалет'
    days = {utc_to_local(r.dt, timezone).date(): 0 for r in records}
    for r in records:
        day = utc_to_local(r.dt, timezone).date()
        toilet_quantity = r.category
        days[day] += toilet_quantity

    x = list(days.keys())
    y = list(days.values())

    title = f'{event_category} [Аналитика за {period_name}]'
    caption = f'📊 {title}\n\n'
    caption += f'<b>Всего за период:</b> {len(records)} раз\n'
    caption += f'<b>Среднее значение за день:</b> {round(sum(days.values()) / len(records), 2)}\n'

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y))

    xaxis = get_axis_parameters(count_days=len(days))
    yaxis = get_axis_parameters(title='Количество, баллы')
    set_fig_layout(fig, title_text=title, xaxis=xaxis, yaxis=yaxis)
    return fig, caption
