import sdl2
import sdl2.ext
import sdl2.sdlgfx as sdlgfx
import time
import random
from buttons import Rectangle
import ctypes
import threading
import socket


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


#-----------------------------------------
# --- init UDP server --------------------
#------------------------------------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 5005))

message = None

def GetSignal():
    global message
    while(True):
        data, addr = sock.recvfrom(1024) # Execution pauses here until a signal arrives
        message = data.decode()

listener = threading.Thread(target=GetSignal, daemon=True)
listener.start()

#------------------------------------------------------

class Win:
    def __init__(self):

        sdl2.ext.init()
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)


        self.frame = 0
        self.frameiter = 0

        self.manfred_on = True
        self.manfreding = True
        self.switch = False

        self.window = sdl2.ext.Window("Manfred",size=(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.renderer = sdl2.ext.Renderer(self.window)
        self.events = sdl2.ext.get_events()

        self.window.show() 
        self.rect = sdl2.SDL_Rect(0,750,WINDOW_WIDTH,150)
        self.color_1 = sdl2.ext.Color(255,0,0)
        self.color_2 = sdl2.ext.Color(0,255,0)
        self.iter = 0 
        self.centery = WINDOW_HEIGHT/2
        self.centerx = WINDOW_WIDTH/2

        self.mousex = ctypes.c_int(0)
        self.mousey = ctypes.c_int(0)

        self.current_color = [self.color_1, self.color_2]

        self.run = True

        self.Event_trigger = {
            "ClickButton" :False,
        }
        self.rect1 = Rectangle(self.centerx,self.centery,w=200,h=200)
        self.rect1.LoadText(self.renderer,"sprites/rectangle1.png")

        self.rect2 = Rectangle(self.centerx,self.centery,w=200,h=200,spin=15)
        self.rect2.LoadText(self.renderer,b"sprites/rectangle1.png")

        self.rect3 = Rectangle(self.centerx,self.centery,w=200,h=200,spin=-15)
        self.rect3.LoadText(self.renderer,b"sprites/rectangle1.png")

        self.TurnOn = Rectangle(self.centerx,self.centery,w=200,h=200,spinning=False)
        self.TurnOn.LoadText(self.renderer,b"sprites/turn_on.png")
        self.TurnOff = Rectangle(self.centerx,self.centery,w=200,h=200,spinning=False)
        self.TurnOff.LoadText(self.renderer,b"sprites/turn_off.png")


    def Events(self):

        global message
        if message == "PRESSED":
            print("button_pressed!")
            self.manfred_on = False
        else:
            self.manfred_on = True


        self.events = sdl2.ext.get_events()

        for event in self.events:
            if(event.type == sdl2.SDL_QUIT):
                self.run = False
            if(event.type == sdl2.SDL_MOUSEBUTTONDOWN):
                button = event.button.button
                mx, my = event.button.x, event.button.y
                if (button == sdl2.SDL_BUTTON_LEFT):
                    print("mouse clicked!!!")
                    self.Event_trigger["ClickButton"] = True

            if(event.type == sdl2.SDL_MOUSEMOTION):
                buttonstate = sdl2.SDL_GetMouseState(ctypes.byref(self.mousex), ctypes.byref(self.mousey))
        
        try:
            if self.TurnOn.Hover(mx,my) and self.Event_trigger["ClickButton"]:
                print("hover down!!")
                self.manfred_on = not self.manfred_on
        except:
            a = 0
                

    def Draw(self,radious=20,prev_radious=30):
        r = 255
        g = 0
        b = 0

        x = int(self.centerx)
        y = int(self.centery)


        try:
            radious += 150
            radious = int(radious)

            prev_radious += 150
            prev_radious = int(prev_radious)

            avg_rad = int((prev_radious+radious)*0.5)

            rand_rad = int(random.uniform(-1,1)*20)


        # x,y, radious, r,g,b, alpha
            sdlgfx.aacircleRGBA(self.renderer.renderer,x, y,radious, r, g, b, 255)  
            sdlgfx.aacircleRGBA(self.renderer.renderer,x, y,80, 100, 50, b, 255)
            sdlgfx.aacircleRGBA(self.renderer.renderer,x, y,prev_radious, 0, 155, b, 255)
            sdlgfx.aacircleRGBA(self.renderer.renderer,x, y,avg_rad, 0, 0, 155, 255)
            sdlgfx.aacircleRGBA(self.renderer.renderer,x, y,radious+rand_rad, 155, g, b, 155)  
            # rand_rad = int(random.uniform(-1,1)*20)
            # sdlgfx.aacircleRGBA(self.renderer.renderer,x, y,radious+rand_rad, 205, 100, b, 255)  
            # rand_rad = int(random.uniform(-1,1)*20)
            # sdlgfx.aacircleRGBA(self.renderer.renderer,x, y,radious+rand_rad, 205, 205, b, 255)  

            # speed = radious - 90
            # print(f"speed = {speed}")
            # scale_factor = int(radious/10)
            # # self.rect1.scale(scale_factor=scale_factor)
            # self.rect1.Render(self.renderer,speed)
            # self.rect2.Render(self.renderer,speed)
            # self.rect3.Render(self.renderer,speed)
        
        # sdl2.setRenderDrawColor(self.renderer,0,0,0,0)
        except:

            radious = 150
            sdlgfx.aacircleRGBA(self.renderer.renderer,x, y,radious, r, g, b, 255)

            # print("radious is NAN")

    def DrawButtons(self):

        if self.manfred_on:
            self.TurnOn.Render(self.renderer)
        else:
            self.TurnOff.Render(self.renderer)

    def Render_start(self):
        
        self.renderer.clear(sdl2.ext.Color(0,0,0))

        self.renderer.fill([self.rect],sdl2.ext.Color(155,155,155))

    def Render_present(self):
        self.renderer.present()
        self.frame += 1

    def Destroy(self):
        self.renderer.destroy()
        self.window.close()

        sdl2.ext.quit()

    def Reset_Events(self):

        for ev in self.Event_trigger:
            self.Event_trigger[ev] = False


# def main():
#     window = Win()
#     while window.run:
#         window.Events()
#         window.Render_start()
#         window.Draw()
#         window.Render_present()
#         window.Reset_Events()

#     window.Destroy()

# main()
        
    





