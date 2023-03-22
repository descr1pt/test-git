field = [[' ']*3 for i in range(3)]


def greet():
    print()
    print(' Добро пожаловать в игру ')
    print(' Крестики Нолики ')
    print(' Правила игры: ')
    print(' Введите координаты куда хотите поставить X или O ')
    print(' Координаты вводятся по типу X и Y')
    print(' Где X - строка ')
    print(' А Y - столбик ')
    print(' GLHF ')


def show():
    print(f'  0 1 2')
    for i in range(3):
        row_info = ' '.join(field[i])
        print(f'{i} {row_info}')


def show2():
    print()
    print(f'  | 0 | 1 | 2 |')
    print('  -------------')
    for i, row in enumerate(field):
        row_str = f"{i} | {' | '.join(row)} | "
        print(row_str)
        print('  -------------')


def ask2():
    while True:
        court = input('            Ваш ход: ').split()

        if len(court) != 2:
            print(' Введите 2 координаты! ')
            continue

        x, y = court

        if not (x.isdigit()) or not (y.isdigit()):
            print(' Введите цифры ')
            continue

        x, y = int(x), int(y)

        if 0 > x or x > 2 or 0 > y or y > 2:
            print(' Вне диапазона координат! ')
            continue

        if field[x][y] != ' ':
            print(' Клетка занята!')
            continue

        return x, y


def check_win():
    win_cord = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2))]
    for cord in win_cord:
        a = cord[0]
        b = cord[1]
        c = cord[2]

        if field[a[0]][a[1]] == field[b[0]][b[1]] == field[c[0]][c[1]] != ' ':
            print(f' Выиграл {field[a[0]][a[1]]}! ')
            return True
    return False


greet()
num = 0
while True:
    num += 1

    show2()

    if num % 2 == 1:
        print(' Ходит крестик ')
    else:
        print(' Ходит нолик ')

    x, y = ask2()

    if num % 2 == 1:
        field[x][y] = 'X'
    else:
        field[x][y] = 'O'

    if check_win():
        break

    if num == 9:
        print(' Ничья ')
        break
