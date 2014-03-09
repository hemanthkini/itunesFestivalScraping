import requests
import sys

host = 'http://streaming.itunesfestival.com'
initial_dir, separator, initial_playlist_file = sys.argv[1].rpartition('/')
print('initial playlist file: ' + initial_playlist_file)

if len(sys.argv) < 3:
    cookie_val = 'token=expires=1394720102~access=/auth/*~md5=0dc73aa30d88bfabef5fbef59e3ec3b1; ITMFID=9760E0D8ADD53C99099B49594144154F'
else:
    cookie_val = sys.argv[2]

if len(sys.argv) < 4:
    sessid_val = 'E4F6365B-08C0-6C42-9D2F-3C49B555A8A2'
else:
    sessid_val = sys.argv[3]

headers = {'User-Agent' : 'AppleCoreMedia/1.0.0. (AAS-3.0.1; U; Windows NT 6.2)', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip', 'X-Playback-Session-Id' : sessid_val, 'Cookie' : cookie_val, 'Connection' : 'keep-alive'}

r = requests.get(host+initial_dir+'/'+initial_playlist_file, headers=headers)

print("here's the list of format directories and the playlist file inside:")
print("(the first number is the video bitrate; the second is the audio bitrate)")

for line in r.text.split('\n'):
    line, sep, junk = line.partition('\r') #to get rid of the carriage return
    if (len(line) > 0):
        if line[0] != '#':
            print(line)

format_dir = raw_input('enter the format dir you want (no slash before or after): ')
playlist_file = raw_input('enter the playlist_file name (no slash before, extension after): ')


format_dir = '/' + format_dir
playlist_file = '/' + playlist_file
directory = initial_dir + format_dir

r = requests.get(host+directory+playlist_file, headers=headers)
print(r.headers)
print(r.text)
print(r.encoding)

output_file = open("test.ts", "w")

for line in r.text.split('\n'):
    line, sep, junk = line.partition('\r') #to get rid of the carriage return
    if (len(line) > 0):
        if line[0] != '#':
#            output_file = open(line, "w")
            ts_req = requests.get(host+directory+'/'+line, headers=headers)
            print("just got: " + line)
            print("the response headers are: ")
            print(ts_req.headers)
            for chunk in ts_req.iter_content(4096):
                output_file.write(chunk)
#            output_file.close()
            print("wrote it!\n\n")

output_file.close()

print("done!")
