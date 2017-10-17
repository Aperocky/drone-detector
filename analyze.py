import json
import os
import datetime
cdir = os.getcwd()
import sys
sys.path.append(cdir)
from readfile import filedata as read

def create_data(filename):

    fn = filename.split('.')
    if fn[1] == 'json':
        with open(filename) as json_data:
            data = json.load(json_data)
    elif fn[1] == 'log':
        data = read(filename)
    else:
        sys.exit("File not found")
    return data

def analyze(data, *args):

    switch = False
    if (len(args) > 0):
        fout = args[0]
        switch = True

    print(args)
    print(switch)

    start = data['Start_Time']
    time = list(map(int, start.split()[2].split(':')))
    start_time = datetime.datetime(100,1,1,*time)
    end = data['End_Time']
    time = list(map(int, end.split()[2].split(':')))
    end_time = datetime.datetime(100,1,1,*time)

    for key, value in data.items():
        if key == 'Start_Time' or key == 'End_Time':
            continue
        index = value['Index']

        #Get times
        index_min = min(index)
        begin_time = start_time + datetime.timedelta(seconds=index_min*5)
        btstr = str(begin_time.time())
        index_max = max(index)
        finish_time = start_time + datetime.timedelta(seconds=index_max*5)
        ftstr = str(end_time.time())

        track = value['Track']
        mini = min(track)
        maxi = max(track)
        length = len(track)*5
        name = value['Name']
        freq = value['Frequency']
        print("\nRadio Source: %s \nMAC: %s \t Frequency: %s MHz \nAppeared for %d seconds"
        % (name, key, freq, length))
        print("First detected in %s, and last found in %s" % (btstr, ftstr))
        print("It's power ranged from %d ~ %d dbm" % (mini, maxi))

        # IF FOUT EXIST
        if switch:
            with open(fout, 'a') as f:
                print("\nRadio Source: %s \nMAC: %s \t Frequency: %s MHz \nAppeared for %d seconds"
                % (name, key, freq, length), file=f)
                print("First detected in %s, and last found in %s" % (btstr, ftstr), file=f)
                print("It's power ranged from %d ~ %d dbm" % (mini, maxi), file=f)

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        sys.exit("You need to specify the filename!")
    filename = sys.argv[1]
    data = create_data(filename)
    if (len(sys.argv) > 2):
        fout = sys.argv[2]
        analyze(data, fout)
    else:
        analyze(data)
