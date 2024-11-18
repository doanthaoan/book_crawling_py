from PIL import Image
import os

path = "D:\\An\\projects\\GranitFel\\Data\\bronze_text_300"
size = (200,200)
crop_box = (0, 78, 200, 120)
# def resize(width,height):
# print(os.listdir(path))
for item in os.listdir(path):
    # if os.path.isfile(path + item):
    try:
        with Image.open(path + "\\" + item) as im:
            # im.thumbnail(size)
            # im.save(path + "\\resized\\" + item.replace("_1",""))
            im.thumbnail(size)
            im_crop = im.crop(crop_box)
            im_crop.save(path + "\\resized\\" + item.replace("-300x300","-w200"))
            print("Saved thumbnail for ", item, "successfully")
    except OSError:
        print("Can't save thumbnail for ", item, ":", OSError)