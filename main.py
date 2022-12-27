import os
import pandas as pd
import matplotlib.pyplot as plt

CK_PATH = 'D:\Desktop\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'

# #Log4j
# PROJECT_DIR = './logging-log4j1'
# GIT_COMMITS_FILE = 'commits.csv'
# OUTPUT_DIR = 'output'
#
# #javaWS
# PROJECT_DIR = './Java-WebSocket'
# GIT_COMMITS_FILE = 'commitsWebSocket.csv'
# OUTPUT_DIR = 'output_WS'

#retrofit
PROJECT_DIR = './retrofit'
GIT_COMMITS_FILE = 'commits_retrofit.csv'
OUTPUT_DIR = 'output_retrofit'

# #freemind
# PROJECT_DIR = './freemind-mmx'
# GIT_COMMITS_FILE = 'commits_freemind.csv'
# OUTPUT_DIR = 'output_freemind'


# #apache-dubbo
# PROJECT_DIR = './dubbo-samples'
# GIT_COMMITS_FILE = 'commitsDubbo.csv'
# OUTPUT_DIR = 'output_Dubbo'



# Moves file from path_from to path_to
def move_file(path_from: str, path_to:str) -> None:
    data = open(path_from, 'r+').read()
    open(path_to, 'w+').write(data)


os.system(f"cd {PROJECT_DIR}  && git log --all --grep=release --date=iso --pretty=format:%H,%an,%ad> {GIT_COMMITS_FILE}")
file_data = open(f'{PROJECT_DIR}/{GIT_COMMITS_FILE}', 'r+').read()
open(GIT_COMMITS_FILE, 'w+').write(file_data)
#i commit sono filtrati per release
os.system(f"cd {PROJECT_DIR} & git reset --hard")

rows = open(GIT_COMMITS_FILE, 'r+').readlines()
commitsSelezionati = []
for i in rows:
    #row = rows[i]
    tokens = i.split(',')
    commit_hash, commit_author, commit_date = tokens

    # Checkout
    os.system(f"cd {PROJECT_DIR} & git checkout {commit_hash}")

#TOOL CK

    os.system(f'java -jar {CK_PATH} {PROJECT_DIR}')

    for file in ['class.csv']:
        if not os.path.exists(OUTPUT_DIR) or not os.path.isdir(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        move_file(file, os.path.join(OUTPUT_DIR,f'{commit_hash}_{file}'))

# delete pending csv files in root directory
os.system('del *.csv')
