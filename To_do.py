import csv,os, datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
to_do = Tk()
to_do.title("To-Do List")
sw = to_do.winfo_screenwidth()
sh = to_do.winfo_screenheight()
to_do.minsize(sw//2, sh//2)
to_do.maxsize(sw, sh)
to_do.geometry(f"{sw}x{sh}")
font_size = min(sw//30, sh//30)
mainfile=f"{os.path.dirname(os.path.abspath(__file__))}\\task.csv"
if not os.path.exists(mainfile): open(mainfile,"w",newline="").close()
def load_tasks():
    with open(mainfile, mode='r') as file:
        reader = csv.reader(file)
        tasks=ksort(list(reader))
    try:
        for i in tr.get_children():
            tr.delete(i)
    except:pass
    for i in range(len(tasks)):
        color = "#A0EFBB"
        if tasks[i][2]=="Pending":
            if tasks[i][3] == "High":
                color = "#FF6666"
            elif tasks[i][3] == "Medium":
                color = "#FFAB66"
            elif tasks[i][3]== "Low":
                color = "#FFEEA7"
        id=i+1
        tr.insert(parent='',index='end',iid=i,text='',values=(id,tasks[i][0],tasks[i][1],tasks[i][2],tasks[i][3]),tags=(color,))
        tr.tag_configure(color, background=color)
def add():
    auwin = Toplevel(to_do)
    auwin.focus_force()
    auwin.resizable(False, False)
    auwin.title("Add Task")
    opened=[]
    def add_task():
        with open(mainfile, mode='r') as file:
            opened = [i[0:2] for i in list(csv.reader(file))]
        task = e1.get().capitalize().strip()
        try:end_date = datetime.datetime.strptime(f"{yr.get()}-{month_values.index(mnth.get())+1}-{dy.get()}", '%Y-%m-%d')
        except:end_date=""
        priority = e3.get()
        if task and end_date and priority:
            if [task, f"{dy.get()}-{mnth.get()}-{yr.get()}"] not in opened:
                with open(mainfile, mode='a', newline='') as file:
                    wr=csv.writer(file)
                    wr.writerow([task, f"{dy.get()}-{mnth.get()}-{yr.get()}","Pending",priority])
                load_tasks()
                auwin.destroy()
            else:l1.configure(text="Task exists either change the name or the date")
        else:l1.config(text="All fields are required! or you have entered the wrong date")
    for i, j in {"Task: ": 1, "End Date: ": 2, "Priority: ": 3}.items():
        Label(auwin, text=i, font=("Times", font_size-10)).grid(row=j, column=0)
    e1 = Entry(auwin, font=("Times", font_size-10))
    e1.focus_force()
    e2=Frame(auwin)
    dayvalues = list(range(1, 32))
    dy = ttk.Combobox(e2, values=dayvalues, width=5)
    dy.set("Day")
    dy.pack(side='left', padx=5, pady=20)
    month_values = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]
    mnth = ttk.Combobox(e2,values=month_values, width=10)
    mnth.set("Month")
    mnth.pack(side='left', padx=5, pady=20)
    crnt_yr =  datetime.datetime.now().year
    year_values = list(range(crnt_yr , crnt_yr + 71))
    yr = ttk.Combobox(e2,values=year_values, width=7)
    yr.set("Year")
    yr.pack(side='left', padx=5, pady=20)
    e3 = ttk.Combobox(auwin, font=("Times", font_size-10), values=["Low", "Medium", "High"],state="readonly")
    e3.current(1)
    b1 = Button(auwin, text="Add", font=("Times", font_size-10), command=add_task)
    b2 = Button(auwin, text="Cancel", font=("Times", font_size-10), command=auwin.destroy)
    l1 = Label(auwin, fg="red",font=("Times", font_size-12,"italic"))
    e1.grid(row=1, column=1, sticky=W, padx=15, pady=5, columnspan=2)
    e2.grid(row=2, column=1, sticky=W, padx=15, pady=5, columnspan=2)
    e3.grid(row=3, column=1, sticky=W, padx=15, pady=5)
    b1.grid(row=4, column=1, sticky=E, padx=10, pady=5)
    b2.grid(row=4, column=2, sticky=E, padx=10, pady=5)
    l1.grid(row=5, column=0, sticky=W, padx=10, pady=5)
def delete():
    selected_item = tr.selection()
    if selected_item:
        with open(mainfile,"r")as file:
            fr=list(csv.reader(file))
        task  =[tr.item(i)["values"][1:] for i in tr.selection()]
        for i in task:
            fr.remove(i)
        with open(mainfile,"w",newline="") as file:
            csv.writer(file).writerows(fr)
        load_tasks()        
    else:messagebox.showwarning("Warning", "No task selected!")
def edit():
    selected_item = tr.selection()
    if len(selected_item)==1:
        task  = tr.item(tr.selection())["values"]
        auwin = Toplevel(to_do)
        auwin.focus_force()
        auwin.resizable(False, False)
        auwin.title("Edit Task")
        def save_task():
            with open(mainfile, mode='r') as file:
                opened=[i for i in list(csv.reader(file)) if i !=task[1:]]
            tasknm = e1.get().capitalize().strip()
            try:end_date = datetime.datetime.strptime(f"{yr.get()}-{month_values.index(mnth.get())+1}-{dy.get()}", '%Y-%m-%d')
            except:end_date=""
            priority = e3.get()
            opened2=[i[0:2] for i in opened]
            if tasknm and end_date and priority:
                if [tasknm, f"{dy.get()}-{mnth.get()}-{yr.get()}"] not in opened2:
                    opened.append([tasknm, f"{dy.get()}-{mnth.get()}-{yr.get()}",task[3],priority])
                    with open(mainfile, mode='w', newline='') as file:
                        wr=csv.writer(file)
                        wr.writerows(opened)
                    load_tasks()
                    auwin.destroy()
                else:l1.configure(text="Task exists either change the name or the date")
            else:l1.config(text="All fields are required! or you have entered the wrong date")
        for i, j in {"Task: ": 1, "End Date: ": 2, "Priority: ": 3}.items():
            Label(auwin, text=i, font=("Times", font_size-10)).grid(row=j, column=0)
        e1 = Entry(auwin, font=("Times", font_size-10))
        e1.focus_force()
        e1.insert(0,task[1])
        e2=Frame(auwin)
        dayvalues = list(range(1, 32))
        dy = ttk.Combobox(e2, values=dayvalues, width=5)
        dy.set(task[2].split(sep='-')[0])
        dy.pack(side='left', padx=5, pady=20)
        month_values = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]
        mnth = ttk.Combobox(e2,values=month_values, width=10)
        mnth.set(task[2].split(sep='-')[1])
        mnth.pack(side='left', padx=5, pady=20)
        crnt_yr =  datetime.datetime.now().year
        year_values = list(range(crnt_yr , crnt_yr + 71))
        yr = ttk.Combobox(e2,values=year_values, width=7)
        yr.set(task[2].split(sep='-')[2])
        yr.pack(side='left', padx=5, pady=20)
        e3 = ttk.Combobox(auwin, font=("Times", font_size-10), values=["Low", "Medium", "High"],state="readonly")
        e3.set(task[4])
        b1 = Button(auwin, text="Save", font=("Times", font_size-10), command=save_task)
        b2 = Button(auwin, text="Cancel", font=("Times", font_size-10), command=auwin.destroy)
        l1 = Label(auwin, fg="red",font=("Times", font_size-10,"italic"))
        e1.grid(row=1, column=1, sticky=W, padx=15, pady=5, columnspan=2)
        e2.grid(row=2, column=1, sticky=W, padx=15, pady=5, columnspan=2)
        e3.grid(row=3, column=1, sticky=W, padx=15, pady=5)
        b1.grid(row=4, column=1, sticky=E, padx=10, pady=5)
        b2.grid(row=4, column=2, sticky=E, padx=10, pady=5)
        l1.grid(row=5, column=0, sticky=W, padx=10, pady=5)
    elif len(selected_item)>1:messagebox.showwarning("Warning", "More than 1 task is selected!")
    else:messagebox.showwarning("Warning", "No task selected!")
