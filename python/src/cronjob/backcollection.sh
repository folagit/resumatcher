

if [[ -z "$1" ]]
  then
    echo "you should give a formated date like: 2014-06-17"
    exit
fi

datestr=$1

LIST_COLL_NAME="daily_job_list_"$datestr
INFO_COLL_NAME="daily_job_info_"$datestr
echo "job list collection name is: "$LIST_COLL_NAME
echo "job info collection name is: "$INFO_COLL_NAME
mongoexport -d jobaly_daily -c $LIST_COLL_NAME -o ./data/$LIST_COLL_NAME.json  
mongoexport -d jobaly_daily -c $INFO_COLL_NAME -o ./data/$INFO_COLL_NAME.json  

#tar -cvzf ./data/$LIST_COLL_NAME.tar.gz  ./data/$LIST_COLL_NAME.json --remove-files
#tar -cvzf ./data/$INFO_COLL_NAME.tar.gz  ./data/$INFO_COLL_NAME.json --remove-files

tar -cvzf ./data/$LIST_COLL_NAME.tar.gz  ./data/$LIST_COLL_NAME.json  
tar -cvzf ./data/$INFO_COLL_NAME.tar.gz  ./data/$INFO_COLL_NAME.json  

mv ./data/$LIST_COLL_NAME.tar.gz    /home/frank/Dropbox/jobaly_daily
mv ./data/$INFO_COLL_NAME.tar.gz    /home/frank/Dropbox/jobaly_daily
echo "cron job completed"
