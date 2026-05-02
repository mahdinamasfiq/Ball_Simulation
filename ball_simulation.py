from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

angle = 0
openAngle = 0
opening = False

posX, posY = 0, 0
scale = 1.0


def drawPokeball():
    global openAngle

    #BLACK BAND 
    glPushMatrix()
    glScalef(1.05, 0.15, 1.05)
    glColor3f(0, 0, 0)
    glutSolidSphere(1, 30, 30)
    glPopMatrix()

    #Top half red
    glPushMatrix()
    glTranslatef(0, 0.05, 0)
    glRotatef(openAngle, 1, 0, 0)

    plane_top = [0, -1, 0, 0]
    glClipPlane(GL_CLIP_PLANE0, plane_top)
    glEnable(GL_CLIP_PLANE0)

    glColor3f(1, 0, 0)
    glutSolidSphere(1, 30, 30)

    glDisable(GL_CLIP_PLANE0)
    glPopMatrix()

    #Bottom half white
    glPushMatrix()
    glTranslatef(0, -0.05, 0)

    plane_bottom = [0, 1, 0, 0]
    glClipPlane(GL_CLIP_PLANE1, plane_bottom)
    glEnable(GL_CLIP_PLANE1)

    glColor3f(1, 1, 1)
    glutSolidSphere(1, 30, 30)

    glDisable(GL_CLIP_PLANE1)
    glPopMatrix()

    #Center Button
    glPushMatrix()
    glTranslatef(0, 0, 1.05)

    quad = gluNewQuadric()

    glColor3f(0.05, 0.05, 0.05)
    gluDisk(quad, 0.18, 0.25, 40, 1)

    glColor3f(0.95, 0.95, 0.95)
    gluCylinder(quad, 0.18, 0.18, 0.08, 40, 1)

    glTranslatef(0, 0, 0.08)
    gluDisk(quad, 0, 0.18, 40, 1)

    glColor3f(0.85, 0.85, 0.85)
    gluDisk(quad, 0, 0.1, 40, 1)

    glPopMatrix()

    # Glow effect
    if opening and openAngle > 60:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        # soft pulse glow (smooth breathing light)
        glow = 0.25 + (openAngle - 60) / 120.0  # grows as it opens

        # outer glow (red energy)
        glColor4f(1, 0.2, 0.2, 0.25)
        glutSolidSphere(glow, 30, 30)

        # mid glow (yellow-white)
        glColor4f(1, 1, 0.6, 0.2)
        glutSolidSphere(glow * 0.6, 25, 25)

        # core (bright white center)
        glColor4f(1, 1, 1, 0.35)
        glutSolidSphere(glow * 0.3, 20, 20)

        glDisable(GL_BLEND)


def display():
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(posX, posY, -5)
    glScalef(scale, scale, scale)

    glRotatef(180, 1, 0, 0)
    glRotatef(angle, 0, 1, 0)

    drawPokeball()

    glutSwapBuffers()


def keyboard(key, x, y):
    global posX, posY, scale, opening, angle

    if key == b'a': posX -= 0.2
    if key == b'd': posX += 0.2
    if key == b'w': posY += 0.2
    if key == b's': posY -= 0.2

    if key == b'+': scale = min(scale + 0.1, 3.0)
    if key == b'-': scale = max(scale - 0.1, 0.3)

    if key == b'o': opening = not opening

    if key == b'r':
        posX, posY = 0, 0
        scale = 1.0
        angle = 0
        opening = False


def update(v):
    global angle, openAngle, opening

    angle += 0.5
    if angle >= 360:
        angle -= 360

    if opening and openAngle < 90:
        openAngle += 3
    elif not opening and openAngle > 0:
        openAngle -= 3

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.8, 0.8, 0.8, 1])
    glMaterialf(GL_FRONT, GL_SHININESS, 60)

    glClearColor(0.1, 0.1, 0.2, 1)


def reshape(w, h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 1, 50)
    glMatrixMode(GL_MODELVIEW)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(600, 600)
glutCreateWindow(b"Press 'O' to Open")

init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutReshapeFunc(reshape)
glutTimerFunc(16, update, 0)

glutMainLoop()