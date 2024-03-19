import mysql.connector
from tkinter import *
from tkinter import ttk
import pandas as pd


main = Tk()
main.title('Управление базой данных')
main.geometry('700x500')

def start_window1():
    root = Tk()
    root.title('Таблица Механиков')
    root.geometry('1000x500')
    #add some style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",background = "#D3D3D3", foreground = "black", rowheight = 25, fieldbackground= "#D3D3D3")
    #Change selected color
    style.map("Treeview", background = [('selected',"#347083")])
    #Create treeview frame
    tree_frame = Frame(root)
    tree_frame.pack(pady = 10)
    #Create treeview scroll
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    #Create treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand = tree_scroll.set, selectmode = "extended")
    my_tree.pack()
    # Configure scrollbar
    tree_scroll.config(command=my_tree.yview)
    #Define column
    my_tree['columns'] = ("Id_mechanic","Id_service","Surname","Speciality","Salary")
    # Format our columns
    my_tree.column("#0", width = 0, stretch = NO)
    my_tree.column("Id_mechanic", width = 140, anchor = CENTER)
    my_tree.column("Id_service", width = 140, anchor = CENTER)
    my_tree.column("Surname", width = 100, anchor = W)
    my_tree.column("Speciality", width = 140, anchor = W)
    my_tree.column("Salary", width = 140, anchor = CENTER)


    #Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Id_mechanic", text="Id_mechanic", anchor=CENTER)
    my_tree.heading("Id_service", text="Id_service", anchor=CENTER)
    my_tree.heading("Surname", text="Surname", anchor=W)
    my_tree.heading("Speciality", text="Speciality", anchor=W)
    my_tree.heading("Salary", text="Salary", anchor=CENTER)



    #Create Striped Row Tags
    my_tree.tag_configure('oddrow',background="white")
    my_tree.tag_configure('evenrow',background="lightblue")
    #Add our data

    #add entry box
    data_frame = LabelFrame(root, text="Record")
    data_frame.pack(fill = "x", expand = "yes", padx=20)

    idm_label = Label(data_frame, text="Id_mechanic")
    idm_label.grid(row=0,column = 0, padx = 10, pady = 10)
    idm_entry = Entry(data_frame)
    idm_entry.grid(row=0,column = 1, padx = 10, pady = 10)

    ids_label = Label(data_frame, text="Id_Service")
    ids_label.grid(row=0,column = 2, padx = 10, pady = 10)
    ids_entry = Entry(data_frame)
    ids_entry.grid(row=0,column = 3, padx = 10, pady = 10)

    sr_label = Label(data_frame, text="Surname")
    sr_label.grid(row=0,column = 4, padx = 10, pady = 10)
    sr_entry = Entry(data_frame)
    sr_entry.grid(row=0,column = 5, padx = 10, pady = 10)

    spec_label = Label(data_frame, text="Speciality")
    spec_label.grid(row=1,column = 0, padx = 10, pady = 10)
    spec_entry = Entry(data_frame)
    spec_entry.grid(row=1,column = 1, padx = 10, pady = 10)

    salary_label = Label(data_frame, text="Salary")
    salary_label.grid(row=1,column = 2, padx = 10, pady = 10)
    salary_entry = Entry(data_frame)
    salary_entry.grid(row=1,column = 3, padx = 10, pady = 10)

    def query_database():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mechanic ")
        records = cursor.fetchall()
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            count +=1
            
    # Move Row up
    def up():
        rows = my_tree.selection()
        for row in rows:
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)
    #Move Row down
    def down():
        rows = my_tree.selection()
        for row in reversed(rows):
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)
    # Remove one
    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        cursor.execute("Delete FROM mechanic where id_mechanic = %s and id_service = %s and surname = %s and specialty =  %s and salary = %s ",(idm_entry.get(),ids_entry.get(),sr_entry.get(),spec_entry.get(),salary_entry.get()))
        conn.commit()
        conn.close

    # Remove many
    def remove_many():
        x = my_tree.selection()
        for record in x:
            my_tree.delete(record)
    # Remove all
    def remove_all():
        for record in my_tree.get_children():
            my_tree.delete(record)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        # Update record
        #cursor.execute("Delete FROM mechanic ") Опасно
        #conn.commit()
        conn.close
        
    # Clear entries
    def clear_entries():
        idm_entry.delete(0,END)
        ids_entry.delete(0,END)
        sr_entry.delete(0,END)
        spec_entry.delete(0,END)
        salary_entry.delete(0,END)
      
    #Select function
    def select_record(e):
        idm_entry.delete(0,END)
        ids_entry.delete(0,END)
        sr_entry.delete(0,END)
        spec_entry.delete(0,END)
        salary_entry.delete(0,END)
        
        #Grab record number
        selected = my_tree.focus()
        #Grab record values
        values = my_tree.item(selected, 'values')
        #Output entry boxes
        idm_entry.insert(0,values[0])
        ids_entry.insert(0,values[1])
        sr_entry.insert(0,values[2])
        spec_entry.insert(0,values[3])
        salary_entry.insert(0,values[4])
        
    # Update
    def update_record():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        my_tree.item(selected, text="", values=(idm_entry.get(),ids_entry.get(),sr_entry.get(),spec_entry.get(),salary_entry.get(),))
        cursor.execute("Update mechanic set id_service = %s, surname = %s, specialty = %s, salary = %s where id_mechanic = %s", (ids_entry.get(),sr_entry.get(),spec_entry.get(),salary_entry.get(),idm_entry.get()))
        conn.commit()
        conn.close
        idm_entry.delete(0,END)
        ids_entry.delete(0,END)
        sr_entry.delete(0,END)
        spec_entry.delete(0,END)
        salary_entry.delete(0,END)
        
    def add():
        my_tree.insert("","end", values = (idm_entry.get(),ids_entry.get(),sr_entry.get(),spec_entry.get(),salary_entry.get()))
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        # Update record
        cursor.execute("Insert into carservice.mechanic values ( %s,  %s,  %s,  %s , %s)", (idm_entry.get(),ids_entry.get(),sr_entry.get(),spec_entry.get(),salary_entry.get()))
        #sql_update_query = "Update mechanic set "
        conn.commit()
        conn.close
    def write_to_csv():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mechanic ")
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        cols = ['Номер механика','Номер сервиса','Фамилия','Специальность','Зарплата']
        df.to_excel('D:/Проекты/mechanic.xlsx',engine='xlsxwriter',header = cols)
        
    #add buttons
    button_frame = LabelFrame(root,text="commands")
    button_frame.pack(fill= "x", expand = "yes", padx = 20)

    update_button = Button(button_frame, text = "Обновить запись", command = update_record)
    update_button.grid(row=0,column = 0, padx = 10, pady = 10)

    add_button = Button(button_frame, text = "Добавить запись", command = add)
    add_button.grid(row=0,column = 1, padx = 10, pady = 10)

    remove_all_button = Button(button_frame, text = "Удалить все записи", command = remove_all)
    remove_all_button.grid(row=0,column = 2, padx = 10, pady = 10)

    remove_one_button = Button(button_frame, text = "Удалить выбранную", command = remove_one)
    remove_one_button.grid(row=0,column = 3, padx = 10, pady = 10)

    move_up_button = Button(button_frame, text = "Вверх", command = up)
    move_up_button.grid(row=0,column = 4, padx = 10, pady = 10)

    move_down_button = Button(button_frame, text = "Вниз", command = down)
    move_down_button.grid(row=0,column = 5, padx = 10, pady = 10)

    select_record_button = Button(button_frame, text = "Очистить поля",command = clear_entries)
    select_record_button.grid(row=0,column = 6, padx = 10, pady = 10)
    
    save_button = Button(button_frame, text = "Сохранить в Excel", command = write_to_csv)
    save_button.grid(row=0,column = 7, padx = 10, pady = 10)
    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)

    query_database()

    root.mainloop
