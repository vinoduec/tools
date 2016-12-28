inputFile=$1
for commit in `cat $inputFile`
do
  echo Looking at $commit;
  git cherry-pick -x $commit;
  if [ "$?" -ne "0" ];
  then
      echo ==== Failed cherry-pick ====
      /opt/local/bin/bash
      read -p "Continue? " -n 1 -r
      echo    # (optional) move to a new line
      if [[ ! $REPLY =~ ^[Yy]$ ]]
      then
        exit 1
      fi 
  fi
  #  git add hadoop-yarn-project/CHANGES.txt ;
  #  git add hadoop-common-project/hadoop-common/CHANGES.txt ;
  #  git add hadoop-hdfs-project/hadoop-hdfs/CHANGES.txt ;
  #  git add hadoop-mapreduce-project/CHANGES.txt ;
  #  git cherry-pick --continue;
  #  if [ "$?" -ne "0" ];
  #  then
  #    echo ==== Failed cherry-pick ====
  #    exit 1
  #  fi
done
