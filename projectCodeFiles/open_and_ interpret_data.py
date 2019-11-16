from midiutil import MIDIFile
import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import itertools
import midi2audio

WHOLE_NOTE         = 4
HALF_NOTE          = 2
QUARTER_NOTE       = 1
EIGHTH_NOTE        = 1/2
SIXTEEN_NOTE       = 1/4
THIRTY_SECOND_NOTE = 1/8


note = {
    "c-2" :0 ,
    "cs-2":1 ,
    "d-2" :2 ,
    "ds-2":3 ,
    "e-2" :4 ,
    "f-2" :5 ,
    "fs-2":6 ,
    "g-2" :7 ,
    "gs-2":8 ,
    "a-2" :9 ,
    "as-2":10,
    "b-2" :11,
    
    "c-1" :12,
    "cs-1":13,
    "d-1" :14,
    "ds-1":15,
    "e-1" :16,
    "f-1" :17,
    "fs-1":18,
    "g-1" :19,
    "gs-1":20,
    "a-1" :21,
    "as-1":22,
    "b-1" :23,
     
    "c0"  :24,
    "cs0" :25,
    "d0"  :26,
    "ds0" :27,
    "e0"  :28,
    "f0"  :29,
    "fs0" :30,
    "g0"  :31,
    "gs0" :32,
    "a0"  :33,
    "as0" :34,
    "b0"  :35,
      
    "c1"  :36,
    "cs1" :37,
    "d1"  :38,
    "ds1" :39,
    "e1"  :40,
    "f1"  :41,
    "fs1" :42,
    "g1"  :43,
    "gs1" :44,
    "a1"  :45,
    "as1" :46,
    "b1"  :47,
     
    "c2"  :48,
    "cs2" :49,
    "d2"  :50,
    "ds2" :51,
    "e2"  :52,
    "f2"  :53,
    "fs2" :54,
    "g2"  :55,
    "gs2" :56,
    "a2"  :57,
    "as2" :58,
    "b2"  :59,

    
    "c3"  :60,
    "cs3" :61,
    "d3"  :62,
    "ds3" :63,
    "e3"  :64,
    "f3"  :65,
    "fs3" :66,
    "g3"  :67,
    "gs3" :68,
    "a3"  :69,
    "as3" :70,
    "b3"  :71,
     
    "c4"  :72,
    "cs4" :73,
    "d4"  :74,
    "ds4" :75,
    "e4"  :76,
    "f4"  :77,
    "fs4" :78,
    "g4"  :79,
    "gs4" :80,
    "a4"  :81,
    "as4" :82,
    "b4"  :83,
      
    "c5"  :84,
    "cs5" :85,
    "d5"  :86,
    "ds5" :87,
    "e5"  :88,
    "f5"  :89,
    "fs5" :90,
    "g5"  :91,
    "gs5" :92,
    "a5"  :93,
    "as5" :94,
    "b5"  :95,
       
    "c6"  :96,
    "cs6" :97,
    "d6"  :98,
    "ds6" :99,
    "e6"  :100,
    "f6"  :101,
    "fs6" :102,
    "g6"  :103,
    "gs6" :104,
    "a6"  :105,
    "as6" :106,
    "b6"  :107,
    
    "c7"  :108,
    "cs7" :109,
    "d7"  :110,
    "ds7" :111,
    "e7"  :112,
    "f7"  :113,
    "fs7" :114,
    "g7"  :115,
    "gs7" :116,
    "a7"  :117,
    "as7" :118,
    "b7"  :119,
    }

def random_offset(start = -0.01, end = 0.01):
    return round(random.uniform(start,end),3)

def random_velocity(low = 100,high = 127):
    return random.randint(low, high)



def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def scale_and_randomize(data_point, max_shift=8192): 
    scaled_pitch = int(round(max_shift * data_point))  
    return random.randint(-scaled_pitch, scaled_pitch)



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



