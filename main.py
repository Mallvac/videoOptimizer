import os
import ffmpeg


def main():
    # fuck you, whole message in one print
    print("#######################\n#                     #\n#   Video Optimizer   #\n#                     #"
          "\n#######################\n\n1. Optimize\n2. Target Size\n3. Target Bitrate\n4. Exit")
    func_list = {
        1: optimize_video,
        2: "fuck",
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
            print(f'"{ch}" is not deifned')
        else:
            break
    # if user not stupid do code :D
    func()


def optimize_video():
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 96000
    max_audio_bitrate = 256000

    while True:
        # why do users have to be so stupid, if we all follow rules this would be redundant
        video_full_path: str = input("video full path:")
        # noinspection PyBroadException
        try:
            if video_full_path is None:
                raise ValueError()
            global probe
            probe = ffmpeg.probe(video_full_path)
        except:
            print("This is not a valid video path")
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

    i = ffmpeg.input(video_full_path)

    # ffmpeg call
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'libvo_aacenc', 'b:a': audio_bitrate}
                  ).overwrite_output().run()


if __name__ == "__main__":
    main()