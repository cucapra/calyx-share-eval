import os
import json
import sys
import csv
import shutil
'''
Once we have generated the resource sharing results, 
you can run this script, with one argument (the output directory)
to get a summary of lut, dsp, register, and mux usage. Currently 
some of this script is hard coded (e.g., the global `files` list)
so I should try to improve it. 
'''

files = ["lenet", "squeeze", "mobile"]

stats = ["lut", "dsp", "registers", "muxes"]

if __name__ == "__main__":
    assert (len(sys.argv) == 2), "please provide an output directory name"

    # reading the json file
    OUTPUR_DIR = sys.argv[1]
    if os.path.exists(OUTPUR_DIR):
        shutil.rmtree(OUTPUR_DIR)
    os.makedirs(OUTPUR_DIR)
    for stat in stats:
        stat_dir = os.path.join(OUTPUR_DIR, stat)
        os.makedirs(stat_dir)
        for f in files:
            with open(f"lenet-squeeze-mobile-results/resource_numbers_{f}.futil.json") as json_file:  
                json_data = json.load(json_file)
            no_infer_data = json_data["no-infer-share"]
            default_data = json_data["default"]
            csv_file = os.path.join(stat_dir, f"{f}.csv")
            csv_writer = csv.writer(open(csv_file, 'w'))
            header = ['setting'] + list(no_infer_data.keys())
            csv_writer.writerow(header)
            no_infer_row = ["no_infer_share"] + [no_infer_data[d][stat] for d in no_infer_data]
            default_row = ["default"] + [default_data[d][stat] for d in default_data]
            csv_writer.writerow(no_infer_row)
            csv_writer.writerow(default_row)   
            