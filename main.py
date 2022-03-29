import pymysql
from config import host, user, password, db_name
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
from tkinter import *
global x,s1
import tkinter.messagebox as mb
s=''
s1=''
connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

# ----------------------------ctrl+c,ctrl+v,ctrl+x----------------------------
def _onKeyRelease(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

# --------------------------фунция поддверждения закрытия программы-------------------------------
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        connection.close()
        window.destroy()

def show_info(tabl,id):
    msg = f"New ID {tabl}={id}"
    mb.showinfo("Информация", msg)
# --------------------------Создание окна------------------------------
window = tk.Tk()
window['background']='#1D334A'
window.bind_all("<Key>", _onKeyRelease, "+")
window.geometry('1200x650+300+150')
window.title('БД')
tab_control = ttk.Notebook(window)
message1=StringVar()
message2=StringVar()
message3=StringVar()
message4=StringVar()
message5=StringVar()
def calculate(s12):
    with connection.cursor() as cursor:
        print(1)
        print(s12)
        if s12=='price_with_action':
            print(globals()[f'ID_action'].get())
            select_all_rows = f"SELECT terms_of_action FROM action WHERE action.ID_action={globals()[f'ID_action'].get()}"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            for row in rows:
                procent = int(row['terms_of_action'][:-1])
            select_all_rows = f"SELECT set_price  FROM setting WHERE setting.ID_set={globals()[f'ID_set'].get()}"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            for row in rows:
                setprice = int(row['set_price'])
            result =int(globals()[f'price'].get()) - int(globals()[f'price'].get()) * procent /100+setprice+int(globals()[f'overhead_costs'].get())
            print(result)
            globals()['price_with_action'].delete(0,END)
            globals()['price_with_action'].insert(END,str(result))
        elif s12=="final_price":
            if globals()[f'ID_oldcar'].get()!="нет":
                select_all_rows = f"SELECT * FROM trade_in WHERE trade_in.ID_oldcar={globals()[f'ID_oldcar'].get()}"
                cursor.execute(select_all_rows)
                rows = cursor.fetchall()
                for row in rows:
                    price = int(row['price_car'])
                    condition=row['Condition_of_car']
                if condition=="плохое":
                    result=-2
                elif condition=="хорошее":
                    result=4
                elif condition=="отличное":
                    result=6
                if price<100000:
                    result=result+5
                elif 100000<=price<300000:
                    result = result + 10
                elif 300000<=price<800000:
                    result = result + 15
                elif 800000<=price:
                    result = result + 20
            else:
                result=0
            select_all_rows = f"SELECT price_with_action FROM car WHERE car.ID_car={globals()[f'ID_car'].get()}"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            for row in rows:
                price = int(row['price_with_action'])
            result1=price-price*result/100
            globals()['final_price'].delete(0, END)
            globals()['final_price'].insert(END, str(result1))
def insert():
    with connection.cursor() as cursor:
        select_all_rows = f"SELECT MAX(ID_{tablname1.get()}) FROM `{tablname1.get()}`"
        cursor.execute(select_all_rows)
        rows = cursor.fetchall()
        print(rows)
        x=f'MAX(ID_{tablname1.get()})'
        print(x)
        for row in rows:
            e = row[f'{x}']
        print(e)
        print(s12)
        k=f"'{e+1}'"
        k1=f"ID_{tablname1.get()}"
        print(k)
        for i in range(len(s12)):
            k= k + "," + "'"+globals()[f'{s12[i]}'].get()+"'"
            k1=k1+","+s12[i]
        print(k1)
        insert_price = f"INSERT INTO `{tablname1.get()}` ({k1}) VALUES ({k})"
        cursor.execute(insert_price)
        connection.commit()
        for g in range(len(s12)):
            globals()[f'{s12[g]}'].destroy()
            globals()[f'{s12[g]}1'].destroy()
            if s12[g] == "price_with_action" or s12[g] == "final_price":
                globals()[f'{s12[g]}b'].destroy()
        buttondel.destroy()
        show_info(tablname1.get(),e+1)
        tablname1.delete(0,END)
        change.delete(0,END)
global s12,m
m=0
s12=[]
def block(tab,collumn):
    global ID, s12, m, buttondel
    print(n)
    if m > 0:
        if len(s12) > 0:
            for g in range(len(s12)):
                globals()[f'{s12[g]}'].destroy()
                globals()[f'{s12[g]}1'].destroy()
                if s12[g] == "price_with_action" or s12[g] == "final_price":
                    globals()[f'{s12[g]}b'].destroy()
            buttondel.destroy()
    m = count1(m)

    with connection.cursor() as cursor:
        if str(tab)=='.!notebook.!frame3':
            global collumnfiltr
            if collumn.get()=="все":
                if collumnfiltr.get() is not None:
                    collumnfiltr.delete(0, END)
                collumnfiltr.config(state="readonly")
            else:
                collumnfiltr.config(state="normal")
        if str(tab) == '.!notebook.!frame4':

            if change.get() == "Добавить":

                print("HGUGIUGUGIUH       ", m)
                globals()['collumn' + str(n)].delete(0,END)
                globals()['collumn'+str(n)].config(state='disabled')
                ID.delete(0,END)
                ID.config(state="readonly")
                cursor.execute(f'describe `{tablname1.get()}`')
                rows = cursor.fetchall()

                s12 = []
                if tablname1.get()== "setting":
                    d = "set"
                elif tablname1.get() == "trade_in":
                    d = "oldcar"
                else:
                    d=tablname1.get()
                for row in rows:
                    if row['Field'].lower()!=f'id_{d}':
                        s12.append(row['Field'])

                print(s12)
                for i in range(len(s12)):
                    if s12[i].lower().startswith('id') == 0 and s12[i]!='Condition_of_car':
                        globals()[f'{s12[i]}message']=StringVar()
                        globals()[f'{s12[i]}']=Entry(tab, textvariable=globals()[f'{s12[i]}message'])
                        globals()[f'{s12[i]}'].place(relx=0.12, rely=0.30+0.05*i, height=25, width=106)

                    else:
                        if s12[i] != 'Condition_of_car':
                            if s12[i][3:]=="set":
                                d="setting"
                            elif s12[i][3:]=="oldcar":
                                d="trade_in"
                            else:
                                d=s12[i][3:]
                            select_all_rows = f"SELECT `{s12[i]}` FROM `{d}`"
                            cursor.execute(select_all_rows)
                            rows = cursor.fetchall()
                            s=[]
                            for k in range(len(rows)):
                                s.append(rows[k][f"{s12[i]}"])
                            if s12[i]=="ID_oldcar":
                                s.append("нет")
                        else:
                            s = ["плохое", "хорошее", "отличное"]
                        print(s)

                        globals()[f'{s12[i]}']=Combobox(tab3, values=s)
                        print(s12[i])
                        globals()[f'{s12[i]}'].place(relx=0.12, rely=0.30+0.05*i, height=25, width=106)


                    if s12[i] == "price_with_action" or s12[i] =="final_price":
                        print (s12[i])
                        k=s12[i]
                        globals()[f'{s12[i]}b'] = Button(tab3, text='посчитать',
                                                            background='#f4ead0',
                                                            command=lambda: calculate(k))
                        globals()[f'{s12[i]}b'].place(relx=0.22, rely=0.30 + 0.05 * i, height=25, width=106)
                        if s12[i] == "price_with_action":
                            globals()[f'{s12[i]}1'] = Label(tab, text=f'{s12[i]}_and_set:',
                                                            font=("Arial", 7),
                                                            bg='#1D334A',
                                                            fg='#f4ead0', justify=LEFT)
                        else:
                            globals()[f'{s12[i]}1'] = Label(tab, text=f'{s12[i]}:', font=("Arial", 7),
                                                            bg='#1D334A',
                                                            fg='#f4ead0', justify=LEFT)
                        globals()[f'{s12[i]}1'].place(relx=0.02, rely=0.30 + 0.05 * i)

                    else:
                        globals()[f'{s12[i]}1'] = Label(tab, text=f'{s12[i]}:',
                                                            font=("Arial", 7),
                                                            bg='#1D334A',
                                                            fg='#f4ead0', justify=LEFT)
                        globals()[f'{s12[i]}1'].place(relx=0.02, rely=0.30 + 0.05 * i)
                    if i== len(s12)-1:
                        buttondel = Button(tab3, text='внести в базу',
                                                         background='#f4ead0',
                                                         command=insert)
                        buttondel.place(relx=0.02, rely=0.30 + 0.05 * (i+1))


            else:
                globals()['collumn'+str(n)].config(state="normal")
                ID.destroy()
                ID = EntryWithPlaceholder(tab3, f'ID_{tablname1.get()}')
                ID.place(relx=0.235, y=20, height=25, relwidth=0.1)
                ID.config(state="normal")





def button1Callback():

    global cursor, connection,collumn0,y6,tablname,tab2,collumnfiltr,tab3,set,collumn1,change,ID,tablname1
    try:
        print("successfully connected...")
        print("#" * 20)
        with connection.cursor() as cursor:
            select_all_rows = f"SELECT role FROM config WHERE login='{login.get()}' and parol='{parol.get()}'"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            for row in rows:
                y6=row['role']
            print(y6)
    except Exception as ex:
        print("Connection refused")
        print(ex)
    deletetab()
    c1=[]
    if y6=="admin":
        s3=[]
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text='поиск')
        tab_control.pack(expand=1, fill='both')
        cursor = connection.cursor()  # get the cursor
        cursor.execute("SHOW tables")
        rows = cursor.fetchall()
        for i in range(len(rows)):
            c1.append(rows[i]['Tables_in_autosalon'])
        tablname = Combobox(tab2, values=c1)
        tablname.place(relx=0.025, y=20, height=25, relwidth=0.1)
        n=0
        collumn0 = Combobox(tab2, values=s3)
        collumn0.place(relx=0.13, y=20, height=25, relwidth=0.1)
        collumnn = Combobox(tab2, values=s3)
        collumnn.place(relx=0.13, y=20, height=25, relwidth=0.1)
        message4 = StringVar()
        collumn0.bind("<<ComboboxSelected>>", block)
        tablname.bind("<<ComboboxSelected>>", lambda event:button2Callback(tablname,tab2))

        collumnfiltr = Entry(tab2, textvariable=message4)
        collumnfiltr.place(relx=0.234, y=20, height=25, relwidth=0.1)

        butt = Button(tab2, text='поиск', background='#f4ead0', command=button3Callback)
        butt.place(relx=0.93, rely=0.93, height=30, relwidth=0.092,anchor=S)

        game_frame = Frame(tab2)
        game_frame.place(relx=0.5, rely=0.5, relheight=0.7, relwidth=0.95,anchor=CENTER)
        game_scroll = Scrollbar(game_frame)
        game_scroll.pack(side=RIGHT, fill=Y)
        game_scroll = Scrollbar(game_frame, orient='horizontal')
        game_scroll.pack(side=BOTTOM, fill=X)
        set = ttk.Treeview(game_frame, yscrollcommand=game_scroll.set, xscrollcommand=game_scroll.set)
        set.place(relx=0.494, rely=0.486, relheight=0.96, relwidth=0.985,anchor=CENTER)
        game_scroll.config(command=set.yview)
        game_scroll.config(command=set.xview)

        tab3 = ttk.Frame(tab_control)
        tab_control.add(tab3, text='Добавление и изменение')
        tab_control.pack(expand=1, fill='both')
        tablname1 = Combobox(tab3, values=c1)
        tablname1.place(relx=0.025, y=20, height=25, relwidth=0.1)
        tablname1.bind("<<ComboboxSelected>>", lambda event:button2Callback(tablname1,tab3))
        collumn1 = Combobox(tab3, values=s3)
        collumn1.place(relx=0.340, y=20, height=25, relwidth=0.1)
        s3=["Изменить","Добавить"]
        change = Combobox(tab3, values=s3)
        change.place(relx=0.13, y=20, height=25, relwidth=0.1)
        change.bind("<<ComboboxSelected>>", lambda event: block(tab3, globals()['collumn'+str(n)]))
        ID = EntryWithPlaceholder(tab3, 'ID')
        ID.place(relx=0.235, y=20, height=25, relwidth=0.1)

    else:
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text='составление заказа')
        tab_control.pack(expand=1, fill='both')
        collumn = Entry(tab2, textvariable=message2)
        collumn.place(x=0, y=20, height=25, width=106)
