# -*- coding: utf-8 -*-

# @author: Hossein Sabri
# @contact: hossein.sabri@gmail.com
# @date: 2015-05-12

import time
import codecs

from psychopy import visual, core, event, gui, data

# ===============================================================================
# global variables: INTERFACE
# ===============================================================================

PATH = 'C:\\pythonProjects\\_project_WM_Experiment'
FIXCROSS_SIZE = 40  # size of the fixation cross (the character '+' in Arial)
INSTR_CHAR_SIZE = 18  # character size for instructions
OUTPATH = '%s\\results\\' % PATH  # output path for storing the results
LANGUAGE = 'DE'  # which language is the experiment in: 'DE'=German. 'CN'=Chinese
SCREEN_SIZE = [800, 480]  # what is your screen resolution?
LANG_FONT_MAP = {'DE': 'Courier New', 'CN': 'SimSun'}  # what font is used for what language?
HALF_WIDTH = 432/8

# ===============================================================================
# initial dialogue box
# ===============================================================================
inputInfo = ['a', '']
count = 0
while inputInfo[0] != inputInfo[1] or not inputInfo[0].isdigit():
    expDlg = gui.Dlg(title="WM Experiment")
    expDlg.addText("Subject info")
    # expDlg.addField("Name:", fieldLength=25)
    expDlg.addField("Subject_ID:", fieldLength=25)
    expDlg.addField("Repeat__ID:", fieldLength=25)
    expDlg.addText("")
    # expDlg.addText("Experiment info")
    # expDlg.addField("Group:", choices=["Test", "Control"], fieldLength=25)
    # expDlg.addText("")
    if count:
        expDlg.addText("ERROR: IDs must be same integers", color='Red')
    expDlg.show()
    count += 1
    if expDlg.OK:
        inputInfo = expDlg.data
    else:
        core.quit()

# ===============================================================================
# read stimuli
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

trials_list, header = read_stimuli('%s\\%s\\stimuli\\Trials_WMExperiment_%s.txt'%(PATH,LANGUAGE,LANGUAGE))

# Edit header line for using in the output
header[0][0] = "trial"
header[0].insert(0, "load")
header[0].insert(0, "Subject_ID")
header[0].append("question1")
header[0].append("rt1")
header[0].append("question2")
header[0].append("rt2")
header[0].append("question3")
header[0].append("rt3")

# ===============================================================================
# Other preparations
# ===============================================================================

# expInfo = {'subjectName':inputInfo[0], 'subjectID':inputInfo[1], 'group':inputInfo[-1], "expName":"WM Experiment"}
expInfo = {'subjectID': inputInfo[1], 'expName': "WM_Experiment"}

output_file = OUTPATH + expInfo['expName'] + '_%s.txt' % expInfo['subjectID']
rtClock = core.Clock()  # reaction time clock

# create a window
expWindow = visual.Window(size=SCREEN_SIZE,monitor="testMonitor",color=(230,230,230), colorSpace='rgb255', units=u'pix')
# fullscr=True,

correct_answer_message = visual.TextStim(expWindow, pos=[0, 0], text="Richtig!", font='Courier New', bold=True,
                                         color=(0, 1.0, 0), height=50, alignHoriz='center', units=u'pix')
false_answer_message = visual.TextStim(expWindow, pos=[0, 0], text="Falsch!", font='Courier New', bold=True,
                                       color=(1.0, 0, 0), height=50, alignHoriz='center', units=u'pix')
time_up_message = visual.TextStim(expWindow, pos=[0, 0], text="Die Zeit ist um!", font='Courier New', bold=True,
                                  color=(1.0, 0, 0), height=35, alignHoriz='center', units=u'pix')

# ===============================================================================
# check answer
# ===============================================================================


def check_answer(x, y, correct_answer):

    # :param x: integer first dimension of mouse click
    # :param y: integer second dimension of mouse click
    # :param correct_answer: string
    # :return:

    interval = []
    if correct_answer == "A1":
        interval = [-4*HALF_WIDTH, -2*HALF_WIDTH, -4*HALF_WIDTH, -2*HALF_WIDTH]
    elif correct_answer == "A2":
        interval = [-2*HALF_WIDTH, 0, -4*HALF_WIDTH, -2*HALF_WIDTH]
    elif correct_answer == "A3":
        interval = [0, 2*HALF_WIDTH, -4*HALF_WIDTH, -2*HALF_WIDTH]
    elif correct_answer == "A4":
        interval = [2*HALF_WIDTH, 4*HALF_WIDTH, -4*HALF_WIDTH, -2*HALF_WIDTH]
    elif correct_answer == "B1":
        interval = [-4*HALF_WIDTH, -2*HALF_WIDTH, -2*HALF_WIDTH, 0]
    elif correct_answer == "B2":
        interval = [-2*HALF_WIDTH, 0, -2*HALF_WIDTH, 0]
    elif correct_answer == "B3":
        interval = [0, 2*HALF_WIDTH, -2*HALF_WIDTH, 0]
    elif correct_answer == "B4":
        interval = [2*HALF_WIDTH, 4*HALF_WIDTH, -2*HALF_WIDTH, 0]
    elif correct_answer == "C1":
        interval = [-4*HALF_WIDTH, -2*HALF_WIDTH, 0, 2*HALF_WIDTH]
    elif correct_answer == "C2":
        interval = [-2*HALF_WIDTH, 0, 0, 2*HALF_WIDTH]
    elif correct_answer == "C3":
        interval = [0, 2*HALF_WIDTH, 0, 2*HALF_WIDTH]
    elif correct_answer == "C4":
        interval = [2*HALF_WIDTH, 4*HALF_WIDTH, 0, 2*HALF_WIDTH]
    elif correct_answer == "D1":
        interval = [-4*HALF_WIDTH, -2*HALF_WIDTH, 2*HALF_WIDTH, 4*HALF_WIDTH]
    elif correct_answer == "D2":
        interval = [-2*HALF_WIDTH, 0, 2*HALF_WIDTH, 4*HALF_WIDTH]
    elif correct_answer == "D3":
        interval = [0, 2*HALF_WIDTH, 2*HALF_WIDTH, 4*HALF_WIDTH]
    elif correct_answer == "D4":
        interval = [2*HALF_WIDTH, 4*HALF_WIDTH, 2*HALF_WIDTH, 4*HALF_WIDTH]

    if (interval[0] <= x <= interval[1]) and (interval[2] <= y <= interval[3]):
        return 1
    else:
        return 0

