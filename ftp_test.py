


import ftplib
import progressbar
import sys


def get_data(filename):

    filename = filename
    path = 'vdelivery/Datasets/Staged/Elevation/13/IMG/{}.zip'.format(filename)
    ftp = ftplib.FTP('rockyftp.cr.usgs.gov')
    ftp.login()
    ftp.voidcmd('TYPE I')
    try:
        filesize = ftp.size(path)
        print filesize
        progress = progressbar.AnimatedProgressBar(end=filesize, width=50)
        with open(filename + '.zip', 'wb') as f:
            def callback(chunk):
                f.write(chunk)
                progress + len(chunk)
                progress.show_progress()
                sys.stdout.flush()
            ftp.retrbinary('RETR ' + path, callback)
    except:
        print "FTP error"
        pass