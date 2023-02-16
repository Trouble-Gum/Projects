from exceptions import *
from random import choice
from constants import *


def merge(lst: list):  # составляет n-мерный список из n+1 мерного
    result = []
    for rec in lst:
        result += rec if type(rec) is list else [rec]
    return result


class Dot:  # Класс точка (палуба корабля)

    def __init__(self, x, y, game_bord):  # инициализация (конструктор)
        self._state = DOT_IS_EMPTY
        self._ship = None
        self.x, self.y = x, y
        self.board = game_bord

    def __eq__(self, other):  # переопределение оператора сравнения
        if not isinstance(other, Dot):
            raise TypeError("Один из операндов сравнения не является точкой")

        result = all([self.x == other.x, self.y == other.y, self.board == other.board])
        return result

    @property
    def dot_left(self):  # левая соседняя точка
        x = max(self.x - 1, 0)
        return self.board.get_dot(x, self.y) if x > 0 else None

    @property
    def dot_right(self):  # правая соседняя точка
        x = min(self.x + 1, GAME_BOARD_SIZE)
        return self.board.get_dot(x, self.y) if x > self.x else None

    @property
    def dot_above(self):  # точка сверху
        y = max(self.y - 1, 0)
        return self.board.get_dot(self.x, y) if y > 0 else None

    @property
    def dot_below(self):  # точка снизу
        y = min(self.y + 1, GAME_BOARD_SIZE)
        return self.board.get_dot(self.x, y) if y > self.y else None

    @property
    def state(self):  # состояние точки
        return self._state

    @property
    def ship(self):  # ссылка на объект-корабль, к которому точка принадлежит
        return self._ship

    def shot(self):  # событие выстрела в данную точку
        if self._state in (DOT_IS_HIT, DOT_IS_MISS):
            raise RepeatableDotShootingError("Вы уже стреляли по данной палубе")
        elif self._state in (DOT_IS_EMPTY, DOT_IS_FORBIDDEN_FOR_SHIP):
            self._state = DOT_IS_MISS
        elif self._state == DOT_IS_SHIP:
            self._state = DOT_IS_HIT
        elif self._state == DOT_IS_SKIPPED:
            self._state = DOT_IS_MISS
            raise ShootOnSkippedWarning("Выстрел в контурную точку. Будьте внимательнее!")
        if self.ship:
            self.ship.shot()

        return self._state

    def mark_as_skipped(self):  # помечаем точку как контурную
        if self._state == DOT_IS_SKIPPED:
            return
        elif self._state in (DOT_IS_EMPTY, DOT_IS_FORBIDDEN_FOR_SHIP):
            self._state = DOT_IS_SKIPPED
        else:
            ValueError("Отметить координату как не предусмотренную для выстрела  можно"
                       "только для пустых координат")

    def assign_ship(self, ship):  # назначаем корабль (управляется в объекте класса поля)
        self._ship = ship
        self._state = DOT_IS_SHIP

    def forbid_ship_placement(self, contour=False):  # помечаем как непригодную для расположения корабля
        if self._state == DOT_IS_FORBIDDEN_FOR_SHIP:
            self._state = DOT_IS_SKIPPED if contour else DOT_IS_FORBIDDEN_FOR_SHIP
        elif self._state == DOT_IS_EMPTY:
            self._state = DOT_IS_FORBIDDEN_FOR_SHIP
        elif self._state in (DOT_IS_MISS, DOT_IS_HIT, DOT_IS_SKIPPED):
            return
        else:
            raise ValueError(f"Координаты уже отмечены другим состоянием: {self._state}")


def to_dot(val) -> Dot:  # явное преобразование
    return val  # (чисто для удобства, чтоб автоматом поля и методы подсвечивались)


