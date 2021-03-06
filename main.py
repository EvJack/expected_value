import os
import random
import time

import numpy as np
import pandas as pd
import plotly.graph_objs as plotly_go

from configuration import *


def get_starting_balance():
    """[Обработчик ошибок.]

    Raises:
        Exception: [Обрабатывает ошибки типа, и специальную ошибку, проверку на то, что баланс больше нуля.]

    Returns:
        [integer]: [Стартовый баланс введенный пользователем.]
    """

    while True:
        try:
            start_balance = int(input("Введите ваш стартовый баланс: "))
            if start_balance <= 0:
                raise Exception("Баланс должен быть больше нуля. \n")
        except ValueError:
            print("Стартовым балансом может являться только целое число.\n")
        except Exception as ex:
            print(ex)
        else:
            return start_balance


def balance_manipulaion(balance, BET):
    """[Функция вычисления баланса перед ставкой.]

    Args:
        balance ([integer]): [Баланс. Меняется после каждой иттерации.]
        BET ([integer]): [сумма ставки. Считается коэффициентом от стартового баланса.]

    Returns:
        [integer]: [сумма ставки.]
    """

    BET = min(BET, balance)
    balance -= BET

    return balance


def check_result(balance, win, loose, BET, start_value, end_value):
    """[проверка того, на какое поле упал "мяч" и сверка с выигрышными полями.]

    Args:
        balance ([integer]): [Текущий баланс по стратегии.]
        win ([integer]): [счётчик побед.]
        loose ([integer]): [счётчик поражений.]
        BET ([integer]): [текущая ставка.]
        start_value ([integer]): [первое поле рулетки.]
        end_value ([integer]): [последнее поле рулетки.]

    Returns:
        [integer]: [Функция возвращает значение нового баланса и изменение счетчиков побед/поражений.]
    """

    ball = random.randint(start_value, end_value)
    if ball in WIN_FIELDS:
        balance += BET * 2
        win += 1
    else:
        loose += 1

    return balance, win, loose


def print_result(index, strategy, win, loose, black, red, all_fields):
    """[Функция выводит в консоль итоговую информацию по каждой стратегии. Информация выводится сразу после того, как игра по стратегии была завершена.]

    Args:
        index ([integer]): [Номер стратегии.]
        strategy ([string]): [Описание по какой стратегии велась игра.]
        win ([integer]): [счётчик побед.]
        loose ([integer]): [счётчик поражений.]
        black ([integer]): [количество черных полей.]
        red ([integer]): [Количество красных полей.]
        all_fields ([integer]): [Количество всех полей.]
    """

    print(
        "\n" f"Стратегия №{index}, {strategy}",
        f"Шанс на победу(в процентах): {(black/all_fields) * 100}%",
        f"Мат.ожидание по данной стратегии: {((black/all_fields) * 100) - ((red/all_fields) * 100)}%",
        f"Общее число игр: {win + loose}",
        f'Выиграно ставок: {win}, ({win/(win + loose) * 100}%)',
        f'Проиграно ставок: {loose}, ({loose/(win + loose) * 100}%)',
        sep="\n",
        end="\n\n",
    )


def game_strategy_1(balance, BET, balance_strategy_1):
    """[Симуляция игры с отрицательным мат.ожиданием.]

    Args:
        balance ([integer]): [Текущий баланс по стратегии.]
        BET ([integer]): [текущая ставка.]
        balance_strategy_1 ([list]): [список заполненный балансом после каждой иттерации.]

    Returns:
        [list]: [список заполненный балансом по данной симуляции после каждой иттерации.]
    """

    win = 0
    loose = 0

    while balance > 0:
        balance = balance_manipulaion(balance, BET)
        balance, win, loose = check_result(balance, win, loose, BET, 0, 36)
        balance_strategy_1.append(balance)

    print_result(1, "отрицательное мат.ожидание", win, loose, 18, 19, 37)

    return balance_strategy_1


def game_strategy_2(balance, BET, balance_strategy_2):
    """[Симуляция игры с нулевым мат.ожиданием.]

    Args:
        balance ([integer]): [Текущий баланс по стратегии.]
        BET ([integer]): [текущая ставка.]
        balance_strategy_1 ([list]): [список заполненный балансом после каждой иттерации.]

    Returns:
        [list]: [список заполненный балансом по данной симуляции после каждой иттерации.]
    """

    win = 0
    loose = 0

    while (balance > 0) and (win + loose < STOP_POINT):
        balance = balance_manipulaion(balance, BET)
        balance, win, loose = check_result(balance, win, loose, BET, 1, 36)
        balance_strategy_2.append(balance)

    print_result(2, "нулевое мат.ожидание", win, loose, 18, 18, 36)

    return balance_strategy_2


def game_strategy_3(balance, BET, balance_strategy_3):
    """[Симуляция игры с положительным мат.ожиданием.]

    Args:
        balance ([integer]): [Текущий баланс по стратегии.]
        BET ([integer]): [текущая ставка.]
        balance_strategy_1 ([list]): [список заполненный балансом после каждой иттерации.]

    Returns:
        [list]: [список заполненный балансом по данной симуляции после каждой иттерации.]
    """

    win = 0
    loose = 0

    while (balance > 0) and (win + loose < STOP_POINT):
        balance = balance_manipulaion(balance, BET)
        balance, win, loose = check_result(balance, win, loose, BET, 1, 35)
        balance_strategy_3.append(balance)

    print_result(3, "положительное мат.ожидание", win, loose,  18, 17, 35)

    return balance_strategy_3


