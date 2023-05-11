#!/bin/sh

# Downloads files from the server ftp server that was
# specified with the env variables
#       - FTP_SERVER
#       - FTP_DIR
#       - FTP_USER
#       - FTP_SECRET
# Moves the files to folders that are named by date within
# the directory given with the env variable
#       - ARCHIVE_DIR
# Deletes the files from the ftp server (only those that
# were successfully downloaded and moved)
# During the whole process it uses
#       - TEMP_DOWNLOAD_DIR
#       - TEMP_FILELIST
#       - TEMP_FILELIST_SUCCESSFUL
# to keep track of handled files.


# load environment variables:
if [ -f .env ]; then export $(cat .env | xargs); fi
echo "Using environment variables"
echo "  FTP_SERVER=${FTP_SERVER}"
echo "  FTP_DIR=${FTP_DIR}"
echo "  FTP_USER=${FTP_USER}"
if [ -z $FTP_SECRET ]; then echo "  FTP_SECRET="; else echo "  FTP_SECRET=*****"; fi

# create list of all files that are currently on the FTP server:
curl --user ${FTP_USER}:${FTP_SECRET} --ftp-ssl --ssl-reqd --ftp-method multicwd -l "ftp://${FTP_SERVER}/${FTP_DIR}/" | grep "^[^\.]" > ${TEMP_FILELIST}

# DEBUG: remove all but 3 lines:
# sed -i '4,$ d' ${TEMP_FILELIST}

# download all files in the list:
mkdir ${TEMP_DOWNLOAD_DIR}
while read filename
do
    echo "Downloading ftp://${FTP_SERVER}/${FTP_DIR}/${filename} to ${TEMP_DOWNLOAD_DIR}/${filename}"
    curl --user "${FTP_USER}:${FTP_SECRET}" --ftp-ssl --ssl-reqd --ftp-method multicwd --output "${TEMP_DOWNLOAD_DIR}/${filename}" "ftp://${FTP_SERVER}/${FTP_DIR}/${filename}"
done < ${TEMP_FILELIST}

# extracts dates from filenames
file_dates_unique=$(cat ${TEMP_FILELIST} | sed -E 's/^([0-9\-]*)_.*$/\1/' | sort -u)

# DEBUG: print dates:
# echo "unique dates: ${file_dates_unique}"

# CONTINUE: make sure, that the /out directory and the $ARCHIVE_DIR match

# creates folders for each date (if not exist)
echo "${file_dates_unique}" | {
    while read -r dirname
    do
        mkdir -p "${ARCHIVE_DIR}/${dirname}"
    done
}

# moves files to the respective folder (matching date pattern)
# store successful transfers in temporary file
while read filename
do
    target_dir=$(echo "${filename}" | sed -E 's/^([0-9\-]*)_.*$/\1/')
    mv "${TEMP_DOWNLOAD_DIR}/${filename}" "${ARCHIVE_DIR}/${target_dir}/${filename}"
    if [ $? -eq 0 ]
    then
        echo ${filename} >> ${TEMP_FILELIST_SUCCESSFUL}
    else
        echo "ERROR: moving ${TEMP_DOWNLOAD_DIR}/${filename} to ${ARCHIVE_DIR}/${target_dir}/${filename} failed! Please check manually!"
    fi
done < ${TEMP_FILELIST}

# deletes files in list of successful transfers from ftp server
while read filename
do
    echo "Deleting ${FTP_DIR}/${filename} from FTP server"
    curl --user "${FTP_USER}:${FTP_SECRET}" --silent --show-error --ftp-ssl --ssl-reqd --ftp-method multicwd --quote "DELE ${FTP_DIR}/${filename}" ftp://${FTP_SERVER}/${FTP_DIR}/ > /dev/null
done < ${TEMP_FILELIST_SUCCESSFUL}

# delete temporary lists
rm ${TEMP_FILELIST}
rm ${TEMP_FILELIST_SUCCESSFUL}
