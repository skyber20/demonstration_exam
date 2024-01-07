from tkinter import *
from tkinter import messagebox, ttk
import os
import datetime
from math import floor

# регистрация
registration = Tk()
registration.title('Авторизация')
registration['bg'] = '#d2d2d2'
registration.geometry('1000x500')

frame_registration = Frame(registration, bg='#d2d2d2')
frame_registration.place(relheight=0.5, relwidth=0.5, rely=0.25, relx=0.35)


def auth():
    try:
        with open('users.csv', encoding='UTF8') as file:
            users = [user.strip().split(';') for user in file.readlines()[1:]]
    except FileNotFoundError:
        print("Файл не найден")
    else:
        login = login_entry.get()
        password = password_entry.get()

        if len(login) != 10 or not(login.isdigit()):
            messagebox.showerror("Ошибка!", "Логин должен включать в себя только 10 цифр")
        else:
            for user in users:
                if login == user[1] and password == user[2]:
                    if user[3] == 'директор':
                        registration.withdraw()
                        director.deiconify()
                        Label(director, text=f'Добро пожаловать, {user[0]}!', bg='white', font='Arial 12').place(anchor='center', rely=0.05, relx=0.5)
                        show_data_director_frame()
                    else:
                        registration.withdraw()
                        admin.deiconify()
                        Label(admin, text=f'Добро пожаловать, {user[0]}!', bg='white', font='Arial 12').place(anchor='center', rely=0.05, relx=0.5)
                    break
            else:
                messagebox.showerror('Ошибка!', "Неправильный логин / пароль")

            

Label(frame_registration, text='Логин:', bg='#d2d2d2', font='Arial 13').grid(row=0, column=0, padx=10)
login_entry = Entry(frame_registration, font='Arial 16')
login_entry.grid(row=0, column=1, pady=10)

Label(frame_registration, text='Пароль:', bg='#d2d2d2', font='Arial 13').grid(row=1, column=0, padx=10)
password_entry = Entry(frame_registration, show='*', font='Arial 16')
password_entry.grid(row=1, column=1, pady=10)

Button(frame_registration, text='Войти', font='Arial 12', bg='#787878', command=auth).grid(row=3, columnspan=2)

Button(registration, text='ВЫХОД', font='Arial 12', bg='#787878', command=registration.destroy).pack(side='left', anchor='sw', padx=20, pady=30)



# директор
director = Tk()
director.geometry('1000x600')
director['bg'] = '#d2d2d2'
director.title('Окно директора') 


def back_to_registration():
    director.withdraw()
    admin.withdraw()
    registration.deiconify()


def go_to_order():
    director.withdraw()
    order.deiconify()


def edit_func():
    show_data_director_frame()


def delete_func():
    selected_item = tree_director.selection()
    if selected_item:
        delete_row = list(map(str, tree_director.item(selected_item)['values']))[:-1]
        try:
            with open('orders.csv', encoding='UTF8') as orders_file:
                first_line = orders_file.readline().strip()
                lines = [line.strip().split(';') for line in orders_file.readlines()]
        except FileNotFoundError:
            print('Файл не найден')
        else:
            with open('orders.csv', encoding='UTF8', mode='w') as orders_file:
                orders_file.write(first_line)
                orders_file.writelines(f'\n{';'.join(line)}' for line in lines if line[:-1] != delete_row)
            tree_director.delete(selected_item)
            show_data_director_frame()
    else:
        print("Строка не выбрана")


frame_director = Frame(director, bg='white', bd=0.5, relief='solid')
frame_director.place(relheight=0.5, relwidth=0.8, rely=0.15, relx=0.1)
frame_director.rowconfigure(index=0, weight=1)
frame_director.columnconfigure(index=0, weight=1)

# ПОМЕНЯТЬ СТИЛИ LABELS ВЕЗДЕ
columns = ['Номер заказа', 'Имя клиента', 'Название товара', 'Количество', 'Оставшийся срок']
tree_director = ttk.Treeview(frame_director, columns=columns, show='headings')
tree_director.grid(row=0, column=0, sticky='nsew')

scrollbar = ttk.Scrollbar(frame_director, orient=VERTICAL, command=tree_director.yview)
tree_director.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

for col in range(len(columns)):
    tree_director.heading(columns[col], text=columns[col], anchor=N)
    tree_director.column(f"#{col+1}", width=96)
    

def convert_in_date(str_date):
    date_date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
    current_time = datetime.datetime.now()
    time_difference = date_date - current_time

    days = time_difference.days
    seconds = time_difference.seconds

    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{days} {hours}:{minutes}:{seconds}'
    

