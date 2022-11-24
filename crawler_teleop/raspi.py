import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String
import serial
import time

class SubscriberNode(Node):
    def __init__(self):
        super().__init__("subscriber")

        self.ser = serial.Serial(
            port='/dev/tty0', # デバイス名 
            baudrate=115200, # ポート番号
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        time.sleep(0.1)

        self.direction = 0
        self.create_subscription(String, "verocity", self.onSubscribed, 10)

    def onSubscribed(self, msg):
        self.get_logger().info("{0}".format(msg.data))
        if self.direction != msg.data:
            self.direction = msg.data

            time.sleep(0.1)

def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
