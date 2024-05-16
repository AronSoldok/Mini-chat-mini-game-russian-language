from socket import *
from Game import game, print_server_art  # импорт игры "камень, ножницы, бумага"

# TCPServer.py
serverPort = 1030
serverName = '127.0.0.1'


serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)

game_start = False      # булева переменная для входа в режим игры
first_message = True    # булева переменная, чтобы убедиться, что сервер печатает приглашение только один раз (после первого сообщения от клиента)
gaming_results = {}     # для хранения выборов сервера и клиента для игры
# ведение учета очков (лучший из трех побед)
server_wins = 0
client_wins = 0
# допустимые вводы для игры, проверка данных
valid_inputs = ['камень', 'ножницы', 'бумага']
# вывод информации о подключении
print('Сервер прослушивает: localhost на порту:' + str(serverPort))
print("Подключено (" + str(serverName) + ',' + str(serverPort))
print("Ожидание сообщения. . . . . ")
connectionSocket, addr = serverSocket.accept()

while True:
    # получаем ответ от клиента
    clientReply = connectionSocket.recv(1024).decode()

    # когда игра еще не началась, обрабатываем ответы клиента
    if not game_start:

        # если клиент хочет сыграть в игру, затем получите ввод сервера и сохраните его в словаре
        # но отправьте сообщение клиенту, что сервер тоже хочет играть, чтобы он мог получить
        # выбор клиента для игры и отправить его серверу
        if clientReply == 'играть в камень, ножницы, бумага':
            print('Клиент хочет сыграть в камень, ножницы, бумагу! Лучший из трех!')
            serverInput = input("Введите свой выбор (камень, ножницы, бумага): ")
            serverInput = serverInput.lower()
            while serverInput not in valid_inputs:
                print("Упс! Это недопустимый ввод, попробуйте еще раз!")
                serverInput = input("Введите свой выбор (камень, ножницы, бумага): ")
                serverInput = serverInput.lower()
            gaming_results['server'] = serverInput
            game_start = True
            connectionSocket.send("Хорошо, давайте сыграем в камень, ножницы, бумагу! Лучший из трех :)".encode())

        # обрабатывает другие сообщения от клиента, похожие на обычные сообщения чата
        else:
            print(clientReply)

            if clientReply == '/q':
                print('Клиент запросил завершение работы. Завершение работы')
                connectionSocket.close()
                break

            if first_message:   # выводит приглашение серверу после того, как клиент отправит первое сообщение
                print("Введите /q для выхода")
                print("Введите сообщение для отправки. Пожалуйста, дождитесь приглашения к вводу перед вводом сообщения. . .")
                print("Примечание: Введите 'играть в камень, ножницы, бумага', чтобы начать игру в камень, ножницы, бумага")
                first_message = False

            # отображает ввод и отправляет его клиенту
            if clientReply != 'играть в камень, ножницы, бумага' and not first_message:
                serverInput = input("Введите ввод > ")
                if serverInput == '/q':
                    print('Завершение работы')
                    connectionSocket.send(serverInput.encode())
                    connectionSocket.close()
                    break

                # обрабатывает, если сервер хочет сыграть в игру
                if serverInput == 'играть в камень, ножницы, бумага':
                    server_choice = input("Введите свой выбор (камень, ножницы, бумага): ")
                    server_choice = server_choice.lower()
                    while server_choice not in valid_inputs:
                        print("Упс! Это недопустимый ввод, попробуйте еще раз!")
                        server_choice = input("Введите свой выбор (камень, ножницы, бумага): ")
                        server_choice = server_choice.lower()
                    gaming_results['server'] = server_choice    # сохраняем выбор сервера в словаре
                    game_start = True
                    connectionSocket.send(serverInput.encode()) # отправляет обратно клиенту строку для начала игры
                else:
                    connectionSocket.send(serverInput.encode()) # отправляет сообщение с вводом пользователя от сервера, как обычно для всех остальных сообщений

    # если игра началась, здесь происходит игровая логика
    else:
        # отправляем клиенту то, что хранится в словаре gaming_results для ввода сервера
        # это по сути та же логика игры, что и у клиента
        connectionSocket.send(gaming_results['server'].encode())
        if clientReply in ['камень', 'ножницы', 'бумага']:
            gaming_results['client'] = clientReply
            server_choice = gaming_results['server']
            game_results = game(server_choice, clientReply)
            art = print_server_art(server_choice, clientReply)
            print('\n' + game_results)
            gaming_results = {}
            if game_results == 'Победил сервер!':
                server_wins += 1
            if game_results == 'Победил клиент!':
                client_wins += 1
            if server_wins < 3 and client_wins < 3:
                promptUser = "Следующий раунд!"
                print("Следующий раунд!")
                serverInput = input("Введите свой выбор (камень, ножницы, бумага): ")
                serverInput = serverInput.lower()
                while serverInput not in valid_inputs:
                    print("Упс! Это недопустимый ввод, попробуйте еще раз!")
                    serverInput = input("Введите свой выбор (камень, ножницы, бумага): ")
                    serverInput = serverInput.lower()
                gaming_results['server'] = serverInput
                # это отправит "Следующий раунд" клиенту
                # это помогает, чтобы и сервер, и клиент могли получить необходимые для игры вводы
                # сервер получит выбор клиента на следующей итерации, так как он ждет сообщение клиента
                connectionSocket.send(promptUser.encode())
            else:
                if server_wins > client_wins:
                    winner = "Сервер"
                else:
                    winner = "Клиент"
                game_over = "Игра окончена!" + winner + ' побеждает!'
                server_wins = 0
                client_wins = 0
                print("Игра окончена! " + winner + " побеждает!")
                game_start = False
