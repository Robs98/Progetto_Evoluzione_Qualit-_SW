import csv
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import self as self

print("Dati Metriche")


#LOG4J
COMMITS_FILE = 'commits.csv'
LOG4J_PROJECT_DIR = "./logging-log4j1"
DIFFERENZE_FILE = './logging-log4j1/differenze.txt'

#DUMBO
DUBBO_PROJECT_DIR = './dubbo-samples'
GIT_COMMITS_FILE_DUBBO = 'commitsDubbo.csv'
DIFFERENZE_FILE_DUMBO = './dubbo-samples/differenzeDumbo.txt'













# path = r'D:\Desktop\downloader\output'                     # use your path
# all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent
#
# df_from_each_file = (pd.read_csv(f) for f in all_files)
# concatenated_df = pd.concat(df_from_each_file, ignore_index=True)




def aggiuntaClasse(class_name):
    dfs = []
    for filename in os.scandir("D:\Desktop\downloader\output"):
        if filename.is_file():
            # il filename viene restituito come <DirEntry 'class417540963a54e5faa4a11378ee87153a1984dc06.csv'>
            # è necessario estrapolare il filename dalla stringa con il .name
            filename_string = os.path.basename(filename)

            df = pd.read_csv("D:\Desktop\downloader\output" + '\\' + filename_string, index_col=False)

            dframe = df[df['class'] == str(class_name)]
            if dframe is not None:
                # inserisco nella prima colonna il numero del committ (per iterare), es 92 commit, va da 0 a 91
                # seconda colonna:commit id
                dfs.append(dframe)  # raccolta dei vari dataframe contenenti ognuno una riga di ogni csv
        final_dataframe = pd.concat(dfs)
    return final_dataframe










def grafico_metriche_CK(rigaClassiCommit,metrica,classe):
    x = np.arange(0,len(rigaClassiCommit.index))
    y = np.array(rigaClassiCommit[metrica])
    # ridimensioniamo l'immagine
    plt.figure(figsize=(100, 100))
    # impostiamo i ticks
    #plt.xticks(x)
    plt.yticks(y)
    # assegniamo etichette agli assi
    plt.xlabel("#commits")
    plt.ylabel("Valori del " + metrica)
    # impostiamo il titolo del grafico
    plt.title("Andamento delle metriche nei vari commits per la classe " + classe)
    # chiediamo di visualizzare la griglia
    plt.grid()
    # disegniamo due linee
    plt.plot(x, y)
    plt.axhline(y=y.mean(), c='r', linestyle='--')
    plt.show()
classi = ["org.apache.log4j.net.SocketAppender","org.apache.log4j.PatternLayout","org.apache.log4j.helpers.PatternParser"]
metriche = ['cbo','dit','fanin','fanout','wmc','lcom','rfc']
for classe in classi:
    for metrica in metriche:
        grafico_metriche_CK(aggiuntaClasse(classe),metrica,classe)





def estrazioniClassiDaCommit(commits_csv):
    rows = open(commits_csv, 'r+').readlines()
    for i in rows:
        # row = rows[i]
        tokens = i.split(',')
        commit_hash, commit_author, commit_date = tokens
        if(commit_date<="2000-12-19 13:59:21 +0000"):
            first_commit_hash = {commit_hash}.pop()
            print(first_commit_hash)
        if (commit_date >= "2012-05-06 10:59:21 +0000"):
            last_commit_hash = {commit_hash}.pop()
            print(last_commit_hash)

    os.system(f"cd {LOG4J_PROJECT_DIR}  && git diff --numstat {first_commit_hash}..{last_commit_hash}> differenze.txt")
    read_file = pd.read_csv (r'./logging-log4j1/differenze.txt', delimiter='|')
    read_file.to_csv (r'differenze.csv',index=None)
    rows = open('differenze.csv', 'r+').readlines()
    listaClassi = []
    for i in rows:
        # row = rows[i]
        tokens = i.split('\t')
        added, deleted, classes = tokens
        if added != '-':
            if int(added)>100 and int(deleted)>100:
                 listaClassi.append(classes)
    return listaClassi


print(estrazioniClassiDaCommit(COMMITS_FILE))