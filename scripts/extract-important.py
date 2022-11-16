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

if __name__ == "__main__":
    assert (len(sys.argv) == 2), "please provide an input json file name"
    json_data = json.load(open(sys.argv[1]))
    
    OUTPUT_DIR = json_data["output_dir"]
    files = json_data["files"] 
    stats = json_data["stats"]

    # reading the json file
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    for stat in stats:
        stat_dir = os.path.join(OUTPUT_DIR, stat)
        os.makedirs(stat_dir)
        for f in files:
            with open(f) as json_file:  
                json_data = json.load(json_file)
            no_infer_data = json_data["no-infer-share"]
            default_data = json_data["default"]
            new_fname = f.replace("/","_")
            csv_file = os.path.join(stat_dir, f"{new_fname}.csv")
            csv_writer = csv.writer(open(csv_file, 'w'))
            header = ['setting'] + list(no_infer_data.keys())
            csv_writer.writerow(header)
            no_infer_row = ["no_infer_share"] + [no_infer_data[d][stat] for d in no_infer_data]
            default_row = ["default"] + [default_data[d][stat] for d in default_data]
            csv_writer.writerow(no_infer_row)
            csv_writer.writerow(default_row)   
            