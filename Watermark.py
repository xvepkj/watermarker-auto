from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import glob
import os, json

configDir = os.path.dirname(os.path.realpath(__file__))
configFile = "config.json"
config = None

def loadConfig():
  try:
    with open(configDir + "/" + configFile, "r") as read_file:
      global config
      config = json.load(read_file)
  except:
    print("Invalid JSON")

loadConfig()

watermark_text = "\n".join(config["watermark"])

gui = Tk()
gui.geometry("400x100")
gui.title("WaterMark Adder")
def getFolderPath():
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)

def doStuff():
    input_image_path = folderPath.get()
    list = glob.glob(input_image_path + "/*.*")
    output_folder = input_image_path + '_watermaked'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for photo in list:
        images = photo.replace(input_image_path,output_folder)
        copyright_apply(photo, images, watermark_text)
def copyright_apply(input_image_path,
 output_image_path,
 text):
 photo = Image.open(input_image_path)
 #Store image width and heigth
 w, h = photo.size
# make the image editable
 drawing = ImageDraw.Draw(photo)
 font = ImageFont.truetype("times.ttf", int(max(h,w)/50))
 
 #get text width and heigth
 
 text = "© " + text + " "
 text_w, text_h = drawing.textsize(text, font)
 
 pos = w - text_w - 50, (h - text_h) - 50
 
 c_text = Image.new('RGB', (text_w + 5, (text_h + 5)), color = '#000000')
 drawing = ImageDraw.Draw(c_text)
 
 drawing.text((0,0), text, fill="#ffffff", font=font)
 c_text.putalpha(100)
 photo.paste(c_text, pos, c_text)
 photo.save(output_image_path)
 
 
folderPath = StringVar()
a = Label(gui ,text="Enter name")
a.grid(row=0,column = 0)
E = Entry(gui,textvariable=folderPath)
E.grid(row=0,column=1)
btnFind = ttk.Button(gui, text="Browse Folder",command=getFolderPath)
btnFind.grid(row=0,column=2)

c = ttk.Button(gui ,text="Add WaterMark", command=doStuff)
c.grid(row=4,column=0)
gui.mainloop()