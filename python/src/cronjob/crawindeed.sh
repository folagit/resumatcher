datestr=`date +%Y-%m-%d`
logfile="./log/"$datestr"_indeed.log"
#logfile=$datestr"_indeed.log"
echo "craw log to: "$logfile
python cronjob.py > $logfile 2>&1
#echo "test test test " > $logfile
#python raiseexception.py > $logfile 2>&1

 
