import urllib.request
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
    
    # Parse the m3u file
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
                        # pull channel link from all other, non-blank lines
                        link=line
                        channel["link"] = link
                        self.channels.append(channel)
                        # make the channel dict empty for the new channel
                        channel = {}
        else:
            print("Not an m4u file")
    
    # Display list to the user
    def list_channels(self):
        print("List of channels available are: ")
        for i, channel in enumerate(self.channels, 1):
            print(i, channel.get("name"))
    
    # Returns the list of channels with {name, link}
    def get_channels(self):
        return self.channels

# Managing the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-file", help="Name of the .m3u file with extension")
args = parser.parse_args()

# Getting the current version info
def update():
    curr_ver = None
    with open("version.txt", "r") as version_file:
        curr_ver = float(version_file.readline().split("=")[-1])
        print("Version : ", curr_ver)
    response = urllib.request.urlopen("https://raw.githubusercontent.com/monuyadav016/Live-TV/master/version.txt").read
    new_ver = float(response.split("=")[-1])
    print("Latest version availble: ", new_ver)
    print("Updating...")
    if new_ver > curr_ver:
        with open("version.txt", "w") as version_file:
            version_file.wirte(new_ver)

if args.file is None:
    print("No filename provided using default file India.m3u")
    args.file = "India.m3u"
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