from tkinter import*
import sqlite3
from tkinter.messagebox import *
from datetime import date
con=sqlite3.connect('bus_ticket.db')
cur=con.cursor()

cur.execute('create table if not exists bus(bus_id varchar(5) not null primary key,bus_type varchar(10),capacity int,fair int,op_id varchar(5) not null,route_id varchar(5) not null,foreign key(op_id) references operator(opr_id),foreign key(route_id) references route(r_id))')
cur.execute('create table if not exists operator(opr_id varchar(5) primary key,name varchar(20),address varchar(50),phone char(10),email varchar(30))')
cur.execute('create table if not exists running(b_id varchar(5) ,run_date date,seat_avail int,foreign key(b_id) references bus(bus_id))')
cur.execute('create table if not exists route(r_id varchar(5) not null primary key,s_name varchar(20),s_id varchar(5),e_name varchar(20),e_id varchar(5) )')
cur.execute('create table if not exists booking_history(name varchar(20),gender char(1),no_of_seat int,phone char(10),age int,booking_ref varchar(10) not null primary key,booking_date date,travel_date date,bid varchar(5),foreign key(bid) references bus(bus_id))')


root=Tk()



'''
def winhome(event=*None*) makes the event parameter optional by providing a default value of None. This way, whether
the function is called with or without an event, it won't raise a type error.
'''

    
def winhome(event=None):
    #Opening a new window
    winhome=Toplevel(root)
    winhome.title("Bus Booking Portal")
    #photo=PhotoImage(file='starbus.PNG')
    #Label(winhome, image=photo).place(relx=0.5,rely=0.5)
    Label(winhome,text="Online Bus Booking System",font='Arial 40',bg='cyan2').place(relx=0.5,rely=0.2,anchor=CENTER)
    Button(winhome,text="Seat Booking",font='Arial 15',bg="green",command=seatbooking).place(relx=0.25,rely=0.4)
    Button(winhome,text="Check Seat",font='Arial 15',bg="green",command=seatcheck).place(relx=0.45,rely=0.4)
    Button(winhome,text="Add Bus Details",font='Arial 15',bg="green",command=adddata).place(relx=0.65,rely=0.4)
    Label(winhome, text="For Admins Only",font="Arial 13",fg="red").place(relx=0.66,rely=0.5)
    winhome.state('zoomed')
    

def newoper():
    opt=Toplevel(root)
    opt.title("Bus Operator Details")
    Label(opt,text="Online Bus Booking System",font='Arial 40',bg='cyan2').place(relx=0.5,rely=0.2,anchor=CENTER)
    Label(opt,text="Add  New Bus Operator Details",font="Arial 25",fg="green").place(relx=0.36,rely=0.26)
    Label(opt,text="Operator ID",font='18').place(relx=0.1,rely=0.38)
    opr_id=Entry(opt)
    opr_id.place(relx=0.18,rely=0.385)
    Label(opt,text="Name",font='18').place(relx=0.27,rely=0.38)
    name=Entry(opt)
    name.place(relx=0.31,rely=0.385)
    Label(opt,text="Address",font='18').place(relx=0.4,rely=0.38)
    address=Entry(opt)
    address.place(relx=0.455,rely=0.385)
    Label(opt,text="Phone",font='18').place(relx=0.547,rely=0.38)
    phone=Entry(opt)
    phone.place(relx=0.59,rely=0.385)
    Label(opt,text="Email",font='18').place(relx=0.685,rely=0.38)
    email=Entry(opt)
    email.place(relx=0.724,rely=0.385)
    #function needs to be defined so that the new data can be added/editted to database
    def addoper():
        iid = opr_id.get()
        iname = name.get()
        iaddress = address.get()
        iphone = phone.get()
        iemail = email.get()
        cur.execute('select opr_id from operator')
        res=cur.fetchall()
        if len(iid) > 0 and len(iid) <= 5 and iid.isnumeric():
            if  len(iname) < 20 and len(iname) > 0:
                if len(iaddress) < 50 and len(iaddress) > 0:
                    if iphone.isnumeric() and len(iphone) == 10:
                        if len(iemail) > 0 and len(iemail) < 30:
                            if (iid,) in res:
                                showerror("ERROR","This operator id already exists!!")
                            else:
                                cur.execute('insert into operator (opr_id,name,address,phone,email)values(?,?,?,?,?)',(iid, iname, iaddress, iphone, iemail))
                                con.commit()
                                showinfo('Success', "New operator added successfully!!")
                        else:
                            showerror("invalid input", "enter email correctly")
                    else:
                        showerror("invalid input", "enter phone correctly")
                else:
                    showerror("invalid input", "enter address correctly")
            else:
                showerror("invalid input", "Enter name correctly")
        else:
            showerror("invalid input", "enter id correctly")
    Button(opt,text="Add",command=addoper).place(relx=0.81,rely=0.38)
    Button(opt,text="Home",command=winhome).place(relx=0.5,rely=0.5)
    opt.state('zoomed')


