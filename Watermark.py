from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import glob
import os, json

gui, config = None, None
folder_path, label_status, images_list = None, None, None
num_files, num_files_done = 0, 0
watermark_text, font_size = "", 0

def load_config():
  try:
    with open("config.json", "r") as read_file:
      global config, watermark_text, font_size
      config = json.load(read_file)
      watermark_text = "\n".join(config["watermark"])
      font_size = config["font_size"]
  except:
    print("Invalid JSON")

def update_status():
  label_status["text"] = "%d out of %d done" % (num_files_done, num_files)

def update_list():
  global images_list, num_files
  if os.path.exists(folder_path.get()):
    images_list = glob.glob(folder_path.get() + "/*.*")
    num_files = len(images_list)
    update_status()

def get_folder_path():
  global num_files, num_files_done
  num_files, num_files_done = 0, 0
  folder_selected = filedialog.askdirectory()
  folder_path.set(folder_selected)
  update_list()
    
def process(input_image_path, output_image_path, text):
  global num_files_done
  photo = Image.open(input_image_path)
  photo = ImageOps.exif_transpose(photo)
  # Store image width and heigth
  w, h = photo.size
  # make the image editable
  drawing = ImageDraw.Draw(photo)
  font = ImageFont.truetype(config["font"], int(max(h,w)/font_size))
  
  # get text width and heigth
  text = " © " + text + " "
  text_w, text_h = drawing.textsize(text, font)
  
  pos = w - text_w - 50, (h - text_h) - 50
  
  c_text = Image.new('RGB', (text_w + 5, (text_h + 5)), color = '#000000')
  drawing = ImageDraw.Draw(c_text)
  
  drawing.text((0,0), text, fill="#ffffff", font=font)
  c_text.putalpha(100)
  photo.paste(c_text, pos, c_text)
  photo.save(output_image_path)
  num_files_done += 1
  update_status()

def process_all():
  global images_list
  if images_list == None:
    update_list()
  
  output_folder = folder_path.get() + '_watermarked'
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)
  for photo in images_list:
    images = photo.replace(folder_path.get(), output_folder)
    process(photo, images, watermark_text)
  folder_path.set("")
  messagebox.showinfo(message="Done")

def setup_gui():
  global gui, folder_path, label_status

  gui = Tk()
  gui.geometry("350x180")
  gui.resizable(False, False)
  gui.title("WaterMark Adder")

  folder_path = StringVar()

  label = Label(gui, text="Enter path of folder containing images")
  entry = Entry(gui, textvariable=folder_path, state="disabled")
  button_browse = ttk.Button(gui, text="Browse Folder", command=get_folder_path)
  button_go = ttk.Button(gui, text="Add WaterMark", command=process_all)
  label_status_pre = Label(gui, text="STATUS:")
  label_status = Label(gui, text="Folder not loaded")
  
  # Component Placement
  label.grid(row=0, column=0, padx=10, pady=10)
  entry.grid(row=1, column=0, padx=10, pady=10, sticky="we")
  button_browse.grid(row=1, column=1, padx=10, pady=10, sticky="we")
  button_go.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")
  label_status_pre.grid(row=3, column=0, padx=10, pady=10)
  label_status.grid(row=3, column=1, padx=10, pady=10)

  gui.mainloop()

def main():
  load_config()
  setup_gui() 

main()
