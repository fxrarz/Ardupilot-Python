#! /usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State, Waypoint
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest, CommandTOL, CommandTOLRequest, WaypointPush, WaypointPushRequest
import time

current_state = State()

def state_cb(msg):
    global current_state
    current_state = msg


if __name__ == "__main__":
	rospy.init_node("offb_node_py")
	
	state_sub = rospy.Subscriber("mavros/state", State, callback = state_cb)

	local_pos_pub = rospy.Publisher("mavros/setpoint_position/local", PoseStamped, queue_size=10)
	
	rospy.wait_for_service("/mavros/set_mode")
	set_mode_client = rospy.ServiceProxy("mavros/set_mode", SetMode)
	
	rospy.wait_for_service("/mavros/cmd/arming")
	arming_client = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)

	rospy.wait_for_service("/mavros/cmd/takeoff")
	takeoff_client = rospy.ServiceProxy("mavros/cmd/takeoff", CommandTOL)
	
	rospy.wait_for_service("/mavros/mission/push")
	wp_client = rospy.ServiceProxy("mavros/mission/push", WaypointPush)



    # Setpoint publishing MUST be faster than 2Hz
	rate = rospy.Rate(20)

    # Wait for Flight Controller connection
	while(not rospy.is_shutdown() and not current_state.connected):
		rate.sleep()



	# Set mode GUIDED        
	message = SetModeRequest()
	message.custom_mode = 'GUIDED'
    
	resp = set_mode_client.call(message)
	print("Guided status:", resp)
	
	assert resp.mode_sent == True, "Guided mode failed"
	
	time.sleep(3)
	
	
	
	# Set ARM THROTTLE
	message = CommandBoolRequest()
	message.value = True
	
	resp = arming_client.call(message)
	print("Armed status:",resp)
	
	assert resp.success == True, "Guided mode failed"
	
	time.sleep(3)
	
	
	
	# Set to TAKEOFF
	message = CommandTOLRequest()
	message.min_pitch = 0.0
	message.yaw = 0.0  
	message.latitude = 0.0  
	message.longitude = 0.0  
	message.altitude = 5.0
	
	resp = takeoff_client.call(message)
	print("Armed status:",resp)
	
	assert resp.success == True, "Takeoff failed"
	
	time.sleep(3)
	
	
	
	# Set waypoint        
	message = WaypointPushRequest()
	message.start_index = 0
	message.waypoints = [
		Waypoint(frame = 3, command = 16, is_current = 0, autocontinue = True, param1 = 5, x_lat = 38.99044, y_long = -76.93776, z_alt = 0),
		Waypoint(frame = 3, command = 16, is_current = 0, autocontinue = True, param1 = 5, x_lat = 40.99066, y_long = -75.93738, z_alt = 0)
		]
	
    
	resp = wp_client.call(message)
	print("Waypoint set:", resp)
	
	assert resp.wp_transfered >= 1, "Waypoint set failed"	
	
	time.sleep(3)
	
	
	
	# Set mode AUTO        
	message = SetModeRequest()
	message.custom_mode = 'AUTO'
    
	resp = set_mode_client.call(message)
	print("Auto status:", resp)
	
	assert resp.mode_sent == True, "Auto mode failed"
	
	time.sleep(10)
	
	
	# Set mode RTL        
	message = SetModeRequest()
	message.custom_mode = 'RTL'
    
	resp = set_mode_client.call(message)
	print("Land status:", resp)
	
	assert resp.mode_sent == True, "Land mode failed"
		
	
	
