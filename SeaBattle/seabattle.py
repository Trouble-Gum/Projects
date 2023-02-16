from ships import *
from time import sleep

dot_state_chr = {  # словарь символов для отображения
    DOT_IS_EMPTY: ' ',
    DOT_IS_SHIP: '■',
    DOT_IS_FORBIDDEN_FOR_SHIP: ' ',
    DOT_IS_MISS: 'O',
    DOT_IS_HIT: 'X',
    DOT_IS_SKIPPED: '.'
}


def symbol(state, hid=False):  # функция возвращает символ по состоянию точки
    return ' ' if hid and state == DOT_IS_SHIP else dot_state_chr[state]


def colour(str_, clr):
    return str_  # пока что решил не использовать цвета (могут быть проблемы в разных ОС и оболочках)
    # if clr == 'red':
    #     clr = f"\033[31m"
    # if clr == 'green':
    #     clr = f"\033[32m"
    # res = ''
    # for i in range(len(str_)):
    #     if str_[i] == 'X':
    #         res = res + clr + 'X'
    #     else:
    #         res = res + f"\033[38m" + str_[i]
    # return res


def refresh_grid(grid: list, game_board: GameBoard):  # наполняем графикой поле по данным о сост. точек
    grid.clear()
    for i in range(BOARD_SIZE):
        grid += [[]]
        for j in range(BOARD_SIZE):
            gb_ = game_board
            dot = gb_.get_dot(j, i) if i and j else None
            grid[i] += [str(j) if i == 0 else str(i) if j == 0 else symbol(dot.state, bool(gb_.hid))]


class Player:  # класс игрока
    def __init__(self):
        self.own_board = None
        self.enemy_board = None
        self.last_move = []
        self._winner = False
        self.enemy = None

    def ask(self) -> tuple:  # запрос хода
        """запрашивает ход"""

    @property
    def winner(self):  # признак победителя
        eb = self.enemy_board
        return eb.is_annihilated()

    def move(self, proc):  # ход
        res = None
        if not (self.winner or self.enemy.winner):
            ans = self.ask()
            res = self.enemy_board.shot(ans[0], ans[1])
        else:
            proc(True)
        return res


class AI(Player):  # компьютер
    _dif_level: int = 1

    # Уровни сложности:
    # 1 - компьютер стреляет рандомно по пустым клеткам
    # 2 - компьютер ищет пустые клетки рядом с подбитыми палубами
    # 3 - компьютер - телепат. Попав по палубе, он всегда угадывает тип корабля (гориз/верт)

    @property  # Уровень сложности
    def dif_level(self):
        return self._dif_level

    @dif_level.setter  # сеттер для уровня сложности
    def dif_level(self, val):
        self._dif_level = val

    @staticmethod  # проверка выбора клетки для уровня сложности 2
    def _check_dot2(dot):
        res = dot.dot_left
        if res and res.state not in (DOT_IS_MISS, DOT_IS_SKIPPED, DOT_IS_HIT):
            return res
        res = dot.dot_right
        if res and res.state not in (DOT_IS_MISS, DOT_IS_SKIPPED, DOT_IS_HIT):
            return res
        res = dot.dot_above
        if res and res.state not in (DOT_IS_MISS, DOT_IS_SKIPPED, DOT_IS_HIT):
            return res
        res = dot.dot_below
        if res and res.state not in (DOT_IS_MISS, DOT_IS_SKIPPED, DOT_IS_HIT):
            return res
        return None

    @staticmethod  # проверка выбора клетки для уровня сложности 3
    def _check_dot3(ship, dot):
        res = dot.dot_left if ship.direction == SHIP_IS_HORIZONTAL else dot.dot_above
        res = res if res and res.state not in (DOT_IS_MISS, DOT_IS_SKIPPED, DOT_IS_HIT) else None
        if not res:
            res = dot.dot_right if ship.direction == SHIP_IS_HORIZONTAL else dot.dot_below
            res = res if res and res.state not in (DOT_IS_MISS, DOT_IS_SKIPPED, DOT_IS_HIT) else None
        return res

    def _choice_dot2(self):  # выбор клетки для уровня сложности 2
        brd = self.enemy_board
        lst = [dot for dot in merge(brd.dot_list) if dot and dot.state == DOT_IS_HIT]
        res = to_dot(None)
        for rec in lst:
            res = self._check_dot2(rec)
            if res:
                return res
        return res

    def _choice_dot3(self):  # выбор клетки для уровня сложности 3
        brd = self.enemy_board
        lst = [ship for ship in brd.ship_list if ship.state == SHIP_IS_DAMAGED]
        res = None
        if len(lst) > 0:
            ship = to_ship(choice(lst))
            dot1 = to_dot(brd.get_dot(ship.space['left'], ship.space['top']))
            dot2 = to_dot(brd.get_dot(ship.space['right'], ship.space['bottom']))
            if dot1.state == DOT_IS_HIT:
                res = self._check_dot3(ship, dot1)
            if not res and dot2.state == DOT_IS_HIT:
                res = self._check_dot3(ship, dot2)
            if not res:
                for dot in ship.dot_list:
                    res = self._check_dot3(ship, dot) if dot.state == DOT_IS_HIT else res
        return res

    def ask(self):
        if self._dif_level == 2:  # поведение компьютера в зависимости ит уровня сложности
            val = self._choice_dot2()
        elif self.dif_level == 3:
            val = self._choice_dot3()
        else:
            val = None

        if val:
            print(f"Ходит компьютер:{val.x} {val.y}")
            return val.x, val.y

        lst = self.enemy_board.empty_dot_list()
        x, y, val = None, None, None
        if len(lst) > 0:
            val = to_dot(choice(lst))
            x, y = val.x, val.y
            print(f"Ходит компьютер:{x} {y}")
        return x, y


