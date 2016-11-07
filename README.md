# playlistparser
PlaylistParser is a Python command-line utility to download videos from a YouTube playlist 

##Description
PlaylistParser takes in the url of a YouTube playlist page and downloads the some or all of the videos listed on it depending on the arguments passed.

By default, PlaylistParser selects the highest resolution among the download options available for your videos. If multiple extensions exist at the highest resolution, it will prefer .mp4 over others.

##Installation
Run the included installscript.sh file. This will install modules necessary for the project, if not available on your machine.
```
$ ./installscript.sh
```
Note: If this does not run, you need to make it executable by running `chmod +x installscript.sh`

##Usage
The program is intended to be run as a command-line utility. It will ask you for a preferred download directory the first time it is run. Skipping this sets it to the default home directory.

Note: If this does not run, you need to make sure it is executable by running `chmod +x playlistparser.py`

The most basic usage is just passing the url of the playlist page. This will download all the videos in the playlist
```
$ ./playlistparser https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBhgcpA8eTYYWg7im72LgLt
```

A download path can be specified by using `-p` or `--path`. This will not be set as default unless the `--setaspath` flag is also passed with it
```
$ ./playlistparser https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBhgcpA8eTYYWg7im72LgLt -p ~/Downloads
```
To download only a certain section of the videos on the playlist, the `--start` and `--end` arguments are passed. Numbering starts from 1, and the range is inclusive of both start and end.
Passing only `--start` will download files from start onwards.
```
$ ./playlistparser https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBhgcpA8eTYYWg7im72LgLt --start 5
```
Similarly, passing only `--end` will download all videos till end
```
$ ./playlistparser https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBhgcpA8eTYYWg7im72LgLt --end 3
```

If a file with the same name as one being downloaded exists in the directory, the user gets a prompt to confirm overwrite. To overwrite all conflicting files, the `-f` flag should be passed. If overwrite is cancelled, that file is skipped and it's url is not added to the text file

**_Incomplete feature_** The current download directory can be checked from command-line by using `-show`
```
$ ./playlistparser x -show
```
This has not been impelmented as a subcommand yet, and therefore needs a positional url argument to be passed thought it does not use it. Hence, any random string ("x" in this case) should be passed with it
