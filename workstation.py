from PIL import Image, ImageDraw
im = Image.open(r"C:\Blender_Box_Sim2\Blender_Box_Sim\sim\Images\picture_0_26.png")


s_x=2.94
s_y=2.94

x_min=1088
x_max=1243
y_min=1080-640
y_max=1080-762
draw = ImageDraw.Draw(im) 

draw.line((x_min,y_min, x_max,y_min), fill=128)
draw.line((x_min,y_max, x_max,y_max), fill=128)
draw.line((x_min,y_min, x_min,y_max), fill=128)
draw.line((x_max,y_min, x_max,y_max), fill=128)

im.show()