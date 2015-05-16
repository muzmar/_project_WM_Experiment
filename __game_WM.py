# -*- coding: utf-8 -*-
'''
@author: Hossein Sabri
@contact: hossein.sabri@gmail.com 
@date: 2015-05-12
'''

import time
import string
import codecs
#import random

#import psychopy as psp

from psychopy import visual, core, event, gui, data

#===============================================================================
# global variables: INTERFACE
#===============================================================================

PATH = 'C:\\pythonProjects\\_project_WM_Experiment'
FIXCROSS_SIZE = 40 #size of the fixation cross (the character '+' in Arial)
INSTR_CHAR_SIZE = 18 #character size for instructions
OUTPATH = '%s\\results\\'%(PATH) #output path for storing the results
AVAILABLE_KEYS = ['lctrl', 'rctrl', 'q']
LANGUAGE = 'DE' #which language is the experiment in: 'DE'=German. 'CN'=Chinese
MATCHING = {'lctrl':'left', 'rctrl':'right'} #matching of buttons to answers
SCREEN_SIZE = [800, 480] #what is your screen resolution?
LANG_FONT_MAP = {'DE':'Courier New', 'CN':'SimSun'} #what font is used for what language?
HALF_WIDTH = 432/8


#===============================================================================
# initial dialogue box
#===============================================================================
inputInfo = ['a', '']
count = 0
while inputInfo[0] != inputInfo[1] or not inputInfo[0].isdigit():
    expDlg = gui.Dlg(title="WM Experiment")
    expDlg.addText("Subject info")
    #expDlg.addField("Name:", fieldLength=25)
    expDlg.addField("Subject_ID:", fieldLength=25)
    expDlg.addField("Repeat__ID:", fieldLength=25)
    expDlg.addText("")
    #expDlg.addText("Experiment info")
    #expDlg.addField("Group:", choices=["Test", "Control"], fieldLength=25)
    #expDlg.addText("")
    if count:
        expDlg.addText("ERROR: IDs must be same integers", color='Red')
    expDlg.show()
    count += 1
    if expDlg.OK:
        inputInfo = expDlg.data
    else:
        core.quit()

#===============================================================================
# read stimuli
#===============================================================================

