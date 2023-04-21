#!/bin/sh

# Downloads files from the server to which the camera uploads the image to the NAS.
# Moves the files to folders that are named by date.
# Deletes the files from the ftp server.

export TEMP_DIR=./temp
export TEMP_FILELIST=filelist.temp
export TEMP_FILELIST_SUCCESSFUL=filelist-successful.temp

# load environment variables:
if [ -f .env ]; then export $(cat .env | xargs); fi
echo "Using environment variables"
echo "  FTP_SERVER=${FTP_SERVER}"
echo "  FTP_DIR=${FTP_DIR}"
echo "  FTP_USER=${FTP_USER}"
if [ -z $FTP_SECRET ]; then echo "  FTP_SECRET="; else echo "  FTP_SECRET=*****"; fi

# create list of all files on the FTP server:
curl --user ${FTP_USER}:${FTP_SECRET} --ftp-ssl --ssl-reqd --ftp-method multicwd -l "ftp://${FTP_SERVER}/${FTP_DIR}/" | grep "^[^\.]" > ${TEMP_FILELIST}

# downloads all files in the list
mkdir -p ${TEMP_DIR}
while read filename
do
    echo "Downloading ftp://${FTP_SERVER}/${FTP_DIR}/${filename} to ${TEMP_DIR}/${filename}"
    curl --user "${FTP_USER}:${FTP_SECRET}" --ftp-ssl --ssl-reqd --ftp-method multicwd --output "${TEMP_DIR}/${filename}" "ftp://${FTP_SERVER}/${FTP_DIR}/${filename}"
done < ${TEMP_FILELIST}

# extracts dates from filenames
file_dates_unique=$(cat ${TEMP_FILELIST} | sed -E 's/^([0-9\-]*)_.*$/\1/' | sort -u)

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
    mv "${TEMP_DIR}/${filename}" "${ARCHIVE_DIR}/${target_dir}/${filename}"
    if [ $? -eq 0 ]
    then
        echo ${filename} >> ${TEMP_FILELIST_SUCCESSFUL}
    else
        echo "ERROR: moving ${TEMP_DIR}/${filename} to ${ARCHIVE_DIR}/${target_dir}/${filename} failed! Please check manually!"
    fi
done < ${TEMP_FILELIST}

# deletes files in list of successful transfers from ftp server
while read filename
do
    echo "Deleting ${FTP_DIR}/${filename} from FTP server"
    curl --user "${FTP_USER}:${FTP_SECRET}" --ftp-ssl --ssl-reqd --ftp-method multicwd "ftp://${FTP_SERVER}/${FTP_DIR}" --quote "DELE /${FTP_DIR}/${filename}" 
done < ${TEMP_FILELIST_SUCCESSFUL}

# delete temporary lists
rm ${TEMP_FILELIST}
rm ${TEMP_FILELIST_SUCCESSFUL}
