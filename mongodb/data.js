db.jobinfo_se_top_corps.update( {},
                    { $unset: { num: "" ,  tf :"" } }  ,
                     false, true )
                     
db.jobinfo_se_top_corps.find().sort({"_id":1})