def count1(m):
    m += 1
    return(m)
global x, cursor,tablname
def count(event):
    global n
    n += 1
global x, cursor,tablname
# --
# ---------------
global n

def change2(tabl,collumn,id,filtr):
    with connection.cursor() as cursor:
        if tabl == "setting":
            d = "set"
        elif tabl == "trade_in":
            d = "oldcar"
        else:
            d = tabl
        print(collumn)
        insert_price = f"UPDATE `{tabl}` SET `{collumn}` = '{filtr}' WHERE ID_{d}={id};"
        cursor.execute(insert_price)
        connection.commit()
        cursor.execute(insert_price)
        connection.commit()
        parol21.delete(0,END)
        parol21.destroy()
        butt21.destroy()
def change1(tablnameu,collumn,id):
    global parol21, butt21
    with connection.cursor() as cursor:
        if tablnameu.get() == "setting":
            d = "set"
        elif tablnameu.get() == "trade_in":
            d = "oldcar"
        else:
            d=tablnameu.get()
        select_all_rows = f"SELECT {collumn.get()} FROM `{tablnameu.get()}` WHERE `{tablnameu.get()}`.ID_{d}={id.get()}"
        cursor.execute(select_all_rows)
        rows = cursor.fetchall()
        print(rows)
        for row in rows:
            filtr = row[f'{collumn.get()}']
        parol21 = Entry(tab3, textvariable=message5, font=('Helvetica', '15'))
        parol21.place(relx=0.1, rely=0.5, anchor=CENTER, relheight=0.05, relwidth=0.18)
        parol21.insert(0,filtr)
        butt21 = Button(tab3, text='изменить', background='#f4ead0', command=lambda: change2(tablnameu.get(),collumn.get(),id.get(),parol21.get()))
        butt21.place(relx=0.17, rely=0.5, anchor=CENTER, relheight=0.05, relwidth=0.1)
