import dotbot_ros
import telepot
from geometry_msgs.msg import Twist
from gpiozero import Robot
import sys

class Node(dotbot_ros.DotbotNode):
    node_name = 'telegram_bot_simpe'
    TOKEN = "Set Your Token here"

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            cmd = msg['text'].split()
            if cmd[0] == '/start':
                bot.sendMessage(chat_id, 'testing custom keyboard',
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[
                                [KeyboardButton(text=""), KeyboardButton(text="avanti"), KeyboardButton(text="")],
                                [KeyboardButton(text="destra"), KeyboardButton(text="stop"), KeyboardButton(text="sinista")],
                                [KeyboardButton(text=""), KeyboardButton(text="indietro"), KeyboardButton(text="")]
                                ]
                            )
                        )
            elif cmd[0] == 'avanti':
                cmd_vel = Twist()
                cmd_vel.linear.x = 1.0
                self.bot.sendMessage(chat_id, "vado avanti!")
                self.vel_publish.publish(cmd_vel)
            elif cmd[0] == 'indietro':
                cmd_vel = Twist()
                cmd_vel.linear.x = -1.0
                self.vel_publish.publish(cmd_vel)
                self.bot.sendMessage(chat_id, "vado indietro!")
            elif cmd[0] == 'destra':
                cmd_vel = Twist()
                cmd_vel.angular.z = 0.2
                self.vel_publish.publish(cmd_vel)
                self.bot.sendMessage(chat_id, "vado a destra!")
            elif cmd[0] == 'sinistra':
                cmd_vel = Twist()
                cmd_vel.angular.z = -0.2
                self.vel_publish.publish(cmd_vel)
                self.bot.sendMessage(chat_id, "vado a sinistra!")
            elif cmd[0] == 'stop':
                cmd_vel = Twist()
                self.vel_publish.publish(cmd_vel)
                self.bot.sendMessage(chat_id, "ok, mi fermo!")
            else:
                self.bot.sendMessage(chat_id, "non ho capito!")

    def setup(self):
        self.bot = telepot.Bot(self.TOKEN)
        self.bot.message_loop(self.handle)
        self.vel_publish = dotbot_ros.Publisher('cmd_vel', Twist)

        print 'ready'
        sys.stdout.flush()
