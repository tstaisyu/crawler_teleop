import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
from std_msgs.msg import Int32MultiArray
import serial
import time

bottom = 50
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
        self.joy_r = 0
        self.joy_l = 0


        self.verocity = None
        self.create_subscription(Int32MultiArray, "verocity", self.onSubscribed, 10)

    def onSubscribed(self, msg):
#        self.get_logger().info("{0}".format(msg.data))
        self.r = msg.data[0]
        self.l = msg.data[1]
        print ("L: {0}, R: {1}".format(self.l, self.r))

    def toGpio(self, msg): 
        self.joy_r = msg.data[0]
        self.jop_l = msg.data[1]
        motor_r = self.joy_r
        motor_l = self.joy_l
        time.sleep(0.1)
        if motor_l > 10 and motor_r > 10:
            GPIO.output(ENABLE_r, GPIO.LOW)
            GPIO.output(ENABLE_l, GPIO.LOW)
            p_r.ChangeDutyCycle(motor_l)
            p_l.ChangeDutyCycle(motor_r)
            print("go:", motor_l, motor_r)
            
        elif motor_l > 10 and motor_r < -10:
            GPIO.output(ENABLE_r, GPIO.HIGH)
            GPIO.output(ENABLE_l, GPIO.LOW)
            p_r.ChangeDutyCycle(motor_l)
            p_l.ChangeDutyCycle(-(motor_r))
            print("turn right:", motor_l, motor_r)
            
        elif motor_l < -10 and motor_r > 10:
            GPIO.output(ENABLE_r, GPIO.LOW)
            GPIO.output(ENABLE_l, GPIO.HIGH)
            p_r.ChangeDutyCycle(-(motor_l))
            p_l.ChangeDutyCycle(motor_r)
            print("turn left:", motor_l, motor_r)
            
        elif motor_l < -10 and motor_r < -10:
            GPIO.output(ENABLE_r, GPIO.HIGH)
            GPIO.output(ENABLE_l, GPIO.HIGH)
            p_r.ChangeDutyCycle(-(motor_l))
            p_l.ChangeDutyCycle(-(motor_r))
            print("back:", motor_l, motor_r)
            
        else:
            print("stop:", motor_l, motor_r)
            p_r.stop()
            p_l.stop()
            p_r.start(0)
            p_l.start(0)



def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    rclpy.spin(node)
    node.destroy_node()
    GPIO.cleanup()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
