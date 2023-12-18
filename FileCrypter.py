import customtkinter
from tkinter import *
from tkinter import filedialog as fd
import os
import ctypes
from cryptography.fernet import Fernet, InvalidToken

# Increases the dpi of the window
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Set the appearance mode and the default color theme
customtkinter.set_appearance_mode("Dark")  
customtkinter.set_default_color_theme("blue")  

# Configure the window
app = customtkinter.CTk() 
app.geometry("800x300")
app.resizable(True, True)
app.title("File Crypter")
app.iconbitmap("file_crypter/icon.ico")

# Generate a key
key = Fernet.generate_key()

# Select a file
def file_select():
    global filePath
    filetypes = (
        ('All files', '*.*'), # if you want to add more file types, just add a comma and a new tuple like this: ('Python files', '*.py')
    )
    filePath = fd.askopenfilename(
        title='Select a file',
        initialdir='/',
        filetypes=filetypes)
        
    change_fileNameTxt(filePath)
    change_filePathTxt(filePath)
    change_consoleTxt('') 
       
# Encrypt the file 
# Open file with read-binary mode, encrypt it, and write it with write-binary mode
def Encrypt():
    try:
        with open("thekey.key","wb") as thekey: # wb = write binary/bytes
            thekey.write(key)
            
        with open(filePath, "rb") as thefile: # rb = read binary/bytes 
                content = thefile.read()

        content_encrypted = Fernet(key).encrypt(content)
        
        with open(filePath, "wb") as thefile: 
            thefile.write(content_encrypted)
             
        print("Encrypted")
        change_consoleTxt('File is encypted.')
        
    except NameError:
        print("File is not selected.")
        change_consoleTxt('File is not selected.')
    except InvalidToken:
        print("File is already encrypted.")
        change_consoleTxt('File is already encrypted.')
    except FileNotFoundError: #if the user closes the file dialog without selecting a file
        print("File is not selected.")
        change_consoleTxt('File is not selected.')
    except Exception as e: #other errors is mostly because of the permission
        print(f"Unexpected Error: \n {e}")
        change_consoleTxt('Unexpected Error!\n(or this user has no permission to\nencrypt this file)')

# Decrypt the file
def Decrypt():
    try:
        with open("thekey.key", "rb") as key:
            secretkey = key.read() 
        
        with open(filePath, "rb") as thefile: 
            contents = thefile.read()
            
        contents_decrypted = Fernet(secretkey).decrypt(contents)
        
        with open(filePath, "wb") as thefile:
            thefile.write(contents_decrypted)
    
        print("Decrypted")
        change_consoleTxt('File is decrypted.')
        
    except NameError:
        print("File is not selected.")
        change_consoleTxt('File is not selected.')
    except InvalidToken:
        print("File is already decrypted.") 
        change_consoleTxt('File is already decrypted.')
    except FileNotFoundError:
        print("File is not selected.")
        change_consoleTxt('File is not selected.')
    except ValueError as ve:
        print(f"ValueError: {ve} / key is incorrect")
        change_consoleTxt('Key is wrong!')
    except Exception as e:
        print(f"Unexpected Error: \n {e}")
        change_consoleTxt('Unexpected Error!\n(or this user has no permission to\ndecrypt this file)')

# Change the text of the labels
def change_fileNameTxt(txt):
    fileNameTxt.configure(text='File Name: ' + os.path.basename(txt)) #os.path.basename() returns the file name
def change_filePathTxt(txt):
    filePathTxt.configure(text='File Path: ' + txt)
def change_consoleTxt(txt):
    consoleTxt.configure(text=txt)

# Create the widgets
fileButton = customtkinter.CTkButton(master=app, text="Select File", command=file_select)
fileButton.grid(row=0, column=0, padx=10, pady=10)

fileNameTxt = customtkinter.CTkLabel(master=app, text="No file selected")
fileNameTxt.grid(row=1, column=2, padx=10, pady=10)

filePathTxt = customtkinter.CTkLabel(master=app, text="No file selected")
filePathTxt.grid(row=2, column=2, padx=10, pady=10)

encryptButton = customtkinter.CTkButton(master=app, text="Encrypt", command=Encrypt)
encryptButton.grid(row=3, column=1, padx=10, pady=20)

decryptButton = customtkinter.CTkButton(master=app, text="Decrypt", command=Decrypt)
decryptButton.grid(row=3, column=3, padx=10, pady=20)

consoleTxt = customtkinter.CTkLabel(master=app, text=" ")
consoleTxt.grid(row=4, column=0, padx=0, pady=10)

# Run the application
app.mainloop()