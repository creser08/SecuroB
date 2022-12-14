import tkinter as tk
from tkinter import filedialog, messagebox

from pathlib import Path
import hashlib
from cryptography.fernet import Fernet
import random

from Other import *


class AppDeCrypt(tk.Tk):

    def __init__(self):
        super().__init__()
        
        self.geometry(resolution)
        self.config(bg=couleur_bg)
        self.title('Securob  -D&Crypt')
        self.iconbitmap(icone)
        self.resizable(width=False, height=False)

        self.FrameMaster()
        self.readSettingsFile()

        if self.listLineSett[1] == "starting_message,1\n":
            messagebox.showinfo('Infos', 'if you never use this app or if you \n had some problems. \nGo on infos in the menu bar \nyou can desactivate this message in settings')

    def FrameMaster(self):
        self.frameMaster = tk.Frame(self, bg=couleur_bg, width=1280, height=700)
        self.frameMaster.grid()

        self.frame0 = tk.Frame(self.frameMaster, bg=couleur_bg, width=640, height=700)
        self.frame1 = tk.Frame(self.frameMaster, bg =couleur_bg, width=640, height=700)

        self.frame0.place(x=0)
        self.frame1.place(x=640)
        #frame 0
        self.can0 = tk.Canvas(self.frame0, width=640, height=700, bg=couleur_bg, highlightthickness=0)
        self.can0.grid(columnspan=3, rowspan=50)
        #label
        self.name_app = tk.Label(self.frame0, text="SecuroB", font=("Impact", 40), bg=couleur_bg, fg=couleur_fg).place(x=10, y=10)
        self.orText = tk.Label(self.frame0, text="Or", font=("Raleway", 16), bg=couleur_bg, fg=couleur_fg)
        self.pswText = tk.Label(self.frame0, text="Password :", font=("Raleway", 10), bg=couleur_bg, fg=couleur_fg)
        self.lblBrowseKey = tk.Label(self.frame0, text="", font=("Raleway", 16), bg=couleur_bg, fg=couleur_fg)
        self.lblChoosePsw = tk.Label(self.frame0, text="", font=("Raleway", 16), bg=couleur_bg, fg=couleur_fg)
        #entry
        self.entryPsw = tk.Entry(self.frame0, width=25,show='*')  
        self.entryPsw.bind('<Button-1>', self.resetPswdEntry)     
        self.entryPsw.bind('<Return>', self.choosePassword)
        #text bouton
        self.keyBtnText = tk.StringVar()
        self.seeText = tk.StringVar()
        self.CBtnTxt = tk.StringVar()
        self.DBtnTxt = tk.StringVar()
        #boutons
        self.keyBtn = tk.Button(self.frame0, textvariable=self.keyBtnText, bg=couleur_bg, relief='groove', bd=3, fg=couleur_fg, padx=2, pady=2, command=lambda:self.findKey())
        self.keyBtnText.set("Browse Key")
        self.seePswBtn = tk.Button(self.frame0, textvariable=self.seeText, bg=couleur_bg, relief='groove', bd=1, fg=couleur_fg, padx=1, pady=1, command=lambda:self.showPassword())
        self.seeText.set("see")
        self.cBtn = tk.Button(self.frame0, textvariable=self.CBtnTxt, bg=couleur_bg, relief='groove', bd=3, fg=couleur_fg, padx=2, pady=2, command=lambda:self.cryptFile())
        self.CBtnTxt.set('Crypt')
        self.dBtn = tk.Button(self.frame0, textvariable=self.DBtnTxt, bg=couleur_bg, relief='groove', bd=3, fg=couleur_fg, padx=2, pady=2, command=lambda:self.decryptFile())
        self.DBtnTxt.set('Decrypt')
        #affichage
        # Boutons
        self.keyBtn.grid(column=1, row=17)
        self.cBtn.grid(column=0 ,row=38)
        self.dBtn.grid(column=2 ,row=38)
        # Textes                                                        # x=400 a droite de key and password, y=208 key 
        self.lblBrowseKey.place(x=50, y=208)
        self.lblChoosePsw.place(x=40, y=321)
        self.orText.grid(column=1, row=19)
        self.pswText.place(x=285, y=300)
        self.seePswBtn.place(x=400, y=324)
        # Entry
        self.entryPsw.grid(column=1, row=22)
        #frame1
        self.can1 = tk.Canvas(self.frame1, width=640, height=700, bg=couleur_bg, highlightthickness=0)
        self.can1.grid(columnspan=3, rowspan=5)
        self.scrollbarTxtBox = tk.Scrollbar(self.frame1, relief='sunken', orient='vertical', width=15)
        #text bouton
        self.txtBtnBrowse = tk.StringVar()
        #bouton
        self.BFileBtn = tk.Button(self.frame1, textvariable=self.txtBtnBrowse, pady=2, relief='groove', padx=2, bg=couleur_bg, bd=3, fg=couleur_fg, command=lambda:self.browseFile())
        self.txtBtnBrowse.set("Browse file")
        self.BSave = tk.Button(self.frame1, text="Save", pady=2, padx=2, bg=couleur_bg, bd=3, relief='groove', fg=couleur_fg, command=lambda:self.saveFile())
        self.lblBrowsefile = tk.Label(self.frame1, text="", font=("Raleway", 16), bg=couleur_bg, fg=couleur_fg)
        self.text_box = tk.Text(self.frame1, height=35, width=70, padx=2, pady=2, yscrollcommand=self.scrollbarTxtBox.set, state='normal')
        self.scrollbarTxtBox.config(command=self.text_box.yview)
        self.scrollbarTxtBox.grid(column=2, row=3)
        self.BFileBtn.grid(column=1, row=1)
        self.lblBrowsefile.grid(column=1, row=2)
        self.text_box.grid(column=1, row=3)

    # Basics fonction

    def showPassword(self):
        global i
        if i == 0:
            self.entryPsw.config(show="")
            i += 1
            self.seeText.set("hide")
        else :
            self.entryPsw.config(show="*")
            i = 0
            self.seeText.set("see")

    def choosePassword(self, event):
        self.psw_len = len(self.entryPsw.get())
        if self.psw_len >= minCarMdp:
            #self.checkWay = True
            self.lblBrowseKey.configure(text="")
            self.lblChoosePsw.configure(text="you used password")
            self.typeOfKey = "password"
            self.checkWay()
        if self.psw_len < minCarMdp:
            #self.checkWay = False
            self.lblBrowseKey.configure(text="")
            self.lblChoosePsw.configure(text=f"min {minCarMdp} lenght")

    def resetPswdEntry(self, event):
        self.lblChoosePsw.configure(text="press enter to \n validate")
        self.key = ""

    def getExtension(self, name_file):
        exten = []
        for each in name_file:
            exten.append(each)
        k = len(exten) - 4
        ext = ""
        while k < len(exten):
            ext += str(exten[k])
            k += 1
        
        return ext

    def getName(self, file_Abs_path):
        path = Path(file_Abs_path)
        name_file = path.name

        return name_file

    # Files Fonctions
    def findKey(self):
        self.keyBtnText.set("loading ...")
        try :
            filekey = filedialog.askopenfile(title="Select key",filetypes=[("Key file", "*.key")])
            self.absPathKey = filekey.name
        except:
            self.keyBtnText.set("Browse Key")
        else:
            nameFileKey = self.getName(self.absPathKey)
            self.lblChoosePsw.configure(text="")
            self.lblBrowseKey.configure(text=nameFileKey)
            self.keyBtnText.set("Browse Key")
            self.typeOfKey = "key"
            self.checkWay()

    def browseFile(self):
        self.txtBtnBrowse.set("loading ...")
        try:
            fileBrowsed = filedialog.askopenfile(title="Select file",filetypes=[("all files","*.*"),("Text file", "*.txt"),("Rar file", "*.rar"),("Zip file", "*.zip")])
            self.absPathFile = fileBrowsed.name
        except:
            self.txtBtnBrowse.set("Browse file")
        else:
            name_file = self.getName(self.absPathFile)
            self.lblBrowsefile.configure(text=name_file)
            self.txtBtnBrowse.set("Browse file")          
            ext = self.getExtension(name_file)
            try:
                if ext == ".txt":
                    self.text_box.config(state='normal')
                    self.BSave.grid(column=1, row=4)
                    self.text_box.delete(1.0, "end")
                    file = open(self.absPathFile, 'rt')
                    content = file.read()
                    file.close()
                    self.text_box.insert(1.0, content)      
                else:
                    self.BSave.grid_forget()
                    self.text_box.delete(1.0, "end")
                    self.text_box.insert(1.0,"Work just for .txt \nbtw you can also (de)crypt it")
                    self.text_box.config(state='disable')
            except:
                self.BSave.grid_forget()
                self.text_box.delete(1.0, "end")
                self.text_box.insert(1.0,"Something wrong sorry \nbtw you can also (de)crypt it")

    def saveFile(self):
        ext = self.getExtension(self.absPathFile)
        if ext == ".txt":
            content = self.text_box.get(1.0, 'end')
            file = open(self.absPathFile, 'w')
            file.write(content)
            file.close()
        else :
            messagebox.showerror('Sorry', 'you can modify \nand save only .txt')

    def checkWay(self):
        if self.typeOfKey == "key":   
            fileKey = open(self.absPathKey, "rb")
            self.key = fileKey.read()
            fileKey.close()
                      
        elif self.typeOfKey == "password":
            if self.checkWay:
                self.key = genKey(self.entryPsw.get())
            else:
                messagebox.showerror('Problem', 'Password probably to small')      

    def readSettingsFile(self):
        fic = open(SettingFile, 'r')
        self.listLineSett = fic.readlines()
        fic.close()

