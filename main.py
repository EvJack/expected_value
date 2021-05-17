import random
import plotly.graph_objs as go

startmoney = int(input("Введите ваш стартовый баланс: "))

COEFFICIENT = 0.001
WIN_FIELDS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 28, 29, 31, 33, 35]
STOP_POINT = 40000

balance1 = []
games1 = []

balance2 = []
games2 = []

balance3 = []
games3 = []


def money_manipulaion(money):
    bet = startmoney * COEFFICIENT
    if bet > money:
        bet = money
    money -= bet
    return money, bet


def strategy1():
    win = 0
    loose = 0
    games = 0
    money = startmoney

    while money > 0:
        money, bet = money_manipulaion(money)

        balance1.append(money)
        games1.append(len(games1) + 1)

        ball = random.randint(0, 36)

        if ball in WIN_FIELDS:
            money += bet * 2
            win += 1
        else:
            loose += 1
    games = win + loose
    print("Стратегия №1", f"Выиграно ставок: {str(win)}, ({str(win/games * 100)}%)", f"Проиграно ставок: {str(loose)}, ({str(loose/games * 100)}%)", sep="\n", end="\n\n")

def strategy2():
    win = 0
    loose = 0
    games = 0
    money = startmoney

    while (money > 0) and (win + loose < STOP_POINT):
        money, bet = money_manipulaion(money)

        balance2.append(money)
        games2.append(len(games2) + 1)

        ball = random.randint(0, 35)

        if ball in WIN_FIELDS:
            money += bet * 2
            win += 1
        else:
            loose += 1
    games = win + loose
    print("Стратегия №2", f"Выиграно ставок: {str(win)}, ({str(win/games * 100)}%)", f"Проиграно ставок: {str(loose)}, ({str(loose/games * 100)}%)", sep="\n", end="\n\n")

def strategy3():
    win = 0
    loose = 0
    games = 0
    money = startmoney

    while (money > 0) and (win + loose < STOP_POINT):
        money, bet = money_manipulaion(money)

        balance3.append(money)
        games3.append(len(games3) + 1)

        ball = random.randint(1, 35)

        if ball in WIN_FIELDS:
            money += bet * 2
            win += 1
        else:
            loose += 1
    games = win + loose
    print("Стратегия №3", f"Выиграно ставок: {str(win)}, ({str(win/games * 100)}%)", f"Проиграно ставок: {str(loose)}, ({str(loose/games * 100)}%)", sep="\n", end="\n\n")

def graph():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=games1, y=balance1, name = "Отрицательное матожидание"))
    fig.add_trace(go.Scatter(x=games2, y=balance2, name = "Нулевое матожидание"))
    fig.add_trace(go.Scatter(x=games3, y=balance3, name = "Положительное матожидание"))
    fig.update_layout(legend_orientation="h",
    legend=dict(x=.5, xanchor="center"),
    margin=dict(l=0, r=0, t=50, b=100)),
    title="Изменение баланса с течением времени",
    xaxis_title="Кол-во игр",
    yaxis_title="Баланс",
    fig.update_traces(hoverinfo="all", hovertemplate="Игра: %{x}<br>Баланс: %{y}")
    fig.show()


def main():
    strategy1()
    strategy2()
    strategy3()
    graph()

if __name__ == "__main__":
    main()