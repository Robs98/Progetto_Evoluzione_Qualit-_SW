import os
import pandas as pd
import matplotlib.pyplot as plt

CK_PATH = 'D:\Desktop\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'
LOG4J_PROJECT_DIR = './logging-log4j1'
GIT_COMMITS_FILE = 'commits.csv'
OUTPUT_DIR = 'output'

# Moves file from path_from to path_to
def move_file(path_from: str, path_to:str) -> None:
    data = open(path_from, 'r+').read()
    open(path_to, 'w+').write(data)


os.system(f"cd {LOG4J_PROJECT_DIR}  && git log --date=iso --pretty=format:%H,%an,%ad > {GIT_COMMITS_FILE}")
file_data = open(f'{LOG4J_PROJECT_DIR}/{GIT_COMMITS_FILE}', 'r+').read()
open(GIT_COMMITS_FILE, 'w+').write(file_data)

os.system(f"cd {LOG4J_PROJECT_DIR} & git reset --hard")

rows = open(GIT_COMMITS_FILE, 'r+').readlines()

for i in [0,1,26]:
    row = rows[i]
    tokens = row.split(',')
    commit_hash, commit_author, commit_date = tokens
    print(commit_hash)

    # Checkout
    os.system(f"cd {LOG4J_PROJECT_DIR} & git checkout {commit_hash}")

    # Execute CK analysis
    os.system(f'java -jar {CK_PATH} {LOG4J_PROJECT_DIR}')

    for file in ['class.csv']:
        if not os.path.exists(OUTPUT_DIR) or not os.path.isdir(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        move_file(file, os.path.join(OUTPUT_DIR,f'{commit_hash}_{file}'))

# delete pending csv files in root directory
#os.system('del *.csv')