#!/usr/bin/env python

from urllib2 import urlopen
from bs4 import BeautifulSoup
from pytube import YouTube
from os import path
import pickle
import argparse

def getArgParser():
        '''Returns ArgParser object to handle command-line args'''
        #Consider using subcommands to make 3 groups: show,set,download
        parser = argparse.ArgumentParser()
        parser.add_argument("-show","--showpath",help="Displays current download dir",action="store_true")
        parser.add_argument("playlist_url",help="url of the playlist page")
        parser.add_argument("--setaspath",help="Sets PATH arg passed as the default download dir",action="store_true")
        parser.add_argument("-p","--path",default="",help="the directory where videos should be downloaded to. Default is ~")
        parser.add_argument("--start",type=int,help="Starting video number, inclusive; numbering begins from 1")
        parser.add_argument("--end",type=int,help="Ending video number, inclusive; numbering begins from 1")
        parser.add_argument("-f",help="Forces overwrite of file with same filename in dir",action="store_true")
        return parser

def setDownloadPath(newpath):
        '''Sets argument as the new download directory'''
        
        pkl_file = open('data.pkl','wb')
        pickle.dump(newpath,pkl_file)
        pkl_file.close()

def getDownloadPath():
        '''Fetches the current download directory'''
        
        try:
                pkl_file = open('data.pkl','rb')
                return pickle.load(pkl_file)
        except IOError:
                #File not found. Prompt for path, with default being home
                #Since it is setting the path in any case, this will be triggered
                #only for first run. Or if pkl file is manually deleted
                inp_path = raw_input("Please specify Download path:(Empty for the default ~ dir)\n")
                if inp_path == "":
                        setDownloadPath(path.expanduser('~'))
                        return path.expanduser('~')
                else:
                        setDownloadPath(inp_path)
                        return inp_path

def getHighestResVid(all_videos):
        ''' Selects the highest resolution video among the available options '''
        
        #This initial value ensures that mp4 filetype is prioritized
        #if multiple highest res vids exist (ie 720p .mp4 and 720p .flv)
        #Else first filetype with highest res
        video_maxRes = filter(lambda x: x.extension=='mp4',all_videos)[-1]

        for vid in all_videos:
                if vid.resolution > video_maxRes.resolution:
                        video_maxRes = vid
        return video_maxRes

def main(url, down_path=getDownloadPath(),start=0,end=-1,overwrite=False):
        #index1 handling has been taken care of. both start and end are index0 here
        
        soup = BeautifulSoup(urlopen(url),"lxml")
        video_links_all = []
        for link in soup.find_all('tr'):
                video_links_all.append("https://www.youtube.com/watch?v="+link.get('data-video-id'))
        if start > len(video_links_all):
                print 'Error: start index out-of-bounds'
                return
        elif end > len(video_links_all):
                print 'Error: end index out-of-bounds'
                return
        
        video_links = video_links_all[:]
        if start != 0:
                if end != -1:
                        video_links = video_links_all[start:end]
                else:
                        video_links = video_links_all[start:]
        elif end != -1:
                video_links = video_links_all[:end]

        #Dynamic filename needed so that multiple .txt(s) can be obtained
        filename = 'LinksList.txt'
        filepath = down_path+filename if (down_path[-1]=="/") else (down_path+"/"+filename)
        print filepath
        links_file = open(filepath,'a')
        
        for link in video_links:
                yt = YouTube(link)
                video = getHighestResVid(yt.get_videos())
                print video.filename
                print "\tDownload in progress..."
                try:
                        video.download(down_path,force_overwrite=overwrite)
                        links_file.write(link+"\n")
                        print "\tDownload is complete!"
                except OSError:
                        response = raw_input("Another file by this name already exists. Force overwrite?[y/n]: ")
                        response = response.lower()
                        if response == "y":
                                video.download(down_path,force_overwrite=True)
                                links_file.write(link+"\n")
                                print "\tDownload is complete!"
                        else:
                                if response != "n":
                                        print "Invalid response"
                                #link not added to file if download skipped
                                print "\tVideo download skipped"

if __name__ == '__main__':
        parser = getArgParser()
        args = parser.parse_args()
        if args.showpath:
                print getDownloadPath()
        else:
                start_index, end_index = 0,-1
                if args.start is not None:
                        # -1 since index1 to index0
                        start_index = args.start - 1
                if args.end is not None:
                        # No modifier since inclusive range end
                        end_index = args.end
                if args.start is not None and args.end is not None:
                        if args.start > args.end:
                                parser.error('start must be less than or equal to end')
                
                if args.setaspath:
                        if args.path == "":
                                parser.error('--path must be given together with --setpath')
                        else:
                                setDownloadPath(args.path)
                                main(args.playlist_url,start=start_index,end=end_index,overwrite=args.f)
                else:
                        if args.path == "":
                                main(args.playlist_url,start=start_index,end=end_index,overwrite=args.f)
                        else:
                                main(args.playlist_url,args.path,start=start_index,end=end_index,overwrite=args.f)
