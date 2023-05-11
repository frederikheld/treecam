#!/bin/sh
ARCHIVE_DIR=${ARCHIVE_DIR:="/out"}

echo "Hello World!"

# curl -X POST -H 'Content-Type: application/json' -d "{\"ftp_server\": \"$FTP_SERVER\", \"FTP_DIR\": \"$FTP_DIR\"}" https://www.toptal.com/developers/postbin/1682028471103-4443627598229

echo "FTP_SERVER: $FTP_SERVER"
echo "FTP_DIR: $FTP_DIR"
echo "FTP_USER: $FTP_USER"
echo "ARCHIVE_DIR: $ARCHIVE_DIR"

# touch /out/debug.txt
# echo "FTP_SERVER: $FTP_SERVER" >> /out/debug.txt
# echo "FTP_DIR: $FTP_DIR" >> /out/debug.txt
# echo "FTP_USER: $FTP_USER" >> /out/debug.txt
# echo "ARCHIVE_DIR: $ARCHIVE_DIR" >> /out/debug.txt