def newbus():
    bus=Toplevel(root)
    bus.title("Add New Bus")
    Label(bus,text="Online Bus Booking System",font='Arial 40',bg='cyan2').place(relx=0.5,rely=0.2,anchor=CENTER)
    Label(bus,text="Add New Bus Details",font="Arial 28",fg="green").place(relx=0.38,rely=0.26)
    Label(bus,text="Bus ID",font="Arial 14").place(relx=0.05,rely=0.35)
    b_id = Entry(bus)
    b_id.place(relx=0.095,rely=0.355)
    Label(bus,text="Bus Type",font="Arial 14").place(relx=0.19,rely=0.35)
    bus_type=StringVar()
    bus_type.set("Click to Select")
    option=["AC 2X2" , "AC 2X1" , "NonAC 2X2" , "NonAC 2X1" , "AC Sleeper 2X1" , "NonAC Sleeper 2X1"]
    OptionMenu(bus,bus_type,*option).place(relx=0.25,rely=0.35)
    Label(bus,text="Capacity",font="Arial 14").place(relx=0.35,rely=0.35)
    capacity=Entry(bus)
    capacity.place(relx=0.41,rely=0.355)
    Label(bus,text="Fare",font="Arial 14").place(relx=0.5,rely=0.35)
    fare = Entry(bus)
    fare.place(relx=0.535,rely=0.355)
    Label(bus,text="Operator ID",font='14').place(relx=0.62,rely=0.35)
    op_id=Entry(bus)
    op_id.place(relx=0.7,rely=0.355)
    Label(bus,text="Route ID",font="Arial 14").place(relx=0.79,rely=0.35)
    r_id=Entry(bus)
    r_id.place(relx=0.85,rely=0.355)
    #function needs to be defined so that the new data can be added/editted to database
    Button(bus,text="Home",command=winhome).place(relx=0.62,rely=0.5)
    def addbus():
        bid=b_id.get()
        dmenu=bus_type.get()
        capa=capacity.get()
        fare_rs=fare.get()
        opid=op_id.get()
        route_id=r_id.get()
        cur.execute('select bus_id from bus')
        res=cur.fetchall()
        if (bid,) in res:
            showerror("Error","Bus id already exists!!!")
        else:
            data="bus_id="+bid+"     bus_type="+dmenu+"     capacity="+capa+"     fare="+fare_rs+"     op_id="+opid+"     route_id="+route_id
            cur.execute('insert into bus(bus_id,bus_type,capacity,fair,op_id,route_id) values(?,?,?,?,?,?)',(bid,dmenu,capa,fare_rs,opid,route_id))
            con.commit()
            showinfo('Success', "Bus added successfully!!")
            Label(bus,text=data).place(relx=0.2,rely=0.45)
    Button(bus,text="Add",command=addbus).place(relx=0.5,rely=0.5)
    '''def editbus():
            bid=b_id.get()
            dmenu=bus_type.get()
            capa=capacity.get()
            fare_rs=fare.get()
            opid=op_id.get()
            route_id=r_id.get()
            cur.execute('select bus_id from bus')
            res=cur.fetchall()
            if (bid,) in res:
                data="bus_id="+bid+"     bus_type="+dmenu+"     capacity="+capa+"     fare="+fare_rs+"     op_id="+opid+"     route_id="+route_id
                cur.execute('update bus set bus_type=dmenu, capacity=capa, fair=fare_rs, route_id=route_id where bus_id==bid')
                con.commit()
                Label(root,text=data).place(relx=0.2,rely=0.45)
            else:
                showerror("error","no such bus id exists, add new bus !!!")
    Button(bus,text="Edit",command=editbus).place(relx=0.57,rely=0.5)'''
    bus.state('zoomed')



