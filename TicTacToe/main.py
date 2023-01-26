SIZE = 3
grid = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
current_move, next_move = ("X", "Крестик"), ("0", "Нолик")
move_number = 1
result_text = ""


def check_game_state():  # Проверяем текущее состояние на поле боя
    grid_ = grid
    transformed_mtrx = zip(*grid_)  # Транспонируем матрицу
    row_sets = list(map(set, grid_))  # Преобразовываем каждую строку (одномерный список) грида во множество
    col_sets = list(map(set, transformed_mtrx))  # аналогично со столбцами (для получения уникальных значений)
    first_diagonal = [set([grid_[i][i] for i in range(SIZE)])]  # сохраняем уник. значения по диагонали
    second_diagonal = [set([grid_[SIZE - 1 - i][i] for i in range(SIZE)])]  # аналогично по другой

    all_lines_collection = [row_sets, col_sets, first_diagonal, second_diagonal]  # проверяем, не является ли
    result = [[max(inner_set) for inner_set in outer_List if inner_set in ({"X"}, {"0"})]  # одно из множеств
              for outer_List in all_lines_collection  # множеством, состоящим лишь из одного элемента
              ]  # это м.б. в том случае, когда все элементы строки/столбца/диагонали равны. Т.е. победа
    result = [rec for rec in result if rec != []]
    if not result:
        result = ""
    else:
        result = str(*result[0])
    return result


def print_grid():  # распечатываем поле боя
    def generate_line(grid_):
        result = " "
        for rec in grid_:
            result = result + rec + " | "
        x = result[:len(result) - 2]
        print(x)
        print("------------")

    list(map(generate_line, grid))


def ask_next_move():  # Реакция на очередной ход игрока
    current_move_, next_move_ = current_move, next_move  # берем значения очереди хода из глобальных переменных
    answer = input(f"Ходит {current_move_[1]}: ").replace(" ", "")
    if not answer.isdigit() or len(answer) > 2 or \
            not {int(answer[0]), int(answer[1])}.issubset(set(range(SIZE))):  # проверки валидности ввода из консоли
        print("Указываемые координаты должны состоять только из цифр и соответствовать размеру поля")
        return current_move_, next_move_, False  # В случае неудачи не меняем очередь хода
    i, j = int(answer[0]), int(answer[1])
    cell = grid[i][j]
    if cell not in ("X", "0"):  # проверяем, что ход не осуществляется в занятую ячейку
        grid[i][j] = current_move_[0]
        return next_move_, current_move_, True  # В случае удачи меняем очередь хода
    else:
        print("Ячейка уже занята")
        return current_move_, next_move_, False  # В случае неудачи не меняем очередь хода

print("Добро пожаловать на игру крестики-нолики!")
print("Для указания координат потребуется ввести две цифры (можно через пробел, можно подряд)")
print("нумерация координат начинается с нуля. т.е. например, центральная ячейка имеет координаты 1 1")

print_grid()

while True and move_number <= pow(SIZE, 2):
    current_move, next_move, success_flag = ask_next_move()  # , current_move
    if move_number > SIZE + 1:
        state = check_game_state()
        if state in ("X", "0"):
            print_grid()
            result_text = f"Победил {next_move[1]}"
            print(result_text)
            break
    print_grid()
    move_number += success_flag and 1

if result_text == "":
    print("Ничья ¯\_(ツ)_/¯ ")