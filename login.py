from tkinter import *
from tkinter import ttk, BOTH
from tkinter import messagebox

import cx_Oracle
from datetime import date
#from PIL import ImageTk
import sqlite3
import csv

from tkcalendar import Calendar, DateEntry
 

class MainFrame:

    
    def __init__(self):
        global bank_screen
        root.withdraw()
        bank_screen=Toplevel(root)
        
        bank_screen.title("Qishloq Qurilish Bank")
        bank_screen.geometry("1355x705+0+0", )  
        root.resizable(height = None, width = None) 
       
        #root.config(bg = "red")
        bank_screen.configure(bg='#333333')
        #self.window.attributes('-fullscreen', True)  
        # bank_screen.attributes('-fullscreen',True)
        # bank_screen.fullScreenState = False
        # bank_screen.bind("<F11>", toggleFullScreen)
        # bank_screen.bind("<Escape>", quitFullScreen)
        #bank_screen.overrideredirect(True)
        #bank_screen.overrideredirect(False)
        

        
        bgl=PhotoImage(file="logo_qqb.png")
        # bgl=PhotoImage(file="logo_qqb.png")
        # Label(bank_screen image=bgl, bg = "#fff").place(x=15, y=30, width=520, height = 180,)
        title= Label(bank_screen, text="Qishloq Qurilish Bank",bd=2,relief=GROOVE, bg="#fff", fg="#2a4291", font=("times new roman", 40, "bold"))
        title.pack(side=TOP, fill=X)
        
       # Label(bank_screen, image=bgl, bg = "#fff").place(x=13, y=30, width=30, height = 20,)
        self.search_invoice = StringVar()
        self.search_mfo = StringVar()

