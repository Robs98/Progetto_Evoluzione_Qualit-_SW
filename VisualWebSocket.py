import csv
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import self as self

print("Dati Metriche")




WEBSOCKET_PROJECT_DIR = './Java-WebSocket'
GIT_COMMITS_FILE_WS = './Java-WebSocket/commitsWebSocket.csv'
DIFFERENZE_FILE_WS= './Java-WebSocket/differenzeWS.txt'












# path = r'D:\Desktop\downloader\output'                     # use your path
# all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent
#
# df_from_each_file = (pd.read_csv(f) for f in all_files)
# concatenated_df = pd.concat(df_from_each_file, ignore_index=True)




#lista i file in ordine di modifca
def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))



def aggiuntaClasse(class_name):
    dfs = []
    files = sorted_ls("D:\Desktop\downloader\output_WS")
    for filename in files:
        filename_string = os.path.basename(filename)
        print(filename_string)
        df = pd.read_csv("D:\Desktop\downloader\output_WS" + '\\' + filename_string, index_col=False)

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
classi = ["org.java_websocket.drafts.Draft_6455","org.java_websocket.server.WebSocketServer","org.java_websocket.autobahn.AutobahnServerResultsTest"]
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
        if(commit_date<="2010-07-24 12:20:50 -0700"):
            first_commit_hash = {commit_hash}.pop()
            print(first_commit_hash)
        if (commit_date >= "2022-01-02 14:23:38 +0200"):
            last_commit_hash = {commit_hash}.pop()
            print(last_commit_hash)

    os.system(f"cd {WEBSOCKET_PROJECT_DIR}  && git diff --numstat {first_commit_hash}..{last_commit_hash}> differenzeWS.txt")
    read_file = pd.read_csv (r'./Java-WebSocket/differenzeWS.txt', delimiter='|')
    read_file.to_csv (r'differenzeWS.csv',index=None)
    rows = open('differenzeWS.csv', 'r+').readlines()
    listaClassi = []
    for i in rows:
        # row = rows[i]
        tokens = i.split('\t')
        added, deleted, classes = tokens
        if added != '-':
            if int(added)>1100:
                 listaClassi.append(classes)
    return listaClassi


print(estrazioniClassiDaCommit(GIT_COMMITS_FILE_WS))


def graficoModificheClassi():

    x = np.array([3, 260])
    label = ['Classi Modificate (>1100 LOC)','Classi modificate (<1100 LOC)']
    explode = [0, 0.2]
    fig, ax = plt.subplots()
    ax.pie(x, labels=label, autopct='%.0f%%', explode = explode)
    ax.set_title('Java WebSocket project-Modifiche classi')
    plt.show()
print(graficoModificheClassi())