class Ship:  # класс корабля

    @staticmethod
    def check_ship_size(size):  # проверить размер корабля
        if size not in range(1, MAX_SHIP_SIZE + 1):
            raise ShipInvalidSizeError("Указанный размер корабля вне допустимого диапазона")

    def __init__(self, size: int, start_dot: Dot, game_bord, direction=SHIP_IS_VERTICAL):  # конструктор
        self._size = size
        self._state = SHIP_IS_WHOLE
        self._space = {}
        self._direction = direction
        self._damages = 0

        self.check_ship_size(size)
        self.master_board = game_bord
        self._dot_list = []
        if direction not in (SHIP_IS_VERTICAL, SHIP_IS_HORIZONTAL):
            raise ValueError("указано не правильное направление корабля")

        if start_dot.state != DOT_IS_EMPTY:
            raise ValueError("Координата уже занята")

        dot_ = start_dot
        lst = [dot_]
        self._space['left'], self._space['top'] = dot_.x, dot_.y

        while len(lst) < size:
            dot_ = dot_.dot_below if direction == SHIP_IS_VERTICAL else dot_.dot_right
            if dot_:
                lst.append(dot_)
            else:
                raise ShipOutOfBoardError("Длина корабля выходит за пределы поля")

        self._space['right'], self._space['bottom'] = dot_.x, dot_.y

        if set([dot_.state for dot_ in lst]) != {DOT_IS_EMPTY}:
            raise DotIsNotEmptyError("Точка не является пустой")

        [dot_.assign_ship(self) for dot_ in lst]
        self._dot_list = lst

    @property
    def dot_list(self):
        return self._dot_list

    @property
    def size(self):  # размер
        return self._size

    @property
    def direction(self):  # тип расположения
        return self._direction

    @property
    def state(self):  # состояние
        return self._state

    @property
    def damages(self):  # количество поврежденных палуб
        return self._damages

    @property
    def lives(self):  # количество оставшихся жизней
        return self.size - self._damages

    @property
    def space(self):  # занимаемое место
        return self._space

    def shot(self):  # событие выстрела
        self._damages += 1
        self._state = SHIP_IS_DEAD if self._damages == self._size else SHIP_IS_DAMAGED


def to_ship(val) -> Ship:  # для удобства явного преобразования
    return val