# (De)Crypt fonctions

    def keyGeneratorRandom(self):
        password = random_password(15, alphabet_plus)
        
        liste_letter = []
        hash_ = hashlib.sha512(password.encode()).hexdigest()
        i = 0
        mot1 = ""
        mot2 = ""
        for each in hash_:
            liste_letter.append(each)
        while i < 64:
            mot1 += liste_letter[i]
            i += 1
        while i < 128:
            mot2 += liste_letter[i]
            i += 1
        mot1 = hashlib.sha256(mot1.encode()).hexdigest()
        mot2 = hashlib.sha256(mot2.encode()).hexdigest()
        key = mot2 + mot1
        key = hashlib.sha256(key.encode()).hexdigest()
        i = 0
        Lmot = list(key)
        while i < 21:
            k = random.randrange(0,len(Lmot))  
            del Lmot[k]
            i += 1
        key = ""
        for each in Lmot:
            key += each
        key += "=" 
        key = key.encode('utf-8')

        fileKey = filedialog.asksaveasfile(title="Create key",filetypes=[("key files","*.key")], defaultextension=".key", initialfile="Mykey")
        try:
            fichierCle = open(fileKey.name, "wb")
        except:
            try:
                self.CBtnTxt.set('Crypt')
            except:
                pass
        else:    
            fichierCle.write(key)
            fichierCle.close()

    def cryptFile(self):
        self.CBtnTxt.set('Wait ...')
        try:
            f = Fernet(self.key)
        except:
            if messagebox.askyesno('somthing Wrong','have problems with the key \nif you use password press return \nor would you generate a key file') == True:
                genKey()
            self.CBtnTxt.set('Crypt')
        
        else:
            try:
                name_file = self.getName(self.absPathFile)
                nameFile = name_file
                
            except:
                messagebox.showerror('Error', 'you need to browse file')
                self.CBtnTxt.set('Crypt')
            else:
                for k in range(0,4):
                    nameFile = nameFile[:-1]

                for word in listExt:
                    if word in name_file:
                        ext = word
                        break
                
                fileTCrypt= open(self.absPathFile, 'rb')
                TCrypt = fileTCrypt.read()
                fileTCrypt.close()

                cryptContent = f.encrypt(TCrypt)
                try:
                    fileCrypt = filedialog.asksaveasfile(title="Save Crypted file",filetypes=[("All file (let extension whitout .)", "*.")], initialfile=(f"{nameFile} crypted {ext}"))
                    
                    OfileCrypt = open(fileCrypt.name,'wb')
                    OfileCrypt.write(cryptContent)
                    OfileCrypt.close()
                except:
                    self.CBtnTxt.set('Crypt')
                self.CBtnTxt.set('Crypt')
                
    def decryptFile(self):
        self.DBtnTxt.set('Wait ...')
        try:
            f = Fernet(self.key)
        except:
            if messagebox.askyesno('Something Wrong','have problems with the key \nif you use password press return \nor would you generate a key file') == True:
                genKey()
            self.DBtnTxt.set('Decrypt')           
        else:
            try:
                name_file = self.getName(self.absPathFile)
            except:
                messagebox.showerror('Error', 'need to browse file')
            else:
                nameFile = name_file
                for k in range(0,4):
                    nameFile = nameFile[:-1] 
                
                for word in listExt:
                    if word in name_file:              
                        ext = '.'+word
                        break
                    else:
                        ext = ''          

                fileTDecrypt= open(self.absPathFile, 'rb')
                TDecrypt = fileTDecrypt.read()
                fileTDecrypt.close()
                try:
                    DecryptContent = f.decrypt(TDecrypt)
                except:
                    messagebox.showerror('Error', 'you use bad key or \nbad password retry')
                    self.DBtnTxt.set('Decrypt')
                else:
                    try:
                        nameFile = nameFile.replace('crypted', '')       
                    except:
                        pass
                    else:
                        try:
                            fileCrypt = filedialog.asksaveasfile(title="Save Decrypted file",filetypes=[("All file (GIVE EXTENSION if not in name)", "*.*")], initialfile=(f"{nameFile}decrypted{ext}"))
                            OfileDecrypt = open(fileCrypt.name,'wb')
                            OfileDecrypt.write(DecryptContent)
                            OfileDecrypt.close()
                        except:
                            self.DBtnTxt.set('Decrypt')
                        self.DBtnTxt.set('Decrypt')
                        try :
                            NDfile = fileCrypt.name
                        except:
                            pass
                        else:
                            RDname = self.getName(NDfile)
                            self.absPathFile = NDfile
                            self.lblBrowsefile.configure(text=RDname)
                            extDfile = self.getExtension(NDfile)                  
                            if extDfile == ".txt":
                                self.text_box.delete(1.0, "end")
                                self.text_box.insert(1.0, DecryptContent)
                            else:
                                self.text_box.delete(1.0, "end")
                                self.text_box.insert(1.0,"work just for .txt \nbtw is decrypted")

