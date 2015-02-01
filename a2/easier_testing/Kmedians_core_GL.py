import ImageDraw
import pyscreenshot as ImageGrab
import os
import sys
import time
from random import *
from Image import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import Kmedians_global_data
from Kmedians_local_search import local_search
from Kmedians_local_search import deterministic_annealing
winID = 0
canvas = new('RGB', [1024, 1024])
blank = new('RGB', [1024, 1024])
kmed_col = [[255, 0, 0],
 [0, 255, 0],
 [0, 0, 255],
 [255, 0, 255],
 [0, 255, 255],
 [128, 0, 255],
 [0, 128, 255],
 [255, 128, 0],
 [255, 0, 128],
 [64, 0, 128],
 [0, 64, 128],
 [128, 64, 0],
 [128, 0, 64],
 [0, 128, 64],
 [64, 128, 0]]
labels = []
iters = 0
N_comps = 7
pis = []
mus = []
sigs = []
screen_shot_on_done=False
screeny_filename='ScreenShot_'+time.strftime('%Y_%m_%d%_%H_%M_%S')+'.jpg'

def renderFrame():
    global canvas
    global labels
    global kmed_col
    global blank
    canvas = blank.copy()
    draw = ImageDraw.Draw(canvas)
    point_assign()
    for i in range(Kmedians_global_data.N):
        pt = Kmedians_global_data.all_points[i]
        col = kmed_col[labels[i]]
        draw.rectangle([pt[0] - 3,
         pt[1] - 3,
         pt[0] + 3,
         pt[1] + 3], outline=(col[0], col[1], col[2]))

    for i in range(Kmedians_global_data.K):
        kp = Kmedians_global_data.current_medians[i]
        draw.ellipse([kp[0] - 6,
         kp[1] - 6,
         kp[0] + 6,
         kp[1] + 6], fill=(255, 255, 64))

    del draw



def point_assign():
    labels[:] = []
    minIdx = -1
    for i in range(Kmedians_global_data.N):
        dst = 1000000000.0
        pt = Kmedians_global_data.all_points[i]
        for j in range(Kmedians_global_data.K):
            kp = Kmedians_global_data.current_medians[j]
            d_est = (pt[0] - kp[0]) * (pt[0] - kp[0]) + (pt[1] - kp[1]) * (pt[1] - kp[1])
            if d_est < dst:
                dst = d_est
                minIdx = j

        labels.append(minIdx)




def initKmedians(seedNo, N, K, screeny=False,filename=''):
    global N_comps
    global sigs
    global pis
    global mus
    global blank
    global screen_shot_on_done
    global screeny_filename

    screen_shot_on_done = screeny
    if filename:
        screeny_filename=filename

    Kmedians_global_data.N = N
    Kmedians_global_data.K = K
    if N < 50 or N > 5000:
        print 'Value of N should be between 50 and 5000. Using 100\n'
        Kmedians_global_data.N = 100
    if K < 1 or K > 15:
        print 'Value of K should be between 1 and 15. Using 10\n'
        Kmedians_global_data.K = 5
    random.seed(31415)
    if seedNo >= 0:
        pisum = 0
        for i in range(N_comps + 1):
            pis.append(random.random())
            mus.append([random.randint(1, 1022), randint(1, 1022)])
            sigs.append([random.randint(50, 500)])
            pisum = pisum + pis[i]

        for i in range(N_comps + 1):
            pis[i] = pis[i] / pisum

    else:
        blank = open('TO_dense.ppm')
        pis.append(7)
        mus.append([165, 697])
        sigs.append(70)
        pis.append(7)
        mus.append([185, 530])
        sigs.append(100)
        pis.append(7)
        mus.append([490, 590])
        sigs.append(55)
        pis.append(7)
        mus.append([710, 475])
        sigs.append(70)
        pis.append(4)
        mus.append([300, 250])
        sigs.append(150)
        pis.append(2.5)
        mus.append([950, 340])
        sigs.append(140)
        pis.append(1.5)
        mus.append([610, 230])
        sigs.append(200)
        pis.append(0.5)
        mus.append([512, 512])
        sigs.append(1)
        pisum = 0
        for i in range(N_comps + 1):
            pisum = pisum + pis[i]

        for i in range(N_comps + 1):
            pis[i] = pis[i] / pisum

    for i in range(Kmedians_global_data.N):
        done = 0
        while not done:
            dice = random.random()
            pisum = 0
            idx = 0
            while idx < N_comps:
                pisum = pisum + pis[idx]
                if pisum >= dice:
                    break
                idx = idx + 1

            if idx < N_comps:
                mu = mus[idx]
                sig = sigs[idx]
                pt = list([random.normal(mu[0], sig, 1), random.normal(mu[1], sig, 1)])
                if pt[0] > 0 and pt[0] < 1023 and pt[1] > 0 and pt[1] < 1023:
                    done = 1
            else:
                pt = [random.randint(1, 1023), random.randint(1, 1023)]
                done = 1
            if seedNo < 0 and done:
                pix = list(blank.getpixel(tuple([round(pt[0]), round(pt[1])])))
                if pix[0] == 0 and pix[1] == 0 and pix[2] == 0:
                    done = 0
            if done == 1:
                Kmedians_global_data.all_points.append(pt)


    random.seed(abs(seedNo))
    for i in range(Kmedians_global_data.K):
        Kmedians_global_data.current_medians.append(Kmedians_global_data.all_points[random.randint(0, N - 1)])

    print 'Initial K-medians guess:\n'
    print Kmedians_global_data.current_medians
    print 'Initial assignment cost (average distance from a point to the closest candidate median):\n'
    print Kmedians_global_data.current_cost(Kmedians_global_data.current_medians)



