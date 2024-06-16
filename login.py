from tkinter import *
from tkinter import messagebox

import pymysql


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        self.root.geometry("%dx%d" % (width, height))
        self.root.config(bg="skyblue")

        left_c = Label(self.root, bg="skyblue", bd=0)
        left_c.place(x=675, y=0, relheight=1, relwidth=1)

        right_c = Label(self.root, bg="#031F3C", bd=0)
        right_c.place(x=675, y=0, relheight=1, relwidth=1)

        frame1 = Frame(self.root, bg="black")
        frame1.place(x=250, y=100, width=800, height=500)

        title = Label(frame1, text="Login", font=("open sans", 40, "bold", "italic"), bg="black", fg="#08A3D2").place(
            x=360, y=40)

        Email = Label(frame1, text="Username", font=("open sans", 19, "bold"), bg="black", fg="white").place(x=115,
                                                                                                             y=175)
        self.txt_Email = Entry(frame1, font=("open sans", 20), bg="Black", fg="green")
        self.txt_Email.place(x=250, y=180, width=350, height=35)

        Password = Label(frame1, text="Password", font=("open sans", 19, "bold"), bg="black", fg="white").place(x=120,
                                                                                                                y=280)
        self.txt_Password = Entry(frame1, show="*", font=("open sans", 20), bg="black", fg="green")
        self.txt_Password.place(x=250, y=280, width=350, height=35)

        btn_reg = Button(frame1, text="Sign-up", command=self.reg_window, font=("open sans", 18, "bold"),
                         bg="green", fg="white", cursor="hand2").place(x=220, y=380, width=180, height=40)

        btn_login = Button(frame1, text="Login", command=self.login, font=("open sans", 18, "bold"), fg="white",
                           bg="green", cursor="hand2").place(x=450, y=380, width=180, height=40)

    def clear(self):
        self.txt_Email.delete(0, END)
        self.txt_Password.delete(0, END)

    def reg_window(self):
        self.root.destroy()
        import register

    def login(self):
        if self.txt_Email.get() == "" or self.txt_Password.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = pymysql.connect(host="localhost", user="root", db="investigation_tool")
                cur = conn.cursor()
                cur.execute("select * from registration where email=%s and password=%s",
                            (self.txt_Email.get(), self.txt_Password.get()))
                row = cur.fetchone()

                if row == None:
                    messagebox.showerror("Error", "Invalid USERNAME & PASSWORD", parent=self.root)

                else:
                    messagebox.showinfo("Success", "Welcome", parent=self.root)
                    import home_page
                    conn.commit()
                    conn.close()
                    self.clear()

            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)


root = Tk()
obj = Login(root)
root.mainloop()