def chngstatus():
    selected_item = tr.selection()
    if selected_item:
        selitem=[tr.item(i)["values"][1:] for i in tr.selection()]
        with open(mainfile,"r")as f:
            allitem=list(csv.reader(f))
        for i in allitem:
            if i in selitem:i[2] = "Completed" if i[2] == "Pending" else "Pending"
        with open(mainfile,"w",newline="") as file:
            wr=csv.writer(file)
            wr.writerows(allitem)
        load_tasks()
    else:messagebox.showwarning("Warning", "No task selected!")
def ksort(tasks):
    cr = g.get()
    ordr = w.get()
    cordr=cw.get()
    if cr == 0:sorted_tasks = tasks
    elif cr == 1:sorted_tasks = [i for i in tasks if i[2] == "Pending"]
    elif cr == 2:sorted_tasks = [i for i in tasks if i[2] == "Completed"]
    if cordr == 0:
        priordict={"High":3,"Medium":2,"Low":1}
        sorted_tasks = sorted(sorted_tasks, key=lambda x: priordict[x[3]])
    elif cordr == 1:
        month_values = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]
        sorted_tasks = sorted(sorted_tasks, key=lambda x: datetime.datetime.strptime(f'{x[1][-4:]}-{month_values.index(x[1].split(sep="-")[1])+1}-{x[1].split(sep="-")[0]}', "%Y-%m-%d"))
    if ordr == 1:sorted_tasks.reverse()
    return sorted_tasks
