import json
import os
import datetime
cdir = os.getcwd()
import sys
sys.path.append(cdir)
from readfile import filedata as read


""" Calls a dictionary to be analyzed """
def create_data(filename):
    # Input types json and log accepted.
    fn = filename.split('.')
    fout = fn[0] + '_report.txt'
    if fn[1] == 'json':
        with open(filename) as json_data:
            data = json.load(json_data)
    elif fn[1] == 'log':
        data = read(filename)
    else:
        sys.exit("File not found")
    return data, fout


""" Returns continuous time interval the radio source has been present. """
def split_intervals(somelist):
    intervals = []
    start_cond = True;
    for element in somelist:
        if start_cond:
            start_tracker = element
            dummy_tracker = element
            start_cond = False
        else:
            increment = element - dummy_tracker
            if increment == 1 and element is not somelist[-1]:
                dummy_tracker = element
            elif element is somelist[-1]:
                intervals.append((start_tracker, element))
            else:
                intervals.append((start_tracker, dummy_tracker))
                start_tracker = element
                dummy_tracker = element
    return intervals


""" Return a string representation of time. """
def str_time(time, index):
    index -= 9 # Append stable time factor.
    new_time = time + datetime.timedelta(seconds=index*5)
    date = new_time.strftime('%d %b %H:%M:%S')
    return date


""" Get int month from string abbreviation """
def get_month(string):
    months = {
        'Jan' : 1,
        'Feb' : 2,
        'Mar' : 3,
        'Apr' : 4,
        'May' : 5,
        'Jun' : 6,
        'Jul' : 7,
        'Aug' : 8,
        'Sep' : 9,
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12
    }
    return months[string]


""" Convert seconds into clearly readable format """
def time_str(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    days, h = divmod(h, 24)
    daystr = ""
    if days > 0:
        daystr += "%d days " % days
    timestr = "%d hr %02d min %02d sec" % (h, m, s)
    timestr = daystr + timestr
    return timestr


def get_start_time(data):
    start = data['Stable_Time']
    time = list(map(int, start.split()[2].split(':')))
    year = int(start.split()[3])
    month = get_month(start.split()[1])
    day = int(start.split()[0])
    start_time = datetime.datetime(year,month,day,*time)
    return start_time


""" Analyze and output results """
def analyze(data, fout='', dt=5, skip=False):

    #Get Stable time
    start_time = get_start_time(data)

    fo = open(fout, 'a')

    if skip==True:
        fo.write("This report has stripped existing wifi network like Duke and eduroam\n")
        print("This report has stripped existing wifi network like Duke and eduroam")

    for key, value in data.items():

        # Skip Stable_Time and End_Time entrees
        if key == 'Stable_Time' or key == 'End_Time':
            continue

        if skip==True:
            name = value['Name']
            ignorelist = ['Duke', 'duke', 'edu', 'HP', 'Open']
            if any(ignored in name for ignored in ignorelist):
                continue

        index = value['Index']
        intervals = split_intervals(index)

        #Get time strings
        times = []
        for interval in intervals:
            stastr = str_time(start_time, interval[0])
            endstr = str_time(start_time, interval[1])
            times.append((stastr, endstr))

        # Get strength and length information.
        track = value['Track']
        mini = min(track)
        maxi = max(track)
        length = len(track)*dt
        timestr = time_str(length)

        # Get some other information
        name = value['Name']
        freq = value['Frequency']

        # Print header
        print("\nRadio Source: %s \nMAC: %s \t Frequency: %s MHz \nAppeared for %s"
        % (name, key, freq, timestr))
        fo.write("\nRadio Source: %s \nMAC: %s \t Frequency: %s MHz \nAppeared for %s\n"
        % (name, key, freq, timestr))

        # Print time intervals
        intervalnum = len(times)

        fo.write("It has been detected in %d intervals\n" % intervalnum)
        if intervalnum > 20:
            fo.write("The interval of it's existance is :\n")
            fo.write("From %s to %s\n" % (times[0][0], times[-1][1]))
            fo.write("A full list of intervals are not printed due to there are too many of them\n")
        else:
            for time in times:
                fo.write("Detected from %s to %s\n" % (time[0], time[1]))
        fo.write("It's power ranged from %d ~ %d dbm\n" % (mini, maxi))

        print("It has been detected in %d intervals" % intervalnum)
        if intervalnum > 20:
            print("The interval of it's existance is :")
            print("From %s to %s" % (times[0][0], times[-1][1]))
            print("A full list of intervals are not printed due to there are too many of them")
        else:
            for time in times:
                print("Detected from %s to %s" % (time[0], time[1]))

        print("It's power ranged from %d ~ %d dbm" % (mini, maxi))
        
    fo.close()

        # IF FOUT EXIST

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        sys.exit("You need to specify the filename!")
    filename = sys.argv[1]
    data, fout = create_data(filename)
    if (len(sys.argv) > 2):
        boo = (sys.argv[2] == 'True')
        analyze(data, fout=fout, skip=boo)
    else:
        analyze(data, fout=fout)
