import json
import os
import datetime
cdir = os.getcwd()
import sys
sys.path.append(cdir)
import analyze
from matplotlib import pyplot as plt

def graph(data, name, num = 0):

    start_time = analyze.get_start_time(data)

    specinfo = data[name]
    callsign = specinfo['Name']
    index = specinfo['Index']
    track = specinfo['Track']
    intervals = analyze.split_intervals(index)
    # print(intervals)
    tracker = 0
    tracks = []
    lengths = []
    times = []

    for interval in intervals:
        leng = interval[1] - interval[0] + 1
        track_slice = track[tracker: tracker+leng]
        tracker += leng + 1
        lengths.append(leng)
        tracks.append(track_slice)
        stastr = analyze.str_time(start_time, interval[0])
        endstr = analyze.str_time(start_time, interval[1])
        times.append((stastr, endstr))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(lengths[num]), tracks[num])
    ax.set_title("Interval %d for %s" % (num, callsign))
    ax.set_xlabel("From %s to %s" % (times[num][0], times[num][1]))
    ax.set_ylabel('dbm')
    ax.grid(True)
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        sys.exit("You need to provide filename!")
    if len(sys.argv) > 2:
        specname = sys.argv[2]
    else:
        sys.exit("You need to provide network MAC address!")
    if len(sys.argv) > 3:
        num = int(sys.argv[3])
    else:
        num = 0
    data = analyze.create_data(filename)
    graph(data, specname, num)