def count_games(balance_strategy_1, balance_strategy_2, balance_strategy_3):
    """[Функция-счетчик. Считает количество игр в каждой симуляции опираясь на данные из списков с балансами.]

    Args:
        balance_strategy_1 ([list]): [список заполненный балансом после каждой иттерации.]
        balance_strategy_2 ([list]): [список заполненный балансом после каждой иттерации.]
        balance_strategy_3 ([list]): [список заполненный балансом после каждой иттерации.]

    Returns:
        [list]: [список с количеством иттераций в каждой иттерации.]
    """

    count_games_strategy_1 = [i for i in range(1, len(balance_strategy_1) + 1)]
    count_games_strategy_2 = [i for i in range(1, len(balance_strategy_2) + 1)]
    count_games_strategy_3 = [i for i in range(1, len(balance_strategy_3) + 1)]

    return count_games_strategy_1, count_games_strategy_2, count_games_strategy_3


def graph(balance_strategy_1, balance_strategy_2, balance_strategy_3):
    """[эта функция отвечает за отображение графиков. Для отрисовки графиков была использована библиотека Pandas.]

    Args:
        balance_strategy_1 ([list]): [список заполненный балансом после каждой иттерации.]
        balance_strategy_2 ([list]): [список заполненный балансом после каждой иттерации.]
        balance_strategy_3 ([list]): [список заполненный балансом после каждой иттерации.]
    """

    question_graph = input(
        "Хотите ли вы построить графики изменения баланса? [y/n]: ")

    if question_graph == "y":

        count_games_strategy_1, count_games_strategy_2, count_games_strategy_3 = count_games(
            balance_strategy_1, balance_strategy_2, balance_strategy_3)
        figure = plotly_go.Figure()
        figure.add_trace(
            plotly_go.Scatter(x=count_games_strategy_1,
                              y=balance_strategy_1,
                              name="Отрицательное матожидание"))
        figure.add_trace(
            plotly_go.Scatter(x=count_games_strategy_2,
                              y=balance_strategy_2,
                              name="Нулевое матожидание"))
        figure.add_trace(
            plotly_go.Scatter(x=count_games_strategy_3,
                              y=balance_strategy_3,
                              name="Положительное матожидание"))

        figure.update_layout(legend_orientation="h",
                             legend=dict(x=.5, xanchor="center"),
                             title="Изменение баланса с течением времени",
                             xaxis_title="Порядковый номер игры по стратегии",
                             yaxis_title="Баланс",
                             margin=dict(l=0, r=0, t=50, b=100)),
        figure.update_traces(hoverinfo="all",
                             hovertemplate="Игра: %{x}<br>Баланс: %{y}")

        figure.show()


def savedata(balance_strategy_1, balance_strategy_2, balance_strategy_3):
    """[Данная функция отвечает за создание и сохранение данных в таблицу excel.]

    Args:
        balance_strategy_1 ([list]): [список заполненный балансом после каждой иттерации.]
        balance_strategy_2 ([list]): [список заполненный балансом после каждой иттерации.]
        balance_strategy_3 ([list]): [список заполненный балансом после каждой иттерации.]
    """

    question = input(
        "Хотите ли вы сохранить Excel-таблицу с результатами? [y/n]: ")

    if question == "y":

        count_games_strategy_1, count_games_strategy_2, count_games_strategy_3 = count_games(
            balance_strategy_1, balance_strategy_2, balance_strategy_3)

        arr_count_games_strategy_1 = np.array(count_games_strategy_1)
        arr_balance_strategy_1 = np.array(balance_strategy_1)
        arr_count_games_strategy_2 = np.array(count_games_strategy_2)
        arr_balance_strategy_2 = np.array(balance_strategy_2)
        arr_count_games_strategy_3 = np.array(count_games_strategy_3)
        arr_balance_strategy_3 = np.array(balance_strategy_3)

        data = {
            'Номер игры по стратегии 1': arr_count_games_strategy_1,
            'Баланс по стратегии 1': arr_balance_strategy_1,
            'Номер игры по стратегии 2': arr_count_games_strategy_2,
            'Баланс по стратегии 2': arr_balance_strategy_2,
            'Номер игры по стратегии 3': arr_count_games_strategy_3,
            'Баланс по стратегии 3': arr_balance_strategy_3,
        }

        df = pd.DataFrame.from_dict(data, orient="index")
        df = df.transpose()

        if not os.path.exists("result"):
            os.mkdir("result")

        filename_date = time.strftime("%d_%m_%Y-%H.%M.%S")
        df.to_excel(f"result/result({filename_date}).xlsx")
        print("Таблица Excel была сохранена в папку result.")


def main():
    """[Главная функция программы, из нее вызываются другие функции и через эту же функцию передаються некоторые данные для вычислений.]
    """

    balance = get_starting_balance()

    BET = balance * BET_COEFFICIENT

    balance_strategy_1 = [balance]
    balance_strategy_2 = [balance]
    balance_strategy_3 = [balance]

    game_strategy_1(balance, BET, balance_strategy_1)
    game_strategy_2(balance, BET, balance_strategy_2)
    game_strategy_3(balance, BET, balance_strategy_3)
    graph(balance_strategy_1, balance_strategy_2, balance_strategy_3)
    savedata(balance_strategy_1, balance_strategy_2, balance_strategy_3)


if __name__ == "__main__":
    main()

input("Для выхода нажмите Enter ...")
