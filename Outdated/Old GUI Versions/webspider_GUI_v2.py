'''
	Web Spider GUI: 
	Status: ???
        Written By Ahmed Mused Yahya

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!! Use NLTK/machine learning to learn a topic, search the web and find information (web pages), to send to you for brainstorming.!!!!
    !!!! Think Search Engine but you don't even have to input a query. Just a topic. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''

from tkinter import *
from webspider_v3 import *

#def update():
#	root.after(3000, update)

def fetch_spider():
	url = urlText.get("1.0",END)
	search_phrase = wordText.get("1.0",END)
	if url == "Enter URL Here...":
		return
	else:
		urlText.config(bg='white')
	if search_phrase == "Enter Search Text Here...":
		return
	else:
		wordText.config(bg='white')
	
	Spider(url, search_phrase)
	restore_defaults()
	return

def clearURLText(event):
	url = urlText.get("1.0",END)
	if "Enter URL Here..." in url:
		urlText.delete("1.0",END)
	return

def clearWordText(event):	
	search_phrase = wordText.get("1.0",END)
	if "Enter Search Text Here..." in search_phrase:	
		wordText.delete("1.0",END)
	return

def urlText_select_all(event):
	urlText.tag_add(SEL, "1.0", END)
	urlText.mark_set(INSERT, "1.0")
	return

def wordText_select_all(event):
	wordText.tag_add(SEL, "1.0", END)
	wordText.mark_set(INSERT, "1.0")
	return

def restore_defaults():
	url = urlText.get("1.0",END)
	if len(url) == 1:
		urlText.insert(END, "Enter URL Here...")
	search_phrase = wordText.get("1.0",END)
	if len(search_phrase) == 1:	
		wordText.insert(END, "Enter Search Text Here...")

root = Tk()
root.resizable(width=True, height=False)
root.geometry('{}x{}'.format(600, 230))
root.wm_title("Oracle Spider")
root.config(bg='white')

frame = Frame(root, bg='white')
#*********** Title Frame: Begin ************
title_frame = Frame(frame, bg='white')
title_font=('Helvetica', 30, 'bold')
title_label = Label(title_frame, text="Oracle Web Spider", bg='white', font=title_font)
logo = PhotoImage(file="GUI Elements/spider_logo.png").subsample(5,5)
logo_label = Label(title_frame, image=logo, bg='white')

title_label.grid(row=0,column=0, padx=50, sticky=N+S+E+W)
logo_label.grid(row=0,column=1, sticky=N+S+E+W)
title_frame.pack()
#************ Title Frame: End ***********
custom_font=('Helvetica', 18)

urlText = Text(frame, width=42, height=1, font=custom_font, relief=RAISED)
urlText.insert(END, "Enter URL Here...")
urlText.bind('<Button-1>', clearURLText)
urlText.bind('<Button-2>', urlText_select_all)

#************* Word & Crawl Frame: Begin *************
word_crawl_frame = Frame(root, bg='white')

wordText = Text(word_crawl_frame, width=32, height=1, font=custom_font, relief=RAISED)
wordText.insert(END, "Enter Search Text Here...")
wordText.bind('<Button-1>', clearWordText)
wordText.bind('<Button-2>', wordText_select_all)

searchButton = Button(word_crawl_frame, width=12, text="Crawl", bg='white', cursor='spider', command=fetch_spider)

wordText.grid(row=0,column=0, sticky=N+S+W)
searchButton.grid(row=0,column=1, padx=3, sticky=N+S+E)

#************* Word & Crawl Frame: End ************

title_frame.grid(row=0,column=0, sticky=N+S+E+W)
urlText.grid(row=1,column=0, pady=5, sticky=N+S+E+W)
#word_crawl_frame.grid(row=0,column=0, pady=5, sticky=N+S+E+W)
#wordText.grid(row=2,column=0, pady=5, sticky=N+S+E+W)
#searchButton.grid(row=4, column=0, ipadx=40, sticky=E)
# Add Elements Here

frame.pack(side=TOP, pady=5)
word_crawl_frame.pack(side=TOP)
#update()
root.mainloop()