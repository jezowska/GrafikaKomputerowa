# Daria Jeżowska 252731
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0
y = 1.0
left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0

delta_x = 0
delta_y = 0

scale = 5.0
move_camera = True
rotation = False


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def shutdown():
    pass

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

def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)

def render(time):
    global theta
    global y
    global phi
    global scale
    global rotation
    global move_camera

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if rotation:
        #aby phi i theta nie przekroczyły 360 dzielimy je modulo przez 360
        phi %= 360
        theta %= 360

        gluLookAt(viewer[0], viewer[1], viewer[2],
                0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        #jeśli lewy klawisz myszy zostanie naciśnięty 
        # zmieniamy kąty theta i phi o delte współrzędnych odpowiednio x i y 
        # pomnożonych przez pix2angle 
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle

        #jeśli prawy klawisz myszy zostanie naciśnięty 
        #odejmujemy od scale deltę y przemnożoną przez pix2angle, aby wiedzieć o ile trzeba
        #pomniejszyć obraz w zależności od położenia kursora 
        if right_mouse_button_pressed:   
            scale -= delta_y * pix2angle

        # jeśli scale jest większe od 10 to zmieniamy je na 10 i analogicznie dla 0.5
        # zapobiega to powiększaniu lub pomniejszaniu obrazu w nieskończoność
        if scale >  10.0:
            scale =  10.0
        if scale < 0.5:
            scale = 0.5
            
        glScalef(scale, scale, scale)
        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)
        

    elif move_camera:
        phi = phi % (2 * math.pi)
        theta = theta % (2 * math.pi)
        
        if left_mouse_button_pressed:
            theta -= delta_x * pix2angle / 100
            phi -= delta_y * pix2angle / 100

        if right_mouse_button_pressed:
            scale += delta_y * pix2angle / 100

        if scale > 10.0:
            scale = 10.0
        if scale < 0.5:
            scale = 0.5
        
        #na podstawie wzorów ze slajdów przypisujemy odpowiednie wartości współrzędnych
        viewer[0] = scale * math.cos(theta) * math.cos(phi)
        viewer[1] = scale * math.sin(phi)
        viewer[2] = scale * math.sin(theta) * math.cos(phi)

        #warunek zapewniający nam poprawne obracanie się kamery
        if math.pi/2 < phi and phi < 3* math.pi / 2:
            y = -1.0
        else:
            y = 1.0

        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0, 0.0, y, 0.0)
    axes()
    example_object()

    glFlush()

def update_viewport(window, width, height):
    #ustalenie wielkości pix2angle
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global rotation
    global move_camera

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if GLFW_KEY_R and action == GLFW_PRESS:
        rotation = True
        move_camera = False
    if GLFW_KEY_C and action == GLFW_PRESS:
        rotation = False
        move_camera = True


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old

    #obliczenie delty oraz poprzedniej pozycji x oraz y 

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old

    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    #jeśli zostanie wykryte naciśnięcie któregoś z klawiszy 
    # myszy zmienia się stan zmiennych left/right_mouse_button_pressed na 0 lub 1 
    # w zależności od naciśniętego klawisza
   
    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    elif button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
