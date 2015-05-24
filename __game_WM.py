# -*- coding: utf-8 -*-

# @author: Hossein Sabri
# @contact: hossein.sabri@gmail.com
# @date: 2015-05-12

import time
import codecs

from win32api import GetSystemMetrics
from psychopy import visual, core, event, gui, data

# ===============================================================================
# global variables: INTERFACE
# ===============================================================================
PATH = 'C:\\pythonProjects\\_project_WM_Experiment'
OUTPATH = '%s\\results\\' % PATH  # output path for storing the results
LANGUAGE = 'DE'  # which language is the experiment in: 'DE'=German. 'CN'=Chinese
# SCREEN_SIZE = [GetSystemMetrics(0), GetSystemMetrics(1)]  # what is your screen resolution?
SCREEN_SIZE = [1000,600]
HALF_WIDTH = int(round((SCREEN_SIZE[0]/7.942)/2))
rtClock = core.Clock()  # reaction time clock


# ===============================================================================
# Other preparations
# ===============================================================================

class Image():  # class that creates ....

    def __init__(self, name, _type, **kwargs):

        # ** if the format of images are different(ie. .png, .jpg, .gif) give the complete name with extension and
        # remove the ".png" from self.path
        # :param name: name of the image
        # :param type: can be "load", "arrow", "questionMark", "questionLoad"
        # :return:

        self.path = '{0}\\images\\{1}.png'.format(PATH, name)
        self.type = _type
        if 'loc' in kwargs:
            self.loc = kwargs['loc']

    def get_position(self):

        position = [0, 0]
        if self.type == "arrow":
            position = [0, 0]
        elif self.type == "questionMark":
            position = [-4*HALF_WIDTH-50-80, 4*HALF_WIDTH-106]
        elif self.type == "questionLoad":
            position = [-4*HALF_WIDTH-50-80, -75]
        elif self.type == "load":
            if self.loc == "D1":
                position = [-3*HALF_WIDTH, -3*HALF_WIDTH]
            elif self.loc == "D2":
                position = [-HALF_WIDTH, -3*HALF_WIDTH]
            elif self.loc == "D3":
                position = [HALF_WIDTH, -3*HALF_WIDTH]
            elif self.loc == "D4":
                position = [3*HALF_WIDTH, -3*HALF_WIDTH]
            elif self.loc == "C1":
                position = [-3*HALF_WIDTH, -HALF_WIDTH]
            elif self.loc == "C2":
                position = [-HALF_WIDTH, -HALF_WIDTH]
            elif self.loc == "C3":
                position = [HALF_WIDTH, -HALF_WIDTH]
            elif self.loc == "C4":
                position = [3*HALF_WIDTH, -HALF_WIDTH]
            elif self.loc == "B1":
                position = [-3*HALF_WIDTH, HALF_WIDTH]
            elif self.loc == "B2":
                position = [-HALF_WIDTH, HALF_WIDTH]
            elif self.loc == "B3":
                position = [HALF_WIDTH, HALF_WIDTH]
            elif self.loc == "B4":
                position = [3*HALF_WIDTH, HALF_WIDTH]
            elif self.loc == "A1":
                position = [-3*HALF_WIDTH, 3*HALF_WIDTH]
            elif self.loc == "A2":
                position = [-HALF_WIDTH, 3*HALF_WIDTH]
            elif self.loc == "A3":
                position = [HALF_WIDTH, 3*HALF_WIDTH]
            elif self.loc == "A4":
                position = [3*HALF_WIDTH, 3*HALF_WIDTH]

        return position

    def buffer(self):

        buffer_image = visual.ImageStim(expWindow, image=self.path, pos=self.get_position(), units=u'pix')
        return buffer_image

# ===============================================================================
# Functions
# ===============================================================================


