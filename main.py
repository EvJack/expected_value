import os
import random
import time

import numpy as np
import pandas as pd
import plotly.graph_objs as plotly_go

from configuration import *


def get_starting_balance():
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
    # balance -= BET if BET < balance else 0
    BET = min(BET, balance)
    balance -= BET

    return balance


def check_result(balance, win, loose, BET, start_value, end_value):
    ball = random.randint(start_value, end_value)
    # (balance += BET * 2) and (win += 1) if ball in WIN_FIELDS else loose += 1
    if ball in WIN_FIELDS:
        balance += BET * 2
        win += 1
    else:
        loose += 1

    return balance, win, loose


def print_result(index, win, loose):
    print(
        "\n"
        f"Стратегия №{index}",
        f"Общее число игр: {win + loose}",
        f"Выиграно ставок: {str(win)}, ({str(win/(win + loose) * 100)}%)",
        f"Проиграно ставок: {str(loose)}, ({str(loose/(win + loose) * 100)}%)",
        sep="\n",
        end="\n\n")


def game_strategy_1(balance, BET, balance_strategy_1):
    win = 0
    loose = 0

    while balance > 0:
        balance = balance_manipulaion(balance, BET)
        # ball = random.randint(0, 36)
        balance, win, loose = check_result(balance, win, loose, BET, 0, 36)
        balance_strategy_1.append(balance)

    print_result(1, win, loose)

    return balance_strategy_1


def game_strategy_2(balance, BET, balance_strategy_2):
    win = 0
    loose = 0

    while (balance > 0) and (win + loose < STOP_POINT):
        balance = balance_manipulaion(balance, BET)
        # ball = random.randint(0, 35)
        balance, win, loose = check_result(balance, win, loose, BET, 0, 35)
        balance_strategy_2.append(balance)

    print_result(2, win, loose)

    return balance_strategy_2


def game_strategy_3(balance, BET, balance_strategy_3):
    win = 0
    loose = 0

    while (balance > 0) and (win + loose < STOP_POINT):
        balance = balance_manipulaion(balance, BET)
        # ball = random.randint(1, 35)
        balance, win, loose = check_result(balance, win, loose, BET, 1, 35)
        balance_strategy_3.append(balance)

    print_result(3, win, loose)
    return balance_strategy_3


def count_games(balance_strategy_1, balance_strategy_2, balance_strategy_3):

    count_games_strategy_1 = [i for i in range(1, len(balance_strategy_1) + 1)]
    count_games_strategy_2 = [i for i in range(1, len(balance_strategy_2) + 1)]
    count_games_strategy_3 = [i for i in range(1, len(balance_strategy_3) + 1)]

    return count_games_strategy_1, count_games_strategy_2, count_games_strategy_3


def graph(balance_strategy_1, balance_strategy_2, balance_strategy_3):
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
                             xaxis_title="Кол-во игр",
                             yaxis_title="Баланс",
                             margin=dict(l=0, r=0, t=50, b=100)),
        figure.update_traces(hoverinfo="all",
                             hovertemplate="Игра: %{x}<br>Баланс: %{y}")

        figure.show()


def savedata(balance_strategy_1, balance_strategy_2, balance_strategy_3):

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
            'Кол-во игр 1': arr_count_games_strategy_1,
            'Баланс по стратегии 1': arr_balance_strategy_1,
            'Кол-во игр 2': arr_count_games_strategy_2,
            'Баланс по стратегии 2': arr_balance_strategy_2,
            'Кол-во игр 3': arr_count_games_strategy_3,
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
