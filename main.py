from debian.debian_support import download_file
from mercurial.pathutil import pathauditor

__author__ = 'reem'


import Tkinter as tk
import cv2
import cv2.cv as cv
from PIL import Image, ImageTk
from constants import *
from previewPicture import PreviewPicture
from downtextFrame import DowntextFrame
from os import system as executeOrder
from uploadOneFile import uploadToGoogleDriveServerWithDaemon
from basic_html_server import init_server_on_different_thread, get_download_url, close_server
import threading

current_image = camera_imgtk = camera1_imgtk = camera2_imgtk = downtext_frame = cap = None
current_id, seconds_since_last_snapshot, current_clock_cicle, frames_left_to_camera_png = 0, 0, 0, 0


root = picture_streaming_label = preview_frame = None
preview_pics_canvases = []

def clock():
    global current_clock_cicle, seconds_since_last_snapshot, frames_left_to_camera_png, downtext_frame

    current_clock_cicle = (current_clock_cicle + 1) % TIME_CLOCK_CICLES_IN_SEC
    if not current_clock_cicle: # once every passing second (or very close to it)
        seconds_since_last_snapshot += 1
        downtext_frame.update_countdown(TIME_SECONDS_FOR_CAPTURE_SNAPSHOT_CIRCLE - seconds_since_last_snapshot) # seconds left
        if seconds_since_last_snapshot == TIME_SECONDS_FOR_CAPTURE_SNAPSHOT_CIRCLE:
            take_snapshot()
            seconds_since_last_snapshot = 0
            frames_left_to_camera_png = TIME_HOW_MANY_FRAMES_SHOW_CAMERA_PNG_ON_STREAM


    show_frame() # update the stream
    root.after(TIME_CLOCK_CICLE_MS, clock)


def init_clock():
    global root
    root.after(TIME_CLOCK_CICLE_MS, clock)

def init_gui():
    global current_id, root, picture_streaming_label, preview_pics_canvases, preview_frame, camera_imgtk, camera1_imgtk, camera2_imgtk, downtext_frame


    # load next id
    f = open(PATH_PROPERTY_CUR_ID, "r")
    current_id = int(f.readline())
    f.close()

    #                   ~*~ make the tkinter window look well ~*~
    # root
    root = tk.Tk()
    root.bind('<Escape>', quit_everything)

    # streaming
    picture_streaming_label = tk.Label(root)
    picture_streaming_label.grid(row = 0, column = 0, sticky = 'NW')

    # FIFO of thunbnails
    preview_frame = tk.Frame(root)
    preview_frame.grid(row = 0, column = 1, rowspan = 2, sticky = 'NE')
    w,h = SIZE_PREVIEW
    img = Image.open(PATH_BLANK_PICTURE)
    thunbnail = img.resize(SIZE_PREVIEW, Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(thunbnail)
    img.close()


    for index in range(NUMBER_OF_PREVIEW_PICS):
        pic_canvas = PreviewPicture(master = preview_frame, preview_id=index, bd=10, highlightthickness=0, height = h, width = w)
        pic_canvas.grid(row = index, column = 0, sticky = 'N')
        preview_pics_canvases.append(pic_canvas)

    for img_id, preview_canvas in zip(reversed(range(current_id)),preview_pics_canvases):
        print "img_id is", img_id
        preview_canvas.showImageFromId(img_id)

    # countdown frame
    downtext_frame = DowntextFrame(root)
    downtext_frame.grid(row = 1, column = 0)

    # prepare the camera background
    camera_png = Image.open(PATH_CAMERA_PICTURE)
    camera_resized = camera_png.resize(SIZE_STREAMING, Image.ANTIALIAS)
    camera_imgtk = ImageTk.PhotoImage(camera_resized)
    camera_png.close()

    # prepare the camera animation
    camera_png = Image.open(PATH_CAMERA_PICTURE1)
    camera_resized = camera_png.resize(SIZE_STREAMING, Image.ANTIALIAS)
    camera1_imgtk = ImageTk.PhotoImage(camera_resized)
    camera_png.close()

    camera_png = Image.open(PATH_CAMERA_PICTURE2)
    camera_resized = camera_png.resize(SIZE_STREAMING, Image.ANTIALIAS)
    camera2_imgtk = ImageTk.PhotoImage(camera_resized)
    camera_png.close()


def init_camera():
    global cap
    width, height = SIZE_STREAMING # for the main stream on the screen
    cap = cv2.VideoCapture(WEBCAM_ID)
    print "setting..."
    cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, height)




