"""This is a docstring
Module that includes some defined functions to parse the log file
"""
import pandas as pd

#create a dataframe to store the only seconds
df = pd.DataFrame(columns=['recv_time_in_seconds', 'pre_send_time_in_seconds', 'send_time_in_seconds'])

with open('1.txt', encoding= 'utf-8') as f:
        linecount = 0
        for line in f:
            linecount = linecount + 1
            if "syscom rcvd time sec:" in line:
                recv_time_in_seconds = int(line.split(' ')[4:][0])
                recv_time_in_nano_seconds = int(line.split(' ')[6:][0] )
            if "for msgId" in line:
                pre_send_time_in_seconds= int(line.split(' ')[18:][0])
                pre_send_time_in_nano_seconds = int(line.split(' ')[20:][0].replace(':',''))
            if "syscom send time sec:" in line:
                send_time_in_seconds = int(line.split(' ')[4:][0])
                send_time_in_nano_seconds = int(line.split(' ')[6:][0])
            if((linecount % 3) == 0):
                #seconds and nano seconds into single column by dot seperation
                recv_time_in_seconds = float(str(recv_time_in_seconds) + '.' + str(recv_time_in_nano_seconds))
                pre_send_time_in_seconds = float(str(pre_send_time_in_seconds) + '.' + str(pre_send_time_in_nano_seconds))
                send_time_in_seconds = float(str(send_time_in_seconds) + '.' + str(send_time_in_nano_seconds))

                #append the values to the dataframe
                df = df.append({'recv_time_in_seconds': recv_time_in_seconds, 'pre_send_time_in_seconds': pre_send_time_in_seconds, 'send_time_in_seconds': send_time_in_seconds}, ignore_index=True)

print(df)
