#!/usr/bin/env python

import rospy
import almath
import numpy as np
import math
import time

import sys
import json

from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

pose_torso_world=[0,0,0,0,0,0,0]
pose_head_world=[0,0,0,0,0,0,0]
pose_arm_world=[0,0,0,0,0,0,0]
pose_wand_world=[0,0,0,0,0,0,0]
transform_torso_world=almath.Transform()
transform_head_world=almath.Transform()
transform_arm_world=almath.Transform()
transform_wand_world=almath.Transform()

################# DNN Helpers ############################
def sigmoid(x):
	return 1.0 / (1.0 + np.exp(-x))

def SiLU(x):
	return x*sigmoid(x)

def softmax(x):
	s = np.max(x, axis=1)
	s = s[:, np.newaxis]
	e_x = np.exp(x - s)
	div = np.sum(e_x, axis=1)
	div = div[:, np.newaxis] # dito
	return e_x / div
##########################################################

def torso_callback(msg):
	global pose_torso_world
	global transform_torso_world
	pose_torso_world[0]=msg.transform.translation.x
	pose_torso_world[1]=msg.transform.translation.y
	pose_torso_world[2]=msg.transform.translation.z
	pose_torso_world[3]=msg.transform.rotation.x
	pose_torso_world[4]=msg.transform.rotation.y
	pose_torso_world[5]=msg.transform.rotation.z
	pose_torso_world[6]=msg.transform.rotation.w
	rotation=almath.rotationFromQuaternion(pose_torso_world[6],pose_torso_world[3],pose_torso_world[4],pose_torso_world[5])
	transform_torso_world=almath.transformFromRotationPosition3D(rotation,pose_torso_world[0],pose_torso_world[1],pose_torso_world[2])
	#position6D=almath.position6DFromTransform(transform_torso_world)
	#print('Torso:',position6D)
	
def head_callback(msg):
	global pose_head_world
	global transform_head_world
	pose_head_world[0]=msg.transform.translation.x
	pose_head_world[1]=msg.transform.translation.y
	pose_head_world[2]=msg.transform.translation.z
	pose_head_world[3]=msg.transform.rotation.x
	pose_head_world[4]=msg.transform.rotation.y
	pose_head_world[5]=msg.transform.rotation.z
	pose_head_world[6]=msg.transform.rotation.w
	rotation=almath.rotationFromQuaternion(pose_head_world[6],pose_head_world[3],pose_head_world[4],pose_head_world[5])
	transform_head_world=almath.transformFromRotationPosition3D(rotation,pose_head_world[0],pose_head_world[1],pose_head_world[2])
	#position6D=almath.position6DFromTransform(transform_head_world)
	#print('Head:',position6D)
	
def arm_callback(msg):
	global pose_arm_world
	global transform_arm_world
	pose_arm_world[0]=msg.transform.translation.x
	pose_arm_world[1]=msg.transform.translation.y
	pose_arm_world[2]=msg.transform.translation.z
	pose_arm_world[3]=msg.transform.rotation.x
	pose_arm_world[4]=msg.transform.rotation.y
	pose_arm_world[5]=msg.transform.rotation.z
	pose_arm_world[6]=msg.transform.rotation.w
	rotation=almath.rotationFromQuaternion(pose_arm_world[6],pose_arm_world[3],pose_arm_world[4],pose_arm_world[5])
	transform_arm_world=almath.transformFromRotationPosition3D(rotation,pose_arm_world[0],pose_arm_world[1],pose_arm_world[2])
	#position6D=almath.position6DFromTransform(transform_arm_world)
	#print('Arm:',position6D)