class User(Player):  # пользователь (игрок)
    def ask(self):
        answer = input("Ходит пользователь: ").replace(" ", "").replace(",", "")
        sleep(0.1)
        if not answer.isdigit() or len(answer) != 2:
            raise IncorrectCoordinatesError("Некорректно указаны координаты")
        return int(answer[0]), int(answer[1])


class SeaBattle:  # основной класс игры
    _user_board: GameBoard
    _comp_board: GameBoard

    @property
    def dif_level(self):
        return self.ai.dif_level

    @dif_level.setter
    def dif_level(self, val):
        if val not in (1, 2, 3):
            raise ValueError("Допустимые значения для уровня игры: 1, 2, 3")
        self.ai.dif_level = val

    @property
    def user_bord(self):  # поле игрока
        return self._user_board

    @property
    def comp_bord(self):  # поле компьютера
        return self._comp_board

    @staticmethod
    def _create_board():  # расставляем рандомно корабли
        sm = 0
        max_ship_dot_count = sum([rec * val for rec, val in SHIP_VALID_AMOUNT.items()])
        gb = None
        while sm < max_ship_dot_count:
            gb = GameBoard()
            gb.place_ships()
            sm = sum([1 for dot_ in merge(gb.dot_list) if dot_ and dot_.state == DOT_IS_SHIP])
        return gb

    def __init__(self):  # конструктор
        self._user_grid = []
        self._comp_grid = []
        self.user = User()
        self.ai = AI()
        self.ai.enemy = self.user
        self.user.enemy = self.ai

    def print_game_status(self):  # распечатываем поле боя
        def format_line(i_, d_, k_):
            if i_ == 0:
                res = f"Данные пользователя:   "
            elif i_ == 1:
                res = f"Подбитых кораблей: {d_}   "
            elif i_ == 2:
                res = f"Убитых кораблей:{k_}      "
            else:
                res = f"                       "
            return res

        refresh_grid(self._user_grid, self._user_board)
        refresh_grid(self._comp_grid, self._comp_board)

        g1, g2 = self._user_grid, self._comp_grid
        line1, line2 = '', ''
        for i in range(BOARD_SIZE):
            gbs = self._user_board.get_count_by_state
            d = gbs(SHIP_IS_DAMAGED)
            k = gbs(SHIP_IS_DEAD)
            line0 = format_line(i, d, k)
            gbs = self._comp_board.get_count_by_state
            d = gbs(SHIP_IS_DAMAGED)
            k = gbs(SHIP_IS_DEAD)
            line3 = format_line(i, d, k)
            for j in range(BOARD_SIZE):
                line1 += g1[i][j] + ' | '
                line2 += g2[i][j] + ' | '
            print(line0 + colour(line1, 'red') + ' ' + line3 + colour(line2, 'green'))
            line1, line2 = '', ''

    def random_board(self):  # присваиваем объектам ссылки друг на друга

        self.user.own_board = self._create_board()
        self._user_board = self.user.own_board

        self.ai.own_board = self._create_board()
        self._comp_board = self.ai.own_board
        self._comp_board.hid = True

        self.user.enemy_board = self._comp_board
        self.ai.enemy_board = self._user_board

    @staticmethod
    def greet():
        print("Добро пожаловать на игру Морской бой")
        print("координаты можно вводить через пробел(x y), слитно(xy) или через запятую(x,y)")
        print("Будьте внимательны, x - по горизонтали y - по вертикали! (т.е. не как 2d list :)")
        print()

    def game_over(self):  # метод завершения игры
        if self.user.winner:
            game_over = "Победил пользователь"
        elif self.ai.winner:
            game_over = "Победил компьютер"
        else:
            game_over = "Ошибка!!!"

        if game_over:
            self.print_game_status()
            print(game_over)
            exit()
        return

    def loop(self):  # Основной цикл программы
        self.print_game_status()
        move_order = 'User'
        while True:
            if self.user.winner or self.ai.winner:
                self.game_over()

            exception_flag = False
            try:
                if move_order == 'User':
                    ship_state = self.user.move(self.game_over)
                    res = ship_state in (SHIP_IS_DAMAGED, SHIP_IS_DEAD)
                    move_order = 'User' if res else 'AI'
                else:
                    ship_state = self.ai.move(self.game_over)
                    res = ship_state in (SHIP_IS_DAMAGED, SHIP_IS_DEAD)
                    move_order = 'AI' if res else 'User'
            except (RepeatableDotShootingError, ShootOnSkippedWarning, IncorrectCoordinatesError) as e:
                exception_flag = True
                warning = str(SeaBattleException(e).message).count("Выстрел в контурную точку")
                print(e.args[0])
                res = None
                ship_state = None
                if warning > 0:
                    move_order = 'AI' if move_order == 'User' else 'AI'
            except Exception:
                raise

            if self.user.winner or self.ai.winner:
                self.game_over()

            if not exception_flag and not (self.user.winner or self.ai.winner):
                print("Корабль поврежден!\n" if ship_state == SHIP_IS_DAMAGED
                      else "Корабль уничтожен!\n" if ship_state == SHIP_IS_DEAD
                else "Мимо!\n" if res is not None else "\n"
                      )

            sleep(0.1)
            if res is not None and not self.user.winner and not self.ai.winner:
                self.print_game_status()
            sleep(0.1)

    def start(self):  # запуск цикла
        self.random_board()
        self.greet()
        self.loop()
