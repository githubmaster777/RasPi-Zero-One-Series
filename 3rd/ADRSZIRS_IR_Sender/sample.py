#!/usr/bin/env python3
# coding: utf-8
#####!�Ŏn�܂�1�s�ڂ̋L�q��Shebang�X�N���v�g���̂����s
#####2�s�ڂɁA�}�W�b�N�R�����g���L�q�����G���R�[�f�B���O
#
# �t�@�C�����F3_2adrszIRS-sample.py  python3�p
# �o�[�W�����F2018/7/27 v1.0
#
# �r�b�g�E�g���[�h�E�����В񋟂� �ԊO�������R�����(�^�ԁFADRSZIRS)�p�̃c�[��
# �@���쌠��:(C) 2015 �r�b�g�E�g���[�h�E������
# �@���C�Z���X: ADL(Assembly Desk License)
#  ���s���@�F�Ǎ��@./3_2adrszIRS-sample.py r
# �@�@�@�@�@�@�����@./3_2adrszIRS-sample.py w�@5B0018002E001800
# �@******�g�����F�R�}���h���C���@�c�[��
# �w�K�����R�������Y�p�C�@�Ǎ��R�}���h�ir:)�F�A �����F�f�[�^
#
# �w�K�����R�������Y�p�C�@�����R�}���h�iw:)�F�A�f�[�^
#
# sample-data�F�\�j�[	�f�W�^���e���r�P	�d��
# 5B0018002E001800180018002E001800170018002E00190017001800170018002E00180018001800170018001700180017004F03

#
# �@******�h�Q�b�֌W�����R�}���h
# cmd R1_log_start     0x15 bus-write(ADR,cmd,n)
# cmd R2_log_stop      0x25 bus-write(ADR,cmd,n)
# cmd R3_data_num_read 0x35 bus-read(ADR,cmd,n)
# cmd R4_data_read     0x45 bus-read(ADR,cmd,n)
# cmd W1_data_num_write 0x19 bus-write(ADR,cmd,n)
# cmd W2_data_write    0x29 bus-read(ADR,cmd,n)
# cmd W3_trans_req    0x39 bus-read(ADR,cmd,n)
#
#

#Add import
from datetime import datetime, timedelta
import sched

from __future__ import print_function
import smbus
import time
from time import sleep

# import commands
import subprocess
import os
import sys
import codecs

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This must match in the Arduino Sketch
# SLAVE_ADDRESS = 0x04 0x5a
# SLAVE_ADDRESS = 0x52

SLAVE_ADDRESS = 0x5A
data_numH = 0x31
data_numL = 0x32
data_numHL = [0x00, 0x31, 0x32]
data_num = 10
memo_no = 0
block = []

# command
R1_log_start = 0x15  # bus-write(ADR,cmd,n)
R2_log_stop = 0x25  # bus-write(ADR,cmd,n)
R3_data_num_read = 0x35  # bus-read(ADR,cmd,n)
R4_data_read = 0x45  # bus-read(ADR,cmd,n)
W1_data_num_write = 0x19  # bus-write(ADR,cmd,n)
W2_data_write = 0x29  # bus-read(ADR,cmd,n)
W3_trans_req = 0x39  # bus-read(ADR,cmd,n)


############# read command
def read_command():
    # print('start_read_command')

    # bus.write_i2c_block_data(SLAVE_ADDRESS, R1_log_start , 1 )   #= 0x15  #bus-write(ADR,cmd,1)
    # bus.write_i2c_block_data(SLAVE_ADDRESS, R1_log_start , 1 )   #= 0x15  #bus-write(ADR,cmd,1)
    # long write_byte(int addr,char val)
    # long write_byte(SLAVE_ADDRESS, R1_log_start)SyntaxError: invalid syntax
    # bus.write_i2c_data(SLAVE_ADDRESS, R1_log_start )   #= 0x15  #bus-write(ADR,cmd,1)
    # bus.write_byte(SLAVE_ADDRESS, R1_log_start )   #= 0x15  #bus-write(ADR,cmd,1)OSError: [Errno 121] Remote I/O error
    bus.write_byte(
        SLAVE_ADDRESS, 0x15
    )  # = 0x15  #bus-write(ADR,cmd,1)OSError: [Errno 121] Remote I/O error

    sleep(5.0)

    # bus.write_i2c_block_data(SLAVE_ADDRESS, R2_log_stop,1  )   #= 0x15  #bus-write(ADR,cmd,1)
    bus.write_byte(SLAVE_ADDRESS, R2_log_stop)  # = 0x15  #bus-write(ADR,cmd,1)

    # sleep(1.0)

    # cmd R2_data_num_read 0x25 bus-read(ADR,cmd,3)
    data_numHL = bus.read_i2c_block_data(
        SLAVE_ADDRESS, R3_data_num_read, 3
    )  # = 0x25 #bus-read(ADR,cmd,3)
    data_num = data_numHL[1]
    data_num *= 256
    data_num += data_numHL[2]
    print("data_num =", data_num)
    if data_num < 65535:

        # print("data_num =",data_num )

        # cmd R3_data_read           0x35 bus-read(ADR,cmd,n)
        block = []
        block_dat = bus.read_i2c_block_data(
            SLAVE_ADDRESS, R4_data_read, 1
        )  # = 0x35 #bus-read(ADR,cmd,n)
        for i in range(data_num):
            block_dat = bus.read_i2c_block_data(
                SLAVE_ADDRESS, R4_data_read, 4
            )  # = 0x35 #bus-read(ADR,cmd,n)
            block.append(block_dat[0])
            block.append(block_dat[1])
            block.append(block_dat[2])
            block.append(block_dat[3])
    # print(block)  #for denug
    else:
        print("data_num error=", data_num)

    return block