def show_frame(camera = False):
    global current_image, picture_streaming_label, frames_left_to_camera_png
    if frames_left_to_camera_png > 0:
        camera_tk = camera2_imgtk if frames_left_to_camera_png % 2 else camera1_imgtk
        frames_left_to_camera_png -= 1
        picture_streaming_label.imgtk = camera_tk
        picture_streaming_label.configure(image=camera_tk)
        return

    _, frame = cap.read()
    frame = cv2.flip(frame, 0)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image) # TODO here will be the added another layer of the images that creates the snapshot
    # resized = img.resize(SIZE_STREAMING, Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img)
    picture_streaming_label.imgtk = imgtk
    picture_streaming_label.configure(image=imgtk)
    current_image = frame

def take_snapshot():
    global current_image, current_id

    if current_image == None: return

    # save as file
    filename = get_picture_path(current_id)
    cv2.imwrite(filename,current_image)

    # save the museum logo above
    background = Image.open(filename)
    foreground = Image.open(PATH_MUSEUM_LOGO)

    bw, bh = background.size
    posy = max(0, bh - DIM_MUSEUM_LOGO_HEIGHT) # put the logo on the bottom of the picture
    posx = 0 # put it in the middle
    background.paste(foreground, (posx,  posy), foreground)
    background.save(filename)

    widget_id = get_view_id_from_picture_id(current_id)
    print filename
    print get_download_url(current_id), "is on preview id", widget_id
    print "if client will send SMS with number", widget_id, "he will get the path - "
    print revert_get_html_path_from_widget_id(widget_id)

    # update it on the screen
    update_screen_picture_added(current_id) # last picture taken

    # upload it to google drive at the background
    #uploadToGoogleDriveServerWithDaemon(filename)
    # TODO: return this later

    # update the variable for the next new file
    current_id += 1

    # save the variable globally in case of an emergency poweroff
    with open(PATH_PROPERTY_CUR_ID, "w") as f:
        f.write(str(current_id))


'''
    will make most of the canvases to show the the previous canvas did before,
    the last canvas will print the new picture
'''
def update_screen_picture_added(picture_id):
    global preview_pics_canvases
    w,h = SIZE_PREVIEW

    for index in reversed(range(1, NUMBER_OF_PREVIEW_PICS)): # without the first one
        fr_canvas = preview_pics_canvases[index]
        sc_canvas = preview_pics_canvases[index - 1]
        fr_canvas.mirrorizeOtherPP(sc_canvas)

    canvas = preview_pics_canvases[0] # last one
    canvas.showImageFromId(picture_id)

def revert_get_html_path_from_widget_id(widget_id):
    cur_empty_widget = get_view_id_from_picture_id(current_id)
    if cur_empty_widget < widget_id: cur_empty_widget += (NUMBER_OF_PREVIEW_PICS + 1)
    offset = cur_empty_widget - widget_id
    img_possible_id = current_id - offset
    # possible because there is no guarantee that the user didn't wait half an hour before sending the SMS

    return get_download_url(img_possible_id)

def quit_everything(event):
    root.quit()
    close_server()

init_camera()
init_server_on_different_thread()
init_gui()
init_clock()
root.mainloop()

#TODO:
'''

@ maybe googleDrive isn't needed anymore - check if the server works right! (update the router to let TCP pass through)
@ add a thread to take care of the SMSs : the thread and the main will share an object that will have references
    to the mapping: preview_canvas <---> img_id
    so that the thread will be able to do:
     prvcnvs = get_from_sms()
     return string of: get_img_url(map[prvcnvs])
@ first captured image will be on top
'''