def shows():
    swin=Toplevel(to_do)
    di={"Ctrl A": "To select all records","Escape": "To deselect the selected ones","Delete": "To delete the selected records","Ctrl G": "To change status of selected ones","Ctrl E": "To edit a single record selected at a time","Ctrl I": "To insert a record" }
    for j,i in enumerate(di,start=0):
        Label(swin, text=f"{j}").grid(row=j,column=1,padx=5,pady=5)
        Label(swin,text=f"{i}").grid(row=j,column=2,sticky=W,padx=5,pady=5)
        Label(swin,text=f"{di[i]}").grid(row=j,column=3,sticky=W,padx=5,pady=5)
menubar = Menu(to_do)
to_do.config(menu=menubar)
menubar.add_command(label="Add Task", command=add)
menubar.add_command(label="Delete Task", command=delete)
menubar.add_command(label="Edit Task", command=edit)
menubar.add_command(label="Change Status", command=chngstatus)
g, w ,cw= IntVar(value=0), IntVar(value=0),IntVar(value=0)
srtmnu = Menu(menubar, tearoff=0)
srtmnu.add_radiobutton(label="All tasks", variable=g, value=0,command=load_tasks)
srtmnu.add_radiobutton(label="Pending tasks", variable=g, value=1,command=load_tasks)
srtmnu.add_radiobutton(label="Completed tasks", variable=g, value=2,command=load_tasks)
srtmnu.add_separator()
srtmnu.add_radiobutton(label="Priority order", variable=cw, value=0,command=load_tasks)
srtmnu.add_radiobutton(label="Due Date order", variable=cw, value=1,command=load_tasks)
srtmnu.add_separator()
srtmnu.add_radiobutton(label="A -> Z", variable=w, value=0,command=load_tasks)
srtmnu.add_radiobutton(label="Z -> A", variable=w, value=1,command=load_tasks)
menubar.add_cascade(label="Sort", menu=srtmnu)
menubar.add_command(label="Shortcuts", command=shows)
scrl = Scrollbar(to_do, orient="vertical")
scrl.pack(side="right", fill="y")
fr = Frame(to_do, width=sw, height=sh, relief="solid")
fr.pack(fill=BOTH, padx=10, pady=10)
style = ttk.Style()
style.theme_use('clam')
tr = ttk.Treeview(fr, height=sh, selectmode="extended", show="headings", yscrollcommand=scrl.set)
tr['columns'] = ("Sr no.", "Task", "End Date", "Status", "Priority")
for i in tr['columns']:
    tr.column(i, minwidth=140)
    tr.heading(i, text=i, anchor=CENTER)
style = ttk.Style()
style.configure("Treeview.Heading", font=("Times", font_size-10, "italic"))
tr.pack(side=LEFT, expand=True, fill=BOTH)
scrl.configure(command=tr.yview)
load_tasks()
to_do.bind("<Control-a>",lambda event:[[tr.selection_add(x) for x in tr.get_children()]])
to_do.bind("<Escape>",lambda event:[[tr.selection_remove(x)for x in tr.get_children()]])
to_do.bind("<Delete>",lambda event : delete())
to_do.bind("<Control-g>",lambda event : chngstatus())
to_do.bind("<Control-e>",lambda event : edit())
to_do.bind("<Control-i>",lambda event : add())
to_do.mainloop()