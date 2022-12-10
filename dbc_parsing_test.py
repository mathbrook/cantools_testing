import cantools
import csv
import pandas as pd
from datetime import datetime
db = cantools.database.load_file('20200701_RMS_PM_CAN_DB.dbc')
dbc_ids = []
for message in db.messages:
    #print(str(vars(message)) + "\n")
    dbc_ids.append(message.frame_id)
    print(str(message.name)+" "+str(message.frame_id)+" "+str(message.comment))
    print("\tsignals: ")
    for signal in message.signals:
        print("\t\t"+ signal.name)

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

def parse_message(id, data):
    labels=[]
    values=[]
    units=[]
    print("Raw ID: "+str(raw_id)+ " Raw DATA: "+str(raw_data))
    for i in dbc_ids:
        if int(id,16)==i:
            actual_message = db.get_message_by_frame_id(int(id,16))
            for signal in actual_message.signals:
                units.append(str(signal.unit))
            parsed_message = db.decode_message(int(id,16),bytes(data,'utf-8'))
            parsed_data = actual_message.decode(bytes(data,'utf-8'))
            print(parsed_data)
            print("The parsed message: "+ str(parsed_message))
            for i in parsed_message:
                # print(str(i)+" "+str(parsed_message[i]))
                message_label = str(i)
                # print("Label: " +message_label)
                labels.append(message_label)
                values.append(str(parsed_message[i]))
            message_name = actual_message.name
            #return(parsed_message)
            # print("Name "+ message_name)
            # print("Labels " + str(labels))
            # print(values)
            # print(units)
            return [message_name,labels,values,units]
    return "INVALID_ID"
    
raw_id = "C0"
raw_data = "0000000001000000"
print(parse_message(raw_id,raw_data))
print("Parsing it straight up with the decode function: ")
print(bytes(raw_data,'utf-8'))
print(db.decode_message(int(raw_id,16),b(bytes(raw_data,'utf-8'))))

# infile = open('data0002.csv',"r")
# outfile = open('data0002test.csv',"w")
# flag_first_line = True
# for line in infile.readlines():
#     # On the first line, do not try to parse. Instead, set up the CSV headers.
#     if flag_first_line:
#         flag_first_line = False
#         outfile.write("time,id,message,label,value,unit\n")

#     # Otherwise attempt to parse the line.
#     else:
#         raw_time = line.split(",")[0]
#         raw_id = line.split(",")[1]
#         length = line.split(",")[2]
#         raw_message = line.split(",")[3]
#         # Do not parse if the length of the message is 0, otherwise bugs will occur later.
#         if length == 0 or raw_message == "\n":
#             continue
        
#         # Call helper functions
#         time = parse_time(raw_time)
#         raw_message = raw_message[:(int(length) * 2)] # Strip trailing end of line/file characters that may cause bad parsing
#         raw_message = raw_message.zfill(16) # Sometimes messages come truncated if 0s on the left. Append 0s so field-width is 16.
#         table = parse_message(raw_id, raw_message)
#         if table == "INVALID_ID" or table == "UNPARSEABLE":
#             continue

#         # Assertions that check for parser failure. Notifies user on where parser broke.
#         assert len(table) == 4, "FATAL ERROR: Parser expected 4 arguments from parse_message at ID: 0x" + table[0] + ", got: " + str(len(table))
#         assert len(table[1]) == len (table[2]) and len(table[1]) == len(table[3]), "FATAL ERROR: Label, Data, or Unit numbers mismatch for ID: 0x" + raw_id
        
#         # Harvest parsed datafields and write to outfile.
#         message = table[0].strip()
#         for i in range(len(table[1])):
#             label = table[1][i].strip()
#             value = str(table[2][i]).strip()
#             unit = table[3][i].strip()

#             outfile.write(time + ",0x" + raw_id + "," + message + "," + label + "," + value + "," + unit + "\n")

# infile.close()
# outfile.close()
