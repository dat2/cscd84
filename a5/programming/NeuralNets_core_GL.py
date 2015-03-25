import ImageDraw
import pyscreenshot as ImageGrab
import time
from random import *
from Image import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import NeuralNets_global_data
from NeuralNets_train import FeedForward
from NeuralNets_train import trainOneSample
winID = 0
canvas = new('RGB', [1024, 1024])
blank = new('RGB', [1024, 1024])
maxErr = -1
wghts = zeros(shape=(NeuralNets_global_data.N_out, 1))
screen_shot_on_done=False
screeny_filename='ScreenShot_'+time.strftime('%Y_%m_%d%_%H_%M_%S')+'.jpg'

def renderFrame(input_list, err_data):
    global canvas
    global blank
    global wghts
    global maxErr
    x_input = 25
    x_hidden = 320
    x_output = 640
    if maxErr == -1 and err_data.max() > 0:
        maxErr = err_data.max()
    canvas = blank.copy()
    draw = ImageDraw.Draw(canvas)
    (oA, hA,) = FeedForward(input_list)
    mi = min(input_list)
    mx = max(input_list)
    for i in range(64):
        col = int((input_list[i] - mi) / (mx - mi) * 232.0)
        px = x_input
        py = 50 + i * 15
        draw.ellipse([px - 3,
         py - 3,
         px + 3,
         py + 3], outline=(255, 255, 255), fill=(col, col, col))

    for i in range(NeuralNets_global_data.N_out):
        px = x_output
        py = 70 + i * (960.0 / 10.0)
        col = int(oA[i] * 250.0)
        if col < 0:
            col = 0
        draw.ellipse([px - 5,
         py - 5,
         px + 5,
         py + 5], outline=(0, 128, 128), fill=(0, col, col))

    if NeuralNets_global_data.N_hidden > 0:
        for i in range(NeuralNets_global_data.N_hidden):
            px = x_hidden
            py = 10 + i * (1010 / (NeuralNets_global_data.N_hidden - 1))
            col = int(hA[i] * 250.0)
            if col < 0:
                col = 0
            draw.ellipse([px - 3,
             py - 3,
             px + 3,
             py + 3], outline=(0, 128, 128), fill=(col, 0, col))

    sampling = 3
    if NeuralNets_global_data.N_hidden > 0:
        for i in range(64):
            px = x_input + 4
            py = 50 + i * 15
            pxh = x_hidden - 4
            idx = i % sampling
            while idx < NeuralNets_global_data.N_hidden:
                pyh = 10 + idx * (1010 / (NeuralNets_global_data.N_hidden - 1))
                col = NeuralNets_global_data.N_in * NeuralNets_global_data.W_ih[i][idx]
                if col < 0:
                    draw.line([px,
                     py,
                     pxh,
                     pyh], fill=(int(-250 * col), 0, 0))
                else:
                    draw.line([px,
                     py,
                     pxh,
                     pyh], fill=(0, 0, int(250 * col)))
                idx = idx + sampling


        for i in range(NeuralNets_global_data.N_hidden):
            pxh = x_hidden + 4
            pyh = 10 + i * (1010 / (NeuralNets_global_data.N_hidden - 1))
            pxo = x_output - 4
            idx = i % sampling
            while idx < NeuralNets_global_data.N_out:
                pyo = 70 + idx * (960.0 / 10.0)
                col = NeuralNets_global_data.N_hidden * NeuralNets_global_data.W_ho[i][idx]
                if col < 0:
                    draw.line([pxh,
                     pyh,
                     pxo,
                     pyo], fill=(int(-250 * col), 0, 0))
                else:
                    draw.line([pxh,
                     pyh,
                     pxo,
                     pyo], fill=(0, 0, int(250 * col)))
                idx = idx + sampling


    else:
        for i in range(64):
            px = x_input + 4
            py = 50 + i * 15
            pxo = x_output - 4
            idx = i % sampling
            while idx < NeuralNets_global_data.N_out:
                pyo = 70 + idx * (960.0 / 10.0)
                col = NeuralNets_global_data.N_in * NeuralNets_global_data.W_io[i][idx]
                if col < 0:
                    draw.line([px,
                     py,
                     pxo,
                     pyo], fill=(int(-250 * col), 0, 0))
                else:
                    draw.line([px,
                     py,
                     pxo,
                     pyo], fill=(0, 0, int(250 * col)))
                idx = idx + sampling


    for i in range(8):
        for j in range(8):
            idx = i + j * 8
            col = int((input_list[idx] - mi) / (mx - mi) * 250)
            px = 5 + i * 4
            py = 5 + j * 4
            draw.rectangle([px,
             py,
             px + 4,
             py + 4], outline=(col, col, col), fill=(col, col, col))


    for i in range(NeuralNets_global_data.N_out):
        px = x_output + 100
        py = 95 + i * (970.0 / 10.0)
        draw.line([px - 3,
         py,
         px + 200,
         py], fill=(192, 192, 192))
        draw.line([px,
         py + 3,
         px,
         py - 60], fill=(192, 192, 192))
        for j in range(99):
            px1 = px + 1 + j * 2
            px2 = px + 1 + (j + 1) * 2
            py1 = py - 1 - 80 * err_data[j][i] / maxErr
            py2 = py - 1 - 80 * err_data[(j + 1)][i] / maxErr
            draw.line([px1,
             py1,
             px2,
             py2], fill=(64, int((10.0 - i) / 10.0 * 255), int(i / 10.0 * 255)))


    if NeuralNets_global_data.N_hidden == 0:
        for i in range(NeuralNets_global_data.N_out):
            mi = NeuralNets_global_data.W_io[:, i].min()
            mx = NeuralNets_global_data.W_io[:, i].max()
            px = x_output + 25
            py = 52 + i * (970 / 10.0)
            for j in range(8):
                for k in range(8):
                    col = int((NeuralNets_global_data.W_io[(j + 8 * k)][i] - mi) / (mx - mi) * 250)
                    px1 = px + j * 4
                    py1 = py + k * 4
                    draw.rectangle([px1,
                     py1,
                     px1 + 4,
                     py1 + 4], outline=(255 - col, 255 - col, col), fill=(255 - col, 255 - col, col))



    else:
        for i in range(NeuralNets_global_data.N_out):
            wghts = zeros(shape=(NeuralNets_global_data.N_in, 1))
            for j in range(NeuralNets_global_data.N_hidden):
                for k in range(NeuralNets_global_data.N_in):
                    wghts[k] = wghts[k] + NeuralNets_global_data.W_ho[j][i] * NeuralNets_global_data.W_ih[k][j]


            mi = wghts.min()
            mx = wghts.max()
            px = x_output + 25
            py = 52 + i * (970 / 10.0)
            for j in range(8):
                for k in range(8):
                    col = int((wghts[(j + 8 * k)] - mi) / (mx - mi) * 250)
                    px1 = px + j * 4
                    py1 = py + k * 4
                    draw.rectangle([px1,
                     py1,
                     px1 + 4,
                     py1 + 4], outline=(255 - col, 255 - col, col), fill=(255 - col, 255 - col, col))






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
    Error = 1000000.0
    round_size = 250
    Error_record = zeros(shape=(100, NeuralNets_global_data.N_out))
    Error_idx = 0
    print 'Initial accuracy on the training set\n'
    correct = zeros(shape=(10, 1))
    counts = zeros(shape=(10, 1))
    for i in range(len(NeuralNets_global_data.trainDigits)):
        (oA, hA,) = FeedForward(NeuralNets_global_data.trainDigits[i])
        lab = NeuralNets_global_data.trainLabels[i]
        w_idx = oA.argmax()
        counts[lab] = counts[lab] + 1
        if w_idx == lab:
            correct[lab] = correct[lab] + 1

    print 'Correct classification rates:'
    for i in range(10):
        print 'For ',
        print i,
        print ' : ',
        print correct[i] / counts[i] * 100.0

    print 'Average for all digits: ',
    print sum(correct) / sum(counts) * 100.0
    print '\nNetwork training in process... error threshold=',
    print NeuralNets_global_data.Err_Thresh,
    print ' round size=',
    print round_size
    non_improv = 0
    past_err = 10000000000.0
    while Error > NeuralNets_global_data.Err_Thresh:
        Error = 0
        err_per_unit = zeros(shape=(NeuralNets_global_data.N_out, 1))
        for i in range(round_size):
            idx = random.randint(0, len(NeuralNets_global_data.trainDigits) - 1)
            sample = NeuralNets_global_data.trainDigits[idx]
            label = NeuralNets_global_data.trainLabels[idx]
            errors = trainOneSample(sample, label)
            renderFrame(sample, Error_record)
            UpdateFrame()
            for j in range(len(errors)):
                err_per_unit[j] = err_per_unit[j] + errors[j] * errors[j]


        Error = sum(err_per_unit) / (NeuralNets_global_data.N_out * round_size)
        if Error > past_err:
            non_improv = non_improv + 1
            if non_improv >= 15:
                print 'No improvement after 10 rounds. Halving learning rate'
                NeuralNets_global_data.alpha = NeuralNets_global_data.alpha / 2
                non_improv = 0
                past_err = Error
        else:
            past_err = Error
            non_improv = 0
        i = 99
        while i > 0:
            for j in range(NeuralNets_global_data.N_out):
                Error_record[i][j] = Error_record[(i - 1)][j]

            i = i - 1

        for i in range(NeuralNets_global_data.N_out):
            Error_record[0][i] = err_per_unit[i]

        print 'Average squared error for this round: ',
        print Error

    print 'Training done!\n'
    print 'Computing accuracy on the training set\n'
    correct = zeros(shape=(10, 1))
    counts = zeros(shape=(10, 1))
    for i in range(len(NeuralNets_global_data.trainDigits)):
        (oA, hA,) = FeedForward(NeuralNets_global_data.trainDigits[i])
        lab = NeuralNets_global_data.trainLabels[i]
        w_idx = oA.argmax()
        counts[lab] = counts[lab] + 1
        if w_idx == lab:
            correct[lab] = correct[lab] + 1

    print 'Correct classification rates:'
    for i in range(10):
        print 'For ',
        print i,
        print ' : ',
        print correct[i] / counts[i] * 100.0

    print 'Average for all digits: ',
    print sum(correct) / sum(counts) * 100.0
    print '\nComputing accuracy on the testing set\n'
    correct = zeros(shape=(10, 1))
    counts = zeros(shape=(10, 1))
    for i in range(len(NeuralNets_global_data.TD)):
        (oA, hA,) = FeedForward(NeuralNets_global_data.TD[i])
        lab = NeuralNets_global_data.TL[i]
        w_idx = oA.argmax()
        counts[lab] = counts[lab] + 1
        if w_idx == lab:
            correct[lab] = correct[lab] + 1

    print 'Correct classification rates:'
    for i in range(10):
        print 'For ',
        print i,
        print ' : ',
        print correct[i] / counts[i] * 100.0

    print 'Average for all digits: ',
    print sum(correct) / sum(counts) * 100.0

    if not screen_shot_on_done:
        exit(0)

    print '\nPress enter to exit'
    # x = raw_input()
    exit(0)