def show_data_director_frame():
    for item in tree_director.get_children():
        tree_director.delete(item)
    try:
        with open('orders.csv', encoding='UTF8') as orders_file:
            data_lines = [order.strip().split(';') for order in orders_file.readlines()[1:]]
            for date_lines_4, date_lines_last in zip([data[:-1] for data in data_lines], [data[-1] for data in data_lines]):
                diff = convert_in_date(date_lines_last)
                tree_director.insert('', END, values=date_lines_4 + [diff])
    except FileNotFoundError:
        print("Файл не найден")


frame_director_btns = Frame(director, bg='#d2d2d2', height=50)
frame_director_btns.place(relwidth=0.38, rely=0.68, relx=0.1)

labels = ['Добавить', 'Изменить', 'Удалить']
funcs = [go_to_order, edit_func, delete_func]

for i in range(len(labels)):
    btn = Button(frame_director_btns, text=labels[i], font='Arial 12', bg='#787878', command=funcs[i])
    btn.place(relx=i/len(labels), rely=0, relwidth=1/len(labels) - (0.02 if i != len(labels) - 1 else 0), relheight=1, anchor='nw')


Button(director, text='НАЗАД', font='Arial 12', bg='#787878', command=back_to_registration).pack(side='left', anchor='sw', padx=20, pady=30)



# админ
admin = Tk()
admin.geometry('1000x600')
admin.title('Окно админа')
admin['bg'] = '#d2d2d2'

frame_admin = Frame(admin, bg='white', bd=0.5, relief='solid')
frame_admin.place(relheight=0.5, relwidth=0.7, rely=0.15, relx=0.2)
frame_admin.columnconfigure(index=0, weight=1)
frame_admin.rowconfigure(index=0, weight=1)

columns = ['Имя пользователя', 'Логин', 'Пароль', 'Роль']

tree_admin = ttk.Treeview(frame_admin, show='headings', columns=columns)
tree_admin.grid(row=0, column=0, sticky='nsew')

scrollbar = ttk.Scrollbar(frame_admin, orient=VERTICAL, command=tree_admin.yview)
tree_admin.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

for col in range(len(columns)):
    tree_admin.heading(columns[col], text=columns[col], anchor=N)
    tree_admin.column(f'#{col+1}', width=175)

try:
    with open('users.csv', encoding='UTF8') as users_file:
        users = [user.strip().split(';') for user in users_file.readlines()[1:]]
except FileNotFoundError:
    print('Файл не найден')
else:
    for user in users:
        tree_admin.insert('', END, values=user)

Button(admin, text='НАЗАД', bg='#787878', font='Arial 12', command=back_to_registration).pack(side='left', anchor='sw', padx=20, pady=30)



# окно заказа
order = Tk()
order.title('Заказ')
order['bg'] = '#d2d2d2'
order.geometry('600x450')


def back_to_director():
    order.withdraw()
    director.deiconify()
    show_data_director_frame()


def accept_order():
    data_entries = []
    for entry in entries:
        data_entry = entry.get()
        data_entries.append(data_entry)
    if all(bool(data) for data in data_entries):
        name_file = 'orders.csv'
        if os.path.exists(name_file):
            with open(name_file, encoding='UTF8', mode='a') as orders_file:
                orders_file.write(f"\n{';'.join(data_entries)}")
            order.withdraw()
            director.deiconify()
            show_data_director_frame()
        else:
            print("Файл не найден")
    else:
        messagebox.showerror("Внимание!", "Должны быть заполнены все поля")
        



frame_order = Frame(order, bg='#d2d2d2')
frame_order.place(relheight=0.8, relwidth=0.8, relx=0.15, rely=0.1)

labels = ['Номер заказа:', 'Заказчик:', 'Название товара:', 'Количество:', 'Дата отгрузки:']
entries = []

for label in range(len(labels)):
    Label(frame_order, text=labels[label], bg='#d2d2d2', font='Arial 12').grid(row=label, column=0, padx=10, pady=10)
    entry = Entry(frame_order, font='Arial 16')
    entry.grid(row=label, column=1, pady=10)
    entries.append(entry)

Button(frame_order, text='Принять', font='Arial 12', bg='#787878', command=accept_order).grid(row=5, columnspan=2, pady=10)

Button(order, text='ВЫХОД', font='Arial 12', bg='#787878', command=back_to_director).pack(side='left', anchor='sw', padx=20, pady=30)



# registration.withdraw()
director.withdraw()
admin.withdraw()
order.withdraw()

director.mainloop()
admin.mainloop()
registration.mainloop()
order.mainloop()
