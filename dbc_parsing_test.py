import cantools
import csv
import pandas as pd
from datetime import datetime
import glob
import os
import sys
def get_dbc_files():
    try:
        path_name = './'
        file_path = []
        file_count = 0
        for root, dirs, files in os.walk(path_name, topdown=False):
            for name in files:
                if ".dbc" in name or ".DBC" in name:
                    fp = os.path.join(root, name)
                    file_path.append(fp)
                    file_count += 1
    except:
        print('FATAL ERROR: Process failed at step 1.')
        sys.exit(0)
    mega_dbc=cantools.database.Database()
    for filename in file_path:
        with open (filename, 'r') as newdbc:
            mega_dbc.add_dbc(newdbc)

    print('Step 1: found ' + str(file_count) + ' files in the DBC files folder')
    return mega_dbc
#print(get_dbc_files())
get_dbc_files()
#db = cantools.database.load_file('20200701_RMS_PM_CAN_DB.dbc')

def print_all_the_shit_in_dbc_file(db):
    dbc_ids=[]
    for message in db.messages:
        #print(str(vars(message)) + "\n")
        dbc_ids.append(message.frame_id)
#        print(str(message.name)+" ID: "+str(message.frame_id)+" Note: "+str(message.comment))
#        print("\tsignals: ")
        for signal in message.signals:
#            print("\t\t"+ signal.name)
            header_list.append(signal.name)
    return dbc_ids
def parse_time(raw_time):
    '''
    @brief: Converts raw time into human-readable time.
    @input: The raw time given by the raw data CSV.
    @return: A string representing the human-readable time.
    '''
    ms = int(raw_time) % 1000
    raw_time = int(raw_time) / 1000
    time = str(datetime.utcfromtimestamp(raw_time).strftime('%Y-%m-%dT%H:%M:%S'))
    time = time + "." + str(ms).zfill(3) + "Z"
    return time

def parse_message_better(id, data, db,dbc_ids):
    if int(id,16) in dbc_ids:
        parsed_message = db.decode_message(int(id,16),bytearray.fromhex(data))
        return parsed_message
    if (id not in unknown_ids) & (int(id,16) not in dbc_ids):
        unknown_ids.append(raw_id)
    return "INVALID_ID"

def parse_message(id, data, db,dbc_ids):
    labels=[]
    values=[]
    units=[]
    if int(id,16) in dbc_ids:
        actual_message = db.get_message_by_frame_id(int(id,16))
        for signal in actual_message.signals:
            units.append(str(signal.unit))
        parsed_message = db.decode_message(int(id,16),bytearray.fromhex(data))
        for i in parsed_message:
            message_label = str(i)
            labels.append(message_label)
            values.append(str(parsed_message[i]))
        message_name = actual_message.name
        return [message_name,labels,values,units]
    if (id not in unknown_ids) & (int(id,16) not in dbc_ids):
        unknown_ids.append(raw_id)
    return "INVALID_ID"
header_list = ["Time"]
unknown_ids = []
dbc_for_parsing = get_dbc_files()
dbc_ids = print_all_the_shit_in_dbc_file(dbc_for_parsing)
nextline = [""] * len(header_list)
header_string=",".join(header_list)
infile = open('data0051.csv',"r")
header_list = ["Time"]

outfile2 = open('test_new_parsing_scheme_data5.csv','w')
flag_first_line = True
flag_second_line = True
print("Beginning parsing")
last_time = ''
for line in infile.readlines():
    if flag_first_line:
        flag_first_line = False
    else:
        raw_time = line.split(",")[0]
        raw_id = line.split(",")[1]
        length = line.split(",")[2]
        raw_message = line.split(",")[3]
        if length == 0 or raw_message == "\n":
            continue
        raw_message = raw_message[:(int(length) * 2)] # Strip trailing end of line/file characters that may cause bad parsing
        raw_message = raw_message.zfill(16) # Sometimes messages come truncated if 0s on the left. Append 0s so field-width is 16.
        current_message = parse_message_better(raw_id,raw_message,dbc_for_parsing,dbc_ids)
        if current_message != "INVALID_ID":
            for i in current_message:
                if i not in header_list:
                    header_list.append(i)
nextline = [""] * len(header_list)
print(nextline)
flag_first_line = True

# infile = open('data0051.csv',"r")
# for linee in infile.readlines():
#     # On the first line, do not try to parse. Instead, set up the CSV headers.
#     if flag_first_line:
#         flag_first_line = False
#         header_string=",".join(header_list)
#         outfile2.write(header_string+"\n")

#     # Otherwise attempt to parse the line.
#     else:
        
#         raw_time = linee.split(",")[0]
#         raw_id = linee.split(",")[1]
#         length = linee.split(",")[2]
#         raw_message = linee.split(",")[3]
        
#         # Do not parse if the length of the message is 0, otherwise bugs will occur later.
#         if length == 0 or raw_message == "\n":
#             continue
        
#         # Call helper functions
#         time = parse_time(raw_time)
#         raw_message = raw_message[:(int(length) * 2)] # Strip trailing end of line/file characters that may cause bad parsing
#         raw_message = raw_message.zfill(16) # Sometimes messages come truncated if 0s on the left. Append 0s so field-width is 16.
#         current_message = parse_message_better(raw_id,raw_message,dbc_for_parsing,dbc_ids)
#         if current_message != "INVALID_ID":
#             for i in current_message:
#                 nextline[header_list.index(str(i))]=str(current_message[i])
#         if time == last_time:
#             continue
#         elif flag_second_line==True:
#             flag_second_line = False
#             print("Second Line")
#             continue
#         elif time != last_time:
#             # write our line to file
#             # clear it out and begin putting new values in it
#             print(nextline)
#             last_time = time
#             nextline[header_list.index("Time")]=raw_time
#             outfile2.write(",".join(nextline) + "\n")
#             nextline = [""] * len(header_list)

# infile.close()
# outfile2.close()
# print("parsing done")

print("These IDs not found in DBC: " +str(unknown_ids))
print(header_list)
