import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Joy
import time
import pygame
from pygame.locals import *

class PublisherNode(Node):
    def __init__(self):
        super().__init__("publisher")
      
        self.msg = Int32MultiArray()
       
        self.pub = self.create_publisher(Int32MultiArray, "verocity", 0)
    
        self.tmr = self.create_timer(0.1, self.callback)


    def onTick(self):
        pygame.init()
        pygame.joystick.init()
        joy = pygame.joystick.Joystick(0)
        joy.init()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.locals.JOYBUTTONDOWN:
#                    print ('L: 0, R: 0  ---> Breaking!')
                    r_y, l_y = int(0), int(0)
                    return r_y, l_y
                elif e.type == pygame.locals.JOYAXISMOTION:
                    r_y = int(joy.get_axis(4)*(-100))
                    l_y = int(joy.get_axis(1)*(-100))
#                    v = l_y*1000+r_y
#                    print (l_y, r_y)
                    return r_y, l_y
#            time.sleep(0.1)
    def callback(self):
        self.r, self.l = self.onTick()          
        self.msg.data = self.r, self.l
        self.get_logger().info("{0}".format(self.msg.data))
        self.pub.publish(self.msg)
        print (self.msg.data[0],self.msg.data[1])

def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()

    try:
        rclpy.spin(node)
    except (KeyboardInterrupt):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
