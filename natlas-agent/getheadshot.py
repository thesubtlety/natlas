#!/usr/bin/env python3

import subprocess
import os
import time

# wkhtmltoimage --width 50 --quality 80 -f jpg <target> out.jpg
# vncsnapshot -quality 50 <target> out.jpg


def getheadshot(ip, rand, service):

    if service in ("vnc"):
        if "DISPLAY" not in os.environ:
            return False
        process = subprocess.Popen(["xvfb-run", "vncsnapshot", "-quality", "50", ip, "data/natlas." +
                                    rand + "." + service + ".headshot.jpg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            out, err = process.communicate(timeout=60)
            if process.returncode is 0:
                return True
        except:
            try:
                print("[!] (%s) Killing slacker process" % rand)
                process.kill()
                return False
            except:
                pass

    else:
        #process = subprocess.Popen(["wkhtmltoimage", "--javascript-delay", "3000", "--width", "800", "--height", "600", "--quality",
        #                            "80", "-f", "jpg", service+"://"+ip, "data/natlas."+rand+"." + service + ".headshot.jpg"], stdout=FNULL, stderr=FNULL)
        if "xml" in service:
            print("running aquatone from nmap xml")
            process = subprocess.Popen(["aquatone","-nmap","-out", "data/aquatone."+rand], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
            process.stdin.write(service.encode('utf-8'))
        else:
            p1 = subprocess.Popen(["echo", service+"://"+ip], stdout=subprocess.PIPE)
            process = subprocess.Popen(["aquatone","-ports",service, "-scan-timeout", "1000", "-out", "data/aquatone."+rand+".port"+service], stdin=p1.stdout, stdout=subprocess.DEVNULL)
            p1.stdout.close()
        
        try:
            out,err = process.communicate(timeout=60)
            if process.returncode is 0:
                time.sleep(0.5) # a small sleep to make sure all file handles are closed so that the agent can read them
                return True
        except subprocess.TimeoutExpired:
            print("[!] (%s) Killing slacker process" % rand)
            process.kill()
        


    # fall through to return false if service is unsupported or if process returncodes aren't 0
    return False
