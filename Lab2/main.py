"""
To tak zwany shebang – ścieżka do interpretera.
– Więcej informacji na ten temat – na kursie Systemów Operacyjnych 2 :-)
"""
#!/usr/bin/env python3
"""
Załadowanie niezbędnych bibliotek.
– Wyrażenia from ... import * służą ułatwieniu na potrzeby zajęć.
– Przez to kod może wyglądać prawie identycznie, jak przykłady w języku C.
– Bardzo przepraszam wszystkich znawców Pythona za tę profanację ;-)
"""
"""
Funkcje pomocnicze, docelowo wykonywane jednorazowo.
– Wprowadzone zostały dla przejrzystości kodu na kolejnych zajęciach.
"""

import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

def zadanie_1():
    glBegin(GL_TRIANGLES); 
    glVertex2f(99.0,1.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-99.0,-1.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(1.0,99.0)
    glColor3f(0.0, 0.0, 1.0)
    glEnd()

#wersja, że (x,y) będą wierzchołkiem prostokąta
def zadanie_2_1(x, y, a, b):
    if(x>=0):
        x2 = x - a
        x3 = x2
        x4 = x
    if(x<0):
        x2 = x + a
        x3 = x2
        x4 = x
    if(y>=0):
        y2 = y
        y3 = y2 - b
        y4 = y - b
    if(y<0):
        y2 = y
        y3 = y + b
        y4 = y + b  
    
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(x2, y2)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(x3, y3)
    glColor3f(0.0, 0.0, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(x3, y3)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(x4, y4)
    glColor3f(0.0, 0.0, 0.0)
    glEnd()

#wersja, że (x,y) będą środkiem prostokąta
def zadanie_2_2(x, y, a, b):
    a=0.5*a
    b=0.5*b

    glBegin(GL_TRIANGLES)
    glVertex2f(x+a, y+b)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(x+a, y-b)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(x-a, y-b)
    glColor3f(0.0, 0.0, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x+a, y+b)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(x-a, y+b)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(x-a, y-b)
    glColor3f(0.0, 0.0, 0.0)
    glEnd()

def zadanie_2_b(x, y, a):
    
    a=0.5*a
    b=a

    glBegin(GL_TRIANGLES)
    glVertex2f(x+a, y+b)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x+a, y-b)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x-a, y-b)
    glColor3f(1.0, 1.0, 1.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x+a, y+b)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x-a, y+b)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x-a, y-b)
    glColor3f(1.0, 1.0, 1.0)
    glEnd()    

def zadanie_3(x, y, a, b, d):
    if(d != 0):
        a*=d
        b*=d
    zadanie_2(x, y, a, b) 

def zadanie_4_p(x, y, a):
    a=a*0.33
    zadanie_2_b(x+a, y+a, a*0.33)
    zadanie_2_b(x+a, y-a, a*0.33)
    zadanie_2_b(x-a, y+a, a*0.33)
    zadanie_2_b(x-a, y-a, a*0.33)
    zadanie_2_b(x, y+a, a*0.33)
    zadanie_2_b(x, y-a, a*0.33)
    zadanie_2_b(x+a, y, a*0.33)
    zadanie_2_b(x-a, y, a*0.33)

def zadanie_4(a, ss):
    zadanie_2_2(0,0,a,a)
    zadanie_2_b(0,0,a*0.33)
    
    #zadanie_2_b(x+a, y+a, a*0.33)
    #zadanie_2_b(x+a, y-a, a*0.33)
    #zadanie_2_b(x-a, y+a, a*0.33)
    #zadanie_2_b(x-a, y-a, a*0.33)
    #zadanie_2_b(0, y+a, a*0.33)
    #zadanie_2_b(0, y-a, a*0.33)
    #zadanie_2_b(x+a, 0, a*0.33)
    #zadanie_2_b(x-a, 0, a*0.33)

    zadanie_4_p(0,0,a)
    x=a*0.33
    zadanie_4_p(0+x, 0+x, x)
    zadanie_4_p(0+x, 0-x, x)
    zadanie_4_p(0-x, 0+x, x)
    zadanie_4_p(0-x, 0-x, x)
    zadanie_4_p(0, 0+x, x)
    zadanie_4_p(0, 0-x, x)
    zadanie_4_p(0+x, 0, x)
    zadanie_4_p(0-x, 0, x)

def startup():
    # Ustawiamy wartość koloru, do jakiego będzie czyszczony bufor.
    glClearColor(1.0, 1.0, 1.0, 1.0)
    update_viewport(None, 400, 400)

def shutdown():
    # zawiera instrukcję, która nic nie robi – tak zwany placeholder
    pass

def render(time):

    # W tym przykładzie jest to wyczyszczenie ramki w pamięci – glClear()
    glClear(GL_COLOR_BUFFER_BIT)
    #zadanie_1()
    #zadanie_2_1(0.0, 0.0, 60.0, 70.0)
    #zadanie_2_2(0.0, 0.0, 60.0, 70.0)
    #zadanie_3(50.0, 50.0, 60.0, 70.0, 1.5)
    zadanie_4(100, 1)
    # Następnie zawartość pamięci jest przesyłana do wyświetlenia – glFlush()
    glFlush()

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
      width = 1
    aspectRatio = width / height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    if width <= height:
     glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
    else:
     glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -
            1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():

    if not glfwInit():
        sys.exit(-1)
    
    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
     glfwTerminate()
     sys.exit(-1)
 
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)

    glfwSwapInterval(1)
    startup()
    
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()

