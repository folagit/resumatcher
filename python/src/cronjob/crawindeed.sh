datestr=`date +%Y-%m-%d`
logfile="./log/"$datestr"_indeed.log"
#logfile=$datestr"_indeed.log"
echo "craw log to: "$logfile
python cronjob.py &> $logfile
 