def wand_callback(msg):
	global pose_wand_world
	global transform_wand_world
	pose_wand_world[0]=msg.transform.translation.x
	pose_wand_world[1]=msg.transform.translation.y
	pose_wand_world[2]=msg.transform.translation.z
	pose_wand_world[3]=msg.transform.rotation.x
	pose_wand_world[4]=msg.transform.rotation.y
	pose_wand_world[5]=msg.transform.rotation.z
	pose_wand_world[6]=msg.transform.rotation.w
	rotation=almath.rotationFromQuaternion(pose_wand_world[6],pose_wand_world[3],pose_wand_world[4],pose_wand_world[5])
	transform_wand_world=almath.transformFromRotationPosition3D(rotation,pose_wand_world[0],pose_wand_world[1],pose_wand_world[2])
	#position6D=almath.position6DFromTransform(transform_wand_world)
	#print('Wand:',position6D)

def input_limit(value,limit):
	if -limit<=value<=limit:
		return value
	elif value > 0:
		return limit
	else:
		return -limit
	
	
def read_pose_1():
	global transform_torso_world
	global transform_head_world
	rospy.init_node('hello_world',anonymous=False)
	
	pub=rospy.Publisher('cmd_vel',Twist,queue_size=10)
	
	rospy.Subscriber('vicon/Nao_Torso/Nao_Torso', TransformStamped, torso_callback)
	rospy.Subscriber('vicon/Nao_Head/Nao_Head', TransformStamped, head_callback)
	rate = rospy.Rate(100)
	#rospy.spin()
	#transform_head_torso=transform_head_world*transform_torso_world.inverse()
	#position6D=almath.position6DFromTransform(transform_head_torso)
	vel=Twist()
	while not rospy.is_shutdown():
		transform_head_torso=transform_head_world * transform_torso_world.inverse()
		position6D=almath.position6DFromTransform(transform_head_torso)
		vel.linear.x=-(position6D.wx)
		vel.linear.y=0
		vel.linear.z=0
		vel.angular.x=0
		vel.angular.y=0
		vel.angular.z=position6D.wz
		pub.publish(vel)
		print(position6D)
		rate.sleep()
		
def createArmPositionCommand(newPosition):
	msg = JointTrajectory()
	point = JointTrajectoryPoint()
	point.positions=newPosition
	point.velocities=[]
	point.accelerations=[]
	point.time_from_start=rospy.Duration(1.0)
	msg.points.append(point)
	jointName=['arm_joint_1','arm_joint_2','arm_joint_3','arm_joint_4','arm_joint_5']
	msg.joint_names=jointName
	msg.header.frame_id='arm_link_0'
	msg.header.stamp=rospy.Time.now()
	return msg
		
def read_pose_2():
	global transform_torso_world
	global transform_arm_world
	rospy.init_node('hello_world',anonymous=False)
	
	pub=rospy.Publisher('arm_1/arm_controller/command', JointTrajectory ,queue_size=10)
	
	rospy.Subscriber('vicon/Nao_Torso/Nao_Torso', TransformStamped, torso_callback)
	rospy.Subscriber('vicon/Nao_RUArm/Nao_RUArm', TransformStamped, arm_callback)
	rate = rospy.Rate(100)
	#rospy.spin()
	#transform_head_torso=transform_head_world*transform_torso_world.inverse()
	#position6D=almath.position6DFromTransform(transform_head_torso)
	while not rospy.is_shutdown():
		transform_arm_torso=transform_arm_world * transform_torso_world.inverse()
		position6D=almath.position6DFromTransform(transform_arm_torso)
		newpos=[0,0,-position6D.wx,0,0]
		trajectory=createArmPositionCommand(newpos)
		pub.publish(trajectory)
		print(position6D)
		rate.sleep()
		