def initWindow(title):
    global winID
    sarg = 'Dummy!'
    carg = 1
    glutInit(carg, sarg)
    glutInitWindowPosition(25, 25)
    glutInitWindowSize(640, 640)
    winID = glutCreateWindow(title)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutReshapeFunc(WindowReshape)
    glutDisplayFunc(MainLoop)
    glutKeyboardFunc(kbHandler)



def WindowReshape(w, h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 800, 0)
    glViewport(0, 0, w, h)



def kbHandler(key, x, y):
    if key == 'q':
        exit(0)

    if key == 'p':
        img=ImageGrab.grab()
        saveas=os.path.join(r'screenshots',screeny_filename)
        img.save(saveas)


def UpdateFrame():
    tsx = canvas.size[0]
    tsy = canvas.size[1]
    texImage = canvas.convert('RGB')
    texImage = canvas.tostring('raw', 'RGB')
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    texture = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, tsx, tsy, 0, GL_RGB, GL_UNSIGNED_BYTE, texImage)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(800.0, 0.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(800.0, 800.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0.0, 800.0, 0.0)
    glEnd()
    glFlush()
    glutSwapBuffers()
    glutSetWindow(winID)
    glutPostRedisplay()
    glDeleteTextures(texture)



def MainLoop():
    global iters
    global screen_shot_on_done
    global screeny_filename
    temp = list(Kmedians_global_data.current_medians)
    if iters < 150:
        if Kmedians_global_data.Temperature <= 0:
            local_search()
            if temp == Kmedians_global_data.current_medians:
                iters = iters + 1
            else:
                iters = 0
        else:
            deterministic_annealing()
            if temp == Kmedians_global_data.current_medians:
                iters = iters + 1
            else:
                iters = 0
        renderFrame()
        UpdateFrame()
    else:
        print 'No improvement for past 150 iterations. Search stop.\n'
        print "Press 'q' to quit\n"
        print "final cost:", Kmedians_global_data.current_cost(Kmedians_global_data.current_medians)

        if not screen_shot_on_done:
            exit(0)



def Kmedians(temperature, decay):
    if Kmedians_global_data.N <= 0 or Kmedians_global_data.K <= 0:
        print 'Must call initKmedians() first!'
        exit(0)
    Kmedians_global_data.Temperature = temperature
    Kmedians_global_data.Decay = decay
    if Kmedians_global_data.Temperature < 0.0:
        Kmedians_global_data.Temperature = 0.0
    if Kmedians_global_data.Decay < 0.0 or Kmedians_global_data.Decay > 1.0:
        Kmedians_global_data.Decay = 1.0
    initWindow("K-Medians CSCD84, F.J.E. '2014")
    glutMainLoop()



