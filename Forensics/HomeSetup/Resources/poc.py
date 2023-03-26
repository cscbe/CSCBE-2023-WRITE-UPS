import time  
import sys  
import shutil  
import subprocess  
import os  
import dpkt  

if len(sys.argv) < 2:  
    print("argument required!" )
    print("txpcap <pcap file>" )
    sys.exit(2)  
pcap_full_path = sys.argv[1]  

ffmp_cmd = ['ffmpeg','-loglevel','debug','-y','-i','109c.sdp','-f','rtp','-i','-','-na','-vcodec','copy','p.mp4']  

ffmpeg_proc = subprocess.Popen(ffmp_cmd,stdout = subprocess.PIPE,stdin = subprocess.PIPE)  

with open(pcap_full_path, "rb") as pcap_file:  
    pcapReader = dpkt.pcap.Reader(pcap_file)  
    for ts, data in pcapReader:  
        if len(data) < 49:  
            continue  
        ffmpeg_proc.stdin.write(data[42:])

sout, err = ffmpeg_proc.communicate()  
print ("stdout ---------------------------------------"  )
print (sout  )
print ("stderr ---------------------------------------"  )
print (err  )