 #!/bin/bash
    
 # Remove all tracks from cmus library without deleting any
 # files from the disk.
 cmus-remote -C clear
    
 # Scans the specified directories and adds contained music
 # files to the cmus library.
 cmus-remote -C "add /mnt/data/Music/"
    
 # Forces a full rescan of the entire library, refreshing 
 # metadata and checking for changes in the files.
 cmus-remote -C "update-cache -f"