def newrun():
    run=Toplevel(root)
    run.title("Add New Run")
    Label(run,text="Online Bus Booking System",font='Arial 40',bg='cyan2').place(relx=0.5,rely=0.2,anchor=CENTER)
    Label(run,text="Add New Run Details",font="Arial 30",fg="green").place(relx=0.38,rely=0.26)
    Label(run,text="Bus ID",font="Arial 15").place(relx=0.2,rely=0.35)
    bus_id = Entry(run)
    bus_id.place(relx=0.25,rely=0.355)
    Label(run,text="Running Date",font="Arial 15").place(relx=0.35,rely=0.35)
    running_date = Entry(run)
    running_date.place(relx=0.44,rely=0.355)
    Label(run,text="Seat Available",font="Arial 15").place(relx=0.53,rely=0.35)
    seat_avail = Entry(run)
    seat_avail.place(relx=0.62,rely=0.355)
    def addrun():
        bid=bus_id.get()
        run_date=running_date.get()
        s_avail=seat_avail.get()
        cur.execute('insert into running(b_id,run_date,seat_avail) values (?,?,?)',(bid,run_date,s_avail))
        con.commit()
        showinfo('sucess','run added successfully!!')
    Button(run,text="Add",command=addrun).place(relx=0.72,rely=0.35)
    Button(run,text="Home",command=winhome).place(relx=0.5,rely=0.5)
    run.state('zoomed')

def newroute():
    route=Toplevel(root)
    route.title("Add New Route")
    Label(route,text="Online Bus Booking System",font='Arial 40',bg='cyan2').place(relx=0.5,rely=0.2,anchor=CENTER)
    Label(route,text="Add New Route Details",font="Arial 30",fg="green").place(relx=0.38,rely=0.26)
    Label(route,text="Route ID",font="Arial 14").place(relx=0.07,rely=0.37)
    r_id = Entry(route)
    r_id.place(relx=0.13,rely=0.375)
    Label(route,text="Station Name(from)",font="Arial 14").place(relx=0.218,rely=0.37)
    stname = Entry(route)
    stname.place(relx=0.33,rely=0.375)
    Label(route,text="From ID",font="Arial 14").place(relx=0.42,rely=0.37)
    stid = Entry(route)
    stid.place(relx=0.47,rely=0.375)
    Label(route,text="Station Name(to)",font="Arial 14").place(relx=0.56,rely=0.37)
    e_station = Entry(route)
    e_station.place(relx=0.663,rely=0.375)
    Label(route,text="To ID",font="Arial 14").place(relx=0.74,rely=0.37)
    end_id = Entry(route)
    end_id.place(relx=0.78,rely=0.375)
    def addroute():
        route_id=r_id.get()
        start_station=stname.get()
        start_id=stid.get()
        end_station=e_station.get()
        end_id=e_station.get()

        cur.execute('select r_id from route')
        res=cur.fetchall()
        if (route_id,) in res:
            showerror('ERROR',"Route id already exists")
        else:
            start_station=start_station.lower()
            end_station=end_station.lower()
            cur.execute('insert into route(r_id,s_name,s_id,e_name,e_id) values(?,?,?,?,?)',(route_id,start_station,start_id,end_station,end_id))
            con.commit()
            showinfo('Success',"route added successfully!!")
    Button(route,text="ADD",command=addroute).place(relx=0.87,rely=0.365)
    Button(route,text="Home",command=winhome,fg="red").place(relx=0.9,rely=0.365)
    route.state('zoomed')

