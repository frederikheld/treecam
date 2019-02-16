# using curl:
#curl --upload-file /home/tc/treecam/pictures/picam.jpg ftp://treecam.frederikheld.de/
# curl does not support --ftp-ssl in piCore. Therefore ftps connections are not possible. curl should therefore not be used!

# using lftp:
lftp << EOF
set ssl:verify-certificate/treecam.frederikheld.de off
open treecam.frederikheld.de
lcd /home/tc/treecam/pictures
put picam.jpg
bye
EOF

# curl and lftp both look into /home/<user>/.netrc for credentials