######################################################################################################  
def start_window2():
    root = Tk()
    root.title('Таблица клиентов')
    root.geometry('1000x500')
    #add some style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",background = "#D3D3D3", foreground = "black", rowheight = 25, fieldbackground= "#D3D3D3")
    #Change selected color
    style.map("Treeview", background = [('selected',"#347083")])
    #Create treeview frame
    tree_frame = Frame(root)
    tree_frame.pack(pady = 10)
    #Create treeview scroll
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    #Create treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand = tree_scroll.set, selectmode = "extended")
    my_tree.pack()
    # Configure scrollbar
    tree_scroll.config(command=my_tree.yview)
    #Define column
    my_tree['columns'] = ("Id_clients","Full_name","Telephone","Email")
    # Format our columns
    my_tree.column("#0", width = 0, stretch = NO)
    my_tree.column("Id_clients", width = 140, anchor = CENTER)
    my_tree.column("Full_name", width = 250, anchor = CENTER)
    my_tree.column("Telephone", width = 100, anchor = W)
    my_tree.column("Email", width = 140, anchor = W)
    #Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Id_clients", text="Id_clients", anchor=CENTER)
    my_tree.heading("Full_name", text="Full_name", anchor=CENTER)
    my_tree.heading("Telephone", text="Telephone", anchor=W)
    my_tree.heading("Email", text="Email", anchor=W)
    #Create Striped Row Tags
    my_tree.tag_configure('oddrow',background="white")
    my_tree.tag_configure('evenrow',background="lightblue")
    #add entry box
    data_frame = LabelFrame(root, text="Record")
    data_frame.pack(fill = "x", expand = "yes", padx=30)

    idc_label = Label(data_frame, text="Id clients")
    idc_label.grid(row=0,column = 0, padx = 10, pady = 10)
    idc_entry = Entry(data_frame)
    idc_entry.grid(row=0,column = 1, padx = 10, pady = 10)

    full_label = Label(data_frame, text="Full name")
    full_label.grid(row=0,column = 2, padx = 10, pady = 10)
    full_entry = Entry(data_frame)
    full_entry.grid(row=0,column = 3, padx = 10, pady = 10)

    telep_label = Label(data_frame, text="Telephone")
    telep_label.grid(row=0,column = 4, padx = 10, pady = 10)
    telep_entry = Entry(data_frame)
    telep_entry.grid(row=0,column = 5, padx = 10, pady = 10)

    email_label = Label(data_frame, text="Email")
    email_label.grid(row=1,column = 0, padx = 10, pady = 10)
    email_entry = Entry(data_frame)
    email_entry.grid(row=1,column = 1, padx = 10, pady = 10)

    def query_database():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients ")
        records = cursor.fetchall()
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2], record[3]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count +=1
            
    # Move Row up
    def up():
        rows = my_tree.selection()
        for row in rows:
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)
    #Move Row down
    def down():
        rows = my_tree.selection()
        for row in reversed(rows):
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)
    # Remove one
    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        cursor.execute("Delete FROM clients where id_client = %s and full_name = %s and telephone = %s and email =  %s ",(idc_entry.get(),full_entry.get(),telep_entry.get(),email_entry.get()))
        conn.commit()
        conn.close

    # Remove many
    def remove_many():
        x = my_tree.selection()
        for record in x:
            my_tree.delete(record)
    # Remove all
    def remove_all():
        for record in my_tree.get_children():
            my_tree.delete(record)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        # Update record
        #cursor.execute("Delete FROM clients ") Опасно
        #conn.commit()
        conn.close
        
    # Clear entries
    def clear_entries():
        idc_entry.delete(0,END)
        full_entry.delete(0,END)
        telep_entry.delete(0,END)
        email_entry.delete(0,END)
      
    #Select function
    def select_record(e):
        idc_entry.delete(0,END)
        full_entry.delete(0,END)
        telep_entry.delete(0,END)
        email_entry.delete(0,END)
        
        #Grab record number
        selected = my_tree.focus()
        #Grab record values
        values = my_tree.item(selected, 'values')
        #Output entry boxes
        idc_entry.insert(0,values[0])
        full_entry.insert(0,values[1])
        telep_entry.insert(0,values[2])
        email_entry.insert(0,values[3])
        
    # Update
    def update_record():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        my_tree.item(selected, text="", values=(idc_entry.get(),full_entry.get(),telep_entry.get(),email_entry.get(),))
        cursor.execute("Update clients set full_name = %s, telephone = %s, email = %s where id_client = %s", (full_entry.get(),telep_entry.get(),email_entry.get(),idc_entry.get()))
        conn.commit()
        conn.close
        idc_entry.delete(0,END)
        full_entry.delete(0,END)
        telep_entry.delete(0,END)
        email_entry.delete(0,END)
        
    def add():
        my_tree.insert("","end", values = (idc_entry.get(),full_entry.get(),telep_entry.get(),email_entry.get()))
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        # Update record
        cursor.execute("Insert into carservice.clients values ( %s,  %s,  %s,  %s)", (idc_entry.get(),full_entry.get(),telep_entry.get(),email_entry.get()))
        #sql_update_query = "Update mechanic set "
        conn.commit()
        conn.close
        
    def write_to_csv():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients ")
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        cols = ['Номер клиента','ФИО','telephone','email']
        df.to_excel('D:/Проекты/clients.xlsx',engine='xlsxwriter',header = cols)    
        
    #add buttons
    button_frame = LabelFrame(root,text="commands")
    button_frame.pack(fill= "x", expand = "yes", padx = 20)

    update_button = Button(button_frame, text = "update record", command = update_record)
    update_button.grid(row=0,column = 0, padx = 10, pady = 10)

    add_button = Button(button_frame, text = "add record", command = add)
    add_button.grid(row=0,column = 1, padx = 10, pady = 10)

    remove_all_button = Button(button_frame, text = "Remove All records", command = remove_all)
    remove_all_button.grid(row=0,column = 2, padx = 10, pady = 10)

    remove_one_button = Button(button_frame, text = "Remove One selected", command = remove_one)
    remove_one_button.grid(row=0,column = 3, padx = 10, pady = 10)

    move_up_button = Button(button_frame, text = "Move up", command = up)
    move_up_button.grid(row=0,column = 4, padx = 10, pady = 10)

    move_down_button = Button(button_frame, text = "Move down", command = down)
    move_down_button.grid(row=0,column = 5, padx = 10, pady = 10)

    select_record_button = Button(button_frame, text = "Clear Entry Button",command = clear_entries)
    select_record_button.grid(row=0,column = 6, padx = 10, pady = 10)
    
    save_button = Button(button_frame, text = "Save to excel", command = write_to_csv)
    save_button.grid(row=0,column = 7, padx = 10, pady = 10)

    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)

    query_database()

    root.mainloop
