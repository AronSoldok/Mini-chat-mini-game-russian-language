from socket import *
from Game import game, print_client_art  # импорт игры "камень, ножницы, бумага"

# Цитата для следующего кода:
# Дата: 11.06.2023
# Адаптировано из: Kurose, James F, и Keith W Ross.
# Компьютерные сети: технология верхнего уровня. Хобокен, Пирсон, 2021, с. 161–165.

# TCPClient.py

serverName = '127.0.0.1'
serverPort = 1030
game_start = False      # булева переменная для входа в режим игры
gaming_results = {}     # для хранения выборов сервера и клиента для игры
# ведение учета очков (лучший из трех побед)
server_wins = 0
client_wins = 0
# допустимые вводы для игры, проверка данных
valid_inputs = ['камень', 'ножницы', 'бумага']
# приглашение для клиента
print('Сервер прослушивает: localhost на порту:' + str(serverPort))
print("Введите /q для выхода")
print("Введите сообщение для отправки. Подождите приглашения к вводу перед вводом сообщения...")
print("Примечание: Введите 'играть в камень, ножницы, бумага', чтобы начать игру в камень, ножницы, бумага")

# Создание сокета клиента (Kurose & Ross, 2021, стр. 162)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    if game_start:      # если игра началась, войдите в это условие для прохождения логики игры
        if 'клиент' not in gaming_results:          # проверяем, есть ли у нас сохраненный ответ от клиента
            userInput = input("Введите свой выбор (камень, ножницы, бумага): ")
            userInput = userInput.lower()           # помогает с валидацией данных, чтобы пользователь мог вводить допустимый ввод с заглавной буквы
            while userInput not in valid_inputs:    # цикл валидации данных, позволяет пользователю попробовать снова
                print("Упс! Это недопустимый ввод, попробуйте еще раз!")
                userInput = input("Введите свой выбор (камень, ножницы, бумага): ")
                userInput = userInput.lower()
            gaming_results['клиент'] = userInput    # сохраняем ответ клиента для игры, чтобы использовать его позже
            clientSocket.send(userInput.encode())   # отправляем ответ серверу

            # получаем ответ сервера и проверяем, находится ли он в допустимых вводах, если да, то сохраняем его в результатах
            serverReply = clientSocket.recv(2048).decode()

            if serverReply in ['камень', 'ножницы', 'бумага']:
                gaming_results['сервер'] = serverReply

            # если у нас есть выборы сервера и клиента, мы можем вызвать игру и ввести ввод, вывести результаты
            if 'сервер' in gaming_results and 'клиент' in gaming_results:
                server_choice = gaming_results['сервер']
                client_choice = gaming_results['клиент']

                # получаем результаты о победителе и выводим ascii с клиентом слева и сервером справа
                results = game(server_choice, client_choice)
                art = print_client_art(client_choice, server_choice)
                print('\n' + results)

                # начать с начала для новой игры
                gaming_results = {}

                # увеличиваем счетчик в зависимости от того, кто выиграл
                if results == 'Победил сервер!':
                    server_wins += 1
                elif results == 'Победил клиент!':
                    client_wins += 1

                # продолжаем игру, если никто не выиграл 3 раунда
                if server_wins < 3 and client_wins < 3:
                    print("Следующий раунд!")
                    userInput = input("Введите свой выбор (камень, ножницы, бумага): ")
                    userInput = userInput.lower()
                    while userInput not in valid_inputs:
                        print("Упс! Это недопустимый ввод, попробуйте еще раз!")
                        userInput = input("Введите свой выбор (камень, ножницы, бумага): ")
                        userInput = userInput.lower()
                    gaming_results['клиент'] = userInput
                    clientSocket.send(userInput.encode())   # отправляем новый ввод клиента для следующего раунда серверу

                # иначе кто-то выиграл 3 раунда, выводим результаты о победителе
                else:
                    if server_wins > client_wins:
                        winner = "Сервер"
                    else:
                        winner = "Клиент"

                    # сбросить счетчик, так как игра окончена
                    server_wins = 0
                    client_wins = 0
                    print("Игра окончена! " + winner + " побеждает!")

                    # сбросить булеву переменную на False, так как игра окончена
                    game_start = False
            else:
                print(serverReply)

        # это ветвление else помогает, когда игра переходит к следующему раунду
        # После первого раунда получаем новый ввод клиента для следующей игры и отправляем его серверу
        # сервер сохранит этот ввод, затем отправит "Следующий раунд" клиенту первым
        # затем это ветвление else будет продолжать вызываться, пока клиент не получит допустимый ввод для игры
        else:
            # логика очень похожа на предыдущее условное выражение
            serverReply = clientSocket.recv(2048).decode()
            if serverReply in ['камень', 'ножницы', 'бумага']:
                gaming_results['сервер'] = serverReply

            if 'сервер' in gaming_results and 'клиент' in gaming_results:
                server_choice = gaming_results['сервер']
                client_choice = gaming_results['клиент']
                results = game(server_choice, client_choice)
                art = print_client_art(client_choice, server_choice)
                print('\n' + results)
                gaming_results = {}
                if results == 'Победил сервер!':
                    server_wins += 1
                elif results == 'Победил клиент!':
                    client_wins += 1
                if server_wins < 3 and client_wins < 3:
                    print("Следующий раунд!")
                    userInput = input("Введите свой выбор (камень, ножницы, бумага): ")
                    userInput = userInput.lower()
                    while userInput not in valid_inputs:
                        print("Упс! Это недопустимый ввод, попробуйте еще раз!")
                        userInput = input("Введите свой выбор (камень, ножницы, бумага): ")
                        userInput = userInput.lower()
                    gaming_results['клиент'] = userInput
                    clientSocket.send(userInput.encode())
                else:
                    if server_wins > client_wins:
                        winner = "Сервер"
                    else:
                        winner = "Клиент"
                    game_over = "Игра окончена! " + winner + ' побеждает!'
                    server_wins = 0
                    client_wins = 0
                    print("Игра окончена! " + winner + " побеждает!")
                    game_start = False

    else:       # иначе: игра не началась, пройдите обычную сеанс чата с сервером
        userInput = input("Ввод > ")
        if userInput == '/q':                       # условный оператор, если клиент хочет выйти
            clientSocket.send(userInput.encode())   # сообщаем серверу, что клиент хочет выйти
            print('Завершение работы!')
            clientSocket.close()
            break                                   # завершаем выполнение
        if userInput == 'играть в камень, ножницы, бумага':       # если клиент хочет сыграть в камень, ножницы, бумагу
            print("Оо, игра! Посмотрим, что скажет сервер")    # сначала нужно сообщить серверу, чтобы он вошел в режим игры
            game_start = True                               # булева переменная для входа в режим игры

        if userInput != '/q':                                   # отправляем сокет и получаем ответ от сервера
            clientSocket.send(userInput.encode())

            serverReply = clientSocket.recv(2048).decode()
            if serverReply == 'играть в камень, ножницы, бумага':     # условный оператор для обработки, если сервер хочет играть в игру
                print('Сервер хочет играть в камень, ножницы, бумагу! Лучший из трех!')
                game_start = True
            if serverReply == '/q':                             # условный оператор, если сервер хочет выйти
                print("Сервер запросил завершение. Завершение работы.")
                clientSocket.close()                            # завершаем выполнение и выходим из цикла на стороне клиента
                break
            else:
                print(serverReply)                              # иначе печатаем ответ сервера как обычно
