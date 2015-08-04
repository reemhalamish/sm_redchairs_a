__author__ = 'reem'

# constants

WEBCAM_ID = 1
TIME_SECONDS_FOR_CAPTURE_SNAPSHOT_CIRCLE = 4 # in seconds
NUMBER_OF_PREVIEW_PICS = 5
DIM_PREVIEW_WIDTH = 160
DIM_PREVIEW_HEIGHT = 120
SIZE_PREVIEW = (DIM_PREVIEW_WIDTH, DIM_PREVIEW_HEIGHT)
DIM_STREAM_W = 640
DIM_STREAM_H = 480
SIZE_STREAMING = (DIM_STREAM_W, DIM_STREAM_H)
PATH_PROPERTY_CUR_ID = "extra_files/current_avail_id"
PATH_BLANK_PICTURE = "extra_files/blank.jpg"
PATH_MUSEUM_LOGO = "extra_files/mada_jerusalem_logo_COLOR_WIDE_WEB.png"
PATH_CAMERA_PICTURE = "extra_files/camera.png"
PATH_CAMERA_PICTURE1 = "extra_files/camera_arrow_1.png"
PATH_CAMERA_PICTURE2 = "extra_files/camera_arrow_2.png"
PATH_FOLDER_OF_PICTURES = "pic"
DIM_MUSEUM_LOGO_HEIGHT = 99
ORDER_CALL_PYTHON_UPLOADER = "python uploadOneFile.py"
PORT_NUMBER = 9876 # for the server
TIME_CLOCK_CICLES_IN_SEC = 10 # times in a seconds
TIME_CLOCK_CICLE_MS = 1000 // TIME_CLOCK_CICLES_IN_SEC
TIME_HOW_MANY_FRAMES_SHOW_CAMERA_PNG_ON_STREAM = 7
FONT_DOWNTEXT_FONT = ("serif", 40)

# lambda functions
get_picture_path = lambda pic_id : PATH_FOLDER_OF_PICTURES + "/" + str(pic_id) + ".jpg"
get_view_id_from_picture_id = lambda pic_id : (pic_id % (NUMBER_OF_PREVIEW_PICS +1)) + 1
