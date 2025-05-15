import subprocess


class base:
    def __init__(self):
        self.workingdir = "/home/soere/Documents/RPi_SSTV_GUI/"
        self.filename = "picture"

    def get_command(self):
        raise NotImplementedError("Command Getter not implemented for this class!")

    def execute(self):
        subprocess.run(self.get_command(), shell=True, check=True);


    


class libcamera(base):
    def __init__(self):
        super().__init__()
        self.command = "libcamera-still --width 320 --height 256 -e png -o " + self.workingdir + self.filename + ".png"

    def get_command(self):
        return self.command


class libsstv(base) :
    def __init__(self):
        super().__init__()
        self.path = "/home/soere/bin/libsstv/bin/"
        self.mode = "MARTIN_M1"

    def get_command(self):
        return self.path + "sstv-encode " + self.mode + " " + self.workingdir + self.filename + ".png" + " " + self.workingdir + self.filename + ".wav"


class rpitx(base):
    def __init__(self):
        super().__init__()
        self.path = "/home/soere/bin/rpitx/"
        self.frequency_Hz = "430200000"

    def get_command(self):
        return "cat " + self.workingdir + self.filename + ".wav   | csdr convert_i16_f   | csdr gain_ff 7000   | csdr convert_f_samplerf 20833   | sudo " + self.path + "rpitx -i- -m RF -f " + self.frequency_Hz
    


if __name__ == "__main__":
    steps = [libcamera(), libsstv(), rpitx()]

    for step in steps:
        try:
            step.execute()
        except subprocess.CalledProcessError as e:
            print(f"[FEHLER] Befehl fehlgeschlagen: {e}")
            break
