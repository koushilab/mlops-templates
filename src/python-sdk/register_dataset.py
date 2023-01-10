# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse
from azureml.core import Workspace, Dataset

def parse_args():
    parser = argparse.ArgumentParser(description="Register dataset")
    parser.add_argument("-n", type=str, help="Name of the dataset you want to register")
    parser.add_argument("-d", type=str, help="Description of the dataset you want to register")
    parser.add_argument("-t", type=str, help="type of dataset", default='local')    
    parser.add_argument("-l", type=str, help="local path of the dataset folder", default='data/training/')
    parser.add_argument("-p", type=str, help="Path on data store", default='dogs-labels/')
    parser.add_argument("-s", type=str, help="Storage url for cloud storage")
    return parser.parse_args()

def main():
    args = parse_args()
    print(args)
    ws = Workspace.from_config()
    if args.t == "local":
        print("local data")
        print(f'Name of the dataset {args.n}')
        print(f'Description of the dataset {args.d}')
        print(f'Type of the dataset {args.t}')
        print(f'Localpath of the dataset {args.l}')
        print(f'DataStorePath of the dataset {args.p}')
        print(f'Storageurl of the dataset {args.s}')
        datastore = ws.get_default_datastore()
        print("Testing by Koushi")
        Dataset.File.upload_directory(src_dir = args.l, target = (datastore, args.p), overwrite = True, show_progress = True)
        print(f"About to register dataset {args.n}")

        dataset = Dataset.File.from_files(path=[(datastore, args.p)], validate=True)
        dataset = dataset.register(workspace=ws,name=args.n, description=args.d,create_new_version=True)
        print("Dataset registered")
    else:
        print("cloud data")
        data_urls = [args.s]
        dataset = Dataset.File.from_files(data_urls)
        dataset = dataset.register(workspace=ws,name=args.n, description=args.d,create_new_version=True)
    

if __name__ == "__main__":
    main()
