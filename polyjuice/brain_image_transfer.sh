#!/bin/bash

source logininfo.bash
echo $PASSWORD
echo $USERNAME
echo $SERVERADDY
echo $INTSOURCE
#Use
#   Uploads zipped brain images-PET and MRI- to respective folders in
#   NACC
#
#
#ENVIRONMENTAL VARIABLES
#   USERNAME    => is the UF username used to connect to tools2 server
#   PASSWORD    => is the credentials needed to connect to tools2 and 
#                  other UF servers
#   SERVERADDY  => is the IP address used to connect directly to NACC
#   SERVERPW    => the key needed to sftp into the NACC
#   IMAGESOURCE => the shared drive directory containing all PET and MRI
#                  zipped files (after running polyjuice)
#   INTSOURCE => the server whose IP address is accepted by NACC standards
#

#echo sftp -o ProxyCommand="'ssh $USERNAME@$INTSOURCE nc -w 10 %h %p'" $SERVERADDY 
#sftp -o ProxyCommand='ssh $USERNAME@$INTSOURCE nc -w 10 %h %p' $SERVERADDY 

pwd
cd ~/Desktop/
scp -r $IMAGESOURCE $USERNAME@$INTSOURCE:/tmp/ 

expect <<EOS 
spawn ssh $USERNAME@$INTSOURCE 
expect "$USERNAME@$INTSOURCE's password:"
send "$PASSWORD\n"

expect "$USERNAME@tools2:~$"
send "cd /tmp/\n"

send "sftp $SERVERADDY\n"
expect "Password:"
send "$SERVERPW\n"

expect "sftp>"
send "cd PET\n"

expect "sftp>"
send "put *"

expect "sftp>"
send "lcd ../MRI/\n"

expect "sftp>"
send "put *\n"

expect "sftp>"
send "bye\n"
EOS

