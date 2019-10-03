from midiutil import MIDIFile
import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import os


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def createMidiFile(data_array, name):
    midiObj = MIDIFile(1)  # create one track
    midiObj.addTempo(0, 0, 120)

    for i, pitch in enumerate(data_array):
        int_pitch = int(round(pitch* 100)) 
        midiObj.addNote(0, 0, int_pitch,  i, 1, 100)
    
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

    createGraphs(clean_data, alert_data, True)

    createDirectory("midiFiles")
    createMidiFile(clean_data, "clean_midi")
    createMidiFile(alert_data, "alert_midi")
