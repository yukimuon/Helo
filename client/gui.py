import tkinter as tk
from mtencrypt import *
from network import *
import sys

class Store:
    def __init__(self):
        self.uid = ""

Store = Store()

def gui_main():
    class Application(tk.Frame):
        def __init__(self, master, obj):
            super().__init__(master)
            self.master = master
            self.pack()
            self.create_widgets()
            self.keypair = obj
            self.RSAkeypair = RSAgenerate(4096)
            self.uid = ""
            self.servern = 0
            self.servere = 0
            self.messages = [""]
            self.upass = ""
            self.server_addr = ""
            self.indi = []

        
        def showmsg(self,msg):
            self.messages.append(msg)
            print(msg)
            tk.Label(self, text=self.messages[-1]).grid(row=10+len(self.messages))

        def create_widgets(self):
            self.indi1 = tk.Label(self, text="User name").grid(row=1)
            self.indi2 = tk.Label(self, text="Password").grid(row=3)
            self.indi3 = tk.Label(self, text="Server addr").grid(row=5)
            self.indi4 = tk.Label(self, text="Send <msg> to <uid>").grid(row=6,column=0)
            self.indi5 = tk.Label(self).grid(row=10)
            self.tbox1 = tk.Entry(self)
            self.tbox1.grid(row=1, column=1)
            self.tbox2 = tk.Entry(self,show="*")
            self.tbox2.grid(row=3, column=1)
            self.tbox3 = tk.Entry(self)
            self.tbox3.grid(row=5, column=1)            
            self.tbox4 = tk.Entry(self)
            self.tbox4.grid(row=6, column=1)
            self.tbox5 = tk.Entry(self)
            self.tbox5.grid(row=6, column=2)
            self.line = tk.Label(self, text="MTing Login").grid(row=0)
            self.line1 = tk.Label(self).grid(row=7, column=0)

            self.login = tk.Button(self, text="Connect", fg="green", command=self.login)
            self.login.grid(row=8, column=0)
            self.quit = tk.Button(self, text="Fetch", fg="blue", command=self.fetch)
            self.quit.grid(row=8, column=1)
            self.quit = tk.Button(self, text="Clear", fg="purple", command=self.clear)
            self.quit.grid(row=8, column=2)
            self.quit = tk.Button(self, text="Send", fg="black", command=self.send)
            self.quit.grid(row=9, column=0)
            self.quit = tk.Button(self, text="Register", fg="black", command=self.register)
            self.quit.grid(row=9, column=1)
            self.quit = tk.Button(self, text="Exit", fg="red", command=self.master.destroy)
            self.quit.grid(row=9, column=2)

        def login(self):
            try:
                self.server_addr = self.tbox3.get()
                response = HANDSHAKE(self.server_addr, 65000)
                self.servern=response.split(",")[0]
                self.servere=response.split(",")[1]

                n = str(self.RSAkeypair.publickey().n)
                e = str(self.RSAkeypair.publickey().e)

                self.uid = self.tbox1.get()
                self.upass = self.tbox2.get()
                response = SENDRSA(self.server_addr, 65003, n, e, self.uid, self.upass)
                print("RESPONSE:",response)
                self.showmsg(response.decode("utf-8"))
            except:
                e = sys.exc_info()
                print(e)

        def fetch(self):
            response = SEND(self.server_addr, 65001, self.servern, self.servere, "FETCH-"+self.uid+"-"+self.upass)
            print("RESPONSE LENG:",len(response))
            self.showmsg(RSAdecrypt(self.RSAkeypair,response))
        
        def clear(self):
            response = SEND(self.server_addr, 65001, self.servern, self.servere, "CLEAR-"+self.uid+"-"+self.upass)
            print("RESPONSE:",response)
            self.showmsg(response)

        def send(self):
            response = SEND(self.server_addr, 65001, self.servern, self.servere, "SEND:"+self.tbox5.get()+":"+self.tbox4.get()+"-" +self.uid+"-"+self.upass)
            print("RESPONSE:",response)
            self.showmsg(response)  

        def add(self):
            response = SEND(self.server_addr, 65001, self.servern, self.servere, "ADD:"+self.tbox1.get()+"-" +self.uid+"-"+self.upass)
            print("RESPONSE:",response)
            self.showmsg(response)                     

        def register(self):
            self.server_addr = self.tbox3.get()
            response = HANDSHAKE(self.server_addr, 65000)
            self.servern=response.split(",")[0]
            self.servere=response.split(",")[1]
            self.uid = self.tbox1.get()
            self.upass = self.tbox2.get()
            response = SEND(self.server_addr, 65001, self.servern, self.servere, "REGISTER-"+self.uid+"-" +self.upass)
            print("RESPONSE:",response)
            self.showmsg(response)             



    root = tk.Tk()
    app = Application(master=root, obj=Store)
    root.minsize(400, 400) 
    scrollbar = tk.Scrollbar(root)
    app.mainloop()

gui_main()