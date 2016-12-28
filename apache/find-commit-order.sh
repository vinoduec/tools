#!/bin/bash
inputFile=$1
if [ "$inputFile" == "" ]
then
  >&2 echo Input File with list of JIRAs absent.
  exit 1
fi

>&2 echo Running git log ..
tmpFile=/tmp/full-log.txt
git log --oneline > $tmpFile

numJIRAsToLook=`wc -l $inputFile`
currentJIRAsFound=0

IFS=$'\r\n' GLOBIGNORE='*' :;
jiras=($(cat $inputFile))

numJIRAsToLook=${#jiras[@]}
>&2 echo $numJIRAsToLook

for commit in `cat $tmpFile`
do
  for i in "${jiras[@]}"
  do
    #if [ $currentJIRAsFound -eq $numJIRAsToLook ]
    #then
    #  exit 0
    #fi

    if [[ "$commit" =~ "$i" ]]
    then
      currentJIRAsFound=$((currentJIRAsFound+1))
      echo $commit
    fi
  done
done

#echo -n "Found JIRAs: "
#printf '%s\n' "${currentJIRAsFound[@]}"

rm $tmpFile
