import datetime

from dateutil import parser


class DateTimeParams(parser.parserinfo):
    """Мета-данные русской локализации для парсера даты и времени"""
    HMS = [('ч', 'час', 'часов'), ('м', 'минута', 'минут'), ('с', 'секунда', 'секунд')]
    MONTHS = [('Янв', 'Января'), ('Фев', 'Февраля'), ('Мар', 'Марта'), ('Апр', 'Апреля'),
              ('Май', 'Мая'), ('Июн', 'Июня'), ('Июл', 'Июля'), ('Авг', 'Августа'),
              ('Сен', 'Сентября'), ('Окт', 'Октября'), ('Ноя', 'Ноября'),
              ('Дек', 'Декабря')]
    WEEKDAYS = [('Пн', 'Пнд', 'Понедельник'), ('Вт', 'Втр', 'Вторник'),
                ('Ср', 'Среду', 'Среда'), ('Чт', 'Чет', 'Четверг'),
                ('Пт', 'Пятницу', 'Пятница'), ('Сб', 'Субботу', 'Суббота', 'Субота', 'Суботу'),
                ('Вс', 'Вос', 'Воскресенье', 'Воскресение')]
    JUMP = [' ', '.', ',', ';', '-', '/', "'", 'at', 'on', 'and', 'ad', 'm', 't', 'of', 'st', 'nd',
            'rd', 'th', 'в', 'во']
    AMPM = [('утра', 'утро'), ('вечера', 'дня')]


def parse_datetime(text: str):
    """Спарсить дату/время из строки текста"""
    text = text.lower().strip()

    if text == 'сейчас':
        return datetime.datetime.now()

    today = datetime.date.today()
    day_delta_func = datetime.timedelta
    replacement_text = {
        'сегодня': today,
        'вчера': today - day_delta_func(1),
        'позавчера': today - day_delta_func(2),
        'завтра': today + day_delta_func(1),
        'послезавтра': today + day_delta_func(2),
    }

    for alias in replacement_text:
        text = text.replace(alias, replacement_text[alias].strftime('%d/%m/%Y'))

    params = DateTimeParams()
    try:
        dt = parser.parse(text, parserinfo=params, dayfirst=True)
    except ValueError or OverflowError:
        return None

    return dt


def parse_json_dt(json: str):
    """Спарсить дату/время из json строки"""
    return parser.parse(json)


def hh_mm_printer(minutes: int) -> str:
    """Получить форматированный вывод времени в формате '%Hч %Mмин'"""
    hh = minutes // 60
    mm = minutes % 60

    output = ''
    if hh == 0:
        output += f'{mm}мин'
    elif mm == 0:
        output += f'{hh}ч'
    else:
        output += f'{hh}ч {mm}мин'

    return output
