# import urllib.request
import subprocess
import argparse

class PlaylistParser():
    def __init__(self):
        self.filename = None
        self.channels = []

    def is_m3u(self, filename=None):
        fname = filename or self.filename
        try:
            with open(fname, "r") as fhand:
                while True:
                    line = fhand.readline()
                    line = line.strip()
                    if line:
                        if line.startswith("#EXTM3U"):
                            return True
                    else:
                        return False
        except FileNotFoundError:
            return False

    def parse_m3u(self, filename=None):
        if filename:
            self.filename = filename
        is_m3u = self.is_m3u(filename)
        if is_m3u:
            print("Is m3u file")
            with open(self.filename, "r") as fhand:
                playlist=[]
                channel = {}
                for line in fhand:
                    line=line.strip()
                    if line.startswith('#EXTINF:'):
                        # pull length and title from #EXTINF line
                        meta_data = line.split(",")
                        channel_name = meta_data[-1]
                        channel["name"] = channel_name
                    elif (len(line) != 0):
                        # pull channel path from all other, non-blank lines
                        link=line
                        channel["link"] = link
                        self.channels.append(channel)
                        channel = {}
        else:
            print("Not an m4u file")
    
    def list_channels(self):
        print("List of channels available are: ")
        for i, channel in enumerate(self.channels, 1):
            print(i, channel.get("name"))
    
    def get_channels(self):
        return self.channels

parser = argparse.ArgumentParser()
parser.add_argument("-file", help="Name of the .m3u file with extension")
args = parser.parse_args()

if args.file is None:
    print("No filename provided")
else:
    print(args.file)
    playlist = PlaylistParser()
    playlist.parse_m3u(args.file)
    playlist.list_channels()
    channels = playlist.get_channels()
    channel_no = int(input("Enter the channel number: "))
    if channel_no > 0:
        try:
            channel = channels[channel_no - 1]
            subprocess.run(["vlc", channel["link"]])
        except Exception as e:
            print(e)
    else:
        print("Invalid channel No")
        
    # print(playlist.get_channels())