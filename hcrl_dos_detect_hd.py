import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def HD(x, y):
    count = 0
    exor = bin(x^y)[2:]
    for x in exor:
        if x == '1':
            count = count + 1
    return count

def HD_str(x,y):
    if len(x) != len(y):
        print("ERROR")
    
    count = 0
    
    for i in range(len(x)):
        x_int = int(x[i],16)
        y_int = int(y[i],16)

        exor = bin(x_int^y_int)[2:]
        for z in exor:
            if z == '1':
                count = count + 1
    return count

HDthreshold = 15
HDthreshold = 5
HDthreshold = 10

ifname = "hcrl/DoS_dataset.csv"
ifh = open(ifname, "r")

number_of_log_lines=0

id_data = {}
histogram_data_list = []
malicious = 0
benign = 0

judgement = []
correct_judgement = []

################################################################
# Load the data
################################################################

# loop over lines
for line in ifh:

    line = line.rstrip()

    # parse fields
    fields = line.split(",")
    # if len(fields) < 12:
    #     print("ERROR: incomplete log line (%s)" % line)
    timestamp = fields[0]
    id = fields[1]
    dlc = int(fields[2])
    message = "".join(fields[3:-1])

    # do sanity check on parsed fields
    if len(id) != 4:
        print("strange ID length")
        break
    id = int(id, 16)

    if dlc not in (2, 5, 8):
        print("strange dlc (%d)" % dlc)
        break

    # do initial preparation
    if number_of_log_lines == 0:
        prev_id = id
        prev_dlc = dlc
        prev_message = message.zfill(32)

    # calculate the HDs
    HD_id = HD(prev_id, id)
    HD_dlc = HD(prev_dlc, dlc)
    HD_message = HD_str(prev_message, message.zfill(32))
    HD_total = HD_id + HD_dlc + HD_message
    

    if HD_total < HDthreshold:
        malicious = malicious + 1
        judgement.append(0)
    else:
        benign = benign + 1
        judgement.append(1)
    
    if fields[-1] == "R":
        correct_judgement.append(1)
    else:
        correct_judgement.append(0)

    # let's not go through all messages
    if number_of_log_lines==0-1:
        break
    else:
        number_of_log_lines = number_of_log_lines + 1

    # prepare for next round
    prev_id = id
    prev_dlc = dlc
    prev_message = message.zfill(32)

ifh.close()

################################################################
# Postproc
################################################################

np_judgement = np.array(judgement)
np_correct_judgement = np.array(correct_judgement)

# print("num of lines: %d - %d" % (np_judgement.size, np_correct_judgement.size))
# print("num of lines: %d - %d - %d" % (benign, np.count_nonzero(np_judgement), np.count_nonzero(np_correct_judgement)))
# print("num of malicious: %d" % malicious)
# print("num of benign: %d" % benign)

print(judgement[0:20])
print(correct_judgement[0:20])

tn, fp, fn, tp = confusion_matrix(np_correct_judgement, np_judgement).ravel()
accuracy = (tn + tp) / (tn + tp + fn + fp)
precision = (tp) / (tp + fp)
recall = (tp) / (tp + fn)

print("Tp: %d, Tn: %d, Fp: %d, Fn: %d" % (tp, tn, fp, fn))
print("accuracy: %04f" % accuracy)
print("precision: %04f" % precision)
print("recall: %04f" % recall)



cm = confusion_matrix(np_correct_judgement, np_judgement)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.array(("benign", "malicious")))
disp.plot()
plt.savefig('images/hcrl_dos_cm_hd'+str(HDthreshold)+'.png')