def button2Callback(tablname,tab):
    print(tab)
    global x, cursor, connection,n
    count
    print("sdsss    ", tablname.get())
    try:
        print(n)
        n=n+1
        print("successfully connected...")
        print("#" * 20)
        s3=[]

        with connection.cursor() as cursor:
            cursor.execute(f'describe `{tablname.get()}`')
            rows = cursor.fetchall()
            for row in rows:
                if str(tab) == ".!notebook.!frame4":
                    if tablname1.get() == "setting":
                        d = "set"
                    elif tablname1.get() == "trade_in":
                        d = "oldcar"
                    else:
                        d = tablname1.get()
                    if row['Field'].lower().startswith(f'id_{d}')==0:
                        s3.append(row['Field'])
                else:
                    s3.append(row['Field'])
            if str(tab) == ".!notebook.!frame3":
                s3.append('все')
            print(s3)
            globals()['collumn'+str(n-1)].destroy()
            globals()['collumn'+str(n)] = Combobox(tab, values=s3)

            if str(tab)==".!notebook.!frame3":
                globals()['collumn'+str(n)].bind("<<ComboboxSelected>>",lambda event: block(tab,globals()['collumn'+str(n)]))
                globals()['collumn' + str(n)].place(relx=0.13, y=20, height=25, relwidth=0.1)
            else:
                globals()['collumn' + str(n)].bind("<<ComboboxSelected>>",
                                                   lambda event: change1(tablname1,globals()['collumn' + str(n)],ID))
                globals()['collumn' + str(n)].place(relx=0.340, y=20, height=25, relwidth=0.1)
    except Exception as ex:
        print("Connection refused")
        print(ex)
    return (n)
