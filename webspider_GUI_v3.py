'''
	Web Spider GUI: 
	Status: ???
        Written By Ahmed Mused Yahya

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!! Use NLTK/machine learning to learn a topic, search the web and find information (web pages), to send to you for brainstorming.!!!!
    !!!! Think Search Engine but you don't even have to input a query. Just a topic. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''

from tkinter import *
from webspider_v5 import *
import sys

class App:
	def __init__(self):
		self.root = Tk()
		self.root.resizable(width=True, height=False)
		self.root.geometry('{}x{}'.format(600, 230))
		self.root.wm_title("Oracle Spider")
		self.root.config(bg='white')

		frame = Frame(self.root, bg='white')
		#*********** Title Frame: Begin ************h
		self.title_frame = Frame(frame, bg='white')
		title_font=('Helvetica', 30, 'bold')
		title_label = Label(self.title_frame, text="Oracle Web Spider", bg='white', font=title_font)
		self.logo = PhotoImage(file="Spider GUI/GUI Elements/spider_logo.png").subsample(5,5)
		self.logo_label = Label(self.title_frame, image=self.logo, bg='white')

		title_label.grid(row=0,column=0, padx=50, sticky=N+S+E+W)
		self.logo_label.grid(row=0,column=1, sticky=N+S+E+W)
		self.title_frame.pack()
		#************ Title Frame: End ***********
		custom_font=('Helvetica', 18)

		self.urlText = Text(frame, width=42, height=1, font=custom_font, relief=RAISED)
		self.urlText.insert(END, "Enter URL Here...")
		#************* Word & Crawl Frame: Begin *************
		self.word_crawl_frame = Frame(self.root, bg='white')

		self.wordText = Text(self.word_crawl_frame, width=32, height=1, font=custom_font, relief=RAISED)
		self.wordText.insert(END, "Enter Search Text Here...")

		self.searchButton = Button(self.word_crawl_frame, width=12, text="Search", bg='white', cursor='spider', command=self.fetch_spider)

		self.wordText.grid(row=0,column=0, sticky=N+S+W)
		self.searchButton.grid(row=0,column=1, padx=3, sticky=N+S+E)

		#************* Word & Crawl Frame: End ************

		self.title_frame.grid(row=0,column=0, sticky=N+S+E+W)
		self.urlText.grid(row=1,column=0, pady=5, sticky=N+S+E+W)

		frame.pack(side=TOP, pady=5)
		self.word_crawl_frame.pack(side=TOP)
		self.create_binding()
		self.run_main()

	def create_binding(self):
		self.urlText.bind('<Button-1>', self.clear_URLText)
		self.urlText.bind('<Button-2>', self.urlText_select_all)
		self.wordText.bind('<Button-1>', self.clear_wordText)
		self.wordText.bind('<Button-2>', self.wordText_select_all)

	def run_main(self):
		self.root.mainloop()

	def fetch_spider(self):
		url = self.urlText.get("1.0",END)
		search_phrase = self.wordText.get("1.0",END)
		if url == "Enter URL Here...":
			return
		else:
			self.urlText.config(bg='white')
		if search_phrase == "Enter Search Text Here...":
			return
		else:
			self.wordText.config(bg='white')
		
		Spider(url, search_phrase)
		self.restore_defaults()
		return

	def clear_URLText(self, event):
		url = self.urlText.get("1.0",END)
		if "Enter URL Here..." in url:
			self.urlText.delete("1.0",END)
		return

	def clear_wordText(self, event):	
		search_phrase = self.wordText.get("1.0",END)
		if "Enter Search Text Here..." in search_phrase:	
			self.wordText.delete("1.0",END)
		return

	def urlText_select_all(self, event):
		self.urlText.tag_add(SEL, "1.0", END)
		self.urlText.mark_set(INSERT, "1.0")
		return

	def wordText_select_all(self, event):
		self.wordText.tag_add(SEL, "1.0", END)
		self.wordText.mark_set(INSERT, "1.0")
		return

	def restore_defaults(self):
		url = self.urlText.get("1.0",END)
		if len(url) == 1:
			self.urlText.insert(END, "Enter URL Here...")
		search_phrase = self.wordText.get("1.0",END)
		if len(search_phrase) == 1:	
			self.wordText.insert(END, "Enter Search Text Here...")

App()
