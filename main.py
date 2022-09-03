import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Такая конструкция плохо читается.
        # Нужно либо написать в одну строку (если не нарушается ограничение на длину),
        # либо расположить на отдельный строках первое значение, if с условием и else со вторым значением,
        # либо использовать обычный условный оператор вместо тернарной операции.
        # Но не разрывать конструкцию if-условие без особой необходимости.
        self.date = (
            # Можно использовать date.today()
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Для повышения эффективности лучше получить текущую дату перед началом цикла.
        for Record in self.records:
            # Для получения текущей даты можно использовать date.today()
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        # Для получения текущей даты можно использовать date.today()
        today = dt.datetime.now().date()
        # Для повышения эффективности лучше вычислить дату начала недели перед началом цикла.
        for record in self.records:
            # Лучше напрямую сравнивать даты, чем вычислять дни, можно использовать двойное сравнение week_begin <= record.date <= today, так нагляднее.
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий к функции должен описывать, что делает эта функция.
    # В данном случае, функция не получает, а возвращает информацию об остатке калорий.
    # Комментарий к функции лучше оформить в виде docstring
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # else после return не нужен
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    # float можно задать литералом, например, 60.0
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Можно завести словарь, где ключ -- обозначение валюты, значение -- тьюпл из курса и строки с обозначением валюты.
        # Это позволит легко добавить новую валюту.
        # Это необязательно для данного задания, но может пригодиться в будущем.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        # Можно предусмотреть генерацию исключения при получении неизвестной валюты.
        # Или, если получена неизвестная валюта, выводить в валюте по умолчанию (в рублях).
        # Это необязательно для данного задания, просто совет по улучшению.
        if cash_remained > 0:
            return (
                # Не нужно использовать вызов функции в f-строке
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # После return elif не нужен, достаточно if
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # После return elif не нужен, if тоже, все другие варианты уже исключены
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Не нужно переопределять метод, если он не добавляет никакой функциональности.
    # Достаточно наличия метода в базовом классе.
    def get_week_stats(self):
        super().get_week_stats()
