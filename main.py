import requests
from bs4 import BeautifulSoup
import csv
import tkinter
import time
from tkinter import ttk


win = tkinter.Tk()
win.geometry('800x200')
userVar = tkinter.StringVar()

win.grid_columnconfigure(0, weight=1)
win.grid_rowconfigure(0, weight=1)

text = tkinter.Text(win,height=200)
scrollbar = ttk.Scrollbar(win,orient='vertical',command=text.yview)



def cmd():
    userid = userVar.get() or 'karnavthakur2908'
    url = f'https://csgobackpack.net/index.php?nick={userid}&currency=USD'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}
    

    r = requests.get(url=url)#,headers=headers)
    
    soup = BeautifulSoup(r.text,features='html.parser')

    text.grid(row=0,column=0,sticky=tkinter.EW)
    
    scrollbar.grid(row=0,column=2,sticky=tkinter.NS)

    text['yscrollcommand'] = scrollbar.set

    well = soup.find('title')

    if well.text == 'Error - Inventory Value':
        tkinter.Label(win,text="User doesn't exist").grid()
        time.sleep(3)

    names = [i.text for i in soup.findAll('td',attrs={'class':'tablename'})]
    prices =[i.text for i in soup.findAll('td',attrs={'class':'tableprice'})]
    amount = [i.text for i in soup.findAll('td',attrs={'class':'tableamount'})]

    data = list(zip(names,prices,amount))

    prices = [float(i.split('$')[1]) for i in prices]
    amount = [int(i) for i in amount]

    prices_data = list(zip(prices,amount))

    total = sum([i*j for i,j in prices_data])

    userLabel.grid_forget()
    invButton.grid_forget()
    userEntry.grid_forget()

    with open(f'{userid}.csv','w') as f:
        writer = csv.writer(f,lineterminator='\r')
        writer.writerow(['Name','Price','Amount'])

        pos = 1

        for i in range(len(data)):
            position = f"{i+1}.0"
            pos+=1
            text.insert(index=position,chars=f"{i+1}. {data[i]}\n\n")
            
            writer.writerow([names[i],prices[i],amount[i]])
        text.insert(index=f"{pos+1}.0",chars=f"Total : {total}")
        writer.writerow(["Total",f"${total}"])

    backButton.grid(column=1)

userLabel = tkinter.Label(win,text='Enter user ID : ')
userEntry = tkinter.Entry(win,textvariable=userVar)
invButton = tkinter.Button(win,text='Get Inventory',command=cmd)
exitButton = tkinter.Button(win,text="Exit",command=win.destroy)
userLabel.grid()
userEntry.grid()
invButton.grid()
exitButton.grid(column=0)

def back():
    text.grid_forget()
    backButton.grid_forget()
    exitButton.grid_forget()
    scrollbar.grid_forget()
    
    userLabel.grid()
    userEntry.grid()
    invButton.grid()
    exitButton.grid()
    

backButton = tkinter.Button(win,text='Back',command=back)

win.mainloop()


