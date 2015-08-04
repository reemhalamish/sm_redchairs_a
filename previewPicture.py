__author__ = 'reem'
from Tkinter import Canvas, Label
from PIL import Image, ImageTk
from constants import *
w,h = SIZE_PREVIEW


class PreviewPicture(Canvas):
    def __init__(self, preview_id, img_path = PATH_BLANK_PICTURE, img_id = -1, master=None, cnf={}, **kw):
        Canvas.__init__(self, master=master, cnf=cnf, **kw)
        self.master = master
        self.img_id = img_id
        self.preview_id = preview_id

        imgfile = Image.open(PATH_BLANK_PICTURE)
        resized = imgfile.resize(SIZE_PREVIEW, Image.ANTIALIAS)
        self.imgtk = ImageTk.PhotoImage(resized)
        imgfile.close()


        self.create_image(0, 0, image=self.imgtk, tags = "IMG")
        self.configure(scrollregion= (-(w//2), -(h//2), (w//2), (h//2)))

        self.id_viewer = Label(self, text=str(preview_id), font = ("serif", 20), fg='red', bg='white')
        self.id_viewer.pack()
        self.create_window(w//2 - 10, h//2 - 10, window=self.id_viewer)

    def mirrorizeOtherPP(self, otherPP):
        self.img_id = otherPP.img_id
        self.delete("IMG")
        self.imgtk = otherPP.imgtk
        self.create_image(0,0,image = self.imgtk, tags = "IMG")
        self.configIdViewer()
        self.startDownAnimation()

    def showImageFromId(self, img_id):
        self.img_id = img_id
        self.delete("IMG")
        img = Image.open(get_picture_path(img_id))
        resized = img.resize(SIZE_PREVIEW, Image.ANTIALIAS)
        self.imgtk = ImageTk.PhotoImage(resized)
        self.create_image(0, 0, image=self.imgtk, tags = "IMG")
        img.close()
        self.configIdViewer()

    def configIdViewer(self):
        self.id_viewer.config(text = str(self.img_id % (NUMBER_OF_PREVIEW_PICS + 1) + 1))

    def getPath(self):
        return get_picture_path(self.img_id)

    def startDownAnimation(self):
        return # TODO: maybe not even needed
        print "starting...", str(self.preview_id)
        moveX, moveY  = 0, -DIM_PREVIEW_HEIGHT
        self.move(self.id_viewer, moveX, moveY)
        self.move(self.imgtk, moveX, moveY)
        self.after(50, PreviewPicture.move_down, (self,DIM_PREVIEW_HEIGHT))
        print "finished...",  str(self.preview_id)


    ''' move the picture down a little bit '''
    def move_down(self, n):
        if (n <= 0):
            return
        moveX, moveY  = 0, 20
        self.move(self.id_viewer, moveX, moveY)
        self.move(self.imgtk, moveX, moveY)
        self.after(50, PreviewPicture.move_down, (self, n - moveY))