class GameBoard:  # класс игрового поля
    _hid: bool

    @staticmethod
    def check_neighboring_cells(x1, y1, x2, y2, chk_diagonal=False):  # проверка соседства ячеек
        if chk_diagonal and abs(x1 - x2) != 1 or abs(y1 - y2) != 1:
            raise ValueError("Две из указанных координат не являются соседними по диагонали")
        elif not chk_diagonal and x1 != x2 and y1 != y2:
            raise ValueError("Две из указанных координат не являются соседними")

    @property
    def hid(self):  # признак скрытия кораблей (компьютера)
        return self._hid

    @hid.setter
    def hid(self, val):  # сеттер
        self._hid = val

    @property
    def dot_list(self):  # список всех точек поля
        return self._dot_list

    @property
    def ship_list(self):  # список кораблей поля
        return self._ship_list

    def __init__(self):  # конструктор
        self._ship_dict = {}
        self._dot_list = [[]]
        self._ship_list = []
        self._hid = False

        for i in range_:
            self._dot_list.append([to_dot(None)])
            for j in range_:
                self._dot_list[i].append(Dot(j, i, self))

    def add_ship(self, ship: Ship):  # добавить корабль на поле
        self._ship_list.append(ship)
        sz = int(ship.size)
        if sz in self._ship_dict.keys():
            self._ship_dict[sz] += [ship]
        else:
            self._ship_dict[sz] = [ship]

    def get_ship_count(self, size):  # получить количество кораблей заданного размера
        try:
            return len(self._ship_dict[size])
        except KeyError:
            return 0

    def get_count_by_state(self, state):  # получить кол-во кораблей по указанному состоянию
        result = sum([1 for ship in self._ship_list if ship.state == state])
        return result

    def get_dot(self, x, y) -> Dot:  # получить точку по заданным координатам
        if all([x in range_, y in range_]):
            return self._dot_list[y][x]
        else:
            raise IncorrectCoordinatesError(f"Переданные координаты точки {x}:{y} выходят за пределы поля ")

    def get_neighbouring_space(self, **kwargs) -> list:  # получить пространство окружения (kwargs - x, y ship)
        x, y = None, None
        ship: Ship = to_ship(None)

        for elem, value in kwargs.items():
            x = value if elem == 'x' else x
            y = value if elem == 'y' else y
            ship = value if elem == 'ship' else ship

        if ship:
            left, right, top, bottom = ship.space['left'], ship.space['right'], \
                ship.space['top'], ship.space['bottom']
            top, bottom = max(top - 1, 0), min(bottom + 2, BOARD_SIZE)
            left, right = max(left - 1, 0), min(right + 2, BOARD_SIZE)
        elif x and y:
            top, bottom = max(y - 1, 0), min(y + 2, BOARD_SIZE)
            left, right = max(x - 1, 0), min(x + 2, BOARD_SIZE)
        else:
            raise ValueError("Координаты соседних точек могут быть вычислены только для точки или корабля")

        slice_ = self._dot_list[top:bottom]
        slice_ = [rec[left:right] for rec in slice_]
        return slice_

    def wrap_ship(self, ship: Ship, contour=False):  # запретить размещение в соприкосновении с кораблем
        space = self.get_neighbouring_space(ship=ship)

        [dot_.forbid_ship_placement(contour) for dot_ in merge(space)
         if dot_ and dot_.state not in (DOT_IS_SHIP, DOT_IS_HIT)
         ]

    def contour(self, ship):  # обвести уничтоженный корабль контуром
        self.wrap_ship(ship, True)

    def get_free_space(self) -> list:  # получить кол-во пустых точек
        return [dot_ for dot_ in merge(self._dot_list) if dot_ and dot_.state == DOT_IS_EMPTY]

    def check_valid_placement(self, size):  # проверка валидности размещения корабля
        if self.get_ship_count(size) + 1 > SHIP_VALID_AMOUNT[size]:
            raise ShipCountExceedError(f"Размещено максимальное число кораблей размером: {size}")

        if self.get_ship_count(size) + 1 > sum([1 for dot_ in merge(self._dot_list)
                                                if dot_ and dot_.state == DOT_IS_EMPTY
                                                ]):
            raise NotEnoughSpaceError(f"Не хватает места для размещения корабля: {size}")

    def place_ships(self):  # разместить корабли (рандомно)
        for size in SHIP_SIZES:
            for count in range(SHIP_VALID_AMOUNT[size]):
                success = False
                while not success:
                    space = self.get_free_space()
                    if space:
                        dt = choice(space)
                    else:
                        return
                    direction = choice([SHIP_IS_HORIZONTAL, SHIP_IS_VERTICAL])
                    try:
                        self.check_valid_placement(size)
                        sh = Ship(size, dt, self, direction)
                        self.wrap_ship(sh)
                        self.add_ship(sh)
                    except (ShipOutOfBoardError, DotIsNotEmptyError):
                        success = False
                    except (ShipInvalidSizeError, ValueError):
                        raise
                    except (ShipCountExceedError, NotEnoughSpaceError):
                        success = True
                    else:
                        success = True

    def is_annihilated(self):  # признак уничтожения всех кораблей на поле
        return self.get_count_by_state(SHIP_IS_DEAD) == len(self._ship_list)

    def empty_dot_list(self):  # список оставшихся (без выстрела) клеток
        return [dot for dot in merge(self._dot_list) if dot and
                dot.state not in (DOT_IS_HIT, DOT_IS_MISS, DOT_IS_SKIPPED)
                ]

    def shot(self, x, y):  # событие выстрела по полю
        dot = self.get_dot(x, y)
        ship = dot.ship
        prev_ship_state = ship.state if ship else None
        dot.shot()
        if ship and ship.state != prev_ship_state:
            if ship.state == SHIP_IS_DEAD:
                self.contour(ship)
        return ship.state if ship else None
