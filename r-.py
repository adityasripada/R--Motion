import pypot.dynamixel
import time
import numpy as np
import xml.etree.cElementTree as ET

tree = ET.ElementTree(file='data2.xml')
tree2 = ET.ElementTree(file='DRIBLE.xml')



ports = pypot.dynamixel.get_available_ports()
if not ports:
    raise IOError('no port found!')

print('ports found', ports)
print('connecting on the first available port:', ports[0])
dxl_io = pypot.dynamixel.DxlIO(ports[0])
ids = dxl_io.scan(range(25))
print(ids)

if len(ids) < 18:
	print("Failed")
	exit()

raw_input("Proceed?")
'''torque = [100 for x in range(len(ids))]
dxl_io.enable_torque(ids)
dxl_io.set_max_torque(dict(zip(ids,torque)))'''
def parsexml(text,tree):
	find = "PageRoot/Page[@name='"+text+"']/steps/step"
	motions = []
	steps = [x for x in tree.findall(find)]
	for step in steps:
		motion = step.attrib['frame'] + " " + step.attrib['pose']
		motions.append(motion)
	
	return motions

def initwalk():
	#pose="-81.15 80.86 -68.26 67.97 -14.65 14.36 -45.12 45.12 -1.46 1.17 -50.1 49.8 -79.69 79.39 39.55 -39.84 -1.46 1.17"
	pose="-81.15 80.86 -68.26 67.97 -14.65 14.36 -45.12 45.12 -1.46 1.17 -50.1 49.8 -84.69 84.39 44.55 -44.84 -1.46 1.17"
	pose = [float(x) for x in pose.strip().split()]
	#dxl_io.set_moving_speed(dict(zip(ids,"45")))
	for i in range(1,19,2):
		dxl_io.set_goal_position({i:pose[i-1],i+1:pose[i]})
		time.sleep(0.001)

def syncmove(begpos,endpos,delay,speed=1):	
	begpos = begpos[1:]
	endpos = endpos[1:]

	frames = [np.linspace(x,y,delay) for x,y in zip(begpos,endpos)]
	print(len(frames))
	frames = zip(*frames)
	
	i = 0
	print len(frames)
	for frame in frames:
		print(i)
		i=i+1
		dxl_io.set_goal_position(dict(zip(ids,frame)))
		time.sleep(0.008/speed)
		
def offset(motion):
	motion = [float(x) for x in motion.strip().split()]
	motion[11] += -9
	motion[12] += 9
	motion[13] += -9
	motion[14] += 9
	motion = [str(x) for x in motion]
	motion = ' '.join(motion)
	return motion

def offset2(motion):
	motion = [float(x) for x in motion.strip().split()]
	motion[1] += 7
	motion[2] += -7
	motion = [str(x) for x in motion]
	motion = ' '.join(motion)
	return motion

def syncset(motions,speed):
	frame = 0
	prev = [0, -81.15, 80.86, -68.26, 67.97, -14.65, 14.36, -45.12, 45.12, -1.46, 1.17, -50.1, 49.8, -79.69, 79.39, 39.55, -39.84, -1.46, 1.17]
	for motion in motions:
		motion = [float(x) for x in motion.strip().split()]
		delay = motion[0] - frame
		frame = motion[0]
		syncmove(prev,motion,delay,speed)
		prev = motion
	
		

def deredy():
	motions = parsexml("43 D_Ready      ",tree2)
	syncset(motions,1)

def deright():
	motions = parsexml("44 D_Right      ",tree2)
	syncset(motions,0.3)

def balance():
	motions = parsexml("2 Balance",tree2)
	syncset(motions,1)

def rturn():
	motions = parsexml("27 RT",tree2)
	syncset(motions,1)
def lturn():
	motions = parsexml("28 LT",tree2)
	syncset(motions,1)



	
def w1():
	motions = parsexml("32 F_S_L",tree)
	motions =[offset(m) for m in motions]
	syncset(motions,2.5)
def w2():
	motions = parsexml("33 ",tree)
	motions =[offset(m) for m in motions]
	syncset(motions,2.5)
	
def w3():
	motions = parsexml("38 F_M_R",tree)
	motions =[offset(m) for m in motions]
	syncset(motions,3)

def w4():
	motions = parsexml("39 ",tree)
	motions =[offset(m) for m in motions]
	syncset(motions,3)

def w5():
	motions = parsexml("36 F_M_L",tree)
	motions =[offset(m) for m in motions]
	syncset(motions,3)

def w6():
	motions = parsexml("37 ",tree)
	motions =[offset(m) for m in motions]
	syncset(motions,3)
	
def bgetup():
	motions = parsexml("28 B getup  ",tree)
	syncset(motions,1.5)
	


def fgetup():
	motions = parsexml("27 F getup",tree)
	motions = [offset(m) for m in motions]
	motions[1] = offset2(motions[1])
	motions[2] = offset2(motions[2])
	syncset(motions,2.7)

def rkick():
	motions = parsexml("19 R kick",tree)
	syncset(motions,1.2)



def lkick():
	motions = parsexml("18 L kick",tree)
	syncset(motions,1.7)

def lstep():
        motions = parsexml("40 F_E_L",tree)
	syncset(motions,2.1)
        motions = parsexml("41 ",tree)
	syncset(motions,2.1)

def rstep():
        motions = parsexml("42 F_E_R",tree)
	syncset(motions,2.1)
        motions = parsexml("43 ",tree)
	syncset(motions,2.1)


def walk(iter):
	w1()
	w2()
	while iter>0:
		w3()
		w4()
		w5()
		w6()
		iter = iter -1


initwalk()
time.sleep(2)


'''
while True:
	initwalk()
	time.sleep(0.65)
	walk(2)

step = 1 
while True:
        if step ==1:
            lstep()
        else:
            rstep()
        step *= -1
	time.sleep(0.1)
        initwalk()    

'''




		
		