def seatcheck():
    seatchk = Toplevel(root)
    seatchk.title("Booking Status")
    Label(seatchk,text="Online Bus Booking System",font='Arial 40',bg='cyan2').place(relx=0.5,rely=0.2,anchor=CENTER)
    Label(seatchk,text="Check your Booking",font='Arial 30').place(relx=0.38,rely=0.26)
    Label(seatchk,text="Enter your mobile No.",font='20').place(relx=0.3,rely=0.36)
    ph=Entry(seatchk)
    ph.place(relx=0.45,rely=0.37)
    Button(seatchk,text="Home",bg="blue",command=winhome).place(relx=0.6,rely=0.365)
    seatchk.state('zoomed')
    def ticketstatus():
        mobile=ph.get()
        if len(mobile)==10 and mobile.isdigit():
            cur.execute('select * from booking_history where phone=?',[mobile])
            res_tkt=cur.fetchall()
            for i in res_tkt:
                name=i[0]
                gen=i[1]
                seat=i[2]
                phone=i[3]
                age=i[4]
                b_ref=i[5]
                travel_date=i[6]
                b_i_d=i[7]
            cur.execute('select fair from bus where bus_id=?',[b_i_d])
            res_bus=cur.fetchall()
            fare=0
            if len(res_bus)>0:
                fare=res_bus[0][0]
            #route_id=res_bus[0][1]
            #cur.execute('select s_name,e_name from route where r_id=?',[route_id])
            #res_route=cur.fetchall()
            #st=res_route[0][0]
            #et=res_route[0][1]
            cur.execute('select booking_ref from booking_history where phone=?',[phone])
            res_ref=cur.fetchall()
            b_ref=res_ref[0][0]
            Label(seatchk,text="YOUR TICKET", font='Arial 12 bold', bg='lightblue').place(relx=0.45,rely=0.45)
            Label(seatchk,text="Booking ref = "+b_ref,font='Arial 12', fg='blue').place(relx=0.4,rely=0.5)
            Label(seatchk,text="Name = " + name, font='Arial 12', fg='blue').place(relx=0.4,rely=0.55)
            Label(seatchk,text="Gender = " + gen, font='Arial 12 ', fg='blue').place(relx=0.4,rely=0.6)
            Label(seatchk,text="No of seats = " + str(seat), font='Arial 12 ', fg='blue').place(relx=0.4,rely=0.65)
            Label(seatchk,text="Age = " + str(age), font='Arial 12 ', fg='blue').place(relx=0.4,rely=0.7)
            Label(seatchk,text="Travel date = " + str(travel_date), font='Arial 12 ', fg='blue').place(relx=0.4,rely=0.75)
            Label(seatchk,text="Fare = " + str(fare), font='Arial 12', fg='blue').place(relx=0.4,rely=0.8)
            Label(seatchk,text="Total fare = " + str(fare*seat), font='Arial 12', fg='blue').place(relx=0.4,rely=0.85)
    Button(seatchk,text="Check",font="Arial 11",fg="green",command=ticketstatus).place(relx=0.54,rely=0.365)

def adddata():
    dataadd = Toplevel(root)
    dataadd.title("Add New Details")
    Label(dataadd,text="Online Bus Booking System",font='Arial 40',bg='cyan2').place(relx=0.5,rely=0.2,anchor=CENTER)
    Label(dataadd,text="Add new details to database",font="Arial 26",bg="orange").place(relx=0.35,rely=0.26)
    Button(dataadd,text="New Operator",font="Arial 11",bg="brown",command=newoper).place(relx=0.33,rely=0.35)
    Button(dataadd,text="New Bus",font="Arial 11",bg="brown",command=newbus).place(relx=0.43,rely=0.35)
    Button(dataadd,text="New Route",font="Arial 11",bg="brown",command=newroute).place(relx=0.53,rely=0.35)
    Button(dataadd,text="New Run",font="Arial 11",bg="brown",command=newrun).place(relx=0.63,rely=0.35)
    Button(dataadd,text="Home",command=winhome).place(relx=0.5,rely=0.5)
    dataadd.state('zoomed')

