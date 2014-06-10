db.jobinfo_se_top_corps.update( {},
                    { $unset: { num: "" ,  tf :"" } }  ,
                     false, true )
                     
db.jobinfo_se_top_corps.find().sort({"_id":1})

db.job_lang_top_corps.find({jobtitle:"Software Engineer (Cloud/OpenStack - Java)"})


db['daily_job_list_2014-06-10'].aggregate (  { 
                                                $group : { _id: "$state" , totalNum: { $sum : 1 } } 
                                              }  ,
                                            
                                             { 
                                                 $sort : { totalNum: -1  } 
                                              }
                                           )
