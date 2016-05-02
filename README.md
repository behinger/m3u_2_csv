### m3u_2_csv
  Download:
  ``` git clone https://github.com/behinger/m3u_2_csv ```
  
### tutorial
  Put your files in the m3u folder, the ./dist/m3u2csv.exe (for windows) or ./dist/m3u2csv (for ubuntu/linux) should be in the parent folder.
  ```
  ./m3u2csv.exe
  ./m3u/playlist1.m3u
  ./m3u/playlist2.m3u
  ...
  ```
  Run the `m3u2csv.exe` (in windows)
  
  Run `sh m3u2csv` (in ubuntu)
  
### What does it do?
This program loops over the audio files from the m3u-playlist and reads their ID3-Tags. It then concatenates some of them to a csv file. Currently the following tags are saved:
- artist
- title
- genre
- duration
- year
- album

### 
The compiled files have been compiled using pyinstaller (-F)

This tool only works if you have read-access to the audio files.
