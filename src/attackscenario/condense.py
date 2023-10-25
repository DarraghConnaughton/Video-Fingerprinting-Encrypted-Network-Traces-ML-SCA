from glob import glob
import sys
import pandas as pd

file_list = glob("./new_data/5_per_second/*.pd")

condense = []

for pfile in file_list:
    print(pfile)
    tmp = pd.read_pickle(pfile)
    
    try: 
        data = {
            "timestamp": [list(tmp["timestamps"].values)],
            "data": [list(tmp["rtts"].values)],
            "video_id": tmp["video_id"]
        }
        condense.append(pd.DataFrame(data))
    except Exception as ex: # applies if tmp is not a single record
        print(f"Exception encountered: {ex}")
   
print(f"[+]condense {condense}")

return_dframe = pd.concat(condense, ignore_index=True)
return_dframe.to_pickle(
    "./5_per_second_super_duper_frame.pd",
    compression="infer",
    protocol=4,
    storage_options=None,
)