def createMelody(melody_pitches, melody_rhythm, data, midiObj, track):
    if(len(melody_pitches) != len(melody_rhythm)):
            print("ERROR: Number of pitches and assigned rhythms is not equal.")
            raise Exception

    iter_melody_data = data.__iter__()
    
    note_position = 0  # 1 == sixteenth note

    for data_point in iter_melody_data:

        if(data_point == 1):
            melody_pitches_iter = melody_pitches.__iter__()
            melody_rhythm_iter = melody_rhythm.__iter__()

            for i in range(len(melody_pitches)):
                note_duration = melody_rhythm_iter.__next__()

                midiObj.addNote(
                                track,  # track
                                0,  # channel
                                melody_pitches_iter.__next__(), # pitch 
                                note_position/4 + random_offset(),  # time
                                note_duration, # duration
                                random_velocity()   # volume
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



def create_midi_with_melody(clean_data, alert_data, name, arpegiation):
    midiObj = MIDIFile(4)  # create one track
    midiObj.addTempo(0, 0, 150)

    ####################################################################
    ##################  CREATE ARPEGGIATION  ########################### 
    ####################################################################

    if(arpegiation == True):    
        clean_rhythm_length = round(len(clean_data)/16)
        note_cutoff = 0.02

        for i in range(clean_rhythm_length):
            forward = i * 4
            #               track, channel, pitch, time      , duration    , volume
            midiObj.addNote(0, 0, note["c1"], forward                   , SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(1, 0, note["g2"], forward + SIXTEEN_NOTE    , SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(2, 0, note["c3"], forward + SIXTEEN_NOTE *2 , SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(1, 0, note["g2"], forward + SIXTEEN_NOTE *3 , SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(0, 0, note["c1"], forward + SIXTEEN_NOTE *4 , SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(1, 0, note["g2"], forward + SIXTEEN_NOTE *5 , SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(2, 0, note["c3"], forward + SIXTEEN_NOTE *6 , SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(1, 0, note["g2"], forward + SIXTEEN_NOTE *7 , SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(0, 0, note["c1"], forward + SIXTEEN_NOTE *8 , SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(1, 0, note["g2"], forward + SIXTEEN_NOTE *9 , SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(2, 0, note["c3"], forward + SIXTEEN_NOTE *10, SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(1, 0, note["g2"], forward + SIXTEEN_NOTE *11, SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(0, 0, note["c1"], forward + SIXTEEN_NOTE *12, SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(1, 0, note["g2"], forward + SIXTEEN_NOTE *13, SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(2, 0, note["c3"], forward + SIXTEEN_NOTE *14, SIXTEEN_NOTE - note_cutoff, 100)
            midiObj.addNote(1, 0, note["g2"], forward + SIXTEEN_NOTE *15, SIXTEEN_NOTE - note_cutoff, 100)


    ####################################################################
    ##################  CREATE DRONE ###################################  
    ####################################################################

    else: 
            duration = len(clean_data)/4
            #               track, channel, pitch, time      , duration    , volume
            midiObj.addNote(0    , 0      , note["c2"]   , 0  , duration, 100)
            midiObj.addNote(1, 0, note["g2"], 0, duration, 100)
            midiObj.addNote(2, 0, note["c1"], 0, duration, 100)


    ####################################################################
    ##################  CREATE PTICH BEND ##############################  
    ####################################################################
   
    
    pitch_bend_ceiling = [0,0,0]
    max_shift = 8192
    previous_data_point = 0
    for i, data_point in enumerate(clean_data):
        note_position = i/4

        if(previous_data_point == 0.0 and data_point > 0.0):
            pitch_bend_ceiling[0] = int(round(max_shift * random.uniform(-1.0, 1.0)))
            pitch_bend_ceiling[1] = int(round(max_shift * random.uniform(-1.0, 1.0)))
            pitch_bend_ceiling[2] = int(round(max_shift * random.uniform(-1.0, 1.0)))
        elif(previous_data_point > 0 and data_point == 0.0): 
            pitch_bend_ceiling = [0,0,0]

        ######## HIGH TONIC NOTE PITCHBEND #################### 
        #                          track, channel, time         , pitchWheelValue
        midiObj.addPitchWheelEvent(0    , 0      , note_position, pitch_bend_ceiling[0])
        midiObj.addPitchWheelEvent(1    , 0      , note_position, pitch_bend_ceiling[1])
        midiObj.addPitchWheelEvent(2    , 0      , note_position, pitch_bend_ceiling[2])

        previous_data_point = data_point


    ####################################################################
    ##################  CREATE MELODY ##################################  
    ####################################################################
   

    melody_pitches1 = [
                       note["c5"],note["c5"], note["c5"],note["c5"], 
                       note["c5"],note["c5"], note["c5"],note["c5"], 
                       note["c6"],note["c6"], note["c6"],note["c6"], 
                       note["c6"],note["c6"], note["c6"],note["c6"], 
    ]

    melody_rhythm1 = [
                       SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,   
                       SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,   
                       SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,   
                       SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,   
    ]
   

    melody_pitches2 = [
                       note["c5"], note["cs5"], note["d5"], note["ds5"], note["e5"], note["f5"], note["fs5"], 
                       note["c6"], note["cs6"], note["d6"], note["ds6"], note["e6"], note["f6"], note["fs6"], 
                       note["c5"], note["cs5"], note["d5"], note["ds5"], note["e5"], note["f5"], note["fs5"], 
                       note["c6"], note["cs6"], note["d6"], note["ds6"], note["e6"], note["f6"], note["fs6"], 
    ]

    melody_rhythm2 = [
                       SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE, SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,
                       SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE, SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,  
                       SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE, SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,  
                       SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE, SIXTEEN_NOTE,SIXTEEN_NOTE,SIXTEEN_NOTE,  
    ]



    melody_pitches3 = [
                       note["c5"], note["fs5"], note["cs6"], note["gs6"], note["ds7"], note["as7"], 
                       note["ds7"], note["gs6"], note["cs6"], note["gs5"], note["c5"], note["f4"]
    ]

    melody_rhythm3 = [
                       EIGHTH_NOTE,EIGHTH_NOTE,EIGHTH_NOTE,EIGHTH_NOTE,EIGHTH_NOTE,EIGHTH_NOTE, 
                       EIGHTH_NOTE,EIGHTH_NOTE,EIGHTH_NOTE,EIGHTH_NOTE,EIGHTH_NOTE, EIGHTH_NOTE, 

    ]


    midiObj = createMelody(melody_pitches2, melody_rhythm2, alert_data, midiObj, 3)
    # midiObj = createMelody(melody_pitches2, melody_rhythm2, alert_data, midiObj, 3)
    # midiObj = createMelody(melody_pitches3, melody_rhythm3, alert_data, midiObj, 3)

    with open("midiFiles/" + name + ".mid", "wb") as midiFile:
        midiObj.writeFile(midiFile)


if __name__ == "__main__":
    clean_stream = open("clean_stream.txt", "r")
    alert_stream = open("alert_stream.txt", "r")

    clean_data = createFloatArray(clean_stream)
    alert_data = createFloatArray(alert_stream)

    # createGraphs(clean_data, alert_data, True)

    createDirectory("midiFiles")
    create_midi_with_melody(clean_data, 
                            alert_data,
                            "melody2_with_arpeg", 
                            True) 