################# write command
def write_command(block2):
    # f = open(filename,'r')
    # block2 =f.read()
    # f.close()
    # print(block2)
    # print(len(block2))
    # print('start_write_command')
    str_tmp = ""
    int_tmp = []
    # for i in range(len(block2)/2): #TypeError: 'float' object cannot be interpreted as an integer
    for i in range(int(len(block2) / 2)):

        str_tmp = block2[i * 2] + block2[i * 2 + 1]
        int_tmp.append(int(str_tmp, 16))
    print(int_tmp)
    print(len(int_tmp))
    # cmd W1_memo_no_write 0x19 bus-write(ADR,cmd,1)
    #    bus.write_i2c_block_data(SLAVE_ADDRESS, W1_memo_no_write ,memo_no )   #=
    # cmd W2_data_num_write 0x29 bus-write(ADR,cmd,3)
    data_num = int(len(int_tmp) / 4)  # for test
    data_numHL = [0x31, 0x32]  # for test
    data_numHL[0] = int(data_num / 256)
    data_numHL[1] = int(data_num % 256)
    print(data_numHL, data_numHL[0], data_numHL[1])
    bus.write_i2c_block_data(SLAVE_ADDRESS, W1_data_num_write, data_numHL)  # =
    # TypeError: Third argument must be a list of at least one, but not more than 32 integers
    # cmd W3_data_write           0x39 bus-read(ADR,cmd,n)
    print(data_num)
    data_numHL = [0x31, 0x32, 0x33, 0x34]  # for test
    for i in range(data_num):
        data_numHL[0] = int_tmp[i * 4 + 0]
        data_numHL[1] = int_tmp[i * 4 + 1]
        data_numHL[2] = int_tmp[i * 4 + 2]
        data_numHL[3] = int_tmp[i * 4 + 3]
        bus.write_i2c_block_data(SLAVE_ADDRESS, W2_data_write, data_numHL)  # =
    # cmd W4_flash_write           0x49 bus-read(ADR,cmd,n)
    bus.write_byte(SLAVE_ADDRESS, W3_trans_req)  # =


###########################   main
# dir_name = '/home/pi/zeroone/3_2adrszIRS/'
# os.chdir(dir_name)

# while True:
argvc = sys.argv
argc = len(argvc)
# print(str(argc))#

# -------------------
if argc >= 2:
    command = argvc[1]
    memo_no = [0x0]
    print(command)
    if command == "w":
	block2 = argvc[2]
	if argc >=4:
		now = datetime.now()
		now = datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
		comp = datetime(now.year, int(argvc[3]), int(argvc[4]), int(argvc[5]), int(argvc[6]))
		diff = comp - now
		if int(diff.days) >= 0:
			print("Waiting ...")
			print("month=",argvc[3],"day=",argvc[4],"hour=",argvc[5],"minute=",argvc[6])
			scheduler = sched.scheduler(time.time, time.sleep)
			scheduler.enter(diff.seconds, 1, write_command, (block2, ))
			scheduler.run()
		else:
			print("Invalid values...")
			print("sample.py 1:w 2:data 3:month 4:day 5:hour 6:minute")
	else:
		print("default mode ...")
		write_command(block2)

    elif command == "r":
        res_data = read_command()
        for i in range(len(res_data)):
            print("{:02X}".format(res_data[i]), end="")
            # 141
            # print('')
            # break
    # if (argc == 2):
    # if (command == 'w'):
    #   block2 = argvc[2]
    # print(block2)
    #  print('start_write_command')
    # write_command(block2)
    # break
    else:
        print("invalid command!!!!!")
elif argc == 1:
    print("usage:./3_2adrszIRS-sample.py r")
    print("usage:./3_2adrszIRS-sample.py w 5B0018002E001800")
    # break

# break