def button3Callback():
    global s12
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print(globals()['collumn'+str(n)].get())
    try:

        print("successfully connected...")
        print("#" * 20)
        s12=[]
        for i in set.get_children():
            set.delete(i)
        with connection.cursor() as cursor:


            cursor.execute(f'describe `{tablname.get()}`')
            rows = cursor.fetchall()
            for row in rows:
                s12.append(row['Field'])
            print(tablname.get(),globals()['collumn'+str(n)].get())
            if globals()['collumn'+str(n)].get()=='все':
                select_all_rows = f"SELECT * FROM `{tablname.get()}`"
            else:
                select_all_rows = f"SELECT * FROM `{tablname.get()}` WHERE `{str(globals()['collumn'+str(n)].get())}` = '{str(collumnfiltr.get())}'"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            print(rows)
            try:
                set['columns'] = (s12)
                f = []
                fi = []
                for i in range(len(rows)):

                    for j in range(len(s12)):
                        if rows[i][s12[j]]==None:
                            fi.append("нет")
                        else:
                            fi.append(rows[i][s12[j]])
                    print(fi)
                    f.append(fi)
                    fi=[]
                set.column("#0", width=0, stretch=NO)
                set.heading("#0", text="", anchor=tk.N)
                for i in range(len(s12)):
                    k=s12[i]
                    k1=int(set.winfo_width()/len(s12))
                    set.column(f'{s12[i]}', anchor=tk.N,width=k1+1)
                    set.heading(f'{s12[i]}', text=f'{k}', anchor=tk.N)
            except Exception as ex:
                print("Connection refused")
                print(ex)
            print(f)
            for i in range(len(f)):
                set.insert(parent='',index='end',iid=i,text='',values=(f[i]))
            tablname.delete(0,END)
            globals()['collumn' + str(n)].delete(0,END)
            collumnfiltr.delete(0,END)
            collumnfiltr.config(state="normal")
            s12=[]
    except Exception as ex:
        print("Connection refused")
        print(ex)