def NeuralNets_init(N_hidden, sig_type, learn_rate, random_seed,screeny=False,filename=''):
    global screeny_filename

    screen_shot_on_done = screeny
    if filename:
        screeny_filename=filename

    random.seed(random_seed)
    if N_hidden < 0 or N_hidden > 100:
        print 'Number of hidden units must be in [0,100]'
        exit(0)
    if sig_type == 1:
        NeuralNets_global_data.sig_type = 1
    else:
        NeuralNets_global_data.sig_type = 0
    if learn_rate > 10 or learn_rate <= 0:
        print 'Learning rate must be in (0,10)'
        exit(0)
    else:
        NeuralNets_global_data.alpha = learn_rate
    if N_hidden == 0:
        NeuralNets_global_data.N_hidden = 0
        NeuralNets_global_data.W_io = zeros(shape=(NeuralNets_global_data.N_in, NeuralNets_global_data.N_out))
        for i in range(NeuralNets_global_data.N_out):
            for j in range(NeuralNets_global_data.N_in):
                NeuralNets_global_data.W_io[j][i] = (random.random() - 0.5) / NeuralNets_global_data.N_in


    else:
        NeuralNets_global_data.N_hidden = N_hidden + 1
        NeuralNets_global_data.W_ih = zeros(shape=(NeuralNets_global_data.N_in, NeuralNets_global_data.N_hidden))
        for i in range(NeuralNets_global_data.N_hidden):
            for j in range(NeuralNets_global_data.N_in):
                NeuralNets_global_data.W_ih[j][i] = (random.random() - 0.5) / NeuralNets_global_data.N_in


        NeuralNets_global_data.W_ho = zeros(shape=(NeuralNets_global_data.N_hidden, NeuralNets_global_data.N_out))
        for i in range(NeuralNets_global_data.N_out):
            for j in range(NeuralNets_global_data.N_hidden):
                NeuralNets_global_data.W_ho[j][i] = (random.random() - 0.5) / NeuralNets_global_data.N_hidden





def NeuralNets_train(thresh):
    if thresh <= 0 or thresh >= 1:
        print 'Error threshold must be in (0,1)'
        exit(0)
    NeuralNets_global_data.Err_Thresh = thresh
    initWindow("Neural Networks, F.J.E., '13")
    glutMainLoop()



