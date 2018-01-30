#!/bin/bash


member=($1)
sudo_file="/etc/sudoers"

add_user_key(){
    for user in ${member[@]}
    do
      local u_home=/home/$user/
      echo "ishangzu@${user}"|passwd --stdin $user
      su - $user <<EOF
      mkdir ${u_home}/.ssh ;
      chmod 700 ${u_home}/.ssh;
      cd ${u_home}/.ssh  ;
      touch ${u_home}/.ssh/authorized_keys ; 
      cat /tmp/${member} >> authorized_keys ;
      chmod 400 authorized_keys ;	  
      exit;
EOF
    done
}



add_user_key

