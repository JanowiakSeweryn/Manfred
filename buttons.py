
import sdl2
import sdl2.ext
import sdl2.sdlgfx as sdlgfx

import sdl2.sdlimage as sdlimage
import random

class Rectangle:
    def __init__(self,x,y,w=100,h=100,spin=0,spinning=False):
        self.rect = sdl2.SDL_Rect(int(x-w*0.5),int(y-h*0.5),w,h)
        self.angle = 0
        self.texture = None
        self.spin = spin
        self.curent_hover = False
        self.spinning = spinning

    def LoadText(self,renderer,image_path):
        try:
            
            self.texture = sdlimage.IMG_LoadTexture(renderer.sdlrenderer, image_path)
            print("IMG loaded succesfully!")
        except:
            print("could not load texure")

    def update_angle(self,speed=10):
        self.angle += (speed+self.spin)
    
    def scale(self,scale_factor=1):
        w = scale_factor
        h = scale_factor
    
    def Hover(self,x,y):
        if (x-self.rect.x-self.rect.w*0.5)**2 + (y-self.rect.y-self.rect.h*0.5)**2 <= (self.rect.w*0.5)**2 :
            self.curent_hover = True
            return True
        else:
            self.curent_hover = False
            return False 

    
    def Render(self,renderer,speed=10):
        if self.texture is None:
            print("texture failed to load")
        else:
            if self.spinning:
                self.update_angle(speed)
            sdl2.SDL_RenderCopyEx(
                renderer.sdlrenderer, 
                self.texture, 
                None, 
                self.rect, 
                self.angle, 
                None, 
                sdl2.SDL_FLIP_NONE
            )


        
        

    

    
