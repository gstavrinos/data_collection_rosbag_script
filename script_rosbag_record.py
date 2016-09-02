#!/usr/bin/env python
import subprocess, shlex
import time, os, signal

if __name__ == '__main__':
    print '\033[92m' + "Welcome to the Radio Dataset Script!\n" + '\033[0m'
    while(True):
        next_ = raw_input("Do you want to initialize the sensors? (y/n):\n").lower()
        while(next_ != "y" and next_ != "n"):
            next_ = raw_input("Do you want to initialize the sensors? (y/n):\n").lower()

        if(next_ == "y"):
            command = "roscore"
            command = shlex.split(command)
            subprocess.Popen(command)
            time.sleep(5)
            print '\033[93m' + "roscore is now running!\n" + '\033[0m'
            command = "roslaunch astra_launch astra.launch"
            command = shlex.split(command)
            subprocess.Popen(command)
            time.sleep(10)
            print '\033[93m' + "Camera is now running!\n" + '\033[0m'
            command = "rosrun urg_node urg_node _ip_address:=192.168.0.10"
            command = shlex.split(command)
            subprocess.Popen(command)
            time.sleep(5)
            print '\033[93m' + "Laser scanner is now running!\n" + '\033[0m'
            command = "rosrun audio_capture audio_capture"
            command = shlex.split(command)
            subprocess.Popen(command)
            command = "roslaunch acoustic_magic_doa doa.launch"
            command = shlex.split(command)
            subprocess.Popen(command)
            time.sleep(5)
            print '\033[93m' + "Microphone is now running!\n" + '\033[0m'

        final_name = "ss"
        next_ = raw_input("Please enter Sensor Setup:\n")
        while(next_ != "1" and next_ != "2"):
            next_ = raw_input("Please enter Sensor Setup:\n")
        print "ok"
        final_name += next_

        final_name += "_ls"
        next_ = raw_input("Please enter Lights Setup:\n").upper()
        while(next_ != "N" and next_ != "A"):
            next_ = raw_input("Please enter Lights Setup:\n").upper()
        final_name += next_

        final_name += "_sc"
        next_ = raw_input("Please enter Scenario:\n").upper()
        while(next_ != "1A" and next_ != "3A" and next_ != "1B" and next_ != "2" and next_ != "3B" and next_ != "4"):
            next_ = raw_input("Please enter Scenario:\n").upper()
        final_name += next_
        scenario = next_

        final_name += "_ru"
        next_ = raw_input("Please enter Radio User (4 characters):\n").lower()
        while(len(next_) != 4):
            next_ = raw_input("Please enter Radio User (4 characters):\n").lower()
        final_name += next_

        final_name += "_cg"
        next_ = ""
        if(scenario != "1A" and scenario != "1B"):
            next_ = raw_input("Please enter Caregiver (4characters):\n").lower()
            while(len(next_) != 4):
                next_ = raw_input("Please enter Caregiver (4 characters):\n").lower()
        final_name += next_

        final_name += "_v"
        next_ = ""
        if(scenario == "3B"):
            next_ = raw_input("Please enter Visitor (4characters):\n").lower()
            while(len(next_) != 4):
                next_ = raw_input("Please enter Visitor (4 characters):\n").lower()
        final_name += next_
        final_name += ".bag"

        command = "rosbag record -O " + final_name + " /scan"#" /camera/rgb/image_raw /camera/depth/image_raw /audio /acoustic_magic/data_raw /scan"
        command = shlex.split(command)
        rosbag_process = subprocess.Popen(command)
        time.sleep(2)

        raw_input('\033[91m' + "Press enter to stop recording\n" + '\033[0m')

        nodes = os.popen("rosnode list").readlines()
        for i in range(len(nodes)):
            nodes[i] = nodes[i].replace("\n","")

        for node in nodes:
            if(node.startswith("/record_")):
                os.system("rosnode kill "+ node)

        next_ = raw_input('\033[94m' + "Do you want to run again? (y/n)\n" + '\033[0m').lower()
        while(next_ != "y" and next_ != "n"):
            next_ = raw_input('\033[94m' + "Do you want to run again? (y/n)\n" + '\033[0m').lower()

        if(next_ == "n"):
            print '\033[91m' + "Good bye then!" + '\033[0m'
            break
