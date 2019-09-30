from midiutil import MIDIFile


def createMidiFile(data_array, name):
    midiObj = MIDIFile(1)  # create one track
    midiObj.addTempo(0, 0, 120)

    for i, pitch in enumerate(data_array):
        int_pitch = round(pitch*100)
        midiObj.addNote(0, 0, int_pitch,  i, 1, 100)
    
    with open(name+".mid", "wb") as midiFile:
        midiObj.writeFile(midiFile)


def createFloatArray(file):
    data_array = []
    for line in file:
        data_array.extend(line.split())
    float_list = [float(i) for i in data_array]
    return float_list


if __name__ == "__main__":
    clean_stream = open("clean_stream.txt", "r")
    alert_stream = open("alert_stream.txt", "r")

    clean_data = createFloatArray(clean_stream)
    createMidiFile(clean_data, "clean_midi")

    alert_data = createFloatArray(alert_stream)
    createMidiFile(alert_data, "alert_midi")
