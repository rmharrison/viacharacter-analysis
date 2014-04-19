#ffmpeg -r 1 -i byRank_%02d.png -r 1 -vcodec mpeg4 -s 600x600 byRank.mp4
#ffmpeg -i byRank.mp4 -pix_fmt rgb24 byRank.gif
for i in {1..9}; do mv byRank_$i.png byRank_0$i.png; done
convert -delay 1 -loop 0 byRank_*.png byRank.gif
convert -delay 2 -loop 0 corrcoef_Q*.png corrcoef.gif
