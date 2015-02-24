from ftplib import FTP

ftp = FTP('ftp.drwestfall.net')

ftp.login('ftp03','student')

ftp.retrlines('LIST')

ftp.quit()
