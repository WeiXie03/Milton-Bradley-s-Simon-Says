from fltk import *
import random
import math
import glob
import wave
import alsaaudio

plyr = alsaaudio.PCM()
print(plyr.cardname())

win = Fl_Window(Fl_w()-math.floor(540/2),math.floor((480+40)/2),math.floor(540),math.floor(480+40),'Boi Says')
colobuts = []
colours = [FL_RED,FL_GREEN,FL_BLUE,FL_YELLOW] #red 1, green 2, blue 3, yellow 4
audio = []
for audfile in glob.iglob('sounds/*.wav'):
    wholef = wave.open(audfile, 'rb')
    audio.append(wholef.readframes(math.floor(wholef.getframerate()*0.2))) #use the first 0.2 seconds of audio frames of each file

seq = []
checkerStep = 0
Fl.scheme('plastic')

def guess(widg):
    global checkerStep, seq, colobuts, audio
    plyr.write(audio[colobuts.index(widg)]) #play the wav audio object corresponding to the colour clicked

    if widg == colobuts[seq[checkerStep]]:
        if checkerStep == len(seq)-1:
            seq.append(random.randrange(4))
            #print(checkerStep)
            checkerStep = 0
            playseq(start)

        elif checkerStep < len(seq)-1:
            #print(checkerStep)
            checkerStep += 1
    else:
        fail(start)

def fail(start):
    global checkerStep, seq
    print('Game Over!')

    restart = fl_choice('You FAILED! Would you like to try again?','Yes','No',None)
    if restart == 0:
        checkerStep = 0
        seq = [random.randrange(4) for step in range(3)]
        playseq(start)
    elif restart == 1:
        exit(0)

def playseq(widg):
    global colobuts, seq
    for colo in colobuts:
        colo.deactivate()

    for step in range(len(seq)):
        Fl.add_timeout(0.7*step,flash,step) #flash dem colours

    Fl.add_timeout(float(len(seq))-0.6,unveil,colobuts)

def flash(step):
    global colobuts, seq, plyr, audio
    colobuts[seq[step]].activate()
    colobuts[seq[step]].value(1)
    plyr.write(audio[seq[step]]) #play the wav audio object corresponding to the colour clicked
    Fl.add_timeout(0.3,release,step)

def release(step):
    global colobuts
    colobuts[seq[step]].value(0)
    #colobuts[seq[step]].deactivate()

def unveil(colobuts):
    for colo in colobuts:
        colo.activate()

win.begin()
for row in range(2):
    for column in range(2):
        colobuts.append(Fl_Button(row*math.floor(540/2),column*math.floor(480/2),math.floor(540/2),math.floor(480/2)))
        #print colours[row*2+column]
        colobuts[-1].color(colours[row*2+column])
        colobuts[-1].callback(guess)

start = Fl_Button(math.floor(540/2-25),485,50,32,'start')
win.end()
for step in range(3):
    randind = random.randrange(4)
    #print(randind)
    seq.append(randind)
#print('\n')

start.callback(playseq)

win.show()
Fl.run()
