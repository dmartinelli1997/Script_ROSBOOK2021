import rclpy
from rclpy.node import Node
import math 
from media_pipe_ros2_msg.msg import  MediaPipeHumanHandList                            
from geometry_msgs.msg import Twist

global handLeft, handRigth
handLeft = []
handRigth = []

class CmdSub(Node):
    global handLeft, handRigth
    def __init__(self):
        super().__init__('envia_comando')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            MediaPipeHumanHandList,
            '/mediapipe/human_hand_list',
            self.listener_callback,
            10)
        self.subscription 

    def listener_callback(self, msg):       
        global linear
        global angular
        handLeft = []
        handRigth = []
        cmd_vel = Twist() 
        if (msg.human_hand_list):
            if (msg.human_hand_list.left_hand_key_points):
                for i in range(0,len(msg.human_hand_list.left_hand_key_points)):
                    handLeft.append(msg.human_hand_list.left_hand_key_points[i])
            
            if (msg.human_hand_list.right_hand_key_points):
                for i in range(0,len(msg.human_hand_list.right_hand_key_points)):
                    handRigth.append(msg.human_hand_list.right_hand_key_points[i])
        
        if (len(handLeft)>0):
            if (handLeft[5]): 
                angle = CalcAngularDif([[handLeft[5].x, handLeft[5].y],[handLeft[8].x, handLeft[8].y]])
                if (angle>=90):
                    linear = (angle/90)*0.5
                elif(angle < 85 and angle != 0.0):
                    linear = (angle/90)*-1*1.5
                elif(angle == 0.0):
                    linear = 0.0
        else:
            linear = 0.0
            
        if (len(handRigth)>0):
            if (handRigth[5]): 
                angle = CalcAngularDif([[handRigth[5].x, handRigth[5].y],[handRigth[8].x, handRigth[8].y]])
                if (angle>=90):
                    angular = (angle/90)*0.5
                    
                elif(angle < 85 and angle != 0.0):
                    angular = (angle/90)*-1*1.5
                elif(angle == 0.0):
                    angular = 0.0
        else:
            angular = 0.0     
        
        print(angular)
        cmd_vel.linear.x = linear   
        cmd_vel.angular.z  = angular
        self.publisher_.publish(cmd_vel)

        
       
def CalcAngularDif(dados):
    difAngular = math.atan2(dados[1][0]-dados[0][0], dados[1][1]-dados[0][1])
    difAngular = abs(math.degrees(difAngular))  
    return (difAngular)


def main(args=None):
    rclpy.init(args=args)

    cmd_sub = CmdSub()   
    
    rclpy.spin(cmd_sub)

    cmd_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()