def read_pose_3(model):
	global transform_wand_world
	rospy.init_node('hello_world',anonymous=False)
	
	pub=rospy.Publisher('cmd_vel',Twist,queue_size=10)
	
	rospy.Subscriber('vicon/Woody/Woody', TransformStamped, wand_callback)
	
	rate = rospy.Rate(100)
	#rospy.spin()
	#transform_head_torso=transform_head_world*transform_torso_world.inverse()
	#position6D=almath.position6DFromTransform(transform_head_torso)
	vel=Twist()
	dataset = []
	count = 0
	gap = 0
	last_det = 5
	last_cls = 5
	while not rospy.is_shutdown():
		position6D=almath.position6DFromTransform(transform_wand_world)
		vel.linear.x=-(input_limit(position6D.wx,1.0))*0.6
		vel.linear.y=-(input_limit(position6D.wy,1.0))*0.6
		vel.linear.z=0
		vel.angular.x=0
		vel.angular.y=0
		vel.angular.z=(input_limit(position6D.wz,1.0))*0.4
		data = [vel.angular.x, vel.angular.y, vel.angular.z, vel.angular.w, vel.linear.x, vel.linear.y, vel.linear.z]
		dataset = arrange_timeseries(dataset, data)
		if len(dataset) == 131:
			out = detect_gesture(model, dataset, count, gap, last_det, last_cls)
			if len(out) == 4:
				# last_det is the prediction, in which 0: BF, 1: FB, 2: CCW, 3: CW
				last_cls, last_det, count, gap = out
			else:
				last_cls, count, gap = out
		pub.publish(vel)
		print(position6D)
		rate.sleep()

def load_model(link_to_file):
	with open(link_to_file, "r") as f:
		model = json.load(f)

	for key in list(model.keys()):
		model[key]["w"] = np.array(model[key]["w"])
		model[key]["b"] = np.array(model[key]["b"])

	return model

def arrange_timeseries(dataset, data):
	if len(dataset) < 131:
		dataset.append(data)
	else:
		dataset.pop(0)
		dataset.append(data)

	return dataset

def detect_gesture(model, dataset, count, gap, last_det):
	dataset[:,4:] = dataset[:,4:] / 4000
	for l in range(3):
		if l < 2:
			x = SiLU(np.array(dataset).reshape(-1,1).dot(model["layer_"+str(l)]["w"].T)+model["layer_"+str(l)]["b"])
		else:
			x = softmax(np.array(dataset).reshape(-1,1).dot(model["layer_"+str(l)]["w"].T)+model["layer_"+str(l)]["b"])

	# Extract class
	cls = np.argmax(x)

	# Measure changes over a window of 5 time frames
	diff0 = np.abs(np.sum(np.array(dataset)[-1,0] - np.array(dataset)[-6:-1, 0].mean()))
	diff1 = np.abs(np.sum(np.array(dataset)[-1,1] - np.array(dataset)[-6:-1, 1].mean()))
	diff2 = np.abs(np.sum(np.array(dataset)[-1,2] - np.array(dataset)[-6:-1, 2].mean()))
	diff3 = np.abs(np.sum(np.array(dataset)[-1,3] - np.array(dataset)[-6:-1, 3].mean()))
	diff4 = np.abs(np.sum(np.array(dataset)[-1,4] - np.array(dataset)[-6:-1, 4].mean()))
	diff5 = np.abs(np.sum(np.array(dataset)[-1,5] - np.array(dataset)[-6:-1, 5].mean()))
	diff6 = np.abs(np.sum(np.array(dataset)[-1,6] - np.array(dataset)[-6:-1, 6].mean()))

	# Measure total change
	diff_all = np.sum((diff0,diff1,diff2,diff3,diff4,diff5,diff6))

	# Decide a gesture to belong to one class if it: matches the last detection, confidence score > 0.9 and has changes in range (1,4)
	if cls == last_cls and x.max() > 0.9 and (diff_all > 1 and diff_all < 4):
		count += 1
	else:
		count = 0

	# Gap between 2 detected gesture
	gap += 1

	# Condition to output the gesture
	if cls != last_det and gap > 131 and count >= 5:
		gap = 0
		count = 0
		last_det = cls
		last_cls = cls
		return last_cls, last_det, count, gap

	last_cls = cls

	return last_cls, count, gap

	
if __name__ == '__main__':
	try:
		model = load_model("../model.json")
		read_pose_3(model)
		
	except rospy.ROSInterruptException:
		pass