# Other Windows fonction
    #generate key file by password
    def afterKfile(self,e):
        password = self.entrypswd.get()
        lenPswd = len(password)
        if lenPswd < minCarMdp:
            self.labelEntry2.configure(text=f'min {minCarMdp} lenght')
        elif lenPswd >= minCarMdp:
            self.labelEntry2.configure(text='Ok')

            key = genKey(password)
            
            try:
                fileKey = filedialog.asksaveasfile(title="Create key",filetypes=[("key files","*.key")], defaultextension=".key", initialfile="Mykey")
            except:
                pass
            else:
                try:
                    filele = open(fileKey.name, "wb")
                except:
                    pass
                else:
                    filele.write(key)
                    filele.close()
                    self.window2.deiconify()
                    self.labelEntry2.configure(text='you can close me')
    #generate a random password
    """def CheckGenerate(self, e):
        size = self.entrySize.get()
        
        if size.isdigit() == True:
            size = int(size)

            if size > minCarMdp:
                self.lblSizeLeft.configure(text='Ok')              
                password = random_password1(size)

                self.TxtBoxPswd.delete(1.0, "end")
                self.TxtBoxPswd.insert(1.0, password)

            elif size <= minCarMdp:
                k = 8   - size
                self.lblSizeLeft.configure(text=f'adds min {k}')
            elif size > 90:
                self.lblSizeLeft.configure(text="Max 90")
        else:
            self.lblSizeLeft.configure(text='number only')"""

    def ShowEntryPswd(self):
        global l
        if l == 0:
            self.entrypswd.config(show="")
            l += 1
            self.seeTxt.set('hide')
        else:
            self.entrypswd.config(show="*")
            l = 0
            self.seeTxt.set('see')

l = 0
i = 0
