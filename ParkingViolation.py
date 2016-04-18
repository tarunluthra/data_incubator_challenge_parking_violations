import csv
import matplotlib.pyplot as plt
import pprint as pp

def main():
    #Read data from CSV file
    violations = getData()
    print str(len(violations)) + " rows of data"

    #bin the data. Each bin is a 2hr time block
    #  create frequency the bins
    bins = [0] * 4380

    #  get the bin number and add one to it
    for violation in violations:
        bin_number = getBinNumber(violation)
        if bin_number < 4380:
            bins[bin_number] += 1

    with open('histogram.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for n, bin in enumerate(bins):
            writer.writerow([getMonthFromBin(n), bin])

def getBinNumber(violation):
    #4380 bins (24/2 * 365 days)
    date = violation['date'].split('/')[:2]

    hour = get24Hour(violation['time'])
    day = int(date[1])
    month = int(date[0])

    return (hour/2) * day * month

def getMonthFromBin(bin_number):
    return (bin_number / 365) + 1

#conver 12-H time to 24-H
def get24Hour(time):
    try:
        hour = int(time[:2])
        ampm = time[-1]

        if(ampm == 'P' and hour < 12):
            hour += 12
    except Exception:
        print time

    return hour


def getData():
    data = []
    i = 0
    with open('parking_violations.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None) # skip csv file column names
        for row in reader:
            violation = {}
            if(row[4] != '' and row[19] != '' and isInt(row[19][:4]) == True):
                violation['date'] = row[4]
                violation['time'] = row[19]
                data.append(violation)
                i += 1
            if i > 807518:
                break
    return data

def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

main()