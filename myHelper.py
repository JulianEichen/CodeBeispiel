# Imports
from music21 import *
import os # files erstellen
import shutil # (nicht-leere) files loeschen
import uuid

'''
Filtert ein music21 Verzeichnis nach Komponist, Taktart und Laenge der Werke, und bildet aus den ersten Stimmen(!) die Mengen der vorhanden pitch classes, octaves, durations und dots. Diese Mengen werden dann als Listen zurueckgegeben.
Input:  
    - paths -> music21 Verzeichnis
    - ratio -> Taktverhaeltnis als String, als so wie es in music21 meter.TimeSignature.ratioString vorliegt z.B. '4/4', '3/4' etc.
Output: 
    - einen wie oben aufgeteilten Wortschatz, gebildet aus dem mit paths definierten und durch ratio gefilterten Corpus. (Es werden nur
    parts mit Taktart ratio betrachtet)       
'''
def getVocab(composer, time_ratio, min_elem, max_elem):
    # Nutzen set(), weil im Folgenden schneller als Listen (nicht getestet)
    # set() verhaelt sich wie eine Menge (Set) aus der Mathematik 
    # d.h. im Folgenden: set.add() analog zu list.append() mit Vermeidung von Duplikaten
    pitch_classes = set() 
    octaves = set()
    durations = set()
    dots = set()
    
    #min_elem = 30
    #max_elem = 70
    
    part_count = 0 # zaehlen der betrachtetn Parts. Wird mit der Ausgabe des DataSet-Objekts spaeter als kleiner 'Sanity Check' genutzt
    
    # Corpus nach Komponist und Taktart filtern
    data_corp = corpus.search(composer,'composer')
    data_corp = data_corp.search(time_ratio)
    
    for work in data_corp:
        temp_score = work.parse() # Werk einlesen und parsen
        
        part = temp_score.parts[0]
        part_rec = part.recurse() # plaetten

        # relevante Elemente zaehlen und evtl den Part ueberspringen
        notes_and_rests = list(part_rec.getElementsByClass([note.Note,note.Rest]))
        nr_sum = len(notes_and_rests)
       
        if min_elem <= nr_sum <= max_elem: # Falls die Anzahl der Elemente den Vorgaben entspricht
            for elem in notes_and_rests:
                if isinstance(elem, note.Note): # falls Note gefunden
                    # im Folgenden, set.add() analog zu list.append() mit Vermeidung von Duplikaten
                    pitch_classes.add(elem.name) # Name (Pitch-Klasse) der Note
                    octaves.add('o'+str(elem.octave)) # Okatevenzahl, liegt als int vor, muss umgewandelt werden
                    durations.add(elem.duration.type) # Duration, 'quarter', 'half' etc.
                    dots.add('d'+str(elem.duration.dots)) # Anzahl der Punkte

                if isinstance(elem, note.Rest):
                    durations.add(elem.duration.type) # Duration, 'quarter', 'half' etc.
                    dots.add('d'+str(elem.duration.dots)) # Anzahl der Punkte

                
            part_count +=1 # zaehlen 
    
    print('Number of parts: ',part_count)
                    
    return list(pitch_classes), list(octaves), list(durations), list(dots)

'''
Codiert einen m21-Part
Input:
    - m21 part
Output:
    - Elemente im Part als Liste von Strings
'''
def part2List(part, target_len = 0):

    part_list = []
    null_elem = 'null'
        
    for part_element in part: # durch den Part iterieren
            
        if isinstance(part_element, note.Note): # falls Note gefunden
            part_list.append(part_element.name) # Name (Pitch-Klasse) der Note
            part_list.append('o'+str(part_element.octave)) # Okatevenzahl, liegt als int vor, muss umgewandelt werden
            part_list.append(part_element.duration.type) # Duration, 'quarter', 'half' etc.
            part_list.append('d'+str(part_element.duration.dots)) # Anzahl der Punkte
            part_list.append(' ') # entsprechend der Codierung
            
        elif isinstance(part_element, note.Rest): # falls Pause gefunden
            # part_list.append('R')
            part_list.append(part_element.duration.type) # Duration, 'quarter', 'half' etc.
            part_list.append('d'+str(part_element.duration.dots)) # Anzahl der Punkte
            part_list.append(' ') # entsprechend der Codierung
                
     # Padding vorne
    while len(part_list) < target_len:
        part_list.insert(0,null_elem)

    return part_list

# ---------*---------*---------*---------*---------*---------*---------
'''
    Automatische Partiturdarstellung in jupyter notebooks mit Musescore funktionert zur Zeit unter (meinem) Windows10 nicht.
    Daher Workaround mit lilypond.
    ->temporaeren Ordner fuer PNG-Files erstellen
    ->wenn noetig mit lilypond PNG-Files erstellen, werden im Order abgelegt
    ->Ausgabe mit IPython.display
    ->am Ende den Ordner wieder loeschen
'''

'''
    Erstellt Ordner
    Input:
    Output:
        Pfad zum Ordner
'''
def myLilyCreate():
    lily_path = 'lily_png_temp'
    os.mkdir(lily_path)
    return lily_path

'''
    Loescht Inhalt des PNG-Ordners
    Input:
        Pfad
    Output:
'''
def myLilyRemove(lily_path):
    if os.path.exists(lily_path):
        shutil.rmtree(lily_path)
    return

'''
    Input:
        music21-Stream-Objekt
    Output:
        pfad zu lilypond-png
'''
def myLilyPNG(stream,path):
    path = path + '/last_png'
    path = stream.write(fp=path,fmt='lily.png')
    return path