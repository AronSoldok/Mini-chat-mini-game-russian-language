# Name: Сабрина Эстрада
# Описание: Игра "Камень, ножницы, бумага" для части проекта чата/игры

# Ссылка на ASCII-арт:
# Дата: 11.06.2023
# Название: ASCII-арт "Камень, Ножницы, Бумага" от wynand1004
# Доступно по: https://gist.github.com/wynand1004/b5c521ea8392e9c6bfe101b025c39abe

left = {'камень':
"""
    _______
---'   ____) 
      (_____)
      (_____)
      (____) 
---.__(___) 
""", 'бумага':
"""
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)   
""", 'ножницы':
"""
    _______
---'    ____)____
           ______)
        __________)
      (____)      
---.__(___)
"""}

right = {'камень':
"""
  _______
 (____     '---
(_____)
(_____)
 (____)
  (___)__.---
""", 'бумага':
"""
      _______ 
 ____(____    '---
(______
(_______
 (_______
   (__________.---
""", 'ножницы':
"""
       _______
  ____(____   '---
 (______
(__________
     (____)
      (___)__.---
"""}

result = ''

# это логика игры, если вводы одинаковые, то это ничья
def game(server_choice, client_choice):
    if server_choice == client_choice:
        result = "Ничья"
    # обрабатывает, кто побеждает на основе их выборов, логика "камень, ножницы, бумага"
    elif (server_choice == 'бумага' and client_choice == 'камень') or (server_choice == 'ножницы' and client_choice == 'бумага') or (server_choice == 'камень' and client_choice == 'ножницы'):
        result = "Победил сервер!"
    else:
        result = "Победил клиент!"
    # возвращает результат, победа сервера/клиента или ничья
    return result

# Ссылка на отображение ASCII-арт:
# Дата: 11.06.2023
# Название: Как разместить два или более изображений ASCII рядом?
# Доступно по: https://stackoverflow.com/questions/69795265/how-do-i-place-two-or-more-ascii-images-side-by-side

# это логика для отображения ASCII-арт, есть две, чтобы отобразить на сервере и
# другой для отображения на стороне клиента
def print_client_art(client_choice, server_choice):
    # это отобразит клиента слева и сервера справа
    server_art = right[server_choice]
    client_art = left[client_choice]

    # нужно разбить ASCII-арт на строки, чтобы можно было отобразить их рядом
    server_art_lines = server_art.splitlines()
    client_art_lines = client_art.splitlines()

    # так как ASCII-арт может иметь разную длину, нужно вычислить заполнение
    # для этого найдите самую длинную строку в ASCII-арт клиента, и это будет использоваться для вычисления заполнения
    max_length = max(len(line) for line in client_art_lines)

    # a и b - это отдельные строки ASCII, которые будут печататься по одной
    # заполнение вычисляется с использованием максимальной длины строк ASCII-арт клиента и текущей строки b.
    # + 2 нужно для печати дополнительного пространства между двумя изображениями ASCII
    for a, b in zip(server_art_lines, client_art_lines):
        print((b + (" " * (max_length - len(b) + 2)) + a))
    # печатает строки по одной

# та же логика, что и в предыдущем, но зеркально, чтобы сервер отображался слева
def print_server_art(server_choice, client_choice):
    # это отобразит сервер слева и клиента справа
    server_art = left[server_choice]
    client_art = right[client_choice]

    # нужно разбить ASCII-арт на строки, чтобы можно было отобразить их рядом
    server_art_lines = server_art.splitlines()
    client_art_lines = client_art.splitlines()

    max_length = max(len(line) for line in server_art_lines)

    for a, b in zip(server_art_lines, client_art_lines):
        print((a + (" " * (max_length - len(a) + 2)) + b))


