import matplotlib.pyplot as plt
import numpy as np

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


ifname = "hcrl/DoS_dataset.csv"
ifh = open(ifname, "r")

number_of_log_lines=0

id_data = {}
histogram_data_list = []

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
    
    if id in id_data: 
        id_data[id] = id_data[id] + 1
    else:
        id_data[id] = 1

    histogram_data_list.append(HD_total)

    # let's not go through all messages
    if number_of_log_lines==-1-1:
        break
    else:
        number_of_log_lines = number_of_log_lines + 1

    # prepare for next round
    prev_id = id
    prev_dlc = dlc
    prev_message = message.zfill(32)

ifh.close()

################################################################
# Convert dictionary to array
################################################################

# get the key-value pairs; convert to a list; convert to an array
result = id_data.items()
data = list(result)
xx = np.array(data)

number_of_ids = np.shape(xx)[0]

max_index = np.argmax(xx, axis=0)

################################################################
# Analyse the data
################################################################
print("################################################################")
print("# SUMMARY")
print("################################################################")
print("# Number of lines parsed: %d" % number_of_log_lines)
print("# Number of unique IDs: %d" % number_of_ids)
print("# Most frequently occuring ID: 0x%04x (=%d)(%d times)" % (xx[max_index[1]][0], xx[max_index[1]][0], xx[max_index[1]][1]))

histogram_data_arr = np.array(histogram_data_list)

# Plotting histogram
plt.figure(1)
 
# Adding labels and titles
plt.xlabel('HD')
plt.title('Histogram (DoS)')
 
# Display the plot
plt.hist(histogram_data_arr, bins = list(range(0, max(histogram_data_list), 5)))
plt.savefig('images/hcrl_dos_hd.png')
