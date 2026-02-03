import utils, TL, TL_Workflow
from datetime import datetime, timedelta

c=0
# API delay set to 3 secs
# epoch from, epoch to, number of connections to be created
for epoch in utils.randomize_epoch(1711909800000, 1730399400000, 50):
    c= c+1
    # data = TL.NewTL_mod("createdTime", epoch)
    # tenants ca.emeryville, ca.berkeley, ca.alameda
    data = TL_Workflow.NewTL_mod_tenant("", epoch, "ke.nakuru")
    print(c, "TL: ", data, " : createdTime: ", datetime.fromtimestamp(epoch / 1000))
    

# for epoch in utils.randomize_epoch(1711909800000, 1730399400000, 10):
#     print(datetime.fromtimestamp(epoch / 1000))