######################################################################################################
def start_window3():
    root = Tk()
    root.title('Таблица Сервисов')
    root.geometry('1000x500')
    #add some style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",background = "#D3D3D3", foreground = "black", rowheight = 25, fieldbackground= "#D3D3D3")
    #Change selected color
    style.map("Treeview", background = [('selected',"#347083")])
    #Create treeview frame
    tree_frame = Frame(root)
    tree_frame.pack(pady = 10)
    #Create treeview scroll
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    #Create treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand = tree_scroll.set, selectmode = "extended")
    my_tree.pack()
    # Configure scrollbar
    tree_scroll.config(command=my_tree.yview)
    #Define column
    my_tree['columns'] = ("Id_service","City","Adress")
    # Format our columns
    my_tree.column("#0", width = 0, stretch = NO)
    my_tree.column("Id_service", width = 100, anchor = CENTER)
    my_tree.column("City", width = 140, anchor = CENTER)
    my_tree.column("Adress", width = 200, anchor = W)

    #Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Id_service", text="Id_service", anchor=CENTER)
    my_tree.heading("City", text="City", anchor=CENTER)
    my_tree.heading("Adress", text="Adress", anchor=W)
    #Create Striped Row Tags
    my_tree.tag_configure('oddrow',background="white")
    my_tree.tag_configure('evenrow',background="lightblue")
    #add entry box
    data_frame = LabelFrame(root, text="Record")
    data_frame.pack(fill = "x", expand = "yes", padx=20)

    idser_label = Label(data_frame, text="Id_service")
    idser_label.grid(row=0,column = 0, padx = 10, pady = 10)
    idser_entry = Entry(data_frame)
    idser_entry.grid(row=0,column = 1, padx = 10, pady = 10)

    city_label = Label(data_frame, text="City")
    city_label.grid(row=0,column = 2, padx = 10, pady = 10)
    city_entry = Entry(data_frame)
    city_entry.grid(row=0,column = 3, padx = 10, pady = 10)

    adress_label = Label(data_frame, text="Adress")
    adress_label.grid(row=0,column = 4, padx = 10, pady = 10)
    adress_entry = Entry(data_frame)
    adress_entry.grid(row=0,column = 5, padx = 10, pady = 10)

    def query_database():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service ")
        records = cursor.fetchall()
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2]), tags=('oddrow',))
            count +=1
            
    # Move Row up
    def up():
        rows = my_tree.selection()
        for row in rows:
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)
    #Move Row down
    def down():
        rows = my_tree.selection()
        for row in reversed(rows):
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)
    # Remove one
    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        cursor.execute("Delete FROM service where id_service = %s and city = %s and adress = %s ",(idser_entry.get(),city_entry.get(),adress_entry.get()))
        conn.commit()
        conn.close

    # Remove many
    def remove_many():
        x = my_tree.selection()
        for record in x:
            my_tree.delete(record)
    # Remove all
    def remove_all():
        for record in my_tree.get_children():
            my_tree.delete(record)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #cursor.execute("Delete FROM clients ") Опасно
        #conn.commit()
        conn.close
        
    # Clear entries
    def clear_entries():
        idser_entry.delete(0,END)
        city_entry.delete(0,END)
        adress_entry.delete(0,END)
        
      
    #Select function
    def select_record(e):
        idser_entry.delete(0,END)
        city_entry.delete(0,END)
        adress_entry.delete(0,END)
        
        #Grab record number
        selected = my_tree.focus()
        #Grab record values
        values = my_tree.item(selected, 'values')
        #Output entry boxes
        idser_entry.insert(0,values[0])
        city_entry.insert(0,values[1])
        adress_entry.insert(0,values[2])
        
        
    # Update
    def update_record():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        my_tree.item(selected, text="", values=(idser_entry.get(),city_entry.get(),adress_entry.get(),))
        cursor.execute("Update service set city = %s, adress = %s where id_service = %s", (city_entry.get(),adress_entry.get(),idser_entry.get()))
        conn.commit()
        conn.close
        idser_entry.delete(0,END)
        city_entry.delete(0,END)
        adress_entry.delete(0,END)
        
    def add():
        my_tree.insert("","end", values = (idser_entry.get(),city_entry.get(),adress_entry.get()))
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        # Update record
        cursor.execute("Insert into carservice.service values ( %s,  %s,  %s)", (idser_entry.get(),city_entry.get(),adress_entry.get()))
        #sql_update_query = "Update mechanic set "
        conn.commit()
        conn.close
    
    def write_to_csv():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service ")
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        cols = ['Номер сервиса','Город','Адрес']
        df.to_excel('D:/Проекты/service.xlsx',engine='xlsxwriter',header = cols)
        
        
    #add buttons
    button_frame = LabelFrame(root,text="commands")
    button_frame.pack(fill= "x", expand = "yes", padx = 20)

    update_button = Button(button_frame, text = "update record", command = update_record)
    update_button.grid(row=0,column = 0, padx = 10, pady = 10)

    add_button = Button(button_frame, text = "add record", command = add)
    add_button.grid(row=0,column = 1, padx = 10, pady = 10)

    remove_all_button = Button(button_frame, text = "Remove All records", command = remove_all)
    remove_all_button.grid(row=0,column = 2, padx = 10, pady = 10)

    remove_one_button = Button(button_frame, text = "Remove One selected", command = remove_one)
    remove_one_button.grid(row=0,column = 3, padx = 10, pady = 10)

    move_up_button = Button(button_frame, text = "Move up", command = up)
    move_up_button.grid(row=0,column = 4, padx = 10, pady = 10)

    move_down_button = Button(button_frame, text = "Move down", command = down)
    move_down_button.grid(row=0,column = 5, padx = 10, pady = 10)

    select_record_button = Button(button_frame, text = "Clear Entry Button",command = clear_entries)
    select_record_button.grid(row=0,column = 6, padx = 10, pady = 10)
    
    save_button = Button(button_frame, text = "Save to excel", command = write_to_csv)
    save_button.grid(row=0,column = 7, padx = 10, pady = 10)

    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)

    query_database()

    root.mainloop
