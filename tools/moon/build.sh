set -e
python3 render.py raw.mp4
ffmpeg -y -loglevel error -i raw.mp4 -i vo/voice.wav -i music.wav -i sfx.wav -filter_complex "[1:a]aresample=48000,highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=90,asplit=2[vs][v1];[2:a]aresample=48000,volume=0.2[m];[m][vs]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];[3:a]aresample=48000,volume=0.35[fx];[md][v1][fx]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5[a]" -map 0:v -map "[a]" -c:v copy -c:a pcm_s16le -shortest mix.mkv
ffmpeg -y -loglevel error -i mix.mkv -c:v libx264 -b:v 1600k -pass 1 -preset slow -pix_fmt yuv420p -an -f mp4 /dev/null
ffmpeg -y -loglevel error -i mix.mkv -c:v libx264 -b:v 1600k -pass 2 -preset slow -pix_fmt yuv420p -c:a aac -b:a 128k -ar 48000 -movflags +faststart final.mp4
echo DONE
