import os
import random
import subprocess
import shutil

samples = 2100
cmd = '-bgcolor 0 -bgthresh 0 -maxxangle 0.1 -maxyangle 0.1 maxzangle 1.1 -maxidev 40 -w 640 -h 480 -info'

pos = "./positives.txt"
neg = "./negatives.txt"
out = "./out2.idl"

f_pos = open(pos, 'r+')
f_neg = open(neg, 'r+')
f_out = open(out, 'w')

pos_lines = f_pos.readlines()
neg_lines = f_neg.readlines()

os.chdir('./Sample/')
target_path = '../Sample2/'
try:
	shutil.rmtree(target_path)
except:
	pass
os.makedirs(target_path)
print os.getcwd()

# multiplier =int(samples/pos_lines)

for pos_no,line in enumerate(pos_lines):
	pos_sample = line.strip()
	# for i in range(multiplier):
	rnd_neg = random.randrange(0, len(neg_lines)-101, 1)
	neg_sample = neg_lines[rnd_neg:rnd_neg+100]
	f_samp = open('../tmp.txt', 'w+')
	f_samp.writelines(neg_sample)
	f_samp.close()
	command = 'opencv_createsamples -img .' + pos_sample + ' -bg ../tmp.txt -info annotations.lst -bgcolor 0 -bgthresh 0 -maxxangle 0.1 -maxyangle 0.1 -maxzangle 1.1 -maxdev 10 -w 150 -h 200'
	p = os.system(command)

	for file in os.listdir("."):
		if file.endswith(".jpg"):
			shutil.move(file, target_path+str(pos_no)+"_"+file)

	f_anno = open('annotations.lst', 'r+')
	for line in f_anno.readlines():
		list_line = line.strip().split(' ')
		write_line = '"./Sample2/'+str(pos_no)+"_"+list_line[0] + '": ('+ list_line[2] +','+ list_line[3] +','+ str(int(list_line[2])+int(list_line[4])) + ','+ str(int(list_line[3])+ int(list_line[5]))
		f_out.write(write_line)
		f_out.write(');\n')
	f_anno.close()