def seatbooking():
    winseatbook=Toplevel(root)
    winseatbook.title("Seat Booking Portal")
    Label(winseatbook,text="Online Bus Booking System",font='Arial 40',bg='cyan2').place(relx=0.5,rely=0.2,anchor=CENTER)
    Label(winseatbook,text="Enter Journey Details",font='Arial 15').place(relx=0.5,rely=0.28,anchor=CENTER)
    Label(winseatbook,text="From",font='Arial 12').place(relx=0.3,rely=0.35)
    start=Entry(winseatbook)
    start.place(relx=0.34,rely=0.35)
    Label(winseatbook,text="To",font='Arial 12').place(relx=0.43,rely=0.35)
    finish=Entry(winseatbook)
    finish.place(relx=0.46,rely=0.35)
    Label(winseatbook,text="Date",font='Arial 12').place(relx=0.55,rely=0.35)
    date=Entry(winseatbook)
    Label(winseatbook,text="Format:YYYY-MM-DD",font='Arial 8',fg='red').place(relx=0.59,rely=0.375)
    date.place(relx=0.59,rely=0.35)
    winseatbook.state('zoomed')
    def showbus():
        st=start.get()
        fn=finish.get()
        dt=date.get()
        if st.isalpha() and fn.isalpha():
            if dt != '':
                cur.execute('select r_id from route where s_name=? and e_name=?',(st,fn,))
                res_route=cur.fetchall()
                print(res_route)
                if len(res_route)==0:
                    showerror('No route found','This route is currently not covered. Sorry for the inconvenience !!')
                else:
                    for i in res_route:
                        for j in i:
                            val_rt=str(j)
                    cur.execute('select bus_id from bus where route_id=?',(val_rt))
                    res_bus_id=cur.fetchall()
                    if len(res_bus_id)==0:
                        Label(winseatbook,text="No bus found !!!",font="Arial 20",fg="Red").place(relx=0.5,rely=0.5)
                    else:
                        val_busid=[]
                        for i in res_bus_id:
                            for j in i:
                                val_busid.append(j)
                        res_newbus=[]
                        for i in range(len(val_busid)):
                            cur.execute('select b_id from running where run_date=? and b_id=? ',(dt, val_busid[i]))
                            res_newbus.append(cur.fetchall())
                        b=[]
                        for i in res_newbus:
                            for j in i:
                                b.append(j[0])
                        if len(b)==0:
                            showerror('No Bus Found','Try another date!')
                        else:
                            Label(winseatbook,text='select bus',font='Arial 11').place(relx=0.2,rely=0.395)
                            Label(winseatbook, text='operator', font='Arial 11').place(relx=0.3,rely=0.395)
                            Label(winseatbook, text='bus type', font='Arial 11').place(relx=0.4,rely=0.395)
                            Label(winseatbook, text='Available Capacity', font='Arial 11').place(relx=0.5,rely=0.395)
                            Label(winseatbook, text='Fare', font='Arial 11').place(relx=0.6,rely=0.395)
                            r=0.45
                            bus_no=IntVar()
                            bus_select = IntVar()
                            serial_no=1
                            for i in b:
                                bus_no=i
                                cur.execute('select op_id from bus where bus_id=?',(i))
                                res_opr_id=cur.fetchall()
                                for j in res_opr_id:
                                    opr_id=j[0]
                                cur.execute('select name from operator where opr_id=?',(opr_id))
                                res_opr_name=cur.fetchall()
                                for j in res_opr_name:
                                    opr_name=j[0]
                                cur.execute('select bus_type from bus where bus_id=?',(i))
                                res_bus_type=cur.fetchall()
                                for j in res_bus_type:
                                    bus_type=j[0]
                                cur.execute('select seat_avail from running where run_date=? and b_id=?',(dt,i))
                                res_seat_avail=cur.fetchall()
                                for j in res_seat_avail:
                                    seat_avail=j[0]
                                cur.execute('select fair from bus where bus_id=?',(i))
                                res_fare=cur.fetchall()
                                for j in res_fare:
                                    fare=j[0]
                                def show_button():
                                    Button(winseatbook, text='PROCEED', bg='green', fg='black', font='Arial 9 bold',command=proceed).place(relx=0.65,rely=0.4)
                                var=Radiobutton(winseatbook,value=bus_no,variable=bus_select,command=show_button)
                                var.place(relx=0.2,rely=r)
                                Label(winseatbook, text=opr_name, font='Arial 13').place(relx=0.3, rely=r)
                                Label(winseatbook, text=bus_type, font='Arial 13').place(relx=0.4, rely=r)
                                Label(winseatbook, text=seat_avail, font='Arial 13').place(relx=0.5, rely=r)
                                Label(winseatbook, text=fare, font='Arial 13').place(relx=0.6, rely=r)
                                r+=0.1
                                serial_no+=1
                                
                            def proceed():
                                f_bus_id = bus_select.get()
                                Label(winseatbook,text='Fill passenger details to book the bus', bg='light green', fg='dark green', font='Arial 14 bold').place(relx=0.4,rely=0.6)
                                Label(winseatbook,text='Name',font='Arial 12').place(relx=0.2,rely=0.65)
                                pname = Entry(winseatbook)
                                pname.place(relx=0.24,rely=0.655)
                                gender = StringVar()
                                gender.set("Gender")
                                opt = ["M", "F", "T"]
                                g_menu = OptionMenu(winseatbook, gender, *opt)
                                g_menu.place(relx=0.33,rely=0.65)
                                Label(winseatbook, text='No of seats', font='Arial 12').place(relx=0.39,rely=0.65)
                                pseat=Entry(winseatbook)
                                pseat.place(relx=0.45,rely=0.655)
                                Label(winseatbook, text='Mobile', font='Arial 12').place(relx=0.55,rely=0.65)
                                pmobile = Entry(winseatbook)
                                pmobile.place(relx=0.59,rely=0.655)
                                Label(winseatbook, text='age', font='Arial 12').place(relx=0.68,rely=0.65)
                                page = Entry(winseatbook)
                                page.place(relx=0.71,rely=0.655)
                                def book_seat():
                                    name=pname.get()
                                    gen=gender.get()
                                    seats=pseat.get()
                                    seats=int(seats)
                                    age=page.get()
                                    age=int(age)
                                    mobile=pmobile.get()
                                    bid=bus_select.get()
                                    if len(mobile)==10:
                                        if len(name)>0 and len(name)<20:
                                            if age>0 and age<100:
                                                if seats>0 and seats<60:
                                                    #print(name, gen, age, mobile, seats, bid)
                                                    booking_ref=1
                                                    cur.execute('select booking_ref from booking_history')
                                                    res_ref=cur.fetchall()
                                                    ref=[]
                                                    for i in res_ref:
                                                        ref.append(i[0])
                                                    booking_ref=len(ref)+1
                                                    #print(booking_ref)
                                                    #cur_date=date.today()
                                                    cur.execute('insert into booking_history(name,gender,no_of_seat,phone,age,booking_ref,travel_date,bid) values(?,?,?,?,?,?,?,?)',(name,gen,seats,mobile,age,booking_ref,dt,bid))
                                                    con.commit()
                                                    cur.execute('select seat_avail from running where b_id=? and run_date=?',(bid,dt))
                                                    res_s=cur.fetchall()
                                                    s=res_s[0][0]
                                                    s=s-seats
                                                    cur.execute('update running set seat_avail=? where b_id=? and run_date=?',(s,bid,dt))
                                                    con.commit()
                                                    showinfo("successful","booking successfully done!!!")
                                                else:
                                                    showerror("Limit Exceeded","you can only book upto 10 seats")
                                            else:
                                                showerror("Invalid Age","Incorrect format of age")
                                        else:
                                            showerror("Invalid Name","Name can only contain alphabets")
                                    else:
                                        showerror("Invalid Mobile Number","Please check number of digits in mobile number again")
                                Button(winseatbook, text='BOOK SEAT', bg='green', fg='black', font='Arial 12 bold',command=book_seat).place(relx=0.5,rely=0.7)      
            else:
                showerror("Error","Enter journey date")
        else:
            showerror("Error","Enter details correctly!")
    Button(winseatbook,text='Show Bus',bg='green',command=showbus).place(relx=0.68,rely=0.345)        
    Button(winseatbook,text="Home",command=winhome).place(relx=0.73,rely=0.345)



root.title("Project Details")
frame=Frame(root)
frame.grid(row=0,column=0)
Label(root,text="Online Bus Booking System",font="Algerian 40",bg='cyan3').place(relx=0.5,rely=0.1,anchor=CENTER)
Label(root,text="Name: Utkarsh Gupta",font="Arial 15").place(relx=0.5,rely=0.2,anchor=CENTER)
Label(root,text="Enrollment No: 221B469",font="Arial 15").place(relx=0.5,rely=0.3,anchor=CENTER)
Label(root,text="Mobile No: 8957369691",font="Arial 15").place(relx=0.5,rely=0.4,anchor=CENTER)
Label(root,text="Submitted to: Dr. Mahesh Kumar",font="Algerian 40",bg='cyan3').place(relx=0.5,rely=0.5,anchor=CENTER)
Label(root,text="Project Based Learning",font="Arial 15").place(relx=0.5,rely=0.58,anchor=CENTER)
Label(root,text="Press any key to continue",font="Arial 15",fg="red").place(relx=0.42,rely=0.9)


#Key Binding
root.bind("<Key>",winhome)


#Maximize the window using state property
root.state('zoomed')

root.mainloop()  
