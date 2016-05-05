### m3u_2_csv
  Download:
  ``` git clone https://github.com/behinger/m3u_2_csv ```
  
### tutorial
  Run the `m3u2csv.exe` (in windows)
  
  Run `./m3u2csv` (in ubuntu)
  
  Run `./m3u2csv` (in mac OS X)

  
  -> Select all .m3u files you want to export to a csv file
  
### What does it do?
This program loops over the audio files from the m3u-playlist and reads their ID3-Tags. It then concatenates some of them to a csv file. Currently the following tags are saved:
- artist
- title
- genre
- duration
- year
- album

### Etc.
The compiled files have been compiled using pyinstaller (-F)

This tool only works if you have read-access to the audio files.

M3Us are not really standardized, so some programs might export the M3U differently. Please write me and I will try to fix it.
