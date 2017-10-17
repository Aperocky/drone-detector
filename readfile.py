import sys
import json
import os
cdir = os.getcwd()
sys.path.append(cdir)

def filedata(filename, *args):
    data = {}
    fi = open(filename, 'r')
    index = 1

    # Find the start of the first scan
    while(True):
        line = fi.readline()
        if 'ITERATION' in line:
            index = int(line.split()[1])
            break

    # Read each scan
    while(True):
        line = fi.readline()

        # Break if reach EOF.
        if not line:
            data['End_Time'] = time
            break

        # For first scan, the iteration is already read, so we must consider that.
        if 'ITERATION' in line:
            # INDEX of the iteration, very important!
            index = int(line.split()[1])
            line  = fi.readline()

        # Process time string
        timepiece = line.split()
        time = " ".join(timepiece[1:4])
        if not 'Start_Time' in data:
            data['Start_Time'] = time

        # Read the scanned entries
        while(True):
            line = fi.readline()
            if 'END' in line:
                break
            info = line.split()

            # MAC address of radio emitter
            mac = info[0]

            # Strength of radio emitter
            strength = int(info[2])

            # Create a tuple that contains the index(time) and strength
            # track = index, strength

            # Update dictionary of the wifi source, if source doesn't exist, create new source (dictionary).
            if mac in data:
                data[mac]['Track'].append(strength)
                data[mac]['Index'].append(index)
            else:
                newdic = {}
                newdic['Name'] = " ".join(info[4:])
                newdic['Frequency'] = info[1]
                newdic['Index'] = []
                newdic['Index'].append(index)
                newdic['Track'] = []
                newdic['Track'].append(strength)
                data[mac] = newdic

    # Dump dict into json just for fun
    print("Completed generating dictionary object, dumping to json..")
    fintend = filename.split('.')[0] + ".json"
    # if not os.path.isfile(fintend):
    with open(fintend, 'w') as fr:
        json.dump(data, fr)

    # Check for error
    # print(data)
    return data

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        sys.exit("You need to specify the filename!")
    filename = sys.argv[1]
    filedata(filename)
