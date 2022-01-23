import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

def startup():
    # Ustawiamy wartość kolorarray_u[i], do jakiego będzie czyszczony bufor.
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    update_viewport(None, 400, 400)

def shutdown():
    # zawiera instrukcję, która nic nie robi – tak zwany placeholder
    pass

# funkcja obliczająca nam ze wzoru kolejne położenia punktów w jaju
def equation_matrix(n):
    matrix = np.zeros((n,n,3))
    array_u = np.linspace(0.0, 1.0, n)
    array_v = np.linspace(0.0, 1.0, n)

    for i in range(n):  
        for j in range(n):
            matrix[i,j,0] = ((-90.0) * (array_u[i]** 5.0) + 225.0 * (array_u[i] **4.0) - 270.0 * (array_u[i] **3.0) + 180.0 * (array_u[i]** 2.0) - 45 * array_u[i]) * math.cos(array_v[j]*math.pi)
            matrix[i,j,1] = 160.0 * (array_u[i]** 4.0) - 320.0 * (array_u[i]** 3.0) + 160.0 * math.pow(array_u[i], 2.0)
            matrix[i,j,2] = ((-90.0) * (array_u[i]** 5.0) + 225.0 * (array_u[i] **4.0) - 270.0 * (array_u[i] **3.0) + 180.0 * (array_u[i]** 2.0) - 45 * array_u[i]) * math.sin(array_v[j]*math.pi)
    return matrix        

def points(n):
    matrix = equation_matrix(n)

    for i in range(n):  
        for j in range(n):
            #rozpoczecie rysowana punktow na osiach, aby wyszlo nam jajko z kropek
            glBegin(GL_POINTS) 
            glColor3f(0.93, 0.35, 0.68)
            glVertex3f(matrix[i,j,0], matrix[i,j,1] - 5.0, matrix[i,j,2])
            glEnd()

def lines(n):
    matrix = equation_matrix(n)
   
    for i in range(n-1):  
        for j in range(n-1):            
            glBegin(GL_LINES) 
            glColor3f(0.93, 0.35, 0.68)
            glVertex3f(matrix[i,j,0], matrix[i,j,1] -5, matrix[i,j,2])
            glVertex3f(matrix[i+1,j,0], matrix[i+1,j,1] -5, matrix[i+1,j,2])
            glVertex3f(matrix[i,j+1,0], matrix[i,j+1,1] -5, matrix[i,j+1,2])
            glEnd()

def triangles(n):
    matrix = equation_matrix(n)
    
    for i in range(n-1):
        for j in range(n-1):
            glBegin(GL_TRIANGLES)
            #rysowanie pierwszego trójkąta
            glColor3f(color_matrix[i,j,0], color_matrix[i,j,1], color_matrix[i,j,2])
            glVertex3f(matrix[i,j,0], matrix[i,j,1] -5, matrix[i,j,2])

            glColor3f(color_matrix[i+1,j,0], color_matrix[i+1,j,1], color_matrix[i+1,j,2])
            glVertex3f(matrix[i+1,j,0], matrix[i+1,j,1] -5, matrix[i+1,j,2])

            glColor3f(color_matrix[i,j+1,0], color_matrix[i,j+1,1], color_matrix[i,j+1,2])
            glVertex3f(matrix[i,j+1,0], matrix[i,j+1,1] -5, matrix[i,j+1,2])

            #rysowanie drugiego trójkąta
            #przy jednym powstają dziury, więc trzeba je uzupełnić
            glColor3f(color_matrix[i+1,j+1,0], color_matrix[i+1,j+1,1], color_matrix[i+1,j+1,2])
            glVertex3f(matrix[i+1,j+1,0], matrix[i+1,j+1,1] -5, matrix[i+1,j+1,2])

            glColor3f(color_matrix[i+1,j,0], color_matrix[i+1,j,1], color_matrix[i+1,j,2])
            glVertex3f(matrix[i+1,j,0], matrix[i+1,j,1] -5, matrix[i+1,j,2])

            glColor3f(color_matrix[i,j+1,0], color_matrix[i,j+1,1], color_matrix[i,j+1,2])
            glVertex3f(matrix[i,j+1,0], matrix[i,j+1,1] -5, matrix[i,j+1,2])

            glEnd()

def random_color_matrix(n):
    global color_matrix
    color_matrix = np.zeros((n,n,3))

    for i in range(n):
        for j in range(n):
            color_matrix[i,j,0] = np.random.uniform(0.0, 1.0)
            color_matrix[i,j,1] = np.random.uniform(0.0, 1.0)
            color_matrix[i,j,2] = np.random.uniform(0.0, 1.0)

def render(time):
    # W tym przykładzie jest to wyczyszczenie ramki w pamięci – glClear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / math.pi)

    axes()

    #points(100)
    #lines(50)
    triangles(50)

    glFlush()

def spin(angle):
    glRotate(angle, 1.0, 0.0, 0.0)
    glRotate(angle, 0.0, 1.0, 0.0)
    glRotate(angle, 0.0, 0.0, 1.0)

def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

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
     glOrtho(-7.5, 7.5, -7.5 / aspectRatio, 7.5 / aspectRatio, 7.5, -7.5)
    else:
     glOrtho(-7.5 * aspectRatio, 7.5 * aspectRatio, -7.5, 7.5, 7.5, -
            7.5)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():

    random_color_matrix(200)

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
    
    random_color_matrix(200)

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()

