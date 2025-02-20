import os
import argparse
import pandas as pd
import numpy as np
import cv2

'''
The query functionality facilitates access to metadata about the failure catalog and its artifacts. 
This functionality provides total samples, size on disk, and duration of the failure in seconds as well as a count of failures per model and summed trace attributes for all failures per model. 
query also provides organized metadata about the training of each model in the catalog.
query takes optional flags -hmft. 
-h, --help prints usage help. 
-m, --model specifies the model of interest, in the form M#.
-f, --failure specifies the failure of interest, in the form F# or F#,F#,... if querying several failures within the same model.
Leaving -f blank queries all failures for the specified model.
Leaving both -m and -f blank queries the entire catalog.
Training metadata is accessed via the -t, --training_metas boolean flag.
'''


def parse_arguments():
    parser = argparse.ArgumentParser(prog='query',
                    description='The query functionality facilitates access to metadata about the failure catalog and its artifacts. This functionality provides the information in column 3 of Table~\ref{tab:examplefailures} as well as a count of failures per model and summed trace attributes for all failures per model.',
                    epilog='Text at the bottom of help')
    parser.add_argument('-m', "--model", type=str, help='model ID')
    parser.add_argument('-f', "--failure", type=str, help='failure ID')
    parser.add_argument('-t', "--training_metas", action="store_true", help='outputs training metadata for the specified model by the -m, --model flag')
    parser.add_argument('-o', "--outdir", type=str, default="query-output/", help='directory in which to save output')
    parser.add_argument("--save", action="store_true")
    # parser.add_argument("--resize", type=str, default=None)
    args = parser.parse_args()
    return args


def randstr():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def timestr():
    localtime = time.localtime()
    return "{}_{}-{}_{}".format(localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min)

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size # in bytes

def main(args):
    d = f"../failure-catalog/{args.model}/"
    if args.failure:
        f = args.failure.split(",")
        tracedirs = [d+i+"/" for i in f]
    else:
        tracedirs = [d + i for i in os.listdir(d) if os.path.isdir(d+i)]
    # print(tracedirs)
    tracedict = dict.fromkeys(tracedirs, {'size': 0, "time": 0.0, "samples": 0})
    for td in tracedirs:
        tracedict[td]["size"] = get_size(td)
        tracedict[td]["samples"] = sum([1 for i in os.listdir(td) if ".jpg" in i])
        tracedict[td]["time"] = tracedict[td]["samples"] / 5.0
    for td in tracedirs:
        print(td)
        print("\tSize on disk:", tracedict[td]["size"] / 1048576.0, "MB")
        print("\tTime elapsed:", tracedict[td]["time"], "seconds")
        print("\tTotal samples:", tracedict[td]["samples"])
    if args.training_metas:
        modelsubdir = ["../pretrained-models/" + i for i in os.listdir("../pretrained-models") if args.model+"-" in i][0]
        modeldir = f"../pretrained-models/{args.model}/"
        a = [modeldir+ i for i in os.listdir(modeldir) if "metainfo.txt" in i][0]
        print(f"{i} training metas:\n{a}")
    


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
