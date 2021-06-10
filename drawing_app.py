import numpy as np
import cv2

# global variables
pressed =False
radius=3
color=(0,255,0)
eraser_flag=False
paint_flag=True
square_flag=False
line_flag=False
circle_flag=False
# white canvas
img1=np.ones([700,700,3],'uint8')*255
# creating the icons
eraser = cv2.imread("eraser.png")
square = cv2.imread("square.png")
line = cv2.imread("line.png")
circle = cv2.imread("circle.png")
paint = cv2.imread("paint.png")
print(square.shape)
# creating copy of the white image
canvas=img1.copy()

#save button
save=np.ones([50,100,3],'uint8')
save[:,:,1]=save[:,:,1]*255
print(save.shape[0])
cv2.putText(save, 'save', (20, 25), cv2.FONT_HERSHEY_SIMPLEX,
                   1, (255,255,255), 2, cv2.LINE_AA)


def create_canvas():
    global color, radius, eraser_flag,eraser,square,line,circle,paint
    dsize = (20, 20)
    eraser = cv2.resize(eraser, dsize)
    square = cv2.resize(square, dsize)
    line = cv2.resize(line, dsize)
    circle = cv2.resize(circle, dsize)
    paint = cv2.resize(paint, dsize)
    # combining the two images
    canvas[10:30,120:140,:] = eraser[0:20,0:20,:]
    canvas[10:30, 150:170, :] = paint[0:20, 0:20, :]
    canvas[10:30, 180:200, :] = line[0:20, 0:20, :]
    canvas[10:30, 210:230, :] = circle[0:20, 0:20, :]
    canvas[10:30, 240:260, :] = square[0:20, 0:20, :]
    canvas[610:660, 300:400, :] = save[0:50, 0:100, :]
    # creating color pallet
    cv2.circle(canvas, (10,20),10,(255,0,0),-1)
    cv2.circle(canvas, (40,20),10,(0,255,0),-1)
    cv2.circle(canvas, (70,20),10,(0,0,255),-1)
    cv2.circle(canvas, (100,20),10,(0,255,255),-1)
    cv2.line(canvas, (0, 40),(700,40), (0, 0, 0),2, -1)
    cv2.line(canvas, (0, 600), (700, 600), (0, 0, 0), 2, -1)


def change_color(x,y):
    global color, radius, eraser_flag
    if x in range(0, 20) and y in range(10, 30):
        color = (255, 0, 0)
        eraser_flag = False
    elif x in range(30, 50) and y in range(10, 30):
        color = (0, 255, 0)
        eraser_flag = False
    elif x in range(60, 80) and y in range(10, 30):
        color = (0, 0, 255)
        eraser_flag = False
    elif x in range(90, 110) and y in range(10, 30):
        color = (0, 255, 255)
        eraser_flag = False
    elif x in range(120, 140) and y in range(10, 30):
        color = (255, 255, 255)
        eraser_flag = False
        radius = 10
        eraser_flag = True

def draw_sqaure(x,y,event,pressed):
    cv2.rectangle(canvas, (x, y), (x+20, y+20), color, 5)

def draw_line(x,y):
    cv2.line(canvas, (x, y), (x+20, y+20), color, 5)

def draw_cirlc(x,y):
    cv2.circle(canvas, (x,y),10,color,2)

def click(event, x,y,flags,param):
    point1=()
    point2 = ()

    global canvas,pressed,color,radius,eraser_flag,square_flag,paint_flag,line_flag,circle_flag
    radius=0
    if event == cv2.EVENT_LBUTTONDOWN:
        pressed = True
        if y in range(10, 30) and x in range(0, 140):
            change_color(x,y)
        elif y in range(10, 30) and x in range(150,170):
            paint_flag=True
            circle_flag = False
            square_flag=False
            line_flag = False
        elif y in range(10, 30) and x in range(180,200):
            paint_flag=False
            square_flag=False
            circle_flag = False
            line_flag=True
        elif y in range(10, 30) and x in range(210,230):
            paint_flag=False
            square_flag=False
            circle_flag = True
            line_flag=False
        elif y in range(10, 30) and x in range(240,260):
            line_flag = False
            paint_flag=False
            circle_flag = False
            square_flag=True
        elif y in range(610, 660) and x in range(300,400):
            print("saved")
            filename = 'Note.jpg'
            savedImage = canvas[41:600, 0:700, :]
            cv2.imwrite(filename, savedImage)
        elif square_flag==True:
            draw_sqaure(x, y,event,pressed)
        elif line_flag==True:
            draw_line(x,y)
        elif circle_flag==True:
            draw_cirlc(x,y)
        else:
            radius = 3
            if(eraser_flag==False):
                cv2.circle(canvas, (x,y),radius,color,-1)
            elif (eraser_flag == True):
                canvas[10:30, 120:140, :] = eraser[0:20, 0:20, :]
    elif event == cv2.EVENT_MOUSEMOVE and pressed==True:
        if (eraser_flag == False):
            radius = 3
        elif (eraser_flag == True):
            radius = 10
        cv2.circle(canvas, (x,y),radius,color,-1)
    elif event == cv2.EVENT_LBUTTONUP:
        pressed =False




#intialization of the canvas
create_canvas() #creating the canvas gui
cv2.namedWindow("canvas")
cv2.setMouseCallback("canvas",click)

#looping forever

while(True):
    cv2.imshow("canvas", canvas)
    ch=cv2.waitKey(1)
    if ch & 0XFF == ord('q'):
        break


# cv2.waitKey(0)
cv2.destroyAllWindows()