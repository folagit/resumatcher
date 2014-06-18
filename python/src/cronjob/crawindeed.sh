datestr=`date +%Y-%m-%d`
logfile="./log/"$datestr"_indeed.log"
LIST_COLL_NAME="daily_job_list_"$datestr
INFO_COLL_NAME="daily_job_info_"$datestr
#logfile=$datestr"_indeed.log"
echo "craw log to: "$logfile


#python cronjob.py
python cronjob.py > $logfile 2>&1

exec 1>> $logfile
exec 2>> $logfile
echo "python result is:"$?
#echo "test test test " > $logfile
#python raiseexception.py > $logfile 2>&1

mongoexport -d jobaly_daily -c $LIST_COLL_NAME -o ./data/$LIST_COLL_NAME.json  
mongoexport -d jobaly_daily -c $INFO_COLL_NAME -o ./data/$INFO_COLL_NAME.json  

#tar -cvzf ./data/$LIST_COLL_NAME.tar.gz  ./data/$LIST_COLL_NAME.json --remove-files
#tar -cvzf ./data/$INFO_COLL_NAME.tar.gz  ./data/$INFO_COLL_NAME.json --remove-files

tar -cvzf ./data/$LIST_COLL_NAME.tar.gz  ./data/$LIST_COLL_NAME.json  
tar -cvzf ./data/$INFO_COLL_NAME.tar.gz  ./data/$INFO_COLL_NAME.json  

mv ./data/$LIST_COLL_NAME.tar.gz    /home/frank/Dropbox/jobaly_daily
mv ./data/$INFO_COLL_NAME.tar.gz    /home/frank/Dropbox/jobaly_daily
echo "cron job completed"
