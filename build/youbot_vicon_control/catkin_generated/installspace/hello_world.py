#!/usr/bin/env python2

import rospy
import almath
import numpy as np
import math
import time

import sys

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
		
def read_pose_3():
	global transform_wand_world
	rospy.init_node('hello_world',anonymous=False)
	
	pub=rospy.Publisher('cmd_vel',Twist,queue_size=10)
	
	rospy.Subscriber('vicon/Woody/Woody', TransformStamped, wand_callback)
	
	rate = rospy.Rate(100)
	#rospy.spin()
	#transform_head_torso=transform_head_world*transform_torso_world.inverse()
	#position6D=almath.position6DFromTransform(transform_head_torso)
	vel=Twist()
	while not rospy.is_shutdown():
		position6D=almath.position6DFromTransform(transform_wand_world)
		vel.linear.x=-(input_limit(position6D.wx,1.0))*0.6
		vel.linear.y=-(input_limit(position6D.wy,1.0))*0.6
		vel.linear.z=0
		vel.angular.x=0
		vel.angular.y=0
		vel.angular.z=(input_limit(position6D.wz,1.0))*0.4
		pub.publish(vel)
		print(position6D)
		rate.sleep()
	
if __name__ == '__main__':
	try:
		read_pose_3()
		
	except rospy.ROSInterruptException:
		pass

