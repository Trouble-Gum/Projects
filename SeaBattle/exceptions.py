class SeaBattleException(Exception):  # Родительский класс используемых исключений
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'SeaBattleException, {self.message}'
        else:
            return 'SeaBattleException with no message'


class ShipCountExceedError(SeaBattleException):  # Ошибка при попытке разместить на поле лишний корабль
    pass


class ShipOutOfBoardError(SeaBattleException):  # Ошибка при попытке разместить (рандомно) корабль
    pass  # выходящий за границы поля


class DotIsNotEmptyError(SeaBattleException):  # Точка занята (при попытке разместить корабль)
    pass


class ShipInvalidSizeError(SeaBattleException):  # Недопустимая дляна корабля
    pass


class NotEnoughSpaceError(SeaBattleException):  # Недостаточно места (проверка перед размещением)
    pass


class RepeatableDotShootingError(SeaBattleException):  # повторный вестрел по палубе (точке)
    pass


class IncorrectCoordinatesError(SeaBattleException):  # попытка выстрелить за пределы поля
    pass


class ShootOnSkippedWarning(SeaBattleException):  # предупреждение быть внимательнее для пользователя
    pass  # при выстреле в контур, при этом реализован переход хода