######################################################################################################
def start_window4():
    root = Tk()
    root.title('Таблица Операторов')
    root.geometry('1000x500')
    #add some style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",background = "#D3D3D3", foreground = "black", rowheight = 25, fieldbackground= "#D3D3D3")
    #Change selected color
    style.map("Treeview", background = [('selected',"#347083")])
    #Create treeview frame
    tree_frame = Frame(root)
    tree_frame.pack(pady = 10)
    #Create treeview scroll
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    #Create treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand = tree_scroll.set, selectmode = "extended")
    my_tree.pack()
    # Configure scrollbar
    tree_scroll.config(command=my_tree.yview)
    #Define column
    my_tree['columns'] = ("Id_operator","Surname","Salary")
    # Format our columns
    my_tree.column("#0", width = 0, stretch = NO)
    my_tree.column("Id_operator", width = 140, anchor = CENTER)
    my_tree.column("Surname", width = 100, anchor = W)
    my_tree.column("Salary", width = 140, anchor = CENTER)


    #Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Id_operator", text="Id_operator", anchor=CENTER)
    my_tree.heading("Surname", text="Surname", anchor=W)
    my_tree.heading("Salary", text="Salary", anchor=CENTER)



    #Create Striped Row Tags
    my_tree.tag_configure('oddrow',background="white")
    my_tree.tag_configure('evenrow',background="lightblue")
    #Add our data

    #add entry box
    data_frame = LabelFrame(root, text="Record")
    data_frame.pack(fill = "x", expand = "yes", padx=20)

    idoper_label = Label(data_frame, text="Id_operator")
    idoper_label.grid(row=0,column = 0, padx = 10, pady = 10)
    idoper_entry = Entry(data_frame)
    idoper_entry.grid(row=0,column = 1, padx = 10, pady = 10)

    sr_label = Label(data_frame, text="Surname")
    sr_label.grid(row=0,column = 2, padx = 10, pady = 10)
    sr_entry = Entry(data_frame)
    sr_entry.grid(row=0,column = 3, padx = 10, pady = 10)

    salary_label = Label(data_frame, text="Salary")
    salary_label.grid(row=0,column = 4, padx = 10, pady = 10)
    salary_entry = Entry(data_frame)
    salary_entry.grid(row=0,column = 5, padx = 10, pady = 10)

    def query_database():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operator ")
        records = cursor.fetchall()
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2]), tags=('oddrow',))
            count +=1
            
    # Move Row up
    def up():
        rows = my_tree.selection()
        for row in rows:
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)
    #Move Row down
    def down():
        rows = my_tree.selection()
        for row in reversed(rows):
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)
    # Remove one
    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        cursor.execute("Delete FROM operator where id_operator = %s and surname = %s and salary = %s ",(idoper_entry.get(),sr_entry.get(),salary_entry.get()))
        conn.commit()
        conn.close

    # Remove many
    def remove_many():
        x = my_tree.selection()
        for record in x:
            my_tree.delete(record)
    # Remove all
    def remove_all():
        for record in my_tree.get_children():
            my_tree.delete(record)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        # Update record
        #cursor.execute("Delete FROM mechanic ") Опасно
        #conn.commit()
        conn.close
        
    # Clear entries
    def clear_entries():
        idoper_entry.delete(0,END)
        sr_entry.delete(0,END)
        salary_entry.delete(0,END)
      
    #Select function
    def select_record(e):
        idoper_entry.delete(0,END)
        sr_entry.delete(0,END)
        salary_entry.delete(0,END)
        
        #Grab record number
        selected = my_tree.focus()
        #Grab record values
        values = my_tree.item(selected, 'values')
        #Output entry boxes
        idoper_entry.insert(0,values[0])
        sr_entry.insert(0,values[1])
        salary_entry.insert(0,values[2])
        
    # Update
    def update_record():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        my_tree.item(selected, text="", values=(idoper_entry.get(),sr_entry.get(),salary_entry.get(),))
        cursor.execute("Update operator set surname = %s, salary = %s where id_operator = %s", (sr_entry.get(),salary_entry.get(),idoper_entry.get()))
        conn.commit()
        conn.close
        idoper_entry.delete(0,END)
        sr_entry.delete(0,END)
        salary_entry.delete(0,END)
        
    def add():
        my_tree.insert("","end", values = (idoper_entry.get(),sr_entry.get(),salary_entry.get()))
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        # Update record
        cursor.execute("Insert into carservice.operator values ( %s,  %s,  %s)", (idoper_entry.get(),sr_entry.get(),salary_entry.get()))
        #sql_update_query = "Update mechanic set "
        conn.commit()
        conn.close
    def write_to_csv():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operator ")
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        cols = ['Номер оператора','Фамилия','Зарплата']
        df.to_excel('D:/Проекты/operator1.xlsx',engine='xlsxwriter',header = cols)
        
    #add buttons
    button_frame = LabelFrame(root,text="commands")
    button_frame.pack(fill= "x", expand = "yes", padx = 20)

    update_button = Button(button_frame, text = "update record", command = update_record)
    update_button.grid(row=0,column = 0, padx = 10, pady = 10)

    add_button = Button(button_frame, text = "add record", command = add)
    add_button.grid(row=0,column = 1, padx = 10, pady = 10)

    remove_all_button = Button(button_frame, text = "Remove All records", command = remove_all)
    remove_all_button.grid(row=0,column = 2, padx = 10, pady = 10)

    remove_one_button = Button(button_frame, text = "Remove One selected", command = remove_one)
    remove_one_button.grid(row=0,column = 3, padx = 10, pady = 10)

    move_up_button = Button(button_frame, text = "Move up", command = up)
    move_up_button.grid(row=0,column = 4, padx = 10, pady = 10)

    move_down_button = Button(button_frame, text = "Move down", command = down)
    move_down_button.grid(row=0,column = 5, padx = 10, pady = 10)

    select_record_button = Button(button_frame, text = "Clear Entry Button",command = clear_entries)
    select_record_button.grid(row=0,column = 6, padx = 10, pady = 10)
    
    save_button = Button(button_frame, text = "Save to excel", command = write_to_csv)
    save_button.grid(row=0,column = 7, padx = 10, pady = 10)
    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)

    query_database()

    root.mainloop
