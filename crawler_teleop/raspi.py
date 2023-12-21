import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import serial
import time

class SubscriberNode(Node):
    def __init__(self):
        super().__init__("subscriber")

#        self.ser = serial.Serial(
#            port='/dev/tty0', # デバイス名 
#            baudrate=115200, # ポート番号
#            parity=serial.PARITY_NONE,
#            stopbits=serial.STOPBITS_ONE,
#            bytesize=serial.EIGHTBITS,
#            timeout=1
#        )
        time.sleep(0.1)

        self.direction = 0
        self.create_subscription(Int32MultiArray, "velocity", self.onSubscribed, 10)

    def onSubscribed(self, msg):
#        self.get_logger().info("{0}".format(msg.data))
        self.r = msg.data[0]
        self.l = msg.data[1]
        print ("L: {0}, R: {1}".format(self.l, self.r))

def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
