from midiutil import MIDIFile
import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import itertools
import midi2audio

# 0 = C-2 
# 12 = C-1 
# 24 = C-0 
# 36 = C1 
# 48 = C2 
# 60 = C3 
# 72 = C4 

WHOLE_NOTE         = 4
HALF_NOTE          = 2
QUARTER_NOTE       = 1
EIGHTH_NOTE        = 1/2
SIXTEEN_NOTE       = 1/4
THIRTY_SECOND_NOTE = 1/8


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def scale_and_randomize(pitch, max_shift=8192): 
    scaled_pitch = int(round(max_shift * pitch))  
    result = random.randint(-scaled_pitch, scaled_pitch)
    return result


def createFloatArray(file):
    data_array = []
    for line in file:
        data_array.extend(line.split())
    return np.array([float(i) for i in data_array])


def createGraphs(clean_data, alert_data, create_png):
    x1 = np.arange(0.0, clean_data.size, 1)
    x2 = np.arange(0.0, alert_data.size, 1)

    fig, ax = plt.subplots()
    ax.plot(x1, clean_data)

    plt.subplot(2, 1, 1)
    plt.plot(x1, clean_data, 'o-')
    plt.title('Clean Stream')
    plt.ylabel('Simulated Data')
    plt.xlabel('time (s)')

    plt.subplot(2, 1, 2)
    plt.plot(x2, alert_data, '.-')
    plt.title('Alert Stream')
    plt.xlabel('time (s)')
    plt.ylabel('Simulated Data')
    plt.tight_layout()
    if(create_png == True): 
        fig.savefig("data.png") # create png of data
    plt.show()


def CreateDroneMidiFile(data_array, name): 
    print("creating Drone " + name + " midi file")
    midiObj = MIDIFile(3)  # create one track
    midiObj.addTempo(0, 0, 150)
    
    #               track, channel, pitch, time      , duration      , volume
    midiObj.addNote(0    , 0      , 48   , 0         ,len(data_array)/4, 100 )
    midiObj.addNote(1    , 0      , 55   , 0         ,len(data_array)/4, 100 )
    midiObj.addNote(2    , 0      , 60   , 0         ,len(data_array)/4, 100 )

    for i, pitch in enumerate(data_array):
        forward =  i/4
        ######## HIGH TONIC NOTE PITCHBEND #################### 
        midiObj.addPitchWheelEvent(0, 0, forward, scale_and_randomize(pitch, 7000))

        ######## DOMINANT NOTE PITCHBEND ###################### 
        midiObj.addPitchWheelEvent(1, 0, forward, scale_and_randomize(pitch, 6000))

        #######  LOW TONIC NOTE PITCHBEND #####################
        # midiObj.addPitchWheelEvent(2, 0, note_division, scale_and_randomize(pitch))

    with open("midiFiles/" + name + ".mid", "wb") as midiFile:
        midiObj.writeFile(midiFile)



def createArpegiatedMidiFile(data_array, name):
    midiObj = MIDIFile(3)  # create one track
    midiObj.addTempo(0, 0, 150)

    for i, pitch in enumerate(data_array):
        forward = i*2
        ######## HIGH TONIC NOTE #################### 
        #               track, channel, pitch, time      , duration    , volume
        midiObj.addNote(0    , 0      , 48   ,(forward + i)/4  , SIXTEEN_NOTE, 100)
        midiObj.addPitchWheelEvent(0, 0, (forward +i)/4, scale_and_randomize(pitch, 7000))

        ######## DOMINANT NOTE ###################### 
        midiObj.addNote(1, 0, 55, (forward +i + 1)/4, SIXTEEN_NOTE, 100)
        midiObj.addPitchWheelEvent(1, 0, (forward + i + 1) /4, scale_and_randomize(pitch, 6000))

        #######  LOW TONIC NOTE #####################
        midiObj.addNote(2, 0, 60, (forward + i + 2)/4, SIXTEEN_NOTE, 100)
        # midiObj.addPitchWheelEvent(2, 0, note_division, scale_and_randomize(pitch))
    
    with open("midiFiles/" + name + ".mid", "wb") as midiFile:
        midiObj.writeFile(midiFile)