#############################################################################################################

def start_window5():
    root = Tk()
    root.title('Таблица Запчастей')
    root.geometry('1000x500')
    #add some style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",background = "#D3D3D3", foreground = "black", rowheight = 25, fieldbackground= "#D3D3D3")
    #Change selected color
    style.map("Treeview", background = [('selected',"#347083")])
    #Create treeview frame
    tree_frame = Frame(root)
    tree_frame.pack(pady = 10)
    #Create treeview scroll
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    #Create treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand = tree_scroll.set, selectmode = "extended")
    my_tree.pack()
    # Configure scrollbar
    tree_scroll.config(command=my_tree.yview)
    #Define column
    my_tree['columns'] = ("Id_spare","Id_service","Price",'Name','Manufacturer','Madein')
    # Format our columns
    my_tree.column("#0", width = 0, stretch = NO)
    my_tree.column("Id_spare", width = 100, anchor = CENTER)
    my_tree.column("Id_service", width = 100, anchor = CENTER)
    my_tree.column("Price", width = 100, anchor = CENTER)
    my_tree.column("Name", width = 160, anchor = W)
    my_tree.column("Manufacturer", width = 140, anchor = W)
    my_tree.column("Madein", width = 140, anchor = W)
    #Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Id_spare", text="Id_spare", anchor=CENTER)
    my_tree.heading("Id_service", text="Id_service", anchor=CENTER)
    my_tree.heading("Price", text="Price", anchor=CENTER)
    my_tree.heading("Name", text="Name", anchor=W)
    my_tree.heading("Manufacturer", text="Manufacturer", anchor=W)
    my_tree.heading("Madein", text="Madein", anchor=W)
    #Create Striped Row Tags
    my_tree.tag_configure('oddrow',background="white")
    my_tree.tag_configure('evenrow',background="lightblue")
    #add entry box
    data_frame = LabelFrame(root, text="Record")
    data_frame.pack(fill = "x", expand = "yes", padx=20)

    idsp_label = Label(data_frame, text="Id_spare")
    idsp_label.grid(row=0,column = 0, padx = 10, pady = 10)
    idsp_entry = Entry(data_frame)
    idsp_entry.grid(row=0,column = 1, padx = 10, pady = 10)

    idser_label = Label(data_frame, text="Id_service")
    idser_label.grid(row=0,column = 2, padx = 10, pady = 10)
    idser_entry = Entry(data_frame)
    idser_entry.grid(row=0,column = 3, padx = 10, pady = 10)

    price_label = Label(data_frame, text="Price")
    price_label.grid(row=0,column = 4, padx = 10, pady = 10)
    price_entry = Entry(data_frame)
    price_entry.grid(row=0,column = 5, padx = 10, pady = 10)
    
    name_label = Label(data_frame, text="Name")
    name_label.grid(row=0,column = 6, padx = 10, pady = 10)
    name_entry = Entry(data_frame)
    name_entry.grid(row=0,column = 7, padx = 10, pady = 10)
    
    manuf_label = Label(data_frame, text="Manufacturer")
    manuf_label.grid(row=1,column = 0, padx = 10, pady = 10)
    manuf_entry = Entry(data_frame)
    manuf_entry.grid(row=1,column = 1, padx = 10, pady = 10)
    
    made_label = Label(data_frame, text="Madein")
    made_label.grid(row=1,column = 2, padx = 10, pady = 10)
    made_entry = Entry(data_frame)
    made_entry.grid(row=1,column = 3, padx = 10, pady = 10)

    def query_database():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM spares ")
        records = cursor.fetchall()
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))
            count +=1
            
    # Move Row up
    def up():
        rows = my_tree.selection()
        for row in rows:
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)
    #Move Row down
    def down():
        rows = my_tree.selection()
        for row in reversed(rows):
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)
    # Remove one
    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        cursor.execute("Delete FROM spares where id_spare = %s and id_service = %s and price = %s and name = %s and manufacturer = %s and madein = %s ",(idsp_entry.get(),idser_entry.get(),price_entry.get(),name_entry.get(),manuf_entry.get(),made_entry.get()))
        conn.commit()
        conn.close

    # Remove many
    def remove_many():
        x = my_tree.selection()
        for record in x:
            my_tree.delete(record)
    # Remove all
    def remove_all():
        for record in my_tree.get_children():
            my_tree.delete(record)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #cursor.execute("Delete FROM operator ") Опасно
        #conn.commit()
        conn.close
        
    # Clear entries
    def clear_entries():
        idsp_entry.delete(0,END)
        idser_entry.delete(0,END)
        price_entry.delete(0,END)
        name_entry.delete(0,END)
        manuf_entry.delete(0,END)
        made_entry.delete(0,END)
        
      
    #Select function
    def select_record(e):
        idsp_entry.delete(0,END)
        idser_entry.delete(0,END)
        price_entry.delete(0,END)
        name_entry.delete(0,END)
        manuf_entry.delete(0,END)
        made_entry.delete(0,END)
        
        #Grab record number
        selected = my_tree.focus()
        #Grab record values
        values = my_tree.item(selected, 'values')
        #Output entry boxes
        idsp_entry.insert(0,values[0])
        idser_entry.insert(0,values[1])
        price_entry.insert(0,values[2])
        name_entry.insert(0,values[3])
        manuf_entry.insert(0,values[4])
        made_entry.insert(0,values[5])
        
        
    # Update
    def update_record():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        my_tree.item(selected, text="", values=(idsp_entry.get(),idser_entry.get(),price_entry.get(),name_entry.get(),manuf_entry.get(),made_entry.get(),))
        cursor.execute("Update spares set id_service = %s, price = %s, name = %s, manufacturer = %s, madein = %s where id_spare = %s", (idser_entry.get(),price_entry.get(),name_entry.get(),manuf_entry.get(),made_entry.get(), idsp_entry.get()))
        conn.commit()
        conn.close
        idsp_entry.delete(0,END)
        idser_entry.delete(0,END)
        price_entry.delete(0,END)
        name_entry.delete(0,END)
        manuf_entry.delete(0,END)
        made_entry.delete(0,END)
        
    def add():
        my_tree.insert("","end", values = (idsp_entry.get(),idser_entry.get(),price_entry.get(),name_entry.get(),manuf_entry.get(),made_entry.get()))
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        # Update record
        cursor.execute("Insert into carservice.spares values ( %s,  %s,  %s, %s, %s, %s)", (idsp_entry.get(),idser_entry.get(),price_entry.get(),name_entry.get(),manuf_entry.get(),made_entry.get()))
        #sql_update_query = "Update mechanic set "
        conn.commit()
        conn.close
    
    def write_to_csv():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM spares ")
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        cols = ['Номер Запчасти','Номер Сервиса','Цена', 'Название', 'Производитель', 'Страна']
        df.to_excel('D:/Проекты/spares.xlsx',engine='xlsxwriter',header = cols)      
        
        
    #add buttons
    button_frame = LabelFrame(root,text="commands")
    button_frame.pack(fill= "x", expand = "yes", padx = 20)

    update_button = Button(button_frame, text = "update record", command = update_record)
    update_button.grid(row=0,column = 0, padx = 10, pady = 10)

    add_button = Button(button_frame, text = "add record", command = add)
    add_button.grid(row=0,column = 1, padx = 10, pady = 10)

    remove_all_button = Button(button_frame, text = "Remove All records", command = remove_all)
    remove_all_button.grid(row=0,column = 2, padx = 10, pady = 10)

    remove_one_button = Button(button_frame, text = "Remove One selected", command = remove_one)
    remove_one_button.grid(row=0,column = 3, padx = 10, pady = 10)

    move_up_button = Button(button_frame, text = "Move up", command = up)
    move_up_button.grid(row=0,column = 4, padx = 10, pady = 10)

    move_down_button = Button(button_frame, text = "Move down", command = down)
    move_down_button.grid(row=0,column = 5, padx = 10, pady = 10)

    select_record_button = Button(button_frame, text = "Clear Entry Button",command = clear_entries)
    select_record_button.grid(row=0,column = 6, padx = 10, pady = 10)
    
    save_button = Button(button_frame, text = "Save to excel", command = write_to_csv)
    save_button.grid(row=0,column = 7, padx = 10, pady = 10)

    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)

    query_database()

    root.mainloop

