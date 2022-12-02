# Generieren von Noten mit Hilfe eines LSTM

## Sinn & Zweck

Bei diesem Repo handelt es sich um ein Projekt aus einem 'Machine Learning & Musicology' Workshop. Zu Grunde lag ein bekannter [Blogpost](https://towardsdatascience.com/how-to-generate-music-using-a-lstm-neural-network-in-keras-68786834d4c5) von Sigurður Skúli. Darauf wurde ein erweitertes Modell zur erzeugung von musikalischen Daten aufgebaut. Übergeordnete Ziele waren ein Schärfen der Python-Skills, im speziellen in der Arbeit mit Pytorch und music21, ein tieferes Verständnis der RNN und LSTMN Konzepte, sowie weiterer elementarer Bestanteile des Machine Learnings, wie der Datenmodellierung, dem Sampling und dem Finden diverser Hyperparamter. 


Die Hauptbestandteile des Repos sind die beiden Notebooks:

- gen_LSTM.ipynb: Datenmodellierung, Netzwerk, Training und Erzeugung
- Dateneigenschaften.ipynb: ein Teil der auf den Datensatz bezogenen Hyperparameterwahl wird in Dateneigenschaften.ipynb erklaert

Da die beiden Notebooks weitesgehend selbsterklärend konzipiert sind, werden im Folgenden nur die wichtigsten Bestandteile genannt. Hierbei ist zu bachten, dass Dateneigenschaften.ipynb zwei Zwischenschritte der Hauptarbeit in gen_LSTM.ipynb darstellt. 

## Ziel, Daten, Modell Und Generierung

### Ziel
Ziel war es mit Hilfe des Konzeptes des LSTM-Netzwerks 'Musik' zu erzeugen, d.h. eine analysierbare Folge von Noten und Pausen. Daher auch der Aufbau auf Skulis Idee(n) mit weiteren Konzepten aus dem NLP (größerer Wortschatz, Embedding, erweitertes Sampling). Auf die Wahl einiger Hyperparameter, wie der Trainingssequenzen, Sequenzlänge und der Größe des Embeddings wird in Dateneigenschaften.ipynb eingangen. 

### Dateneigenschaten.ipynb
In Dateneigenschaften.ipynb betrachten wir den Bach-Korpus, welcher in music21 vorliegt. Wir wollen das Modell nur mit Stücken um 4/4-Takt trainieren und filtern deshalb nach diesen. Weiterhin stellen wir Überlegungen zu einer Mindest- und Maximallänge und eventuellem Padding an. <br>
Außerdem folgen wir einem Algorithmus zur Bestimmung der Embedding-Dimension.

### Modell
Das Netzwerk besteht aus folgenden Layern:
- ein Embedding-Layer, mit embedding_dim=3
- drei Embedding- + Dropout-Layer, mit den Größen 6, 12 und 6, sowie Dropout Quoten 0.2, 0.3, 0.3
- ein linearer Output Layer der Größe 512
- auf den letzten Layer wird KEINE Softmax-Funktion angewandt, da wir mit Pytorch anwenden

Trainiert wurde mit batchsize=64 und stateless.

### generate()
Die gängigen Sampling-Methoden sind Greedy, Top K, Top P und Temperature. Mit der generate()-Funktion kann je nach Parameterwahl zwischen diesen gewählt werden. Es wird schnell klar, dass das Ergebnis stark von der Wahl der Methode abhängt. Z.B. führt Greedy sehr schnell zu sich wiederholenden Sequenzen.
