import os
import pandas as pd
import matplotlib.pyplot as plt

CK_PATH = 'D:\Desktop\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'

#log4j
LOG4J_PROJECT_DIR = './logging-log4j1'
GIT_COMMITS_FILE_LOG4j = 'commits.csv'
OUTPUT_DIR_LOG4j = 'output'

#javaWS
WEBSOCKET_PROJECT_DIR = './Java-WebSocket'
GIT_COMMITS_FILE_WS = 'commitsWebSocket.csv'
OUTPUT_DIR_WS = 'output_WS'

#apache-dubbo
DUBBO_PROJECT_DIR = './dubbo-samples'
GIT_COMMITS_FILE_DUBBO = 'commitsDubbo.csv'
OUTPUT_DIR_DUBBO = 'output_Dubbo'



# Moves file from path_from to path_to
def move_file(path_from: str, path_to:str) -> None:
    data = open(path_from, 'r+').read()
    open(path_to, 'w+').write(data)


os.system(f"cd {WEBSOCKET_PROJECT_DIR}  && git log --tags --simplify-by-decoration --date=iso --pretty=format:%H,%an,%ad> {GIT_COMMITS_FILE_WS}")
file_data = open(f'{WEBSOCKET_PROJECT_DIR}/{GIT_COMMITS_FILE_WS}', 'r+').read()
open(GIT_COMMITS_FILE_WS, 'w+').write(file_data)
#i commit sono filtrati per release
os.system(f"cd {WEBSOCKET_PROJECT_DIR} & git reset --hard")

rows = open(GIT_COMMITS_FILE_WS, 'r+').readlines()
commitsSelezionati = []
for i in rows:
    #row = rows[i]
    tokens = i.split(',')
    commit_hash, commit_author, commit_date = tokens

    # Checkout
    os.system(f"cd {WEBSOCKET_PROJECT_DIR} & git checkout {commit_hash}")

#TOOL CK

    os.system(f'java -jar {CK_PATH} {WEBSOCKET_PROJECT_DIR}')

    for file in ['class.csv']:
        if not os.path.exists(OUTPUT_DIR_WS) or not os.path.isdir(OUTPUT_DIR_WS):
            os.makedirs(OUTPUT_DIR_WS)
        move_file(file, os.path.join(OUTPUT_DIR_WS,f'{commit_hash}_{file}'))

# delete pending csv files in root directory
#os.system('del *.csv')
