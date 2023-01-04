import csv
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import self as self

print("Dati Metriche")


CK_PATH = 'D:\Desktop\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'


PROJECT_DIR = './commons-dbutils'
GIT_COMMITS_FILE = './commons-dbutils/commits_commons.csv'
OUTPUT_DIR = 'output_commons'




#lista i file in ordine di modifca
def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime,reverse=True))



def aggiuntaClasse(class_name):
    dfs = []
    files = sorted_ls("D:\Desktop\downloader\output_commons")
    for filename in files:
        filename_string = os.path.basename(filename)
        print(filename_string)
        df = pd.read_csv("D:\Desktop\downloader\output_commons" + '\\' + filename_string, index_col=False)

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
    plt.ylabel("Valore " + metrica)
    # impostiamo il titolo del grafico
    plt.title("Andamento delle metriche nei vari commits per la classe " + classe)
    # chiediamo di visualizzare la griglia
    plt.grid()
    # disegniamo due linee
    plt.plot(x, y)
    plt.axhline(y=y.mean(), c='r', linestyle='--')
    plt.show()
classi = ["org.apache.commons.dbutils.wrappers.SqlNullCheckedResultSet","org.apache.commons.dbutils.BaseTestCase","org.apache.commons.dbutils.wrappers.SqlNullCheckedResultSetTest"]
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
        if(commit_date<="2007-07-29 03:42:34 +0000"):
            first_commit_hash = {commit_hash}.pop()
            print(first_commit_hash)
        if (commit_date >= "2020-01-08 22:14:42 -0800"):
            last_commit_hash = {commit_hash}.pop()
            print(last_commit_hash)

    os.system(f"cd {PROJECT_DIR}  && git diff --numstat {first_commit_hash}..{last_commit_hash}> differenzeCommons.txt")
    read_file = pd.read_csv (r'./commons-dbutils/differenzeCommons.txt', delimiter='|')
    read_file.to_csv (r'differenzeCommons.csv',index=None)
    rows = open('differenzeCommons.csv', 'r+').readlines()
    listaClassi = []
    for i in rows:
        # row = rows[i]
        tokens = i.split('\t')
        added, deleted, classes = tokens
        if added != '-':
            if int(added)>100 and int(deleted)>100:
                 listaClassi.append(classes)
    return listaClassi


print(estrazioniClassiDaCommit(GIT_COMMITS_FILE))


def graficoModificheClassi():

    x = np.array([3, 130])
    label = ['Classi Modificate (>100LOC)','Classi modificate (<100 LOC)']
    explode = [0, 0.2]
    fig, ax = plt.subplots()
    ax.pie(x, labels=label, autopct='%.0f%%', explode = explode)
    ax.set_title('CommondDB project-Modifiche classi')
    plt.show()
print(graficoModificheClassi())

def matriceDiCorrelazione(GIT_COMMITS_FILE):
    dfs = []
    rows = open(GIT_COMMITS_FILE, 'r+').readlines()
    for i in rows:
        # row = rows[i]
        tokens = i.split(',')
        commit_hash, commit_author, commit_date = tokens

        # Checkout
        os.system(f"cd {PROJECT_DIR} & git checkout {commit_hash}")

        # TOOL CK
        os.system(f'java -jar {CK_PATH} {PROJECT_DIR}')
        file = pd.read_csv('class.csv',usecols = ['cbo','dit','fanin','fanout','wmc','rfc','lcom'])
        dfs.append(file)
    final_dataframe = pd.concat(dfs)
    rounded_corr_matrix = final_dataframe.corr().round(2)

    plt.figure(figsize=(8, 6))
    sns.heatmap(rounded_corr_matrix, annot=True)
    plt.show()

matriceDiCorrelazione(GIT_COMMITS_FILE_DUBBO)