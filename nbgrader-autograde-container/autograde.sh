#!/usr/bin/env bash
# Parameter 1: name of the user
# Parameter 2: name of the assessment
# Parameter 3: ID of the instructor user on the host to chown back
cd /home/instructor

echo "user-submission: $(ls -al user-submission)"
#echo "autograded: $(ls -al autograded)"

#ls /home/instructor/autograded/${1}/${2}
#echo "
#mv /home/instructor/autograded/${1}/${2}/* /home/instructor/autograded-docker/${1}/${2}
mkdir /home/instructor/submitted/${1}
echo "cp -R /home/instructor/user-submission/${1}/${2} /home/instructor/submitted/${1}"
cp -R /home/instructor/user-submission/${1}/${2} /home/instructor/submitted/${1}
echo "ls -l /home/instructor/submitted/ 
$(ls -l /home/instructor/submitted/)"

# echo "submitted again: ls -al submitted/user-1 $(ls -al submitted/user-1)"
nbgrader autograde ${2}
# #/bin/bash
echo "ls -al autograded 
$(ls -al autograded)"
echo "autograded-docker 
$(ls -al autograded-docker)"

# rm -r autograded-docker/${1}/${2}
mv -f autograded/${1}/${2}/* autograded-docker/${1}/${2}

