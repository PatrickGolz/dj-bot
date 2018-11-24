import telepot
from telepot.loop import MessageLoop

import os, signal, subprocess, time

VOLUME_SETTINGS = (LOW, MEDIUM, NORMAL, HI, MAX) = ('low', 'medium', 'normal', 'hi', 'max')
COMMANDS = (PLAY, STOP, PAUSE, RESUME, VOLUME) = ('play', 'stop', 'pause', 'resume', 'volume')
VOLUME_CONTROL = {LOW: 0, MEDIUM: 10, NORMAL: 20, HI: 25, MAX: 30}


class DJRaspberry(object):

    def __init__(self):
        self.music_process = None
        self.current_volume = VOLUME_CONTROL[NORMAL]

    def run(self, data):
        print 'called'
        action = data.split(' ')[0]
        if PLAY in action:
            self.play_music(data.split(PLAY)[1].strip())
        elif STOP in action:
            self.stop_music()
        elif VOLUME in action:
            self.adjust_volume(data.split(VOLUME)[1].strip())
        elif PAUSE in action or RESUME in action:
            self.pause_and_resume()
        else:
            print 'invalid input'

    def play_music(self, song):
        print 'play music'
        self.stop_music()
        self.music_process = subprocess.Popen('sudo mpsyt;'.format(**locals()),
                                              shell=True,
                                              stdout=subprocess.PIPE,
                                              stdin=subprocess.PIPE,
                                              preexec_fn=os.setsid)
        self.music_process.stdin.write("/{song}\n1\n".format(**locals()))


    def stop_music(self):
        print 'stop'
        if self.music_process:
            print 'kill'
            os.killpg(self.music_process.pid, signal.SIGTERM)
            self.music_process = None


    def pause_and_resume(self):
        print 'pause'
        if self.music_process:
            self.music_process.stdin.write(" ")


    def adjust_volume(self, target_volume):
        if not self.music_process:
            return
        target_volume = VOLUME_CONTROL.get(target_volume.split(' ')[0])
        while self.current_volume < target_volume:
            self.current_volume += 1
            self.music_process.stdin.write("=")
            time.sleep(1)

        while self.current_volume > target_volume:
            self.current_volume -= 1
            self.music_process.stdin.write("-")
            time.sleep(1)



dj = DJRaspberry()


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text'].strip().lower()

    print 'Got command: %s' % command

    dj.run(command)

    bot.sendMessage(chat_id, 'Playing...')


bot = telepot.Bot('620551592:AAG0cstQ3y3QEyyyN0dsRy9A4KteNWmPgQs')

MessageLoop(bot, handle).run_as_thread()
print 'I am listening ...'

while 1:
    time.sleep(10)