def read_stimuli(stimuli):
    trials = []
    file_header = []
    with codecs.open(stimuli, 'rb', encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if '###' in line:  # its the header
                line = line.split(';')
                file_header.append(line[0:len(line)-1])
            elif len(line) == 0:  # last line if an empty one
                break
            else:
                line = line.split(';')
                trials.append(line[0:len(line)-1])  # write entire rest of the line
    return trials, file_header


def check_answer(x, y, correct_answer):

    # :param x: integer first dimension of mouse click
    # :param y: integer second dimension of mouse click
    # :param correct_answer: string
    # :return:

    interval = []
    if correct_answer == "D1":
        interval = [-4*HALF_WIDTH, -2*HALF_WIDTH, -4*HALF_WIDTH, -2*HALF_WIDTH]
    elif correct_answer == "D2":
        interval = [-2*HALF_WIDTH, 0, -4*HALF_WIDTH, -2*HALF_WIDTH]
    elif correct_answer == "D3":
        interval = [0, 2*HALF_WIDTH, -4*HALF_WIDTH, -2*HALF_WIDTH]
    elif correct_answer == "D4":
        interval = [2*HALF_WIDTH, 4*HALF_WIDTH, -4*HALF_WIDTH, -2*HALF_WIDTH]
    elif correct_answer == "C1":
        interval = [-4*HALF_WIDTH, -2*HALF_WIDTH, -2*HALF_WIDTH, 0]
    elif correct_answer == "C2":
        interval = [-2*HALF_WIDTH, 0, -2*HALF_WIDTH, 0]
    elif correct_answer == "C3":
        interval = [0, 2*HALF_WIDTH, -2*HALF_WIDTH, 0]
    elif correct_answer == "C4":
        interval = [2*HALF_WIDTH, 4*HALF_WIDTH, -2*HALF_WIDTH, 0]
    elif correct_answer == "B1":
        interval = [-4*HALF_WIDTH, -2*HALF_WIDTH, 0, 2*HALF_WIDTH]
    elif correct_answer == "B2":
        interval = [-2*HALF_WIDTH, 0, 0, 2*HALF_WIDTH]
    elif correct_answer == "B3":
        interval = [0, 2*HALF_WIDTH, 0, 2*HALF_WIDTH]
    elif correct_answer == "B4":
        interval = [2*HALF_WIDTH, 4*HALF_WIDTH, 0, 2*HALF_WIDTH]
    elif correct_answer == "A1":
        interval = [-4*HALF_WIDTH, -2*HALF_WIDTH, 2*HALF_WIDTH, 4*HALF_WIDTH]
    elif correct_answer == "A2":
        interval = [-2*HALF_WIDTH, 0, 2*HALF_WIDTH, 4*HALF_WIDTH]
    elif correct_answer == "A3":
        interval = [0, 2*HALF_WIDTH, 2*HALF_WIDTH, 4*HALF_WIDTH]
    elif correct_answer == "A4":
        interval = [2*HALF_WIDTH, 4*HALF_WIDTH, 2*HALF_WIDTH, 4*HALF_WIDTH]

    if (interval[0] < x < interval[1]) and (interval[2] < y < interval[3]):
        return 1
    else:
        return 0


def update_direction_finder(dir):

    if dir == "N":
        return 0
    elif dir == "NW":
        return 45
    elif dir == "W":
        return 90
    elif dir == "SW":
        return 135
    elif dir == "S":
        return 180
    elif dir == "SO":
        return 225
    elif dir == "O":
        return 270
    elif dir == "NO":
        return 315


def load_background(): # Load background fit to expWindow
    bg = Image("Background", "arrow").buffer()
    bg.setSize(SCREEN_SIZE[0]/3150.0, '*')
    return bg.draw()


def load_update_arrow(kind, direction):

    arrow = Image("A_" + kind, "arrow").buffer()
    arrow.ori = update_direction_finder(direction)
    return arrow.draw()


def load_small_cartoon(color):

    small_cartoon = Image("Nadel_" + color, "arrow").buffer()
    return small_cartoon.draw()


def run_trials(items, practice=False):

    # loop through trials
    for i in [0,4]:  # range(len(items)):  # trial_order:

        item = items[i]  # -1]

        # create and edit a list for the output file
        out_item = [expInfo['subjectID']]
        if item[5]:
            out_item.insert(1, "3")
        else:
            out_item.insert(1, "2")

        # prepare stimulus and draw on screen
        cartoon1 = Image(item[1], "load", loc=item[2]).buffer()
        cartoon2 = Image(item[3], "load", loc=item[4]).buffer()

        # stimulus interval
        expWindow.flip()  # flip blank screen
        core.wait(1.5)  # 1500 ms

        # Initial view
        load_background()
        cartoon1.draw()
        cartoon2.draw()
        if item[5]:
            Image(item[5], "load", loc=item[6]).buffer().draw()
        expWindow.flip()
        core.wait(3)  # 3000 ms

        # ISI
        expWindow.flip()
        core.wait(.5)  # 500 ms

        # updates
        for jj in range(4):
            if jj == 3 and not item[5]:
                break
            load_background()
            load_update_arrow(item[7+jj*2], item[8+jj*2])
            load_small_cartoon(item[7+jj*2])
            expWindow.flip()
            core.wait(2.5)  # 2500 ms

            # ISI
            expWindow.flip()
            core.wait(.5)  # 500 ms

        # questions
        for ii in range(3):
            if ii == 2 and not item[5]:  # check that the trial is two loads or three loads
                for j in range(2):
                    item.append("")
                break
            load_background()
            Image("Question", "questionMark").buffer().draw()
            Image(item[15+ii*2], "questionLoad").buffer().draw()

            # mouse interaction
            mouse = event.Mouse(win=expWindow)
            expWindow.flip()
            rtClock.reset()

            timeout = time.time() + 60*0.5   # 30 seconds from now
            while True:
                if time.time() > timeout:
                    answer = 0
                    rt = 31
                    if practice:
                        load_background()
                        Image("Question", "questionMark").buffer().draw()
                        Image(item[15+ii*2], "questionLoad").buffer().draw()
                        time_up_message.draw()
                        expWindow.flip()
                        core.wait(1)
                    else:
                        item.append(str(answer))
                        item.append(str(rt))
                    break
                if mouse.getPressed()[0]:
                    x, y = mouse.getPos()
                    answer = check_answer(x, y, item[16+ii*2])
                    rt = rtClock.getTime()
                    if practice:
                        load_background()
                        Image("Question", "questionMark").buffer().draw()
                        Image(item[15+ii*2], "questionLoad").buffer().draw()
                        if answer:
                            correct_answer_message.draw()
                        else:
                            false_answer_message.draw()
                        expWindow.flip()
                        core.wait(1)
                    else:
                        item.append(str(answer))
                        item.append(str(rt))
                    break

        if not practice:
            o.write(";".join(out_item) + ";" + ";".join(item) + ";" + "\n")

        # ISI
        expWindow.flip()
        core.wait(1.5)  # 1500 ms

# ===============================================================================
# initial dialogue box
# ===============================================================================
inputInfo = ['a', '']
count = 0
while inputInfo[0] != inputInfo[1] or not inputInfo[0].isdigit():
    expDlg = gui.Dlg(title="WM Experiment")
    expDlg.addText("Subject info")
    expDlg.addField("Subject_ID:")
    expDlg.addField("Repeat__ID:")
    expDlg.addText("")
    if count:
        expDlg.addText("ERROR: IDs must be same integers", color='Red')
    expDlg.show()
    count += 1
    if expDlg.OK:
        inputInfo = expDlg.data
    else:
        core.quit()

# ===============================================================================
# experiment preparation
# ===============================================================================
practice_list, header = read_stimuli('{0}\\stimuli\\Trials_Practice_WMExperiment.txt'.format(PATH))
trials_list, header = read_stimuli('{0}\\stimuli\\Trials_WMExperiment.txt'.format(PATH))
# Edit header line for using in the output
header[0][0] = "trial"
header[0][0:0] = ["Subject_ID", "load"]
header[0].extend(["Answer1", "rt1", "Answer", "rt2", "Answer3", "rt3"])
# output file
expInfo = {'subjectID': inputInfo[1], 'expName': "WM_Experiment"}
output_file = OUTPATH + expInfo['expName'] + '_%s.txt' % expInfo['subjectID']
# create a window
expWindow = visual.Window(size=SCREEN_SIZE, monitor="testMonitor", color=(230, 230, 230),
                          colorSpace='rgb255', units=u'pix')
# fullscr=True,
# messages in practice part
correct_answer_message = visual.TextStim(expWindow, pos=[0, 0], text="Richtig!", font='Courier New', bold=True,
                                         color=(0, 1.0, 0), height=50, alignHoriz='center', units=u'pix')
false_answer_message = visual.TextStim(expWindow, pos=[0, 0], text="Falsch!", font='Courier New', bold=True,
                                       color=(1.0, 0, 0), height=50, alignHoriz='center', units=u'pix')
time_up_message = visual.TextStim(expWindow, pos=[0, 0], text="Die Zeit ist um!", font='Courier New', bold=True,
                                  color=(1.0, 0, 0), height=35, alignHoriz='center', units=u'pix')

# ===============================================================================
# instruction + practice_start_screen
# ===============================================================================
for im in range(20):
    Image("Intro" + str(im+1) + "_Murks", "arrow").buffer().draw()
    expWindow.flip()
    event.waitKeys(keyList=['space'])
Image("practice_start_screen", "arrow").buffer().draw()
expWindow.flip()  # flip blank screen
event.waitKeys(keyList=['space'])

# ===============================================================================
# practice part + practice_start_screen
# ===============================================================================
run_trials(practice_list, practice=True)
Image("practice_end_screen", "arrow").buffer().draw()
expWindow.flip()  # flip blank screen
event.waitKeys(keyList=['space'])

# ===============================================================================
# main part + Test_End_Screen
# ===============================================================================
with open(output_file, 'w') as o:
    o.write(";".join(header[0]) + "\n")
    run_trials(trials_list)
Image("Test_End_Screen", "arrow").buffer().draw()
expWindow.flip()  # flip blank screen
event.waitKeys(keyList=['space'])

expWindow.close()
core.quit()


#expWindow.flip()
#event.waitKeys(keyList=['space'])

# expWindow.close()
#core.quit()
