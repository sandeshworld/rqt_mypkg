import os
import rospy
import rospkg

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget
from geometry_msgs.msg import Twist, Vector3 #import the message needed



class MyPlugin(Plugin):

    def __init__(self, context):


        super(MyPlugin, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('MyPlugin')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns

        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which should be in the "resource" folder of this package
        ui_file = os.path.join(rospkg.RosPack().get_path('rqt_mypkg'), 'resource', 'MyPlugin.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('MyPluginUi')
        # Show _widget.windowTitle on left-top of each plugin (when 
        # it's set in _widget). This is useful when you open multiple 
        # plugins at once. Also if you open multiple instances of your 
        # plugin at once, these lines add number to make it easy to 
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)

	#MOVE ROCAM 
	self._widget.Up.clicked[bool].connect(self.move_up)
	

	self._widget.Down.clicked[bool].connect(self.move_down)

	self._widget.Right.clicked[bool].connect(self.move_right)

	self._widget.Left.clicked[bool].connect(self.move_left)

	#MOVE MOTOR SHIELD
	self._widget.MUp.clicked[bool].connect(self.move_mup)

	self._widget.MDown.clicked[bool].connect(self.move_mdown)

	self._widget.MRight.clicked[bool].connect(self.move_mright)

	self._widget.MLeft.clicked[bool].connect(self.move_mleft)
	

	
	self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1) #no need to instantiate another rosnode
	
	self.mpub = rospy.Publisher('/motorshield',Vector3, queue_size=1) #no need to instantiate another rosnode
	
	self.forward_delta = 1
	self.left_delta = 1


	self.cmd_vel = Twist() #instantiating the twist object to be modified for sending
	self.motor_vel = Vector3()

    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    def move_up(self,checked):
		print("up")
		self.cmd_vel.angular.z = self.forward_delta
		self.publish()
    def move_down(self,checked):	
		print("down")
		self.cmd_vel.angular.z = -1*self.forward_delta
		self.publish()

    def move_right(self,checked):	
		print("right")
		self.cmd_vel.linear.x = self.left_delta
		self.publish()

    def move_left(self,checked):	
		print("left")
		self.cmd_vel.linear.x = -1*self.left_delta
		self.publish()
    def publish(self):
		self.pub.publish(self.cmd_vel)

    def move_mup(self,checked):
		print("mup")
		num12 = 400.0
		self.motor_vel.x = num12
		self.motor_vel.y = num12
		self.publishmotor()
    def move_mdown(self,checked):	
		print("mdown")
		num12 = 400.0
		self.motor_vel.x = -1*num12
		self.motor_vel.y = -1*num12
		self.publishmotor()

    def move_mright(self,checked):	
		print("mright")
		num12 = 400.0
		self.motor_vel.x = num12
		self.motor_vel.y = 0
		self.publishmotor()

    def move_mleft(self,checked):	
		print("mleft")
		num12 = 400.0
		self.motor_vel.x = 0
		self.motor_vel.y = num12
		self.publishmotor()
    def publishmotor(self):
		self.mpub.publish(self.motor_vel)
	


   #def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog
