import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

print("Dati Metriche")

PROJECT_DIR = 'C:\\Users\\franc\\PycharmProjects\\EvoluzioneQualitaSW\\dubbo-samples'
GIT_COMMITS_FILE = 'C:\\Users\\franc\\PycharmProjects\\EvoluzioneQualitaSW\\dubbo-samples\\commitsDubbo.csv'
OUTPUT_DIR = 'output_dubbo'


def sorted_ls(path):

    """
        Ordinamento dei commit per ultima modifica

        :param path: Il percorso in cui si trovano i commit da ordinare
        :return: lista dei commit ordinati

    """

    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime,reverse=True))


def creation_df_class(class_name):

    """
        Creazione di un dataframe contenente le metriche relative alla classe specificata come parametro

        :param class_name: Il nome della classe di interesse
        :return: dataframe contenente le metriche relative alla classe

    """

    dfs = []
    files = sorted_ls("C:\\Users\\franc\\PycharmProjects\\EvoluzioneQualitaSW\\Progetto_Evoluzione_Qualit-_SW\\output_dubbo")
    for filename in files:
        filename_string = os.path.basename(filename)
        print(filename_string)
        df = pd.read_csv("C:\\Users\\franc\\PycharmProjects\\EvoluzioneQualitaSW\\Progetto_Evoluzione_Qualit-_SW\\output_dubbo" + '\\' + filename_string, index_col=False)

        dframe = df[df['class'] == str(class_name)]
        if dframe is not None:
                # inserisco nella prima colonna il numero del committ (per iterare), es 92 commit, va da 0 a 91
                # seconda colonna:commit id
                dfs.append(dframe)  # raccolta dei vari dataframe contenenti ognuno una riga di ogni csv
        final_dataframe = pd.concat(dfs)
    return final_dataframe


def plot_CK_metrics(commit_class_row, metric, class_name, color_line):

    """
        Creazione dei grafici delle metriche CK per ogni classe

        :param commit_class_row: Il percorso in cui si trovano i commit da ordinare
        :return: lista dei commit ordinati

    """

    print(plt.style.available)
    plt.style.use("seaborn-v0_8-dark")
    x = np.arange(0, len(commit_class_row.index))
    y = np.array(commit_class_row[metric])
    # ridimensioniamo l'immagine
    plt.figure(figsize=(100, 100))
    # impostiamo i ticks
    #plt.xticks(x)
    plt.yticks(y)
    # assegniamo etichette agli assi
    plt.xlabel("#commits")
    plt.ylabel("Valori del " + metric)
    # impostiamo il titolo del grafico
    plt.title("Andamento della metrica " + metric + " nel tempo per la classe " + class_name)
    # chiediamo di visualizzare la griglia
    plt.grid()
    # disegniamo due linee
    plt.plot(x, y, color = color_line, linewidth = 3)

    plt.show()


classi = ["ZKTools", "org.apache.dubbo.samples.annotation.EmbeddedZooKeeper",
          "org.apache.dubbo.samples.simplified.annotation.ZkUtil"]
metriche = ['cbo','dit','fanin','fanout','wmc','lcom','rfc']
colori = ['red', 'blue', 'green', 'purple', 'orange', 'yellow', 'brown']
for classe in classi:
    for (metrica,colore) in zip(metriche,colori):
        plot_CK_metrics(creation_df_class(classe), metrica, classe, colore)


def extraction_classes_from_commit(commits_csv):

    """
        Estrazione delle classi dai commit in un file csv

        :param commit_csv: Il file csv da cui estrarre i commit
        :return risultati, lista_soglie: lista dei risultati e lista delle soglie da analizzare

    """

    rows = open(commits_csv, 'r+').readlines()
    for i in rows:
        tokens = i.split(',')
        commit_hash, commit_author, commit_date = tokens
        if(commit_date<="2018-11-20 10:02:04 +0800"):
            first_commit_hash = {commit_hash}.pop()
            print(first_commit_hash)
        if (commit_date >= "2021-09-14 11:04:28 +0800"):
            last_commit_hash = {commit_hash}.pop()
            print(last_commit_hash)

    os.system(f"cd {PROJECT_DIR}  && git diff --numstat {first_commit_hash}..{last_commit_hash} > differenzeDubbo.txt")
    read_file = pd.read_csv ("C:\\Users\\franc\\PycharmProjects\\EvoluzioneQualitaSW\\dubbo-samples\\differenzeDubbo.txt", delimiter='|')
    read_file.to_csv (r'differenzeDubbo.csv',index=None)
    rows = open('differenzeDubbo.csv', 'r+').readlines()

    lista_soglie = [100, 250]
    risultati = [0, 0, 0]
    nulli = 0
    for i in rows:
        tokens = i.split('\t')
        added, deleted, classes = tokens
        if added != '-':
            if int(added)<lista_soglie[0]:
                risultati[0] = risultati[0] + 1
            elif int(added)>lista_soglie[0] and int(added)<lista_soglie[1]:
                risultati[1] = risultati[1] + 1
            else:
                risultati[2] = risultati[2] + 1
        else:
            nulli = nulli+1
    print(nulli)
    return risultati, lista_soglie

result, lista_soglie = extraction_classes_from_commit(GIT_COMMITS_FILE)
print(result)
print(lista_soglie)


def plot_class_changes(lista_soglie, result):

    """
        Creazione del grafico a torta relativo alle modifiche (in aggiunta) della classe

        :param lista_soglie, result: lista delle soglie analizzate, lista dei risultati ottenuti

    """

    x = np.array([result[0], result[1], result[2]])
    label = ['Classi Modificate (<'+str(lista_soglie[0])+' LOC)',
             'Classi modificate ('+str(lista_soglie[0])+'< LOC <'+str(lista_soglie[1])+' LOC)',
             'Classi Modificate (>'+str(lista_soglie[1])+' LOC)']
    explode = [0, 0, 0]
    fig, ax = plt.subplots()
    ax.pie(x, labels=label, autopct='%.3f%%', explode = explode)
    ax.set_title('Dubbo Samples project-Modifiche classi')
    plt.show()

print(plot_class_changes(lista_soglie, result))


def correlationMatrix(GIT_COMMITS_FILE):

    """
        Creazione della matrice di correlazione relativa al progetto
        :param GIT_COMMITS_FILE: path assoluto della cartella contenente i file csv di commit
    """

    dfs = []
    rows = open(GIT_COMMITS_FILE, 'r+').readlines()
    for i in rows:
        tokens = i.split(',')
        commit_hash, commit_author, commit_date = tokens

        # Checkout
        os.system(f"cd {PROJECT_DIR} & git checkout {commit_hash}")

        # TOOL CK
        os.system(f'java -jar "C:\\Users\\franc\\PycharmProjects\\EvoluzioneQualitaSW\\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar" {PROJECT_DIR}')
        file = pd.read_csv('class.csv',usecols = ['cbo','dit','fanin','fanout','wmc','rfc','lcom'])
        dfs.append(file)
    final_dataframe = pd.concat(dfs)
    rounded_corr_matrix = final_dataframe.corr().round(2)

    plt.figure(figsize=(8, 6))
    sns.heatmap(rounded_corr_matrix, annot=True)
    plt.show()

correlationMatrix(GIT_COMMITS_FILE)
