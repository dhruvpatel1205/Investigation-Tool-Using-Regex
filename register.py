from tkinter import *
from tkinter import messagebox
import pymysql

class Register:
    def __init__(self, root):
        self.root = root
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        self.root.title("Registration")
        self.root.geometry("%dx%d" % (width, height))
        self.root.config(bg="skyblue")

        left_c = Label(self.root, bg="skyblue", bd=0)
        left_c.place(x=675, y=0, relheight=1, relwidth=1)

        right_c = Label(self.root, bg="#031F3C", bd=0)
        right_c.place(x=675, y=0, relheight=1, relwidth=1)

        frame1 = Frame(self.root, bg="black")
        frame1.place(x=250, y=100, width=800, height=500)

        title = Label(frame1, text="Register", font=("open sans", 30, "bold", "italic"), bg="black",
                      fg="skyblue").place(x=330, y=20)

        Name = Label(frame1, text="Name", font=("open sans", 18, "bold"), bg="black", fg="white").place(x=150, y=100)
        self.txt_Name = Entry(frame1, font=("open sans", 18), bg="black", fg="green")
        self.txt_Name.place(x=250, y=100, width=330)

        Email = Label(frame1, text="Email", font=("open sans", 18, "bold"), bg="black", fg="white").place(x=150, y=170)
        self.txt_Email = Entry(frame1, font=("open sans", 18), bg="black", fg="green")
        self.txt_Email.place(x=250, y=170, width=330)

        Password = Label(frame1, text="Password", font=("open sans", 18, "bold"), bg="black", fg="white").place(x=123,
                                                                                                                y=240)
        self.txt_Password = Entry(frame1, show="*", font=("open sans", 18), bg="black", fg="green")
        self.txt_Password.place(x=250, y=240, width=330)

        MobileNo = Label(frame1, text="MobileNo", font=("open sans", 18, "bold"), bg="black", fg="white").place(x=125,
                                                                                                                y=310)
        self.txt_Number = Entry(frame1, font=("open sans", 18), bg="black", fg="green")
        self.txt_Number.place(x=250, y=310, width=330)

        btn = Button(frame1, text="Register", font=("open sans", 18, "bold"), bg="green", fg="white",
                     cursor="hand2", command=self.register_data).place(x=230, y=400, width=130)

        btn = Button(frame1, text="Sign-In", command=self.main_window, font=("open sans", 18, "bold"),
                     bg="green", fg="white", cursor="hand2").place(x=400, y=400, width=130)

    def clear(self):
        self.txt_Name.delete(0, END)
        self.txt_Email.delete(0, END)
        self.txt_Password.delete(0, END)
        self.txt_Number.delete(0, END)

    def main_window(self):
        self.root.destroy()
        import login

    def register_data(self):

        if self.txt_Name.get() == "" or self.txt_Email.get() == "" or self.txt_Password.get() == "" or self.txt_Number.get() == "":
            messagebox.showerror("Error", "All Fields are Required", parent=self.root)
        else:
            try:
                conn = pymysql.connect(host="localhost", user="root", db="investigation_tool")
                cur = conn.cursor()
                cur.execute("select * from registration where email=%s", self.txt_Email.get())
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "USER ALREADY EXIST", parent=self.root)
                else:
                    cur.execute("INSERT INTO registration(name,email,password,mobileno) VALUES(%s,%s,%s,%s)",
                                (self.txt_Name.get(),
                                 self.txt_Email.get(),
                                 self.txt_Password.get(),
                                 self.txt_Number.get(),))

                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Registration Successful", parent=self.root)
                self.clear()

            except Exception as es:
                messagebox.showerror("Error", f"Errors due to: {str(es)}", parent=self.root)


root = Tk()
obj = Register(root)
root.mainloop()
