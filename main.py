import subprocess
import time

class base:
    def __init__(self):
        self.workingdir = "/home/soere/Documents/RPi_SSTV_GUI/"
        self.filename = "picture"
        self.mode = "PD50"
        self.hres = 320
        self.vres = 240

    def get_command(self):
        raise NotImplementedError("Command Getter not implemented for this class!")

    def execute(self):
        subprocess.run(self.get_command(), shell=True, check=True);


    


class libcamera(base):
    def __init__(self):
        super().__init__()
        self.command = "libcamera-still --immediate --width {} --height {} -e bmp -o ".format(self.hres, self.vres) + self.workingdir + self.filename + ".bmp"

    def get_command(self):
        return self.command
    

class overlayprinter(base):
    def __init__(self):
        super().__init__()
        self.logoname = "logo02" #w:43 h:93
        self.bannername = "banner" #w:320 h:32
        self.command = "convert -page +0+0 " + self.workingdir + self.filename + ".bmp" \
            + " -page +0+0 " + self.logoname + ".png" \
            + " -page +0+{} ".format(self.vres - 32) + self.bannername + ".png" \
            + " -background none -layers merge +repage" \
            + " -crop {}x{}".format(self.hres, self.vres) + self.workingdir + self.filename + ".bmp"

    def get_command(self):
        return self.command
    

class libsstv(base):
    def __init__(self):
        super().__init__()
        self.path = "/home/soere/bin/libsstv/bin/"

    def get_command(self):
        return self.path + "sstv-encode " + self.mode + " " + self.workingdir + self.filename + ".bmp" + " " + self.workingdir + self.filename + ".wav"


class displaycontroller(base):
    def __init__(self):
        super().__init__()
        self.command = "echo \"Done displaying Countdown.\""
        self.countdown_time_s = 5;

    def get_command(self):
        subprocess.run("echo \"Displaying Countdown ...\"", shell=True, check=True);
        i = self.countdown_time_s;
        while i > 0:
            subprocess.run("echo \"{}\"".format(i), shell=True, check=True);
            time.sleep(1);
            i -= 1;
            
        return self.command


class rpitx(base):
    def __init__(self):
        super().__init__()
        self.path = "/home/soere/bin/rpitx/"
        self.frequency_Hz = "433400000"

    def get_command(self):
        return "cat " + self.workingdir + self.filename \
            + ".wav   | csdr convert_i16_f   | csdr gain_ff 7000   | csdr convert_f_samplerf 20833   | sudo " \
            + self.path + "rpitx -i- -m RF -f " + self.frequency_Hz
    


if __name__ == "__main__":
    steps = [libcamera(), overlayprinter(), libsstv(), displaycontroller(), rpitx()]

    for step in steps:
        try:
            step.execute()
        except subprocess.CalledProcessError as e:
            print(f"[FEHLER] Befehl fehlgeschlagen: {e}")
            break
