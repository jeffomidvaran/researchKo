from midiutil import MIDIFile
import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import os
import random


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def scale_and_randomize(pitch, max_shift=8192): 
    scaled_pitch = int(round(max_shift * pitch))  
    #  randomly choose between positive and negative value 
    random_bool = bool(random.getrandbits(1)) 
    if(random_bool == False):
        scaled_pitch = scaled_pitch * -1
    print(scaled_pitch)
    return scaled_pitch


def createMidiFile(data_array, name):
    midiObj = MIDIFile(3)  # create one track
    midiObj.addTempo(0, 0, 150)

        # 0 = C-2 
        # 12 = C-1 
        # 24 = C-0 
        # 36 = C1 
        # 48 = C2 
        # 60 = C3 
        # 72 = C4 

    for i, pitch in enumerate(data_array):
        print("start of notes") 
        ###############  HIGH TONIC NOTE ########## 
        midiObj.addNote(0, 0, 48,  i, 1, 100)
        midiObj.addPitchWheelEvent(0, 0, i, scale_and_randomize(pitch, 7000))

        ############ DOMINANT NOTE ############ 
        midiObj.addNote(1, 0, 55,  i + 0.333, 1, 100)
        midiObj.addPitchWheelEvent(1, 0, i, scale_and_randomize(pitch, 6000))

        ###############  LOW TONIC NOTE ########## 
        midiObj.addNote(2, 0, 60,  i + 0.6666, 1, 100)
        # midiObj.addPitchWheelEvent(2, 0, i, scale_and_randomize(pitch))

    with open("midiFiles/" + name + ".mid", "wb") as midiFile:
        midiObj.writeFile(midiFile)


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


if __name__ == "__main__":
    clean_stream = open("clean_stream.txt", "r")
    alert_stream = open("alert_stream.txt", "r")

    clean_data = createFloatArray(clean_stream)
    alert_data = createFloatArray(alert_stream)

    # createGraphs(clean_data, alert_data, True)

    createDirectory("midiFiles")
    createMidiFile(clean_data, "clean_midi")
    createMidiFile(alert_data, "alert_midi")