##################################################################################################
def start_window6():
    root = Tk()
    root.title('Таблица Автомобилей на ремонте')
    root.geometry('1000x720')
    #add some style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview", background = "#D3D3D3", foreground = "black", rowheight = 25, fieldbackground= "#D3D3D3")
    #Change selected color
    style.map("Treeview", background = [('selected',"#347083")])
    #Create treeview frame
    tree_frame = Frame(root)
    tree_frame.pack(pady = 10)
    #Create treeview scroll
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    #Create treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand = tree_scroll.set, selectmode = "extended")
    my_tree.pack()
    # Configure scrollbar
    tree_scroll.config(command=my_tree.yview)
    #Define column
    my_tree['columns'] = ("Id_auto","Id_client","Id_service",'Brand','Car_Numbers','Date_receipt','Expirition_date','Id_spare','Cost_work', 'Id_mechanic', 'Id_operator' )
    # Format our columns
    my_tree.column("#0", width = 0, stretch = NO)
    my_tree.column("Id_auto", width = 60, anchor = CENTER)
    my_tree.column("Id_client", width = 60, anchor = CENTER)
    my_tree.column("Id_service", width = 60, anchor = CENTER)
    my_tree.column("Brand", width = 80, anchor = W)
    my_tree.column("Car_Numbers", width = 80, anchor = CENTER)
    my_tree.column("Date_receipt", width = 80, anchor = CENTER)
    my_tree.column("Expirition_date", width = 80, anchor = CENTER)
    my_tree.column("Id_spare", width = 60, anchor = CENTER)
    my_tree.column("Cost_work", width = 60, anchor = CENTER)
    my_tree.column("Id_mechanic", width = 60, anchor = CENTER)
    my_tree.column("Id_operator", width = 60, anchor = CENTER)
    #Create Headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Id_auto", text="Id_auto", anchor=CENTER)
    my_tree.heading("Id_client", text="Id_client", anchor=CENTER)
    my_tree.heading("Id_service", text="Id_service", anchor=CENTER)
    my_tree.heading("Brand", text="Brand", anchor=W)
    my_tree.heading("Car_Numbers", text="Car_Numbers", anchor=W)
    my_tree.heading("Date_receipt", text="Date_receipt", anchor=CENTER)
    my_tree.heading("Expirition_date", text="Expirition_date", anchor=CENTER)
    my_tree.heading("Id_spare", text="Id_spare", anchor=CENTER)
    my_tree.heading("Cost_work", text="Cost_work", anchor=CENTER)
    my_tree.heading("Id_mechanic", text="Id_mechanic", anchor=CENTER)
    my_tree.heading("Id_operator", text="Id_operator", anchor=CENTER)
    #Create Striped Row Tags
    my_tree.tag_configure('oddrow',background="white")
    my_tree.tag_configure('evenrow',background="lightblue")
    #add entry box
    data_frame = LabelFrame(root, text="Record")
    data_frame.pack(fill = "x", expand = "yes", padx=20)

    auto_label = Label(data_frame, text="Id_auto")
    auto_label.grid(row=0,column = 0, padx = 10, pady = 10)
    auto_entry = Entry(data_frame)
    auto_entry.grid(row=0,column = 1, padx = 10, pady = 10)

    client_label = Label(data_frame, text="Id_client")
    client_label.grid(row=0,column = 2, padx = 10, pady = 10)
    client_entry = Entry(data_frame)
    client_entry.grid(row=0,column = 3, padx = 10, pady = 10)

    service_label = Label(data_frame, text="Id_service")
    service_label.grid(row=0,column = 4, padx = 10, pady = 10)
    service_entry = Entry(data_frame)
    service_entry.grid(row=0,column = 5, padx = 10, pady = 10)
    
    brand_label = Label(data_frame, text="Brand")
    brand_label.grid(row=0,column = 6, padx = 10, pady = 10)
    brand_entry = Entry(data_frame)
    brand_entry.grid(row=0,column = 7, padx = 10, pady = 10)
    
    numb_label = Label(data_frame, text="Car_numbers")
    numb_label.grid(row=1,column = 0, padx = 10, pady = 10)
    numb_entry = Entry(data_frame)
    numb_entry.grid(row=1,column = 1, padx = 10, pady = 10)
    
    dtrec_label = Label(data_frame, text="Date_receipt")
    dtrec_label.grid(row=1,column = 2, padx = 10, pady = 10)
    dtrec_entry = Entry(data_frame)
    dtrec_entry.grid(row=1,column = 3, padx = 10, pady = 10)
    
    exdt_label = Label(data_frame, text="Expirition_date")
    exdt_label.grid(row=1,column = 4, padx = 10, pady = 10)
    exdt_entry = Entry(data_frame)
    exdt_entry.grid(row=1,column = 5, padx = 10, pady = 10)
    
    spare_label = Label(data_frame, text="Id_spare")
    spare_label.grid(row=1,column = 6, padx = 10, pady = 10)
    spare_entry = Entry(data_frame)
    spare_entry.grid(row=1,column = 7, padx = 10, pady = 10)
    
    cost_label = Label(data_frame, text="Cost_work")
    cost_label.grid(row=2,column = 0, padx = 10, pady = 10)
    cost_entry = Entry(data_frame)
    cost_entry.grid(row=2,column = 1, padx = 10, pady = 10)
    
    mech_label = Label(data_frame, text="Id_mechanic")
    mech_label.grid(row=2,column = 2, padx = 10, pady = 10)
    mech_entry = Entry(data_frame)
    mech_entry.grid(row=2,column = 3, padx = 10, pady = 10)
    
    oper_label = Label(data_frame, text="Id_operator")
    oper_label.grid(row=2,column = 4, padx = 10, pady = 10)
    oper_entry = Entry(data_frame)
    oper_entry.grid(row=2,column = 5, padx = 10, pady = 10)

    def query_database():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM autorepair ")
        records = cursor.fetchall()
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9],record[10]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid = count, text ='', values =(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9],record[10]), tags=('oddrow',))
            count +=1
            
    # Move Row up
    def up():
        rows = my_tree.selection()
        for row in rows:
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)
    #Move Row down
    def down():
        rows = my_tree.selection()
        for row in reversed(rows):
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)
    # Remove one
    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        cursor.execute("Delete FROM autorepair where id_auto = %s and id_client = %s and id_service = %s and brand = %s and car_numbers = %s and date_receipt = %s and expiration_date = %s and id_spare = %s and cost_work = %s and id_mechanic = %s and id_operator = %s ",(auto_entry.get(),client_entry.get(),service_entry.get(),brand_entry.get(),numb_entry.get(),dtrec_entry.get(),exdt_entry.get(),spare_entry.get(),cost_entry.get(), mech_entry.get(), oper_entry.get()))
        conn.commit()
        conn.close

    # Remove many
    def remove_many():
        x = my_tree.selection()
        for record in x:
            my_tree.delete(record)
    # Remove all
    def remove_all():
        for record in my_tree.get_children():
            my_tree.delete(record)
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #cursor.execute("Delete FROM operator ") Опасно
        #conn.commit()
        conn.close
        
    # Clear entries
    def clear_entries():
        auto_entry.delete(0,END)
        client_entry.delete(0,END)
        service_entry.delete(0,END)
        brand_entry.delete(0,END)
        numb_entry.delete(0,END)
        dtrec_entry.delete(0,END)
        exdt_entry.delete(0,END)
        spare_entry.delete(0,END)
        cost_entry.delete(0,END)
        mech_entry.delete(0,END)
        oper_entry.delete(0,END)
      
    #Select function
    def select_record(e):
        auto_entry.delete(0,END)
        client_entry.delete(0,END)
        service_entry.delete(0,END)
        brand_entry.delete(0,END)
        numb_entry.delete(0,END)
        dtrec_entry.delete(0,END)
        exdt_entry.delete(0,END)
        spare_entry.delete(0,END)
        cost_entry.delete(0,END)
        mech_entry.delete(0,END)
        oper_entry.delete(0,END)
        
        #Grab record number
        selected = my_tree.focus()
        #Grab record values
        values = my_tree.item(selected, 'values')
        #Output entry boxes
        auto_entry.insert(0,values[0])
        client_entry.insert(0,values[1])
        service_entry.insert(0,values[2])
        brand_entry.insert(0,values[3])
        numb_entry.insert(0,values[4])
        dtrec_entry.insert(0,values[5])
        exdt_entry.insert(0,values[6])
        spare_entry.insert(0,values[7])
        cost_entry.insert(0,values[8])
        mech_entry.insert(0,values[9])
        oper_entry.insert(0,values[10])
        
        
    # Update
    def update_record():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        #Grab record number
        selected = my_tree.focus()
        # Update record
        my_tree.item(selected, text="", values=(auto_entry.get(),client_entry.get(),service_entry.get(),brand_entry.get(),numb_entry.get(),dtrec_entry.get(),exdt_entry.get(),spare_entry.get(),cost_entry.get(), mech_entry.get(), oper_entry.get(),))
        cursor.execute("Update autorepair set id_client = %s, id_service = %s, brand = %s , car_numbers = %s ,date_receipt = %s , expiration_date = %s ,id_spare = %s , cost_work = %s , id_mechanic = %s,  id_operator = %s  where id_auto = %s",(client_entry.get(),service_entry.get(),brand_entry.get(),numb_entry.get(),dtrec_entry.get(),exdt_entry.get(),spare_entry.get(),cost_entry.get(), mech_entry.get(), oper_entry.get(),auto_entry.get()))
        conn.commit()
        conn.close
        auto_entry.delete(0,END)
        client_entry.delete(0,END)
        service_entry.delete(0,END)
        brand_entry.delete(0,END)
        numb_entry.delete(0,END)
        dtrec_entry.delete(0,END)
        exdt_entry.delete(0,END)
        spare_entry.delete(0,END)
        cost_entry.delete(0,END)
        mech_entry.delete(0,END)
        oper_entry.delete(0,END)
        
    def add():
        my_tree.insert("","end", values = (auto_entry.get(),client_entry.get(),service_entry.get(),brand_entry.get(),numb_entry.get(),dtrec_entry.get(),exdt_entry.get(),spare_entry.get(),cost_entry.get(), mech_entry.get(), oper_entry.get()))
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        # Update record
        cursor.execute("Insert into autorepair values ( %s,  %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s)",(auto_entry.get(),client_entry.get(),service_entry.get(),brand_entry.get(),numb_entry.get(),dtrec_entry.get(),exdt_entry.get(),spare_entry.get(),cost_entry.get(), mech_entry.get(), oper_entry.get()))
        #sql_update_query = "Update mechanic set "
        conn.commit()
        conn.close
    
    def write_to_csv():
        conn = mysql.connector.connect(host='127.0.0.1',database='carservice',user='root',password='1234')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM autorepair ")
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        cols = ['Номер авто','Номер клиента','Номер сервиса', 'Бренд', 'Номера машины', 'Дата приема', 'Дата выдачи', 'Номер запчасти', 'Стоимость работ', 'Номер механика', 'Номер оператора' ]
        df.to_excel('D:/Проекты/autorepair.xlsx',engine='xlsxwriter',header = cols)      
        
        
    #add buttons
    button_frame = LabelFrame(root,text="commands")
    button_frame.pack(fill= "x", expand = "yes", padx = 20)

    update_button = Button(button_frame, text = "update record", command = update_record)
    update_button.grid(row=0,column = 0, padx = 10, pady = 10)

    add_button = Button(button_frame, text = "add record", command = add)
    add_button.grid(row=0,column = 1, padx = 10, pady = 10)

    remove_all_button = Button(button_frame, text = "Remove All records", command = remove_all)
    remove_all_button.grid(row=0,column = 2, padx = 10, pady = 10)

    remove_one_button = Button(button_frame, text = "Remove One selected", command = remove_one)
    remove_one_button.grid(row=0,column = 3, padx = 10, pady = 10)

    move_up_button = Button(button_frame, text = "Move up", command = up)
    move_up_button.grid(row=0,column = 4, padx = 10, pady = 10)

    move_down_button = Button(button_frame, text = "Move down", command = down)
    move_down_button.grid(row=0,column = 5, padx = 10, pady = 10)

    select_record_button = Button(button_frame, text = "Clear Entry Button",command = clear_entries)
    select_record_button.grid(row=0,column = 6, padx = 10, pady = 10)
    
    save_button = Button(button_frame, text = "Save to excel", command = write_to_csv)
    save_button.grid(row=0,column = 7, padx = 10, pady = 10)

    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)

    query_database()

    root.mainloop
#########################################################################################################
button_frame = LabelFrame(main,text="Таблицы")
button_frame.pack(fill= "y", expand = "yes", padx = 20)

btn_window1 = Button(button_frame, text = "Механики", command= start_window1)
btn_window1.grid(row=0,column = 1, padx = 10, pady = 10)

btn_window2 = Button(button_frame, text = "Клиенты", command= start_window2)
btn_window2.grid(row=1,column = 1, padx = 10, pady = 10)

btn_window3 = Button(button_frame, text = "Cервисы", command= start_window3)
btn_window3.grid(row=2,column = 1, padx = 10, pady = 10)

btn_window4 = Button(button_frame, text = "Операторы", command= start_window4)
btn_window4.grid(row=3,column = 1, padx = 10, pady = 10)

btn_window5 = Button(button_frame, text = "Запчасти", command= start_window5)
btn_window5.grid(row=4,column = 1, padx = 10, pady = 10)

btn_window6 = Button(button_frame, text = "Машины на ремонте", command= start_window6)
btn_window6.grid(row=5,column = 1, padx = 10, pady = 10)


main.mainloop