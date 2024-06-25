import tkinter as tk
from tkinter import messagebox
from generator import Generator

# Input from user
def add():
    username = entryName.get()
    website = entryWeb.get()
    
    if not website:
        messagebox.showerror("Error","Please input a website name")
        return
    
    if not username:
        messagebox.showerror("Error","Please input a username")
        return
    
    try:
        length = int(entryLength.get())
    except ValueError:
        messagebox.showerror("Error", "Password length must be an integer")
        return
    
    digits = varDigits.get()
    letters = varLetters.get()
    specialchars = varSpecialChars.get()
    
    try:
        password = generator.create_password(length, digits, letters, specialchars)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    if website and username and password:
        with open("passwords.txt", 'a') as f:
            f.write(f"{website} {username} {password}\n")
        messagebox.showinfo("Generated and Added Password", f"Generated and Added Password:\n\n{password}")
        
    else:
        messagebox.showerror("Error", "Please fill out all the fields")

def get():
    website = entryWeb.get().strip() 
    username = entryName.get().strip() 
    passwords = {}
    
    try:
        with open("passwords.txt", 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 3:  
                    site = parts[0]
                    user = parts[1]
                    pwd = ' '.join(parts[2:])
                    
                    if website and website == site:
                        if user in passwords:
                            passwords[user].append(pwd)
                        else:
                            passwords[user] = [pwd]
                    elif username and username == user:
                        if site in passwords:
                            passwords[site].append(pwd)
                        else:
                            passwords[site] = [pwd]
    except FileNotFoundError:
        messagebox.showerror("Error", "Passwords file not found")
        return
    except Exception as e:
        messagebox.showerror("Error", f"Error reading passwords: {e}")
        return

    if passwords:
        mess = "Your passwords:\n"
        for name, pwds in passwords.items():
            mess += f"For Username: {name}\n"
            for pwd in pwds:
                mess += f"  - Website: {website}, Password: {pwd}\n"
            mess += "\n"
        messagebox.showinfo("Passwords", mess)
    else:
        messagebox.showinfo("Passwords", "No passwords found for the specified website or username")


def getlist():
    passwords = {}
    try:
        with open("passwords.txt", 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 3: 
                    website = parts[0]
                    username = parts[1]
                    password = ' '.join(parts[2:])
                    passwords[(website, username)] = password
    except FileNotFoundError:
        messagebox.showerror("Error", "Passwords file not found")
        return
    except Exception as e:
        messagebox.showerror("Error", f"Error reading passwords: {e}")
        return

    if passwords:
        mess = "List of passwords:\n"
        for (website, username), password in passwords.items():
            mess += f"Website: {website}\nUsername: {username}\nPassword: {password}\n\n"
        messagebox.showinfo("Passwords", mess)
    else:
        messagebox.showinfo("Passwords", "Empty List !!")

def delete():
    username = entryName.get().strip()
    website = entryWeb.get().strip()
    temp_passwords = []

    try:
        with open("passwords.txt", 'r') as f:
            for k in f:
                parts = k.split()
                if len(parts) >= 3: 
                    current_website = parts[0]
                    current_username = parts[1]
                    current_password = ' '.join(parts[2:])
                    
                    if (website and website == current_website) or (username and username == current_username):
                        continue  
                    temp_passwords.append(f"{current_website} {current_username} {current_password.strip()}")

        with open("passwords.txt", 'w') as f:
            for line in temp_passwords:
                f.write(line + '\n')

        if username or website:
            messagebox.showinfo("Success", "Password(s) deleted successfully!")
        else:
            messagebox.showinfo("Success", "No passwords found for deletion.")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting password(s): {e}")

    
    
    
def deleteall():
    try:
        with open("passwords.txt", 'w') as f:
            f.write("") 
        messagebox.showinfo("Success", "All passwords deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting passwords: {e}")        

if __name__ == "__main__":
    generator = Generator()

    app = tk.Tk()
    app.geometry("800x400")
    app.title("Password Manager and Generator")
    
    
    labeltext = tk.Label(app, text="Note: to update password, enter in the website and username for the password you want to change then click add password again!")
    labeltext.grid(row=0, column=0, columnspan=3, padx=15, pady=15)

    labelWeb = tk.Label(app,text="WEBSITE:")
    labelWeb.grid(row=1,column=0,padx=15,pady=15)
    entryWeb = tk.Entry(app)
    entryWeb.grid(row=1, column=1, padx=15, pady=15)
    
    labelName = tk.Label(app, text="USERNAME:")
    labelName.grid(row=2, column=0, padx=15, pady=15)
    entryName = tk.Entry(app)
    entryName.grid(row=2, column=1, padx=15, pady=15)

    labelLength = tk.Label(app, text="LENGTH:")
    labelLength.grid(row=3, column=0, padx=10, pady=5)
    entryLength = tk.Entry(app)
    entryLength.grid(row=3, column=1, padx=10, pady=5)

    varDigits = tk.BooleanVar()
    checkDigits = tk.Checkbutton(app, text="Include Digits", variable=varDigits)
    checkDigits.grid(row=4, column=0, padx=10, pady=5)

    varLetters = tk.BooleanVar()
    checkLetters = tk.Checkbutton(app, text="Include Letters", variable=varLetters)
    checkLetters.grid(row=4, column=1, padx=10, pady=5)

    varSpecialChars = tk.BooleanVar()
    checkSpecialChars = tk.Checkbutton(app, text="Include Special Characters", variable=varSpecialChars)
    checkSpecialChars.grid(row=4, column=2, padx=10, pady=5)

    buttonAdd = tk.Button(app, text="Add Password", command=add)
    buttonAdd.grid(row=5, column=0, padx=15, pady=8, sticky="we")
    
    buttonGet = tk.Button(app, text="Get From Specific Website/Username", command=get)
    buttonGet.grid(row=5, column=1, padx=15, pady=8, sticky="we")

    buttonList = tk.Button(app, text="List All", command=getlist)
    buttonList.grid(row=6, column=0, padx=15, pady=8, sticky="we")

    buttonDelete = tk.Button(app, text="Delete From Specific Website/Username", command=delete)
    buttonDelete.grid(row=6, column=1, padx=15, pady=8, sticky="we")
    
    buttonDeleteAll = tk.Button(app, text="Delete All", command=deleteall)
    buttonDeleteAll.grid(row=6, column=2, padx=15, pady=8, sticky="we")
    app.mainloop()

