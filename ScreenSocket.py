#!/usr/bin/env python

##-- Zachary Trette & Michael duPont
##-- Accepts commands for screen responses
##-- EV3- Remote - https://github.com/flyinactor91/EV3-Remote

## 2013-12-05

import os , pygame
from socket import *
from pygame.locals import *

port = 5678
defaultTimeout = 5

class screen:
        #Init window
        def __init__(self , ht , wt):
                pygame.init()
                self.size = (ht , wt)
                self.win = screen = pygame.display.set_mode(self.size,HWSURFACE|DOUBLEBUF|RESIZABLE)
        
        #Display text in window
        def showText(self , txt):
                self.win.fill((0,0,0))
                basicfont = pygame.font.SysFont(None, 48)
                w, h = basicfont.size(txt) #gets size of font
                lines = self.wrapline(txt,basicfont,640) #gets lines of text that will be put up with text wraping engaged
                for x in range(0,len(lines)): #places all lines on screen with text wrapping
                        text = basicfont.render(lines[x] , True , (255,0,0), (0,0,0))
                        textRect = text.get_rect()
                        textRect.centerx = self.win.get_rect().centerx
                        textRect.centery = h + h * x # used to determine where to place the letters so that they aren't on top of each other
                        self.win.blit(text , textRect)
                        
                pygame.display.update() #updates window all at once
        
        #Display image in window
        def showImg(self , fName):
                if os.path.isfile(fName):
                        img = pygame.image.load(fName)
                        self.win.blit(pygame.transform.scale(img , self.size) , (0,0))
                        pygame.display.flip()
                else: print 'File not found: ' + fName
        
        #Clear text or image from screen
        def clearWin(self):
                basicfont = pygame.font.SysFont(None , 48)
                text = basicfont.render("" , True , (0,0,0) , (0,0,0))
                textrect = text.get_rect()
                textrect.centerx = self.win.get_rect().centerx
                textrect.centery = self.win.get_rect().centery
                self.win.fill((0,0,0))
                self.win.blit(text , textrect)
                pygame.display.flip()
 
        def truncline(self,text, font, maxwidth):
                real=len(text)       
                stext=text           
                l=font.size(text)[0]
                cut=0
                a=0                  
                done=1
                old = None
                while l > maxwidth:
                        a=a+1
                        n=text.rsplit(None, a)[0]
                        if stext == n:
                                cut += 1
                                stext= n[:-cut]
                        else:
                                stext = n
                        l=font.size(stext)[0]
                        real=len(stext)               
                        done=0
                        
                return real, done, stext             
                
        def wrapline(self,text, font, maxwidth): 
                done=0                      
                wrapped=[]                  
                                       
                while not done:             
                        nl, done, stext=self.truncline(text, font, maxwidth) 
                        wrapped.append(stext.strip())                  
                        text=text[nl:]                                 
                return wrapped        
         



def main():
        #Init socket
        screenSocket = socket(AF_INET, SOCK_STREAM)
        screenSocket.bind(('' , port))
        screenSocket.listen(1)
        
        #Create screen
        disp = screen(640 , 480)
        quitFlag = True
        disp.showText("Hello World haoewjangaeinarebha;eh   parwoghaoeihgair; a;oihjaorighaphrvaoihrgij iha rrighaerihgoaghj 0gaegh;aerh")
        while not quitFlag:
                
                #Recieve connection / command
                connectionSocket , addr = screenSocket.accept()
                connectionSocket.settimeout(defaultTimeout)
                msg = connectionSocket.recv(1024).strip()
                
                #Command indent
                #Text
                if msg[0] == 'T': disp.showText(msg[1:].strip())
                #Image
                elif msg[0] == 'I': disp.showImg(msg[1:].strip())
                #Clear
                elif msg[0] == 'C': disp.clearWin()
                #Quit
                elif msg == 'QUIT': quitFlag = True
                #Catch
                else: print 'Not a valid command'
                
                #Close connection
                connectionSocket.close()
        
        #Close socket
        screenSocket.close()


if __name__ == '__main__':
        main()


