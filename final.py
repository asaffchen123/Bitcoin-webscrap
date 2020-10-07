from tkinter import*
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
import smtplib
import re
from time import sleep
from secret import mail,password,hd,rmail
import sys
import os


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


"""
background and program setup
"""
root=tk.Tk()
root.title("Bitcoin Tracker")
root.geometry("900x506")
x=IntVar()

pricer=[]
pricen=[]

C=Canvas(root, bg="grey", height=900, width=506)
filename=ImageTk.PhotoImage(Image.open(r"C:\Users\Home\Documents\studying\webscraperpython\wallpaper.jpg"))
background_label=Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()


"""
labels and entries
"""

label1=tk.Label(root,text="Time between each search: ",font="Helvetica 12 bold",fg="white",bg="#081E2C")
label1.place(x=130,y=10)
entry1=tk.Entry(root,textvariable=x)
entry1.place(x=355,y=10,height=23,width=200)

label2=tk.Label(root,text="",font="Helvetica 8 bold",fg="white",bg="#081E2C")
label2.place(x=0,y=100)
label3=tk.Label(root,text="",font="Helvetica 12 bold",fg="white",bg="#07253D")
label3.place(x=350,y=350)

"""
the inital scrape function
"""
def scrape():
    wt=x.get()
    url="https://cointelegraph.com/bitcoin-price-index"
    headers= hd
    page=requests.get(url,headers=headers)

    soup=BeautifulSoup(page.content,"html.parser")

    total_price=soup.find("div",class_="summaryData").get_text()
    label2.config(text=total_price)    
    but2.place(x=400,y=150)
    
    url="https://cointelegraph.com/bitcoin-price-index"
    headers= hd
       
    page=requests.get(url,headers=headers)

    soup=BeautifulSoup(page.content,"html.parser")
    price=soup.find("span",class_="price-value").get_text()[1:].strip().replace(',','')
    non_decimal = re.compile(r'[^\d.]+')
    fprice=int(non_decimal.sub('', price))
    pricer.append(fprice)
    
"""
when pressing continue will start the conti function, it search for the price itself 
makes it an integer and divide it by 90% ,after wards it compares it with the new price we got,
if the new price is equal or lower than 90% of the original price, it emails us then restarts the program
to prevent self spam 
"""
def conti():
    wt=x.get()
    url="https://cointelegraph.com/bitcoin-price-index"
    headers= hd
    page=requests.get(url,headers=headers)

    soup=BeautifulSoup(page.content,"html.parser")
    price2=soup.find("span",class_="price-value").get_text()[1:].strip().replace(',','')
    non_decimal = re.compile(r'[^\d.]+')
    fprice2=int(non_decimal.sub('', price2))
    fprice3=float(fprice2*0.9)
    pricen.append(fprice3)
    
    label3.config(text=("Current price is:",price2))
    
    URL="https://cointelegraph.com/bitcoin-price-index"
    if pricer[0] <= pricen[0]: 
        server = smtplib.SMTP('smtp.gmail.com',587)                     
        server.ehlo()
        server.starttls()
        server.ehlo()                      
        server.login(mail,password)                        
        subject = 'Price fell down by 10 percent for bitcoin'
        body = 'data from: '+URL
        msg = f"Subject:{subject}\n\n{body}"     
        server.sendmail(mail,rmail,msg)         
        server.quit()
        restart_program()
    root.after(wt*60,conti)
    


but=tk.Button(root,text="Initialize",font="Helvetica 12",anchor="center",justify=CENTER,command=scrape)
but.place(x=1,y=50,width=898)

but2=tk.Button(root,text="Continue?",font="Helvetica 12",anchor="center",justify=CENTER,command=conti)
wt=x.get()

    
clear_button=tk.Button(root,text="Restart",font="Helvetica 12",anchor="center",justify=CENTER,command=restart_program)
clear_button.place(x=355,y=450,width=200)

root.mainloop()
"""
since its tkinter and we cant use whileloops, root.after makes another loop while the mainloops runs 
so the program will update itself without freezing
"""
root.after(wt*60,conti)



