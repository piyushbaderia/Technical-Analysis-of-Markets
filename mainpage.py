import mysql.connector
import sys
from tkinter import *
from tkinter import messagebox
#from UpdateStockData import update_data
#from StockDataFetch import get_data_from_yahoo
#from test2 import visual


#database connection
conn=mysql.connector.connect(host='localhost',user='root',passwd='piyush123') #connection
cursor = conn.cursor()
cursor.execute('use stockprediction;')


#def updatedata():
 #   print("In updatedata")

#def visualization():
 #   print("In visualization")

#def fetchdata():
 #   print("In fetchdata")

#def predefined_analysis():
 #   print("In predefined_anaylysis")


def CheckLogin(luname,lpass):
    
    cursor.execute("SELECT name FROM login_tb where uname=%s and password=%s",(luname,lpass))

    
    row = cursor.fetchone()

    if(row):
          after_login=Tk()
          after_login.title('Welcome')
          name=Label(after_login, text="Hello!  "+row[0],fg="slate blue",font="Helvetica 12 bold").pack(pady=20)
          row = cursor.fetchone()
 #         updateButton = Button(after_login, text='UPDATE DATA',fg="white",bg="slate blue",font="Helvetica 10",pady=5, command=lambda:update_data()).pack(pady=10,padx=20)
  #        fetchButton = Button(after_login, text='FETCH DATA',fg="white",bg="slate blue",font="Helvetica 10",pady=5,command=lambda:get_data_from_yahoo() ).pack(pady=10,padx=20)
          visualButton = Button(after_login, text='VISUALIZATION',fg="white",bg="slate blue",font="Helvetica 10",pady=5,command=lambda:visual() ).pack(pady=10,padx=20)
          paButton = Button(after_login, text='PREDEFINED ANALYSIS',fg="white",bg="slate blue",font="Helvetica 10",pady=5,command=lambda:predefined_analysis() ).pack(pady=10,padx=20)
    else:
          messagebox.showinfo(title="login",message="Incorrect login credentials")




def FSSignup(suname,spass,sname):
    
    try:
   # Execute the SQL command
     cursor.execute("""INSERT INTO login_tb (uname,password,name) VALUES(%s,%s,%s)""",(suname,spass,sname))
   # Commit your changes in the database
     conn.commit()
     messagebox.showinfo(title="Signup",message="signup successful!")
    except:
     # Rollback in case there is any error
     conn.rollback
    


def quit():
    mexit = messagebox.askyesno(title="Quit", message="Are you sure?")
    if mexit > 0:
       root.destroy()
       return

def login():
        llabel=Label(root, text='LOGIN',fg="slate blue",font="Helvetica 12 bold")
        llabel.grid(row=2,column=64)

        #photo = PhotoImage(file="C:/Users/Khattar/Desktop/stock/index.png")
        #plabel=Label(root, image=photo)
        llabel.grid(row=3,column=64)

        nameL = Label(root, text='Username: ',fg="slate blue",font="Helvetica 10") # More labels
        pwordL = Label(root, text='Password: ',fg="slate blue",font="Helvetica 10") # ^
        nameL.grid(row=6, sticky=W, column=63,pady=10,padx=15)
        pwordL.grid(row=7, sticky=W, column=63,pady=10,padx=15)
     
        nameEL = Entry(root) # The entry input
        pwordEL = Entry(root, show='*')
        nameEL.grid(row=6, column=65,padx=15)
        pwordEL.grid(row=7, column=65,padx=15)
     
        loginB = Button(root, text='Submit',fg="white", bg="slate blue", command=lambda: CheckLogin(nameEL.get(), pwordEL.get())) # This makes the login button, which will go to the CheckLogin def.
        loginB.grid(row=9,column=64, sticky=W,pady=10,padx=15)

          

         

def signup():

    
       Sroot=Tk()
       Sroot.title('New User Signup')
       slabel=Label(Sroot, text='New User!',fg="slate blue",font="Helvetica 12 bold")
       slabel.grid(row=1,column=1,pady=20)
       unameL = Label(Sroot, text='New Email: ',fg="slate blue",font="Helvetica 10") # This just does the same as above, instead with the text new username.
       pwordL = Label(Sroot, text='New Password: ',fg="slate blue",font="Helvetica 10") # ^^
       nameL = Label(Sroot, text='Name : ',fg="slate blue",font="Helvetica 10")
       unameL.grid(row=2, column=0, sticky=W,padx=15,pady=10) # Same thing as the instruction var just on different rows. :) Tkinter is like that.
       pwordL.grid(row=3, column=0, sticky=W,padx=15,pady=10) # ^^
       nameL.grid(row=4, column=0, sticky=W,padx=15,pady=10) # ^^

       unameE = Entry(Sroot,textvariable=uname) # This now puts a text box waiting for input.
       pwordE = Entry(Sroot, show='*',textvariable=passw) # Same as above, yet 'show="*"' What this does is replace the text with *, like a password box :D
       nameE = Entry(Sroot,textvariable=name)
       unameE.grid(row=2, column=2,padx=15) # You know what this does now :D
       pwordE.grid(row=3, column=2,padx=15) # ^^
       nameE.grid(row=4, column=2,padx=15)
     
       signupButton = Button(Sroot, text='Submit',fg="white",bg="slate blue",font="Helvetica 10", command=lambda: FSSignup(unameE.get(), pwordE.get(),nameE.get())) # This creates the button with the text 'signup', when you click it, the command 'fssignup' will run. which is the def
       signupButton.grid(row=6,column=1, sticky=W,padx=15,pady=10)
       Sroot.mainloop()


    

#main page    
root=Tk()
#signup variables
uname=StringVar()
passw=StringVar()
name=StringVar()

root.title('Prediction of stock')


#menu
menubar=Menu(root)
menubar.add_cascade(label='Login', command= login)
menubar.add_cascade(label='Signup', command= signup)
menubar.add_cascade(label='Close', command= quit)

root.config(menu=menubar)


root.mainloop()
