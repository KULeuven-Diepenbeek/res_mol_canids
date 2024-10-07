import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import random

ifname = "hcrl/DoS_dataset.csv"
ifh = open(ifname, "r")

number_of_log_lines=0

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

    
    if random.random() >=0.75:
        judgement.append(0)
    else:
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

tn, fp, fn, tp = confusion_matrix(np_correct_judgement, np_judgement).ravel()
accuracy = (tn + tp) / (tn + tp + fn + fp)
precision = (tp) / (tp + fp)
recall = (tp) / (tp + fn)

print("Tp: %d, Tn: %d, Fp: %d, Fn: %d" % (tp, tn, fp, fn))
print("accuracy: %04f" % accuracy)
print("precision: %04f" % precision)
print("recall: %04f" % recall)

