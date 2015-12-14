#!/usr/bin/env python3

import re
import os
import shutil

"""
Scan FTP Upload >>> Target1Root/Restomax  containing only Doss 006 folders. FolderName w/o doss 
                >>> Target1Root/RVMSoft   containing only Doss 005 folders. FolderName w/o doss 

Scan ATrier     >>> Target2Root/          containing Doss 006 and 005. FolderName containing the doss  
"""

ftpUploadFolder         = "/home/cdc/source"
ftpUploadTarget1Root    = "/home/cdc/targetFtp"
ftpUploadTarget1_006    = "/"
ftpUploadTarget1_005    = "/"

docFolder               = "/home/cdc/source"
docTarget               = "/home/cdc/targetDoc/"

prefixRestomax = "006"
prefixRVMSoft = "005"

"""
    Array of source and corresponding target folders and prefixes
    
    First dimension is for the FTP Folder
        0 => Source Folder
        1 => Default Restomax prefix
        2 => Corresponding Restomax target folder
        3 => Default RVMSoft prefix
        4 => Corresponding RVMSoft target folder
    
    Second dimension is for the ToSort Folder
        0 => Source Folder
        1 => Default Restomax prefix
        2 => Corresponding Restomax target folder
        3 => Default Restomax prefix (idem for easiness)
        4 => Corresponding Restomax target folder (idem for easiness)
"""
Folders2Scan =  [[ftpUploadFolder,prefixRestomax,ftpUploadTarget1Root+ftpUploadTarget1_006,prefixRVMSoft,ftpUploadTarget1Root+ftpUploadTarget1_005],
                 [docFolder,prefixRestomax,docTarget,prefixRestomax,docTarget]]

""" 
    Function will extract doss,cmaxnum from a filename str
    Args:
        str (string): The filename.
    Returns:
        (doss,cmaxnum) if successful, None otherwise.
"""
def parse_filename(stri,defPrefix):
    r = re.search('('+prefixRVMSoft+'|'+prefixRestomax+')(.)*[0-9]{6,6}', stri)
    
    if r:
        s = r.group(0)
        r = re.search(prefixRVMSoft, s)
        doss = prefixRVMSoft if r else prefixRestomax
        r = re.search('[0-9]{6,6}', s)
        if r:
            cmaxnum = r.group(0) 
            result = (doss,cmaxnum)
            return result
    else:
        r = re.search('[0-9]{6,6}', stri)
        if r:
            cmaxnum = r.group(0) 
            result = (defPrefix,cmaxnum)
            return result

""" 
    Function will search existing folder to move file in
    Args:
        gFullFileName (string): Full file name.
        fres (array) result of parse source file in parse_filename() function
        defPrefix (string) result of default prefix (005 or 006) find in search_and_move() method
        target (string) target find in search_and_move() method
    Returns:
        result of move files.
"""
def move_file_in_known_folder(gFullFileName,fres,defPrefix,target):
    for d in filter(os.path.isfdir, os.listdir(target)):
        dres = parse_filename(d,defPrefix)
        if not dres:
            continue       
        if (dres[0]==fres[0] and dres[1]==fres[1]):
            shutil.move(gFullFileName,target+"/"+d)
            return d
    print (d + ' not found')
    
"""
    Method will search files in source folders and move it if possible
    Args:
        sourceFolder (string): find in array Folders2Scan.
"""
def search_and_move(sourceFolder):

    for gFile in filter(os.path.isfile, os.listdir(sourceFolder[0])):
        
        fres = parse_filename(gFile,prefixRestomax)
        
        if not fres:
            continue
        
        defPrefix = sourceFolder[1] if fres[0]==prefixRestomax else sourceFolder[3]
        target  = sourceFolder[2] if fres[0]==prefixRestomax else sourceFolder[4]
        move_file_in_known_folder(sourceFolder[0] + "/" + gFile,fres,defPrefix,target)


#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Start sort files
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

for d in Folders2Scan:
    search_and_move(d)
    
    
    
    