def read_stimuli(stimuli):
    itemList = []
    header = []
    with codecs.open(stimuli, 'rb', encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if '###' in line: #its the header
                line = line.split(';')
                header.append(line[0:21])
            elif len(line) == 0: #last line if an empty one
                break
            else:
                line = line.split(';')
                itemList.append(line[0:21]) #write entire rest of the line
    return itemList, header

#practice_items, practice_trial_order = read_stims('%s/%s/stimuli/Practice_PartWholeFaces_%s.txt'%(PATH,LANGUAGE,LANGUAGE))
items, header = read_stimuli('%s\\%s\\stimuli\\Trials_WMExperiment_%s.txt'%(PATH,LANGUAGE,LANGUAGE))


#===============================================================================
# Other preparations
#===============================================================================

expInfo = {'subjectName':inputInfo[0], 'subjectID':inputInfo[1], 'group':inputInfo[-1], "expName":"WM Experiment"}

output_file = OUTPATH + expInfo['expName'] + '_%s.txt'%expInfo['subjectID']
rt_clock = core.Clock() #reaction time clock

#create a window
expWindow = visual.Window(size=SCREEN_SIZE,monitor="testMonitor",color=(230,230,230), colorSpace='rgb255', units=u'pix')
# fullscr=True,

correct_answer_message = visual.TextStim(expWindow, pos=[0, 0], text="Richtig!", font='Courier New', bold=True,
                                         color=(0, 1.0, 0), height=50, alignHoriz='center', units=u'pix')
false_answer_message = visual.TextStim(expWindow, pos=[0, 0], text="Falsch!", font='Courier New', bold=True,
                                       color=(1.0, 0, 0), height=50, alignHoriz='center', units=u'pix')
time_up_message = visual.TextStim(expWindow, pos=[0, 0], text="Die Zeit ist um!", font='Courier New', bold=True,
                                         color=(1.0, 0, 0), height=35, alignHoriz='center', units=u'pix')

#===============================================================================
# read instructions
#===============================================================================

def check_answer(x, y, correct_answer):
    '''
    :param x: integer first dimension of mouse click
    :param y: integer second dimension of mouse click
    :param correct_answer: string
    :return:
    '''
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

    if (x >= interval[0] and x <= interval[1]) and (y >= interval[2] and y <= interval[3]):
        return True
    else:
        return False
#===============================================================================
# experiment class
#===============================================================================
class Image():


    def __init__(self, name, type, **kwargs):
        '''
        ** if the format of images are different(ie. .png, .jpg, .gif) give the complete name with extension and
        remove the ".png" from self.path
        :param name: name of the image
        :param type: can be "load", "arrow", "questionMark", "questionLoad"
        :return:
        '''
        self.path = '{0}\\images\\{1}.png'.format(PATH, name)
        self.type = type
        if 'loc' in kwargs:
            self.loc = kwargs['loc']

    def get_position(self):

        if self.type == "arrow":
            position = [0,0]
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

        bufferImage = visual.ImageStim(expWindow, image=self.path, pos=self.get_position(), units=u'pix')
        return bufferImage

#-----------------------------------------------------------------------------
# instruction
Image("instruction", "arrow").buffer().draw()
expWindow.flip() #flip blank screen
core.wait(10) #10000 ms

#------------------------------------------------------------------------------
# define trial procedure

def run_trials(items, practice=False):

    #loop through trials
    for i in [0,1]:#trial_order:

        item = items[i]#-1]

        #prepare stimulus and draw on screen
        background = Image("background", "arrow").buffer()
        cartoon1 = Image(item[1], "load", loc=item[2]).buffer()
        cartoon2 = Image(item[3], "load", loc=item[4]).buffer()

        #pre-stimulus interval
        expWindow.flip() #flip blank screen
        core.wait(1.5) #1500 ms

        # Initial view
        background.draw()
        cartoon1.draw()
        cartoon2.draw()
        if item[5]:
            Image(item[5], "load", loc=item[6]).buffer().draw()
        expWindow.flip()
        core.wait(3) #3000 ms

        # ISI
        expWindow.flip()
        core.wait(.5) #500 ms


        # updates
        for i in range(4):
            if i == 3 and not item[5]:
                break
            Image("background", "arrow").buffer().draw()
            update = Image(item[i+7], "arrow").buffer()
            update.ori = 45
            update.draw()
            expWindow.flip()
            core.wait(2.5) #2500 ms

            # ISI
            expWindow.flip()
            core.wait(.5) #500 ms

        # questions ---------------------- now we have one column for update (it should get modified for two)
        for i in range(3):
            if i == 2 and not item[5]:
                break
            Image("background", "arrow").buffer().draw()
            Image("questionMark", "questionMark").buffer().draw()
            #ques.ori = 45
            #ques.draw()
            Image(item[11+i*2], "questionLoad").buffer().draw()

            # mouse interaction
            mouse = event.Mouse(win=expWindow)
            expWindow.flip()
            rtClock = core.Clock()
            rtClock.reset()

            timeout = time.time() + 60*0.5   # 30 seconds from now
            while True:
                if time.time() > timeout:
                    answer = False
                    rt = 31
                    if practice:
                        Image("background", "arrow").buffer().draw()
                        Image("questionMark", "questionMark").buffer().draw()
                        Image(item[11+i*2], "questionLoad").buffer().draw()
                        time_up_message.draw()
                        expWindow.flip()
                        core.wait(1)
                    break
                if mouse.getPressed()[0]:
                    x, y = mouse.getPos()
                    answer = check_answer(x, y, item[12+i*2])
                    rt = rtClock.getTime()
                    if practice:
                        Image("background", "arrow").buffer().draw()
                        Image("questionMark", "questionMark").buffer().draw()
                        Image(item[11+i*2], "questionLoad").buffer().draw()
                        if answer:
                            correct_answer_message.draw()
                        else:
                            false_answer_message.draw()
                        expWindow.flip()
                        core.wait(1)
                    break

            # ISI
            expWindow.flip()
            core.wait(.5) #500 ms

        #write out answers
        #string_output = [expInfo['subjectID'], str(trial_count)] #initialize output list: subject ID, trial number (in exp)
        #string_output.extend([str(x) for x in item]) #add trial infos
        #string_output.extend([str(int(practice)),str(ans[-1]), str(match_answer(ans[-1], item[6])), str(rt)]) #add answer infos
        #outfile.write(';'.join(string_output) + '\n') #write to file


        #check if experiment was aborted
        #if len(ans) == 2:
        #    if ans[-2] == 'lctrl' and ans[-1] == 'q':
        #        expWindow.close()
        #        core.quit()

        #trial_count += 1


#===============================================================================
# experiment
#===============================================================================

#------------------------------------------------------------------------------
# present instructions
run_trials(items, practice=True)
import pdb
pdb.set_trace()

expWindow.flip()
event.waitKeys(keyList=['space'])

#------------------------------------------------------------------------------
# run experiment
with codecs.open(output_file, 'wb', encoding="utf-8") as outfile:

    #write outfile header
    #outfile.write('### Experiment: %s\n### Subject ID: %s\n### Date: %s\n\n' %(exp_info['exp_name'], exp_info['Subject'], exp_info['date']))
    outfile.write('subject_id;trial;trial_id;cond;face_id;sex;focus_part;face_id_foil;target_pos;first_pres_in_cond;image_name_target;image_name_l;image_name_r;practice;ans;correct;rt\n')
    #practice start if no questions

    expWindow.flip()
    event.waitKeys(keyList=['space'])

    #run practice trials
    #run_trials(practice_items, practice_trial_order, practice=True)

    #practice end
    #practice_end_screen.draw()
    #exp_win.flip()
    #event.waitKeys(keyList=['space'])

    #exp start
    run_trials(items, trial_order)

test_end_screen.draw()
expWindow.flip()
event.waitKeys()

expWindow.close()
core.quit()