#=======Detail Frame======================
        # Detail_label =Label(bank_screen,  bg="#fff" )
        # Detail_label.pack( side = TOP, fill=X, )
        Detail_Frame=Frame(bank_screen, bd=1, relief=RIDGE, bg="#fff")
        Detail_Frame.pack( fill=X, side = TOP )
        # Detail_Frame.place( x=5, y=70, width = 1350, height= 620, )
        
        r_c=Label(Detail_Frame, text="P/C", bg="#fff", fg="black", font=("times new roman", 12, "bold"))
        r_c.grid( row=0, column=0, pady=10, padx=15, sticky="w")
  
        # combo_search= ttk.Combobox(Detail_Frame, width=10, font=("times new roman",13, "bold"),state='readonly')
        # combo_search['values']=("Roll", "Name", "Contact")
        # combo_search.grid(row=0, column=2, pady=10, padx=20, sticky="w")
    
        r_c_input=Entry(Detail_Frame, width=20, textvariable=self.search_invoice, borderwidth=2, font=("times new roman",12, "bold"))
        r_c_input.grid(row=0, column=0, pady=10, padx=60, sticky="w")
 
        mfo=Label(Detail_Frame, text="МФО", bg="#fff", fg="black", font=("times new roman", 12, "bold"))
        mfo.grid(row=0, column=1, pady=10, padx=0, sticky="w")

        mfo_input = Entry(Detail_Frame, width=7, textvariable=self.search_mfo, borderwidth=2, font=("times new roman",12, "bold"))
        mfo_input.grid(row=0, column=1, pady=10, padx=55, sticky="w")

        
        f_date=Label(Detail_Frame, text="Санадан", bg="#fff", fg="black", font=("times new roman", 12, "bold"))
        f_date.grid(row=0, column=2, pady=10, padx=10, sticky="w")
         #calendar 1
        cal = DateEntry(Detail_Frame,  selectmode="day", width=10, background='darkblue',foreground='white',  borderwidth=2,font=("times new roman",10, "bold"))
        cal.grid(row=0, column=2, pady=10, padx=90, sticky="w")

        s_date=Label(Detail_Frame, text="Санагача", bg="#fff", fg="black", font=("times new roman", 12, "bold"))
        s_date.grid(row=0, column=3, pady=10, padx=10, sticky="w")
        #calendar 2
        cal = DateEntry(Detail_Frame,  selectmode="day",  width=10, background='darkblue',foreground='white',  borderwidth=2, font=("times new roman",10, "bold"))
        cal.grid(row=0, column=3, pady=10, padx=90, sticky="w")


        
        # wa=Label(Detail_Frame, text=f"{date.datetime.now():%a, %b %d %Y}", fg="white", bg="black", font=("helvetica", 20))
        # wa.grid(row=0, column=6, pady=10, padx=50, sticky="w")

        #today = date.today()

        

        Button(Detail_Frame, text="Қидириш", command=self.search_data,  bg="#2a4291", fg="#fff", width=10, font=("times new roman", 10, "bold")).grid(row=0, column=4, pady=10, padx=10,)
        Button(Detail_Frame, text="Excelга сақлаш", command=lambda: write_tocsv(self.search_mfo.get()), bg="#2a4291", fg="#fff", width=15, font=("times new roman", 10, "bold")).grid(row=0, column=5, pady=10, padx=10,)
        #======Tabel_Frame=============================
        
        

        

        Tabel_Frame=Frame(bank_screen, bd=4, relief=RIDGE, bg="#fff")
       
        Tabel_Frame.pack( fill=BOTH, expand=True)
        

        scroll_x=Scrollbar(Tabel_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Tabel_Frame,orient=VERTICAL)
        self.Bank_table=ttk.Treeview(Tabel_Frame, columns=("number","date","mfo", "invoice","name", "debet", "credit", "remainder"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Bank_table.xview)
        scroll_y.config(command=self.Bank_table.yview)

        self.Bank_table.heading("number", text="№")
        self.Bank_table.heading("date", text="сана")
        self.Bank_table.heading("mfo", text="мфо")
        self.Bank_table.heading("invoice", text="P/C")
        self.Bank_table.heading("name", text="номи")
        self.Bank_table.heading("debet", text="дебет")
        self.Bank_table.heading("credit", text="кредит")
        self.Bank_table.heading("remainder", text="сана холатига қолдиқ")
        self.Bank_table['show']='headings'

        self.Bank_table.column("number",width=20)
        self.Bank_table.column("date",width=80)
        self.Bank_table.column("mfo",width=80)
        self.Bank_table.column("invoice",width=150)
        self.Bank_table.column("name",width=110)
        self.Bank_table.column("debet",width=110)
        self.Bank_table.column("credit",width=110)
        self.Bank_table.column("remainder",width=110)
        
        self.Bank_table.pack(fill=BOTH, expand=True)
    
    
    def search_data(self):
        import mysql.connector
        con = mysql.connector.connect(host="localhost", user="root", password="", database="qqb_project")
        cur = con.cursor()
        
        print(self.search_mfo.get())
        print(self.search_invoice.get())

        cur.execute(f"select * from qqb where mfo='{self.search_mfo.get()}' or invoice='{self.search_invoice.get()}';")
        rows=cur.fetchall()
        print(rows)
        
        self.Bank_table.delete(*self.Bank_table.get_children())
        for row in rows:
            self.Bank_table.insert('',END, values=row)
            con.commit()
            con.close()

#write to CVS Excel function
def write_tocsv(mfo):
    import mysql.connector
    con = mysql.connector.connect(host="localhost", user="root", password="", database="qqb_project")
    cur = con.cursor()
        
    #print(self.search_mfo.get())
    #print(self.search_invoice.get())

    cur.execute(f"select * from qqb where mfo='{mfo}';")
    rows=cur.fetchall()
    with open('customers.csv','a', newline='') as f:
         w = csv.writer(f, dialect='excel')
         for row in rows:
            w.writerow(row)
         #search_data(rows)
         
def insert_data(self):
    import mysql.connector
    con = mysql.connector.connect(host="localhost", user="root", password="", database="qqb_project")
    cur=con.cursor()

    cur.execute("insert into qqb values(%s, %s,%s,%s,%s,%s,%s,%s)",(self.number.get(),
                                                                    self.date.get(),
                                                                    self.mfo.get(),
                                                                    self.number2.get(),
                                                                    self.name.get(),
                                                                    self.debet.get(),
                                                                    self.credit.get(),
                                                                    self.remainder.get(),
                                                                    self.txt_Address.get('1.0', END)
    
    
                                                                                            ))
    con.commit()
    self.search_data()
    con.close()


    


    
def Password_func(event):
    password = e2.get()

    if(password == ""):
        messagebox.showinfo("", "Parol xato")


    elif(password == "123"):

        mf = MainFrame() 

    else :
        messagebox.showinfo("", "Parol xato")

    
def main_screen():
    global root    
    root = Tk()
   
    root=root 
    root.title("Qishloq Qurilish Bank")
    root.geometry("380x480+100+50")
    root.resizable(False, False)
    root.config(bg = "#fff")
    
   
    global e2
    
    bg=PhotoImage(file="qqb1.png")
    Label(root, image=bg, bg = "#fff").place(x=13, y=30, width=350, height = 100,)
    
    Label(root, text="Parolni kriting", font=("times new roman", 20, "bold"), fg="#2a4291", bg = "#fff" ).place(x=100, y=190)

    e2 = Entry(root)
    e2.place( x=90, y=250, width=200, height = 30,  )
    e2.config(show="*", font=("times new roman", 25, "bold"), bg = "#c9c9c9",)    
       
    Button(root, text="Kirish", command=Password_func, height = 1, width = 10, fg="#fff", bg="#2a4291", font=("times new roman", 18, "bold")).place(x=115, y=350)
    root.bind('<Return>', Password_func )
    root.mainloop()

main_screen()    