def createMelody(melody_pitches, melody_rhythm, clean_data, alert_dat, midiObj):
    if(len(melody_pitches) != len(melody_rhythm)):
            print("ERROR: Number of pitches and assigned rhythms is not equal.")
            raise Exception

    iter_melody_data = clean_data.__iter__()
    
    note_position = 0  # 1 == sixteenth note

    for data_point in iter_melody_data:

        if(data_point == 1):
            melody_pitches_iter = melody_pitches.__iter__()
            melody_rhythm_iter = melody_rhythm.__iter__()

            for i in range(len(melody_pitches)):
                note_duration = melody_rhythm_iter.__next__()

                midiObj.addNote(
                                2,  # track
                                0,  # channel
                                melody_pitches_iter.__next__(), # pitch 
                                note_position/4,  # time
                                note_duration, # duration
                                100   # volume
                )

                if(note_duration == SIXTEEN_NOTE): 
                    note_position += 1
                    iter_melody_data.__next__()
                elif(note_duration == EIGHTH_NOTE):
                    skip = 2
                    note_position += skip
                    for _ in range(skip): iter_melody_data.__next__()
                elif(note_duration == QUARTER_NOTE):
                    skip = 4
                    note_position += skip
                    for _ in range(skip): iter_melody_data.__next__()
                elif(note_duration == HALF_NOTE):
                    skip = 8
                    note_position += skip
                    for _ in range(skip): iter_melody_data.__next__()
                elif(note_duration == WHOLE_NOTE):
                    skip = 16
                    note_position += skip
                    for _ in range(skip): iter_melody_data.__next__()
        else: 
            note_position+= 1
    return midiObj



def create_midi_clean_rythmic_dirty_melody(clean_data, alert_data, name, rhythm = False):
    midiObj = MIDIFile(3)  # create one track
    midiObj.addTempo(0, 0, 150)

    ####################################################################
    ##################  CREATE RHYTHM ##################################  
    ####################################################################
    if( rhythm == True):    
        clean_rhythm_length = round(len(clean_data)/16)
        note_cutoff = 0.05

        for i in range(clean_rhythm_length):
            forward = i * 4
            ######## HIGH TONIC NOTE #################### 
            #               track, channel, pitch, time      , duration    , volume
            midiObj.addNote(0    , 0      , 48   , forward  , WHOLE_NOTE - note_cutoff, 100)

            ######## DOMINANT NOTE ###################### 
            midiObj.addNote(1, 0, 55, forward, WHOLE_NOTE - note_cutoff, 100)

            #######  LOW TONIC NOTE #####################
            midiObj.addNote(2, 0, 36, forward, WHOLE_NOTE - note_cutoff, 100)

    else: 
            duration = len(clean_data)/4
            ######## HIGH TONIC NOTE #################### 
            #               track, channel, pitch, time      , duration    , volume
            midiObj.addNote(0    , 0      , 48   , 0  , duration, 100)

            ######## DOMINANT NOTE ###################### 
            midiObj.addNote(1, 0, 55, 0, duration, 100)

            #######  LOW TONIC NOTE #####################
            midiObj.addNote(2, 0, 36, 0, duration, 100)


    ####################################################################
    ##################  CREATE PTICH BEND ##############################  
    ####################################################################
   
    
    for i, data_point in enumerate(clean_data):
        note_position = i/4
        ######## HIGH TONIC NOTE PITCHBEND #################### 
        midiObj.addPitchWheelEvent(0, 0, note_position, scale_and_randomize(data_point))

        ######## DOMINANT NOTE PITCHBEND ###################### 
        midiObj.addPitchWheelEvent(1, 0, note_position, scale_and_randomize(data_point))

        #######  LOW TONIC NOTE PITCHBEND #####################
        midiObj.addPitchWheelEvent(2, 0, note_position, scale_and_randomize(data_point))

    ####################################################################
    ##################  CREATE MELODY ##################################  
    ####################################################################
   

    melody_pitches = [
                       77,
                       84,
                       81,79,77,74,
                       75,73
    ]

    melody_rhythm = [
                       QUARTER_NOTE,
                       QUARTER_NOTE,
                       SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE, 
                       EIGHTH_NOTE,EIGHTH_NOTE,   
    ]

    midiObj = createMelody(melody_pitches, melody_rhythm, clean_data, alert_data, midiObj)

    with open("midiFiles/" + name + ".mid", "wb") as midiFile:
        midiObj.writeFile(midiFile)



if __name__ == "__main__":
    clean_stream = open("clean_stream.txt", "r")
    alert_stream = open("alert_stream.txt", "r")

    clean_data = createFloatArray(clean_stream)
    alert_data = createFloatArray(alert_stream)

    # createGraphs(clean_data, alert_data, True)

    createDirectory("midiFiles")
    create_midi_clean_rythmic_dirty_melody(clean_data, alert_data,
                                            "clean_rhythm_alert_melody", False) 

    # CreateDroneMidiFile(clean_data, "CleanDrone")
    # createMidiFile(clean_data, "clean_arpeg", True)
    # createMidiFile(clean_data, "clean", False)
    # createMidiFile(alert_data, "alert_midi", False)
