#!/usr/bin/env python
# coding: utf-8

# # <u>Image Manipulator GUI Using Tkinter</u>

# In[5]:


import tkinter as tk
from tkinter import filedialog
import numpy as np
import cv2
from PIL import Image, ImageTk

from backEnd.imgEnhance import Enhance

class MainApp:
    def __init__(self, master):
        self.master = master
        
        self.im = None
        self.imgTk = None
        self.im2 = None
        self.imgTk2 = None
        self.rect = None
        self.xStart = None
        self.yStart = None
        self.x = 0
        self.y = 0
        
        # variable to determine which function the box drawing feature performs
        self.boxMode = 'enhance'
        
        # creates an instance of the Enhance class for use in image enhancement
        self.enhancer = Enhance()
        
        # creates Canvas object to contain the image manipulation view
        self.imgView = tk.Canvas(self.master, width=1280,
                                 height=720, bg="black", cursor="cross")
        # places the image manipluation Canvas in the top-left of the application window
        self.imgView.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W+tk.N)
        
        # creates a horizontal scrollbar and places it beneath the image view
        self.hbar=tk.Scrollbar(self.master,orient=tk.HORIZONTAL)
        self.hbar.grid(column=0, row=1, padx=10, columnspan=1, sticky=tk.W+tk.E)
        
        # creates a vertical scrollbar and places it on the right of the image view
        self.vbar=tk.Scrollbar(self.master,orient=tk.VERTICAL)
        self.vbar.grid(column=1, row=0, pady=10, rowspan=1, sticky=tk.N+tk.S+tk.W)
        
        # configures the scrollbars to control the scrolling of the image view Canvas
        self.hbar.config(command=self.imgView.xview)
        self.vbar.config(command=self.imgView.yview)
        self.imgView.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        
        # creates a button that is tied to the method to load an image into the image view canvas
        self.fileBtn = tk.Button(self.master, text="LOAD IMAGE", height=4, width=25, command=self.load_image, bg='#cbcace')
        self.fileBtn.grid(column=0, row=3, padx=50, pady=25, sticky=tk.W+tk.S)
        
        # creates a button that is tied to the method to save the current view in the image view canvas to file
        self.saveBtn = tk.Button(self.master, text="SAVE IMAGE", height=4, width=25, command=self.save_image, bg='#cbcace')
        self.saveBtn.grid(column=0, row=3, padx=275, pady=25, sticky=tk.W+tk.S)
        
        # creates a button that is tied to the method to zoom in on the image in the image view
        self.zoomInBtn = tk.Button(self.master, text="ZOOM IN", height=2, width=25, command=self.zoom_image_in, bg='#cbcace')
        self.zoomInBtn.grid(column=3, row=0, padx=20, pady=120, sticky=tk.S+tk.W)
        
        # creates a button that is tied to the method to zoom out on the image in the image view
        self.zoomOutBtn = tk.Button(self.master, text="ZOOM OUT", height=2, width=25, command=self.zoom_image_out, bg='#cbcace')
        self.zoomOutBtn.grid(column=3, row=0, padx=20, pady=70, sticky=tk.S+tk.W)
        
        # creates a button that is tied to the method to upscale the image in the image view
        self.upscaleBtn = tk.Button(self.master, text="UPSCALE FULL IMAGE", height=4, width=25, command=self.upscale_image, bg='#cbcace')
        self.upscaleBtn.grid(column=3, row=0, padx=20, pady=20, sticky=tk.W+tk.N)
        
        # creates a button that is tied to the method to change the function of the box drawing feature
        self.boxModeButton = tk.Button(self.master, text="MODE: ZOOM & ENHANCE", height=4, width=25, command=self.toggle_box_mode, bg='#cbcace')
        self.boxModeButton.grid(column=3, row=0, padx=20, pady=120, sticky=tk.W+tk.N)
        
        # binds certain button events taking place within the image view canvas to the handling functions
        # left click, drag and release
        self.imgView.bind("<ButtonPress-1>", self.imgView_on_left_click)
        self.imgView.bind("<B1-Motion>", self.imgView_on_move_left_click)
        self.imgView.bind("<ButtonRelease-1>", self.imgView_on_left_click_release)
        
        # right click, drag and release
        self.imgView.bind("<Button-3>", self.imgView_on_right_click)
        self.imgView.bind("<B3-Motion>", self.imgView_on_move_right_click)
        self.imgView.bind("<ButtonRelease-3>", self.imgView_on_right_click_release)
        
    # method to toggle which function the box drawing feature performs
    def toggle_box_mode(self):
        if self.boxMode == 'enhance':
            self.boxMode = 'zoomOnly'
            self.boxModeButton.config(text="MODE: ZOOM ONLY")
        elif self.boxMode == 'zoomOnly':
            self.boxMode = 'enhance'
            self.boxModeButton.config(text="MODE: ZOOM & ENHANCE")
    
    # method to load an image file into the imgView Canvas
    def load_image(self):
        
        # reset attributes when new image is loaded
        # consider making child variable for photo image
        self.im = None
        self.imgTk = None
        self.im2 = None
        self.imgTk2 = None
        self.rect = None
        self.xStart = None
        self.yStart = None
        self.x = 0
        self.y = 0
        
        # opens a file selection window to allow user to pick image file
        # filetypes arguement ensures only files with certain extensions can be opened
        path = filedialog.askopenfilename(
            title="Load Image File...",
            filetypes=[('image files', ('.png', '.jpg'))])
        
        if len(path) > 0:
            # loads the given filepath as a cv2 image
            img = cv2.imread(path)

            # set scrollable region to image size
            self.imgView.config(scrollregion=[0,0,img.shape[1],img.shape[0]])

            blue,green,red = cv2.split(img)
            img = cv2.merge((red,green,blue))
            self.im = Image.fromarray(img)
            self.imgTk = ImageTk.PhotoImage(image=self.im)
            self.imgView.create_image(0, 0, image=self.imgTk, anchor=tk.NW)
    
    # method to save the current image in the imgView canvas to file
    def save_image(self):
        path = filedialog.asksaveasfile(
            mode='w', defaultextension=".png",
            filetypes=(
                #("PNG file", "*.png"),
                ("JPEG file", "*.jpg"),
                ("All Files", "*.*")
            )
        )
        
        if path:
            self.im.save(path)
            
    def upscale_image(self):
        self.im = self.enhancer.upscaleImage(self.im)
        self.imgTk = ImageTk.PhotoImage(image=self.im)
        self.imgView.config(scrollregion=[0, 0, self.imgTk.width(), self.imgTk.height()])
        self.imgView.create_image(0, 0, image=self.imgTk, anchor=tk.NW)
            
    def zoom_image_in(self):
        self.im = self.im.resize((round(self.imgTk.width() * 1.05),
                             round(self.imgTk.height() * 1.05)))
        self.imgTk = ImageTk.PhotoImage(image=self.im)
        self.imgView.config(scrollregion=[0, 0, self.imgTk.width(), self.imgTk.height()])
        self.imgView.create_image(0, 0, image=self.imgTk, anchor=tk.NW)

    def zoom_image_out(self):
        self.im = self.im.resize((round(self.imgTk.width() * 0.95), round(self.imgTk.height() * 0.95)))
        self.imgTk = ImageTk.PhotoImage(image=self.im)
        self.imgView.config(scrollregion=[0, 0, self.imgTk.width(), self.imgTk.height()])
        self.imgView.create_image(0, 0, image=self.imgTk, anchor=tk.NW)

    def imgView_on_left_click(self, event):
        self.xStart = self.imgView.canvasx(event.x)
        self.yStart = self.imgView.canvasy(event.y)
        if not self.rect:
            self.rect = self.imgView.create_rectangle(self.x, self.y, 1, 1, outline="red", width=5, tags="rect")

    def imgView_on_move_left_click(self, event):
        curX = self.imgView.canvasx(event.x)
        curY = self.imgView.canvasy(event.y)
        self.imgView.coords(self.rect, self.xStart, self.yStart, curX, curY)

        # ensures height and width are greater than 0
        # allows bounding to drawn in every possible direction
        if (curX < self.xStart and curY < self.yStart):
            self.im2 = self.im.crop((curX, curY, self.xStart, self.yStart))
        elif (curX < self.xStart):
            self.im2 = self.im.crop((curX, self.yStart, self.xStart, curY))
        elif (curY < self.yStart) :
            self.im2 = self.im.crop((self.xStart, curY, curX, self.yStart))
        else:
            self.im2 = self.im.crop((self.xStart, self.yStart, curX, curY))

        self.imgTk2 = ImageTk.PhotoImage(self.im2)

    def imgView_on_left_click_release(self, event):
        
        # image will not crop and zoom if the mouse wasn't dragged
        if self.im2 != None:
            if self.boxMode == 'enhance':
                self.im = self.enhancer.upscaleImage(self.im2)
            elif self.boxMode == 'zoomOnly':
                self.im = self.im2.resize((round(self.imgTk2.width() * 3), round(self.imgTk2.height() * 3)))
            
            self.imgTk = ImageTk.PhotoImage(image=self.im)
            self.imgView.config(scrollregion=[0, 0, self.imgTk.width(), self.imgTk.height()])
            self.imgView.create_image(0, 0, image=self.imgTk, anchor=tk.NW)      
        
        self.imgView.delete("rect")
        self.rect = None
        
    def imgView_on_right_click(self, event):
        
        self.imgView.config(yscrollincrement=1.5) 
        self.imgView.config(xscrollincrement=1.5)
        
        self.xStart = event.x
        self.yStart = event.y
        
        self.imgView.config(cursor="fleur")
        
    def imgView_on_move_right_click(self, event):
        
        xDiff = round(event.x - self.xStart)
        yDiff = round(event.y - self.yStart)
        
        self.imgView.xview('scroll', xDiff, 'units')
        self.imgView.yview('scroll', yDiff, 'units')
        
        self.xStart = event.x
        self.yStart = event.y
        
    def imgView_on_right_click_release(self, event):
        self.imgView.config(xscrollincrement=0) 
        self.imgView.config(yscrollincrement=0)
        self.imgView.config(cursor="cross")

def main():
    rootScreen = tk.Tk()
    rootScreen.title('Image Manipulator Concept')
    rootScreen.geometry("1600x900")
    rootScreen.configure(bg="#6082B6")
    app = MainApp(rootScreen)
    rootScreen.mainloop()

if __name__ == '__main__':
    main()