# ===============================================================================
# experiment class
# ===============================================================================


class Image():

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
            position = [-216-54, 216-75]
        elif self.type == "questionLoad":
            position = [-216-54, -34]
        elif self.type == "load":
            if self.loc == "A1":
                position = [-3*HALF_WIDTH, -3*HALF_WIDTH]
            elif self.loc == "A2":
                position = [-HALF_WIDTH, -3*HALF_WIDTH]
            elif self.loc == "A3":
                position = [HALF_WIDTH, -3*HALF_WIDTH]
            elif self.loc == "A4":
                position = [3*HALF_WIDTH, -3*HALF_WIDTH]
            elif self.loc == "B1":
                position = [-3*HALF_WIDTH, -HALF_WIDTH]
            elif self.loc == "B2":
                position = [-HALF_WIDTH, -HALF_WIDTH]
            elif self.loc == "B3":
                position = [HALF_WIDTH, -HALF_WIDTH]
            elif self.loc == "B4":
                position = [3*HALF_WIDTH, -HALF_WIDTH]
            elif self.loc == "C1":
                position = [-3*HALF_WIDTH, HALF_WIDTH]
            elif self.loc == "C2":
                position = [-HALF_WIDTH, HALF_WIDTH]
            elif self.loc == "C3":
                position = [HALF_WIDTH, HALF_WIDTH]
            elif self.loc == "C4":
                position = [3*HALF_WIDTH, HALF_WIDTH]
            elif self.loc == "D1":
                position = [-3*HALF_WIDTH, 3*HALF_WIDTH]
            elif self.loc == "D2":
                position = [-HALF_WIDTH, 3*HALF_WIDTH]
            elif self.loc == "D3":
                position = [HALF_WIDTH, 3*HALF_WIDTH]
            elif self.loc == "D4":
                position = [3*HALF_WIDTH, 3*HALF_WIDTH]

        return position

    def buffer(self):

        buffer_image = visual.ImageStim(expWindow, image=self.path, pos=self.get_position(), units=u'pix')
        return buffer_image

# -----------------------------------------------------------------------------
# define trial procedure


def run_trials(items, practice=False):

    # loop through trials
    for i in range(len(items)):  # trial_order:

        item = items[i]  # -1]

        # create and edit a list for the output file
        out_item = [expInfo['subjectID']]
        if item[5]:
            out_item.insert(1, "3")
        else:
            out_item.insert(1, "2")

        # prepare stimulus and draw on screen
        background = Image("background", "arrow").buffer()
        cartoon1 = Image(item[1], "load", loc=item[2]).buffer()
        cartoon2 = Image(item[3], "load", loc=item[4]).buffer()

        # stimulus interval
        expWindow.flip()  # flip blank screen
        core.wait(1.5)  # 1500 ms

        # Initial view
        background.draw()
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
            Image("background", "arrow").buffer().draw()
            update = Image(item[jj+7], "arrow").buffer()
            update.ori = 45
            update.draw()
            expWindow.flip()
            core.wait(2.5)  # 2500 ms

            # ISI
            expWindow.flip()
            core.wait(.5)  # 500 ms

        # questions ---------------------- now we have one column for update (it should get modified for two)
        for ii in range(3):
            if ii == 2 and not item[5]:  # check that the trial is two loads or three loads
                for j in range(2):
                    item.append("")
                break
            Image("background", "arrow").buffer().draw()
            Image("questionMark", "questionMark").buffer().draw()
            Image(item[11+ii*2], "questionLoad").buffer().draw()

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
                        Image("background", "arrow").buffer().draw()
                        Image("questionMark", "questionMark").buffer().draw()
                        Image(item[11+ii*2], "questionLoad").buffer().draw()
                        time_up_message.draw()
                        expWindow.flip()
                        core.wait(1)
                    else:
                        item.append(str(answer))
                        item.append(str(rt))
                    break
                if mouse.getPressed()[0]:
                    x, y = mouse.getPos()
                    answer = check_answer(x, y, item[12+ii*2])
                    rt = rtClock.getTime()
                    if practice:
                        Image("background", "arrow").buffer().draw()
                        Image("questionMark", "questionMark").buffer().draw()
                        Image(item[11+ii*2], "questionLoad").buffer().draw()
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
# experiment
# ===============================================================================

# -----------------------------------------------------------------------------
# instruction
Image("instruction", "arrow").buffer().draw()
expWindow.flip()  # flip blank screen
event.waitKeys(keyList=['space'])

# ------------------------------------------------------------------------------
# practice part
# run_trials(items, practice=True)

# ------------------------------------------------------------------------------
# experiment part
with open(output_file, 'w') as o:
    o.write(";".join(header[0]) + "\n")
    run_trials(trials_list)  # , practice=True)


import pdb
pdb.set_trace()

# ------------------------------------------------------------------------------
# finish screen

expWindow.flip()
event.waitKeys(keyList=['space'])

expWindow.close()
core.quit()
