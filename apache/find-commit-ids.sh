inputFile=$1
outputFile=$2
if [ "$inputFile" == "" ]
then
  echo Input File with list of JIRAs absent.
  exit 1
fi
if [ "$outputFile" == "" ]
then
  echo Output File absent.
  exit 1
fi

echo Running git log ..
git log --oneline > /tmp/full-log.txt

> $outputFile
for commit in `cat $inputFile`
do
  fgrep $commit /tmp/full-log.txt >> $outputFile;
done

echo Output created in $outputFile