# --------------------------Создание 1 вкладки------------------------------
# tab1 = ttk.Frame(tab_control)
def deletetab():
    print(tab_control.winfo_children())
    for i in range(1,len(tab_control.winfo_children())):
        print(tab_control.winfo_children()[i])
        tab_control.winfo_children()[i].destroy()
        print(len(tab_control.winfo_children()))
        if len(tab_control.winfo_children()) != 1:
            deletetab()
n=0
def toggle_password():
    global our_button,id_button1,n
    if parol.cget('show') == '':
        parol.config(show='*')
        our_button=PhotoImage(file="eye1.png")
        our_button = our_button.subsample(2, 2)
    else:
        parol.config(show='')
        our_button=PhotoImage(file="eye2.png")
        our_button = our_button.subsample(2, 2)
    id_button1 = Button(tab1, image=our_button, bd=0,bg="white", command=toggle_password)
    id_button1.place(relx=0.58, rely=0.5,anchor=CENTER)



class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder=None):
        super().__init__(master)

        if placeholder is not None:
            self.placeholder = placeholder
            self.placeholder_color = 'grey'
            self.default_fg_color = self['fg']
            self.configure(font=('Helvetica', '15'))
            self.bind("<FocusIn>", self.focus_in)
            self.bind("<FocusOut>", self.focus_out)

            self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()

frame_style=ttk.Style()
frame_style.configure('TFrame',background='#1D334A')
tab1 = ttk.Frame(tab_control, style='Frame1.TFrame')
tab_control.add(tab1, text='начальная страница')
tab_control.pack(expand=0, fill='both')
login=EntryWithPlaceholder(tab1, 'логин')
login.place(relx=0.5, rely=0.4,anchor=CENTER, relheight=0.05, relwidth=0.18)
parol=Entry(tab1, textvariable=message3,font=('Helvetica', '15'))
parol.place(relx=0.5, rely=0.5,anchor=CENTER, relheight=0.05, relwidth=0.18)
butt = Button(tab1, text='войти', background='#f4ead0', command=button1Callback)
butt.place(relx=0.5, rely=0.6,anchor=CENTER, relheight=0.05, relwidth=0.1)

our_button = PhotoImage(file="eye1.png")
our_button = our_button.subsample(2, 2)
# id_img1 = canvas.create_image(130,100, anchor="nw", image=our_button)
# Button(tk, image=our_button, highlightthickness=0, bd=0, command=lambda: print("Clicked!")).place(x=130, y=100)
#Button(tk, image=our_button, highlightthickness=0, bd=0, command=bg_color_red).place(x=130, y=100)

parol.config(show='*')
id_button1 = Button(tab1, image=our_button, highlightthickness=0, bd=0,bg="white", command=toggle_password)
id_button1.place(relx=0.58, rely=0.5,anchor=CENTER)


tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='начальная страница3')
tab_control.pack(expand=1, fill='both')
deletetab()


# --------------------------вывод информации-------------------------------



# button = ttk.Button(tab1,text='сменить аккаунт', command=deletetab)
# button.place(x=0,y=0)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()

