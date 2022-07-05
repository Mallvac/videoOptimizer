import os
import ffmpeg

max_audio_bitrate = 256000
min_audio_bitrate = 96000


def main():
    # fuck you, whole message in one print
    print("#######################\n#                     #\n#   Video Optimizer   #\n#                     #"
          "\n#######################\n\n1. Optimize\n2. Target Size\n3. Target Bitrate\n4. Exit")
    func_list = {
        1: optimize_video,
        2: target_size,
        3: "do later",
        4: exit
    }

    # check if user stupid
    while True:
        ch = input()
        try:
            ch_: int = int(ch)
            func = func_list.get(ch_, "Invalid entry")
        except ValueError:
            print(f'[Err] "{ch}" is not defined, please try again')
        else:
            break
    # if user not stupid do code :D
    func()


def run_ffmpeg(input_path, video_bitrate, audio_bitrate, output_file_name):
    ffmpeg.output(input_path, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(input_path, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'libvo_aacenc', 'b:a': audio_bitrate}
                  ).overwrite_output().run()


def optimize_video():
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate

    while True:
        # why do users have to be so stupid, if we all follow rules this would be redundant
        video_full_path: str = input("video full path:")
        # noinspection PyBroadException
        try:
            if video_full_path is None:
                raise ValueError()
            # noinspection PyGlobalUndefined
            global probe
            probe = ffmpeg.probe(video_full_path)
        except:
            print("[Err] This is not a valid video path")
        else:
            break

    output_file_name: str = input("Output file name:")
    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    alldata = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
    target_total_bitrate = ((alldata["width"]) * (alldata["height"]) / 648) * 1000

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate

    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate
    print(video_bitrate)
    print(audio_bitrate)

    input_path = ffmpeg.input(video_full_path)

    # ffmpeg call
    run_ffmpeg(input_path, video_bitrate, audio_bitrate, output_file_name)


def target_size():
    # make code not dumb

    while True:
        video_full_path: str = input("video full path:")
        # noinspection PyBroadException
        try:
            if video_full_path is None:
                raise ValueError()
            # noinspection PyGlobalUndefined
            global probe
            probe = ffmpeg.probe(video_full_path)
        except:
            print("[Err] This is not a valid video path")
        else:
            break

    output_file_name: str = input("Output file name:") 

    alldata = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    time_str = alldata['duration']
    time = float(time_str)

    while True:
        size_str = input("Video target size in MB:")
        # this is gonna make it run itty bitty slower, but I did it for the vine
        if size_str == "yourmom":
            print("[Err] The value is too big")
        else:
            try:
                size = float(size_str)
                break
            except ValueError:
                print("[Err] This is not a valid size")

    # meth
    megabit = size*8
    bit = megabit*1000000
    target_total_bitrate = bit/time

    # audio bitrate calc
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate

    video_bitrate = target_total_bitrate - audio_bitrate

    input_path = ffmpeg.input(video_full_path)
    # ffmpeg call
    run_ffmpeg(input_path, video_bitrate, audio_bitrate, output_file_name)


if __name__ == "__main__":
    main()
