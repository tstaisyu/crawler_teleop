import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import serial
import time

R = 12
L = 13
ENABLE_r = 17
ENABLE_l = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(L, GPIO.OUT)
GPIO.setup(ENABLE_r, GPIO.OUT)
GPIO.setup(ENABLE_l, GPIO.OUT)
GPIO.output(ENABLE_r, GPIO.LOW)
GPIO.output(ENABLE_l, GPIO.LOW)

p_r = GPIO.PWM(R, bottom)
p_l = GPIO.PWM(L, bottom)

p_r.start(0)
p_l.start(0)

class SubscriberNode(Node):
    def __init__(self):
        super().__init__("subscriber")

        time.sleep(0.1)

        self.verocity = None
        self.create_subscription(Int32MultiArray, "verocity", self.onSubscribed, 10)

    def onSubscribed(self, msg):
#        self.get_logger().info("{0}".format(msg.data))
        self.r = msg.data[0]
        self.l = msg.data[1]
        print ("L: {0}, R: {1}".format(self.l, self.r))

    def toGpio(self, msg): 
        self.r = 0
        self.l = 0
        r = msg.data[0]
        l = msg.data[1]



def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
