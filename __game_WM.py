# -*- coding: utf-8 -*-
'''
@author: Hossein Sabri
@contact: hossein.sabri@gmail.com 
@date: 2015-05-12
'''

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
SCREEN_SIZE = [1000, 500] #what is your screen resolution?
LANG_FONT_MAP = {'DE':'Courier New', 'CN':'SimSun'} #what font is used for what language?
HALF_WIDTH = 432/8


#===============================================================================
# initial dialogue box
#===============================================================================
inputInfo = ['', 'a', '']
count = 0
while inputInfo[1] != inputInfo[2] or not inputInfo[1].isdigit():
    expDlg = gui.Dlg(title="WM Experiment")
    expDlg.addText("Subject info")
    expDlg.addField("Name:", fieldLength=25)
    expDlg.addField("ID:", fieldLength=25)
    expDlg.addField("ID:", fieldLength=25)
    expDlg.addText("")
    expDlg.addText("Experiment info")
    expDlg.addField("Group:", choices=["Test", "Control"], fieldLength=25)
    expDlg.addText("")
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

print header
print items

import pdb
pdb.set_trace()
#===============================================================================
# Other preparations
#===============================================================================

expInfo = {'subjectName':inputInfo[0], 'subjectID':inputInfo[1], 'group':inputInfo[-1], "expName":"WM Experiment"}

output_file = OUTPATH + expInfo['expName'] + '_%s.txt'%expInfo['subjectID']
rt_clock = core.Clock() #reaction time clock

#create a window
expWindow = visual.Window(size=SCREEN_SIZE, monitor="testMonitor", color=(230,230,230), colorSpace='rgb255', units="deg")
# fullscr=True,

#===============================================================================
# read instructions
#===============================================================================

def match_answer(answer_given, condition):
    '''
    Function to match the answer of the participant with the correct answer.
    lctrl: left
    rctrl: right
    '''
    return int(MATCHING.get(answer_given, 'escape') == condition)

#===============================================================================
# experiment class
#===============================================================================
class Cartoon():


    def get_position(self, loc):

        if loc == "A1":
            position = [-3*HALF_WIDTH, -3*HALF_WIDTH]
        elif loc == "A2":
            position = [-HALF_WIDTH, -3*HALF_WIDTH]
        elif loc == "A3":
            position = [HALF_WIDTH, -3*HALF_WIDTH]
        elif loc == "A4":
            position = [3*HALF_WIDTH, -3*HALF_WIDTH]
        elif loc == "B1":
            position = [-3*HALF_WIDTH, -HALF_WIDTH]
        elif loc == "B2":
            position = [-HALF_WIDTH, -HALF_WIDTH]
        elif loc == "B3":
            position = [HALF_WIDTH, -HALF_WIDTH]
        elif loc == "B4":
            position = [3*HALF_WIDTH, -HALF_WIDTH]
        elif loc == "C1":
            position = [-3*HALF_WIDTH, HALF_WIDTH]
        elif loc == "C2":
            position = [-HALF_WIDTH, HALF_WIDTH]
        elif loc == "C3":
            position = [HALF_WIDTH, HALF_WIDTH]
        elif loc == "C4":
            position = [3*HALF_WIDTH, HALF_WIDTH]
        if loc == "D1":
            position = [-3*HALF_WIDTH, 3*HALF_WIDTH]
        elif loc == "D2":
            position = [-HALF_WIDTH, 3*HALF_WIDTH]
        elif loc == "D3":
            position = [HALF_WIDTH, 3*HALF_WIDTH]
        elif loc == "D4":
            position = [3*HALF_WIDTH, 3*HALF_WIDTH]

        self.pos = position


    def image_path(self, type):

        self.image = '%s/images/%s.png'%(PATH, type)



#------------------------------------------------------------------------------
# define trial procedure

def run_trials(items, trial_order, practice=False):

    trial_count = 1

    #loop through trials
    for i in [0,1]:#trial_order:

        item = items[i]#-1]

        #prepare stimulus and draw on screen
        background = visual.ImageStim(expWindow, image='%s/images/background.gif'%PATH, pos=[-0,0], units=u'pix')
        cartoon1 = visual.ImageStim(expWindow, image='%s/images/%s.png'%(PATH, item[1]), pos=[-200,0], units=u'pix')
        stim_right = visual.ImageStim(expWindow, image='%s/%s/stimuli/%s%s'%(PATH, LANGUAGE, item_prefix, item[10]), pos=[200,0], units=u'pix')

        #pre-stimulus interval
        expWindow.flip() #flip blank screen
        core.wait(1.3) #1300 ms

        #fix_cross
        fix_cross.draw()
        expWindow.flip()
        core.wait(0.2) #200 ms

        #draw target
        target.draw()
        expWindow.flip()
        core.wait(1) #1000 ms

        #mask (200 ms)
        mask.draw()
        expWindow.flip()
        core.wait(0.2) #200 ms

        #blank (1 cycle)
        expWindow.flip()

        #draw to back buffer
        stim_left.draw()
        stim_right.draw()
        reminder_screen.draw()
        #present
        expWindow.flip()

        #start reaction time clock and collect answer
        rt_clock.reset()
        ans = event.waitKeys(keyList=AVAILABLE_KEYS)

        #get reaction time
        rt = rt_clock.getTime()

        #write out answers
        string_output = [expInfo['subjectID'], str(trial_count)] #initialize output list: subject ID, trial number (in exp)
        string_output.extend([str(x) for x in item]) #add trial infos
        string_output.extend([str(int(practice)),str(ans[-1]), str(match_answer(ans[-1], item[6])), str(rt)]) #add answer infos
        outfile.write(';'.join(string_output) + '\n') #write to file

        if practice and match_answer(ans[-1], item[6]):
            correct_screen.draw()
            expWindow.flip()
            core.wait(1)
        elif practice:
            incorrect_screen.draw()
            expWindow.flip()
            core.wait(1)

        #check if experiment was aborted
        if len(ans) == 2:
            if ans[-2] == 'lctrl' and ans[-1] == 'q':
                expWindow.close()
                core.quit()

        trial_count += 1


#===============================================================================
# experiment
#===============================================================================

#------------------------------------------------------------------------------
# present instructions
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

