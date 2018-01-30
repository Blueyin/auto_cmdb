#!/bin/bash

#Author: yanf
#Description: 


member=($1)
sudo_file="/etc/sudoers"
cp /etc/sudoers /etc/sudoers_bak
#cp /tmp/user/sudoers /etc/sudoers

add_user_key(){
    for user in ${member[@]}
    do
      echo ${user}
      local u_home=/home/$user/
      cd ${u_home}
      echo "ishangzu@${user}"
      su - $user <<EOF
      mkdir ${u_home}.ssh ;
      chmod 700 ${u_home}.ssh;
      cd ${u_home}.ssh  ;
      touch ${u_home}.ssh/authorized_keys ; 
      cat /tmp/user/${user} >> authorized_keys ;
      chmod 400 authorized_keys ;	  
      exit;
EOF
      rm /tmp/user/${user}
    done
}



add_user_key

