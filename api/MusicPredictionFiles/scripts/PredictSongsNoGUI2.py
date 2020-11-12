# Library imports
# from tkinter import filedialog
# from tkinter import *

import pandas
import numpy as np
#
# Local imports
from sklearn.svm import SVC
import sklearn

import joblib
import pickle

import numpy as np
import pandas as pd


from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from music21 import *
import re
import os

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler

class Predictor:
    def __init__(self):
        print(self," doesn't have any arguments")


    class ChordObject:
        def __init__(self, chord):
            self.count = 1
            self.chord = chord
        def __eq__(self,other):
            if(self.chord==other.chord):
                return True
            else:
                return False
        def IncrementCount(self):
            self.count+=1

    #how similar is each measure in comparison to entire piece
    #score1 is the score to search for(looking for these notes)
    #score2 is the score to search(looking at this corpus)
    def advancedRhythm2Similarity(self,score1,score2):
        similarity = 0
        aggregate_similarity = 0
        total_measures = 0
        try:
            if score1 is not None and score2 is not None:
                stream_segments1 = score1.getElementsByClass(stream.Part)
                stream_segments2 = score2.getElementsByClass(stream.Part)
                similar_measures = 0
                total_measures = len(stream_segments1[0])-1
                
                i = 1
                while  i < len(stream_segments1[0]):
                    stream_segment1 = stream_segments1[0][i]
                    new_score = stream.Score()
                    new_score.insert(0,stream_segment1)
                    notes_and_rest_to_search = new_score.flat.notesAndRests.stream()
                    j = 1
                    while j<len(stream_segments1[0]):
                        measure_segment = stream_segments2[0][j]
                        segment_score = stream.Score()
                        segment_score.insert(0,measure_segment)
                        notes_and_rest_search = segment_score.flat.notesAndRests.stream()
                        a = 0
                        rhythm_match = True
                        #print(len(notes_and_rest_search), "  ",len(notes_and_rest_to_search))
                        if len(notes_and_rest_search)==len(notes_and_rest_to_search):
                            while a<len(notes_and_rest_to_search):
                                note_to_match = notes_and_rest_search[a]
                                curr_note = notes_and_rest_to_search[a]
                                if not(type(note_to_match)==type(curr_note) or ((type(note_to_match)==note.Note and type(curr_note)==chord.Chord)or(type(note_to_match)==chord.Chord and type(curr_note)==note.Note))):
                                    rhythm_match = False
                                a+=1
                            if rhythm_match:
                                similar_measures+=1
                        j+=1
                    i+=1
                    #print("similar measures: ",similar_measures)
                    avg_for_measure = similar_measures/total_measures
                    aggregate_similarity+=avg_for_measure
                    #print("avg ", avg_for_measure)
                    similar_measures = 0
                similarity = aggregate_similarity/total_measures
            

            return similarity
        except:
            return 0
    #similarity of rythm
    #1:1 rhythm
    def rhythmSimilarity(self,score1,score2):
        similarity = 0
        try:
            if score1 is not None and score2 is not None:
                score1.getElementsByClass(stream.Part)[0][0:5]
                try:
                    l = search.approximateNoteSearchOnlyRhythm(score1,score2)
                    similarity = l[0].matchProbability
                except:
                    # print("error when getting rhythm similairty")
                    return 0
            # print("similarity: ",similarity)
            return similarity
        except:
            return 0


    #average x chord notes
    def averageXChordPlusNotes(self,chords,number_of_notes):
        average = 0
        try:
            if chords is not None:
                total_x_chord_notes = float(self.totalXChordPlusNotes(chords,number_of_notes))
                total = float(len(chords))
                average = total_x_chord_notes/total
            return average
        except:
            return 0
    #total x plus chord notes
    def totalXChordPlusNotes(self, chords,number_of_notes):
        total = 0
        try:
            if chords is not None:
                for chord in chords:
                    #print("length of chord: ",len(chord))
                    if len(chord)>=number_of_notes:
                        total+=1
            return total
        except:
            return 0

    def averageXChordNotes(self,chords,number_of_notes):
        average = 0
        try:
            if chords is not None:
                total_x_chord_notes = float(self.totalXChordPlusNotes(chords,number_of_notes))
                total = float(len(chords))
                average = total_x_chord_notes/total
            return average
        except:
            return 0
    #total x plus chord notes
    def totalXChordNotes(self,chords,number_of_notes):
        total = 0
        try:
            if chords is not None:
                for chord in chords:
                    #print("length of chord: ",len(chord))
                    if len(chord)==number_of_notes:
                        total+=1
            return total
        except:
            return 0
    #advanced rhythmic similarity
    #how similar is each measure in comparison to entire piece
    def advancedRhythmSimilarity(self,score):
        similarity = 0
        aggregate_similarity = 0
        total_measures = 0
        try:
            if score is not None:
                stream_segments = score.getElementsByClass(stream.Part)
                similar_measures = 0
                total_measures = len(stream_segments[0])-1
                i = 1
                while  i < len(stream_segments[0]):
                    stream_segment = stream_segments[0][i]
                    new_score = stream.Score()
                    new_score.insert(0,stream_segment)
                    notes_and_rest_to_search = new_score.flat.notesAndRests.stream()
                    j = 1
                    while j<len(stream_segments[0]):
                        measure_segment = stream_segments[0][j]
                        segment_score = stream.Score()
                        segment_score.insert(0,measure_segment)
                        notes_and_rest_search = segment_score.flat.notesAndRests.stream()
                        a = 0
                        rhythm_match = True
                        #print(len(notes_and_rest_search), "  ",len(notes_and_rest_to_search))
                        if len(notes_and_rest_search)==len(notes_and_rest_to_search):
                            while a<len(notes_and_rest_to_search):
                                note_to_match = notes_and_rest_search[a]
                                curr_note = notes_and_rest_to_search[a]
                                if not(type(note_to_match)==type(curr_note) or ((type(note_to_match)==note.Note and type(curr_note)==chord.Chord)or(type(note_to_match)==chord.Chord and type(curr_note)==note.Note))):
                                    rhythm_match = False
                                a+=1
                            if rhythm_match:
                                similar_measures+=1
                        j+=1
                    i+=1
                    #print("similar measures: ",similar_measures)
                    avg_for_measure = similar_measures/total_measures
                    aggregate_similarity+=avg_for_measure
                    #print("avg ", avg_for_measure)
                    similar_measures = 0
                similarity = aggregate_similarity/total_measures
            return similarity
        except:
            return 0
    # #similarity between two scores
    # def similarityBetween2Score(score1,score2,file):
    #     total_similarity = 0
    #     avg_similarity = 0
    #     scoreDict = OrderedDict()
    #     if score1 is not None and score2 is not None:
    #         scoreList1 = search.segment.indexScoreParts(score1)
    #         scoreList2 = search.segment.indexScoreParts(score2)
    #         scoreDict["1 "+file] = scoreList1
    #         scoreDict["2 "+file] = scoreList2
    #         scoreSim = search.segment.scoreSimilarity(scoreDict,minimumLength=1,includeReverse=False)

    #         total_segments = len(scoreSim)
    #         print("total_segmentsssss; ", total_segments)
    #         count = 0
    #         for result in scoreSim:
    #             print("simm: ", result)
    #             similarity = float(result[len(result)-1])
    #             total_similarity+=similarity
    #         try:
    #             avg_similarity = total_similarity/total_segments
    #         except:
    #             print("cannot divide by 0 error(similarityBetween2Score)")
    #             return -1

    #         print("similarityBetween2Score: ",avg_similarity)
    #     return avg_similarity

    # #compare similarity between a segment(1 or more measures) to another segment(1 or more other measures)
    # def similarityBetween1Score(score,file):
    #     total_similarity = 0
    #     avg_similarity = 0
    #     if score is not None:
    #         scoreDict = OrderedDict()
    #         scoreList = search.segment.indexScoreParts(score)
    #         scoreDict["1 "+file] = scoreList
    #         scoreDict["2 "+file] = scoreList
    #         scoreSim = search.segment.scoreSimilarity(scoreDict,minimumLength=1,includeReverse=False)
    #         total_segments = len(scoreSim)
    #         count = 0
    #         for result in scoreSim:
    #             print("ress: ", result)
    #             similarity = float(result[len(result)-1])
    #             total_similarity+=similarity
    #         try:
    #             avg_similarity = total_similarity/total_segments
    #         except:
    #             print("cannot divide by 0 error(similarityBetween1Score)")
    #             return -1

    #     print("similarityBetween1Score: ",avg_similarity)
    #     return avg_similarity

    #gets the average density of chords played at the same time
    def averageDensity(self,chords):
        average = 0
        total = 0
        count = 0
        try:
            if chords is not None:
                for chord in chords:
                    total+=len(chord)
                    count+=1
                average = float(total)/float(count)

            return average
        except:
            return 0

    #range between most common notes of both hands
    def RLHandCommonNoteRange(self,right_hand_stream,left_hand_stream):
        aInterval = 0
        try:
            if(right_hand_stream is not None and left_hand_stream is not None):
                chord_objects = []
                chords_count = dict()
                most_common_rh_notes = self.ReturnMostCommonNotesInOrder(right_hand_stream,1000000000000000)
                most_common_lh_notes = self.ReturnMostCommonNotesInOrder(left_hand_stream,1000000000000000)
                most_common_rh_note = most_common_rh_notes[0]
                most_common_lh_note = most_common_lh_notes[0]
                combinedChord = chord.Chord([most_common_lh_note,most_common_rh_note])
                combinedChord = combinedChord.sortDiatonicAscending(inPlace=True)

                lower_note = combinedChord[0]
                higher_note = combinedChord[len(combinedChord)-1]
                aInterval = interval.Interval(noteStart=lowest_note,noteEnd=highest_note)
                aInterval = abs(int(re.search(r'\d+', str(aInterval.name)).group()))

            return float(aInterval)
        except:
            return 0


    def ReturnMostCommonChordsInOrder(self,chords,chord_count):
        chord_array = []
        try:
            if(chords is not None):
                chords_count = dict()
                chords_object_array = []
                
                for chord in chords:
                    if(str(chord.pitchNames) not in chords_count):
                        chord_object = ChordObject(chord)
                        chords_count[str(chord.pitches)] = chord_object
                        chords_object_array.append(chord_object)
                    else:
                        chords_count[str(chord.pitches)].IncrementCount()
                #sort list of common chords
                chords_object_array.sort(key=lambda x: x.count, reverse = True)
                previous_current_count = -1
                #put chords into chord array
                for chord_object in chords_object_array:
                    #print("chord object: ",chord_object.count)
                    if chord_count==-1 or previous_current_count==chord_object.count or chord_count>0:
                        chord_array.append(chord_object.chord)
                        chord_count-=chord_object.count
                        previous_current_count = chord_object.count

                return chord_array
        except:
            return chord_array

    #return list of most common notes in order
    def ReturnMostCommonNotesInOrder(self,stream,notes_count):
        note_list = []
        try:
            if(stream is not None):
                pitches = stream.flat.notes.pitches
                pitch_dict = dict()
                
                for pitch in pitches:
                    if(pitch.nameWithOctave not in pitch_dict):
                        pitch_dict[pitch.nameWithOctave] = 1
                    else:
                        pitch_dict[pitch.nameWithOctave] += 1
                #sort by count
                pitch_dict = sorted(pitch_dict.items(), key=lambda x: x[1],reverse = True)
                #place notes in list
                total = 0
                for pitch in pitch_dict:
                    if(total<notes_count):
                        new_note = note.Note(str(pitch[0]))
                        note_list.append(new_note)
                    total+=pitch[1]
            return note_list
        except:
            return note_list


        


    #find the highest chord from a list of chords
    def find_highest_chord(self,chords):
        highest_chord = chords[0]
        if(len(chords)>1):
            curr = 1
            while curr<len(chords):
                current = chords[curr]
                if current[0]>highest_chord[0]:
                    highest_chord = current
                curr+=1

        return highest_chord

    #find the lowest chord from a list of chords
    def find_lowest_chord(self,chords):
        lowest_chord = chords[0]
        if(len(chords)>1):
            curr = 1
            while curr<len(chords):
                current = chords[curr]
                # print("current: ",current.chord[0])
                #print("lowest: ",lowest_chord[0])
                if current[0]<lowest_chord[0]:
                    lowest_chord = current
                curr+=1

        return lowest_chord

    #returns the range of the top x percent of notes
    #subset range
    def rangeOfTopXPercent(self,given_stream,percent):
        aInterval = 0
        try:
            if(given_stream is not None):
                total_notes = self.totalNotes(given_stream)
                number_of_notes = int(total_notes*(percent))
                notes = self.ReturnMostCommonNotesInOrder(given_stream,number_of_notes)
                if(len(notes)>0):
                    combinedChord = None
                    combinedChord = chord.Chord(notes)
                    combinedChord = combinedChord.sortDiatonicAscending(inPlace=True)
                    lower_note = combinedChord[0]
                    higher_note = combinedChord[len(combinedChord)-1]
                    aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
                    aInterval = int(re.search(r'\d+', str(aInterval.name)).group())

            return float(aInterval)
        except:
            return 0

    #range of lowest and highest CHORDS
    #subset range
    def fakeRangeOfTopXPercent(self,chords,percent):
        aInterval = 0
        try:
            if(chords is not None):
                number_of_chords = int(len(chords)*(percent))
                chord_objects = []
                chords_count = dict()
                most_common_chords = self.ReturnMostCommonChordsInOrder(chords,number_of_chords)
                if(len(most_common_chords)>1):
                    chords_in_order = self.returnChordsInPianoOrder(most_common_chords)
                    #print("number of chords: ",number_of_chords,"    ",len(most_common_chords))
                    combinedChord = None
                    combinedChord = chord.Chord([chords_in_order[0],chords_in_order[len(chords_in_order)-1]])
                    combinedChord = combinedChord.sortDiatonicAscending(inPlace=True)
                    lower_note = combinedChord[0]
                    higher_note = combinedChord[len(combinedChord)-1]
                    aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
                    aInterval = abs(int(re.search(r'\d+', str(aInterval.name)).group()))
        
            return float(aInterval)
        except:
            return 0

    #get top x chords, place them in order from lowest to highest and find average range
    #from each note to the next(distance is calculated between lowest note in chords being compared)
    #tested
    def averageRangeOfTopXPercent(self,chords,percent):
        total_interval = 0
        average_interval = 0
        try:
            if(chords is not None):
                #get most common chords in piano order
                number_of_chords = int(len(chords)*(percent))
                if(number_of_chords>1):
                    chord_objects = []
                    chords_count = dict()
                    #print("number of chords: ",number_of_chords)
                    most_common_chords = self.ReturnMostCommonChordsInOrder(chords,number_of_chords)
                    
                    if(len(most_common_chords)>1):
                        chords_in_order = self.returnChordsInPianoOrder(most_common_chords)
                        if len(chords_in_order)<2:
                            return -1
                        index = 0
                        #print("chords in order: ",len(chords_in_order))
                        #get average range
                        while index<len(chords_in_order)-1:
                            chord1 = chords_in_order[index]
                            chord2 = chords_in_order[index+1]
                            combinedChord = None
                            combinedChord = chord.Chord([chord1,chord2])
                            combinedChord = combinedChord.sortDiatonicAscending(inPlace=True)
                            lower_note = combinedChord[0]
                            higher_note = combinedChord[len(combinedChord)-1]
                            aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
                            aInterval = abs(int(re.search(r'\d+', str(aInterval.name)).group()))
                            total_interval+=aInterval
                            index+=1
                        average_interval = (float(total_interval)/float(index))
        
            return float(average_interval)
        except:
            return 0


    #returns chords lowest to highest on piano
    def returnChordsInPianoOrder(self,chords):
        index = 0
        chords_in_order = []
        count = len(chords)
        while index<count:
            try:
                lowest_chord = self.find_lowest_chord(chords)
                chords.remove(lowest_chord)
                chords_in_order.append(lowest_chord)
                index+=1
            except:
                return chords_in_order
        return chords_in_order
    #average largeJumps
    #return the number of large jumps>=largeJump
    def largeJumps(self,chords,largeJump):
        totalLargeJumps = 0
        i = 0
        try:
            if chords is not None:
                while i<len(chords)-1:
                    #get first note of first chord
                    note1_chord1 = chords[i][0]
                    #get first note of second chord
                    note1_chord2 = chords[i+1][0]

                    combinedChord = chord.Chord([note1_chord1,note1_chord2])
                    combinedChord = combinedChord.sortDiatonicAscending(inPlace=True)

                    lower_note = combinedChord[0]
                    higher_note = combinedChord[len(combinedChord)-1]

                    #print(chords[i],"  ",chords[i+1],"  ",note1,">",note2,"    ",note1<note2)
                    #interval between both notes
                    aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
                    if(int(re.search(r'\d+', str(aInterval.name)).group())>=largeJump):
                        #print(chords[i],"   ",chords[i+1])
                        totalLargeJumps+=1
                        #print(aInterval.name)
                    i+=1
            return float(totalLargeJumps)
        except:
            return 0


    #average largeJumps
    def averageLargeJump(self,chords,largeJump):
        totalLargeJumps = 0
        average_weighted_large_jumps = 0
        i = 0
        try:
            if chords is not None:
                while i<len(chords)-1:
                    #get first note of first chord
                    note1_chord1 = chords[i][0]
                    #get first note of second chord
                    note1_chord2 = chords[i+1][0]

                    combinedChord = chord.Chord([note1_chord1,note1_chord2])
                    combinedChord = combinedChord.sortDiatonicAscending(inPlace=True)

                    lower_note = combinedChord[0]
                    higher_note = combinedChord[len(combinedChord)-1]

                    #print(chords[i],"  ",chords[i+1],"  ",note1,">",note2,"    ",note1<note2)
                    #interval between both notes
                    aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
                    if(int(re.search(r'\d+', str(aInterval.name)).group())>=largeJump):
                        #print(chords[i],"   ",chords[i+1])
                        totalLargeJumps+=1
                        #print(aInterval.name)
                    i+=1
                average_weighted_large_jumps = totalLargeJumps/len(chords)
            return float(average_weighted_large_jumps)
        except:
            return 0

    #average interval value of large jumps
    def averageLargeJumpValues(self,chords,largeJump):
        totalLargeJumps = 0
        total = 0
        average = 0
        i = 0
        try:
            if chords is not None:
                while i<len(chords)-1:
                    #get first note of first chord
                    note1_chord1 = chords[i][0]
                    #get first note of second chord
                    note1_chord2 = chords[i+1][0]

                    combinedChord = chord.Chord([note1_chord1,note1_chord2])
                    combinedChord = combinedChord.sortDiatonicAscending(inPlace=True)

                    lower_note = combinedChord[0]
                    higher_note = combinedChord[len(combinedChord)-1]
                    #print(chords[i],"   ",chords[i+1])
                    #print(chords[i],"  ",chords[i+1],"  ",note1,">",note2,"    ",note1<note2)
                    #interval between both notes
                    aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
                    if(int(re.search(r'\d+', str(aInterval.name)).group())>=largeJump):
                        totalLargeJumps+=1
                        total += int(re.search(r'\d+', str(aInterval.name)).group())
                        #print(aInterval.name)
                    i+=1
                #print ("total large jumps: ",totalLargeJumps)
                if totalLargeJumps>0:
                    average = float(total)/float(totalLargeJumps)
            return float(average)
        except:
            return 0

    #average large jump value * (large jumps/total chords)
    def weightedAverageLargeJumpValues(self,chords,largeJump):
        totalLargeJumps = 0
        total = 0
        average = 0
        weighted_average = 0
        i = 0
        try:
            if chords is not None:
                averageValue = self.averageLargeJumpValues(chords, largeJump)
                large_jumps = self.largeJumps(chords, largeJump)
                weighted_average = averageValue*(large_jumps/len(chords))
            return float(weighted_average)
        except:
            return 0





    #average range of played ntoes
    #combine both chords into one and get range from lowest to highest
    def averageRangeForNextNotes(self,chords):
        i = 0
        total = 0
        average = 0
        try:
            if chords is not None:
                while i<len(chords)-1:
                    #combine chords into one
                    combinedChord = chord.Chord([chords[i],chords[i+1]])
                    combinedChord = combinedChord.sortDiatonicAscending(inPlace=True)

                    lower_note = combinedChord[0]
                    higher_note = combinedChord[len(combinedChord)-1]
                    
                    #interval between both notes
                    aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
                    total+=int(re.search(r'\d+', str(aInterval.name)).group())
                    i+=1
                if(len(chords)>1):
                    average = float(total)/(float(len(chords))-1)
            return float(average)
        except:
            return 0

    #average range of played ntoes
    #range from A3 to B3C4 is the interval from A3 to B3
    #You should take the left and right hand as streams*******
    def average2RangeForNextNotes(self,chords):
        i = 0
        total = 0
        average = 0
        try:
            if chords is not None:
                while i<len(chords)-1:
                    #get first note of first chord
                    note1_chord1 = chords[i][0]
                    #get first note of second chord
                    note1_chord2 = chords[i+1][0]
                    combinedChord = chord.Chord([note1_chord1,note1_chord2])
                    combinedChord = combinedChord.sortDiatonicAscending(inPlace=True)

                    lower_note = combinedChord[0]
                    higher_note = combinedChord[len(combinedChord)-1]
                    
                    #first chord lower than second
                    if higher_note<lower_note:
                        lower_note = note1_chord2
                        higher_note = note1_chord1
                    #interval between both notes
                    aInterval = interval.Interval(noteStart=lower_note,noteEnd=higher_note)
                    total+=int(re.search(r'\d+', str(aInterval.name)).group())
                    #print(aInterval.name)
                    i+=1
                if(len(chords)>0):
                    average = float(total)/(float(len(chords))-1)
            return float(average)
        except:
            return 0





    def average2ChordPlusRangeForHand(self,chords,chord_length):
        average = 0
        chord_average_total = 0
        total_chords = 0
        try:
            if chords is not None:
                for chord in chords:
                    #calculate range in chord
                    if(len(chord)>=chord_length):
                        total_chords+=1
                        total = 0
                        average = 0
                        index = 0
                        #print(chord)
                        #interval between notes in chord
                        while index!=len(chord)-1:
                            aInterval = interval.Interval(noteStart=chord[index],noteEnd=chord[index+1])
                            total+=int(re.search(r'\d+', str(aInterval.name)).group())
                            index+=1
                        #average of chord
                        average = float(total)/float((len(chord)-1))
                        chord_average_total+=average
                        #print(average)
                if(total_chords>0):

                    average = float(chord_average_total)/float(total_chords)
                else:
                    average = 0
            return float(average)
        except:
            return 0





    def weightedAverage2ChordPlusRangeForHand(self,chords,chord_length):
        average = 0
        weighted_average = 0
        chord_average_total = 0
        total_chords = 0
        try:
            if chords is not None:
                average = self.average2ChordPlusRangeForHand(chords,chord_length)
                weighted_average = average * self.averageXChordPlusNotes(chords, chord_length)
            return float(weighted_average)
        except:
            return 0





    #assume you have the correct stream##############################################
    #tested but is it actually useful????
    #for every chord, what is the range from one note to the next
    #basically this tells you how far you have to spread each finger on average
    #3 note chord,distance from 1-2+distance from 2-3 /2
    #average this out
    def average2ChordRangeForHand(self,chords,chord_length):
        average = 0
        chord_average_total = 0
        total_chords = 0
        try:
            if chords is not None:
                for chord in chords:
                    #calculate range in chord
                    if(len(chord)==chord_length):
                        total_chords+=1
                        total = 0
                        average = 0
                        index = 0
                        #print(chord)
                        #interval between notes in chord
                        while index!=len(chord)-1:
                            aInterval = interval.Interval(noteStart=chord[index],noteEnd=chord[index+1])
                            total+=int(re.search(r'\d+', str(aInterval.name)).group())
                            index+=1
                        #average of chord
                        average = float(total)/float((len(chord)-1))
                        chord_average_total+=average
                        #print(average)
                if(total_chords>0):

                    average = float(chord_average_total)/float(total_chords)
                else:
                    average = 0
            return float(average)
        except:
            return 0


    def weightedAverage2ChordRangeForHand(self,chords,chord_length):
        average = 0
        weighted_average = 0
        chord_average_total = 0
        total_chords = 0
        try:
            if chords is not None:
                average = self.average2ChordRangeForHand(chords, chord_length)
                weighted_average = average * self.averageXChordNotes(chords, chord_length)
            return float(average)
        except:
            return 0

    #for every chord, what is the range from the left most note to the right most note
    #basically how far is your hand spread out for each chord
    #average this out
    #simple and useful tested
    def averageChordRangeForHand(self,chords,chord_length):
        total_chords = 0
        total = 0
        average = 0
        try:
            #distance between first and last note of each chord
            if chords is not None:
                for chord in chords:
                    if(len(chord)==chord_length):
                        aInterval = interval.Interval(noteStart=chord[0],noteEnd=chord[len(chord)-1])
                        total+=int(re.search(r'\d+', str(aInterval.name)).group())
                        total_chords+=1
                        #print(chord ," ",aInterval)
                if(total_chords>0):
                    average = float(total)/float(total_chords)
            return float(average)
        except:
            return 0

    #averageChordRangeForHand * averageXChordNotes
    def weightedAverageChordRangeForHand(self,chords, chord_length):
        weighted_average = 0
        average_chord_range = 0
        average_x_chord_notes = 0
        try:
            if chords is not None:
                average_chord_range = float(self.averageChordRangeForHand(chords, chord_length))
                average_x_chord_notes = float(self.averageXChordNotes(chords, chord_length))
                weighted_average = float(average_chord_range * average_x_chord_notes)
                return weighted_average
        except:
            return 0
        

    #averageChordPlusRangeForHand * averageXChordPlusNotes
    def weightedAverageChordPlusRangeForHand(self,chords, chord_length):
        weighted_average = 0
        average_chord_plus_range = 0
        average_x_chord_plus_notes = 0
        try:
            if chords is not None:
                average_chord_plus_range = float(self.averageChordPlusRangeForHand(chords, chord_length))
                average_x_chord_plus_notes = float(self.averageXChordPlusNotes(chords, chord_length))
                weighted_average = float(average_chord_plus_range * average_x_chord_plus_notes)
                return weighted_average
        except:
            return 0



    #same as averageChordRangeForHand but uses >= operator
    def averageChordPlusRangeForHand(self,chords,chord_length):
        total_chords = 0
        total = 0
        average = 0
        try:
            #distance between first and last note of each chord
            if chords is not None:
                for chord in chords:
                    if(len(chord)>=chord_length):
                        aInterval = interval.Interval(noteStart=chord[0],noteEnd=chord[len(chord)-1])
                        total+=int(re.search(r'\d+', str(aInterval.name)).group())
                        total_chords+=1
                        #print(chord ," ",aInterval)
                if(total_chords>0):
                    average = float(total)/float(total_chords)
            return float(average)
        except:
            return 0
    #average
    def averageWholeNotes(self,given_stream):
        average = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes.pitches
                totalNotes = len(notes)
                if totalNotes>0:
                    average = float(self.totalWholeNotes(given_stream))/float(totalNotes)
            return float(average)
        except:
            return 0

    def averageHalfNotes(self,given_stream):
        average = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes.pitches
                totalNotes = len(notes)
                if totalNotes>0:
                    average = float(self.totalHalfNotes(given_stream))/float(totalNotes)
            return float(average)
        except:
            return 0

    def averageQuarterNotes(self,given_stream):
        average = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes.pitches
                totalNotes = len(notes)
                if totalNotes>0:
                    average = float(self.totalQuarterNotes(given_stream))/float(totalNotes)
            return float(average)
        except:
            return 0

    def averageEighthNotes(self,given_stream):
        average = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes.pitches
                totalNotes = len(notes)
                if totalNotes>0:
                    average = float(self.totalEighthNotes(given_stream))/float(totalNotes)
            return float(average)
        except:
            return 0

    def average16thNotes(self,given_stream):
        average = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes.pitches
                totalNotes = len(notes)
                if totalNotes>0:
                    average = float(self.total16thNotes(given_stream))/float(totalNotes)
            return float(average)
        except:
            return 0

    def average32ndNotes(self,given_stream):
        average = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes.pitches
                totalNotes = len(notes)
                if totalNotes>0:
                    average = float(self.total32ndNotes(given_stream))/float(totalNotes)
            return float(average)
        except:
            return 0

    def average64thNotes(self,given_stream):
        average = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes.pitches
                totalNotes = len(notes)
                if totalNotes>0:
                    average = float(self.total64thNotes(given_stream))/float(totalNotes)
            return float(average)
        except:
            return 0

    def totalWholeNotes(self,given_stream):
        total = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes
                for note in notes:
                    if note.quarterLength==4:
                        total+=len(note.pitches)
            return float(total)
        except:
            return 0

    def totalHalfNotes(self,given_stream):
        total = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes
                for note in notes:
                    if note.quarterLength==2:
                        total+=len(note.pitches)
            return float(total)
        except:
            return 0

    def totalQuarterNotes(self,given_stream):
        total = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes
                for note in notes:
                    if note.quarterLength==1:
                        total+=len(note.pitches)
            return float(total)
        except:
            return 0

    def totalEighthNotes(self,given_stream):
        total = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes
                for note in notes:
                    if note.quarterLength==.5:
                        total+=len(note.pitches)
            return float(total)
        except:
            return 0

    def total16thNotes(self,given_stream):
        total = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes
                for note in notes:
                    if note.quarterLength==.25:
                        total+=len(note.pitches)
            return float(total)
        except:
            return 0

    def total32ndNotes(self,given_stream):
        total = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes
                for note in notes:
                    if note.quarterLength==.125:
                        total+=len(note.pitches)
            return float(total)
        except:
            return 0

    def total64thNotes(self,given_stream):
        total = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.notes
                for note in notes:
                    if note.quarterLength==.0625:
                        total+=len(note.pitches)
            return float(total)
        except:
            return 0

    #total notes
    #total notes right hand
    #total notes left hand
    def totalNotes(self,given_stream):
        try:
            notes = given_stream.flat.pitches
            if(notes is not None):
                return float(len(notes))
            else:
                return float(0)
        except:
            return 0 
    #total sharp notes in the entire piece
    #total sharp notes in right hand
    #total sharp notes in left hand
    def totalSharpNotes(self,given_stream):
        totalSharpNotes = 0
        try:
            if given_stream is not None:
                pitches = given_stream.flat.pitches
                for pitch in pitches:
                    if '#' in pitch.name:
                        totalSharpNotes+=1
                        #print(note.name)
            return float(totalSharpNotes)
        except:
            return 0
        


    #total flat notes in the entrire piece
    #total flat notes in right hand
    #total flat notes in left hand
    def totalFlatNotes(self,given_stream):
        totalFlatNotes = 0
        try:
            if given_stream is not None:
                pitches = given_stream.flat.pitches
                for pitch in pitches:
                    if '-' in pitch.name:
                        totalFlatNotes+=1
                        #print(note.name)
            return float(totalFlatNotes)
        except:
            return 0
        

    def totalNaturalNotes(self,given_stream):
        totalNaturalNotes = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.pitches
                for pitch in notes:
                    if '-' not in pitch.name and '#' not in pitch.name:
                        totalNaturalNotes+=1
            return float(totalNaturalNotes)
        except:
            return 0
        




    #total sharp notes in the entire piece
    #total sharp notes in right hand
    #total sharp notes in left hand
    def averageSharpNotes(self,given_stream):
        total_sharp_notes = 0
        average_sharp_notes = 0
        try:
            if given_stream is not None:
                total_sharp_notes = self.totalSharpNotes(given_stream)
                total_notes = self.totalNotes(given_stream)
                average_sharp_notes =total_sharp_notes/total_notes
                        #print(note.name)
            return float(average_sharp_notes)
        except:
            return 0
        


    #total flat notes in the entrire piece
    #total flat notes in right hand
    #total flat notes in left hand
    def averageFlatNotes(self,given_stream):
        total_flat_notes = 0
        average_flat_notes = 0
        try:
            if given_stream is not None:
                total_flat_notes = self.totalFlatNotes(given_stream)
                total_notes = self.totalNotes(given_stream)
                average_flat_notes = total_flat_notes/total_notes
            return float(average_flat_notes)
        except:
            return 0
        

    def averageNaturalNotes(self,given_stream):
        total_natural_notes = 0
        average_natural_notes = 0
        try:
            if given_stream is not None:
                total_natural_notes = self.totalNaturalNotes(given_stream)
                total_notes = self.totalNotes(given_stream)
                average_natural_notes = total_natural_notes/total_notes
            return float(average_natural_notes)
        except:
            return 0
        



    # if you have a stream you should be able to detect any
    # changes in key signature
    def totalAccidentals(self,given_stream,altered_pitches):
        total_accidentals = 0
        try:
            if given_stream is not None:
                pitches = given_stream.flat.pitches
                for pitch in pitches:
                    #loook for a note match
                    for altered_pitch in altered_pitches:
                        #check for pitch class match
                        if altered_pitch[0]==pitch.name[0]:
                            if(altered_pitch!=pitch.name):
                                total_accidentals+=1

            return float(total_accidentals)
        except:
            return 0
        

    def averageAccidentals(self,given_stream,altered_pitches):
        average_accidentals = 0
        try:
            if given_stream is not None:
                notes = given_stream.flat.pitches
                total_accidentals = self.totalAccidentals(given_stream,altered_pitches)
                total_notes = len(notes)
                average_accidentals=float(total_accidentals)/float(total_notes)
            return float(average_accidentals)
        except:
            return 0

    def predictSong(self,file,model_name, data_name, N, less_than_grade, scaleData, reduceFeatures):
        key_signatures = {"C major": 0,"G major" : .10, "e minor":.10,"D major":.20,
        "b minor":.20,"A major":.40,"f# minor":.40,"E major":.60,"c# minor":.60,
        "B major":.75,"g# minor":.75,"F# major":.90,"d# minor":.90,"C# major":1,
        "a# minor":100,
        "F major":.10,"d minor":.10,"B- major":.20,"g minor":.20,"E- major":.40,
        "c minor":.40,"A- major":.60,"f minor":.60,"D- major":.75,
        "b- minor":.75,"G- major":.90,"e- minor":.90,"C- major":1,
        "a- minor":1, "a minor":0}       

        songs_features = dict()
        feature_index = 0
      
        feature_values = dict()
        print("file: ",file)

        score = converter.parseData(file, format='musicxml', forceSource=True)

        #initialize custom features
        #get parts
        parts = score.parts
        left_hand_stream = None
        right_hand_stream = None
        both_hands_stream = None
        left_hand_chords = None
        right_hand_chords = None
        both_hands_chords = None
        #only one part so assign one part to right hand
        if len(parts)<2:
            right_hand_stream = parts[0]
        #two or more parts
        else:
            #right hand is always the first staff
            right_hand_stream = parts[0]
            #assign left hand to stream that has the most notes
            left_hand_parts = parts[1:]
            sChords = left_hand_parts[0].chordify()
            sFlat = sChords.flat
            i = 0
            index = 0
            left_hand_index = 0
            left_hand_chords = sFlat.getElementsByClass('Chord')
    

            while index<len(left_hand_parts):
                left_hand_part = left_hand_parts[index]
                sChords = left_hand_part.chordify()
                sFlat = sChords.flat
                current = sFlat.getElementsByClass('Chord')
                if len(current)>len(left_hand_chords):
                    left_hand_chords = current
                    left_hand_index = index
                i+=1
                index+=1

            left_hand_stream = left_hand_parts[left_hand_index]
        #score contains both left and right hand
        score = stream.Score()
        score.insert(0,right_hand_stream)
        if left_hand_stream is not None:
            score.insert(0,left_hand_stream)
        both_hands_stream = score.getElementsByClass(stream.Part)

        #assign chords
        sChords = right_hand_stream.chordify()
        sFlat = sChords.flat
        right_hand_chords = sFlat.getElementsByClass('Chord')
        if left_hand_stream is not None:
            sChords = left_hand_stream.chordify()
            sFlat = sChords.flat
            left_hand_chords = sFlat.getElementsByClass('Chord')
        sChords = both_hands_stream.chordify()
        sFlat = sChords.flat
        both_hands_chords = sFlat.getElementsByClass('Chord')
    ####################################################################extract custom features
        #total notes as chords&&&&&&&&&&&&
        feature_values['total_RH_chords'] = len(right_hand_chords)
        
        left_notes_count = 0
        if left_hand_stream is not None:
            feature_values['total_LH_chords'] = len(left_hand_chords)  
        else:
            feature_values['total_LH_chords'] = 0
        
        feature_values['total_LRH_chords'] = feature_values['total_LH_chords'] + feature_values['total_RH_chords']

    
        
        
        feature_values['total_LRH_raw_notes'] = len(both_hands_stream.flat.pitches)
        if left_hand_stream is not None:
            feature_values['total_LH_raw_notes'] = len(left_hand_stream.flat.pitches)
        else:
            feature_values['total_LH_raw_notes'] = 0
        feature_values['total_RH_raw_notes'] = len(right_hand_stream.flat.pitches)

        #key signature:
        music_key = score.analyze('key')
        altered_pitches = music_key.alteredPitches
        temp_pitches = []
        for pitch in altered_pitches:
            temp_pitches.append(pitch.name)
        altered_pitches = temp_pitches

        feature_values['total_LRH_accidentals'] = self.totalAccidentals(both_hands_stream,altered_pitches)
        feature_values['total_RH_accidentals'] = self.totalAccidentals(right_hand_stream,altered_pitches)
        feature_values['total_LH_accidentals'] = self.totalAccidentals(left_hand_stream,altered_pitches)
        feature_values['average_LRH_accidentals'] = self.averageAccidentals(both_hands_stream,altered_pitches)
        feature_values['average_RH_accidentals'] = self.averageAccidentals(right_hand_stream,altered_pitches)
        feature_values['average_LH_accidentals'] = self.averageAccidentals(left_hand_stream,altered_pitches)

        feature_values['music_key'] = key_signatures[str(music_key)]

        feature_values['total_LRH_natural_keys_pressed'] = self.totalNaturalNotes(both_hands_stream)
        feature_values['total_LH_natural_keys_pressed'] = self.totalNaturalNotes(left_hand_stream)
        feature_values['total_R_natural_keys_pressed'] = self.totalNaturalNotes(right_hand_stream)
        #number of black keys pressed
        feature_values['total_LRH_sharp_keys_pressed'] = self.totalSharpNotes(both_hands_stream)
        feature_values['total_LH_sharp_keys_pressed'] = self.totalSharpNotes(left_hand_stream)
        feature_values['total_RH_sharp_keys_pressed'] = self.totalSharpNotes(right_hand_stream)
        # #number of flat keys pressed
        feature_values['total_LRH_flat_keys_pressed'] = self.totalFlatNotes(both_hands_stream)
        feature_values['total_LH_flat_keys_pressed'] = self.totalFlatNotes(left_hand_stream)
        feature_values['total_RH_flat_keys_pressed'] = self.totalFlatNotes(right_hand_stream)

        feature_values['average_LRH_natural_keys_pressed'] = self.averageNaturalNotes(both_hands_stream)
        feature_values['average_LH_natural_keys_pressed'] = self.averageNaturalNotes(left_hand_stream)
        feature_values['average_R_natural_keys_pressed'] = self.averageNaturalNotes(right_hand_stream)

        #number of black keys pressed
        feature_values['average_LRH_sharp_keys_pressed'] = self.averageSharpNotes(both_hands_stream)
        feature_values['average_LH_sharp_keys_pressed'] = self.averageSharpNotes(left_hand_stream)
        feature_values['average_RH_sharp_keys_pressed'] = self.averageSharpNotes(right_hand_stream)
        # #number of flat keys pressed
        feature_values['average_LRH_flat_keys_pressed'] = self.averageFlatNotes(both_hands_stream)
        feature_values['average_LH_flat_keys_pressed'] = self.averageFlatNotes(left_hand_stream)
        feature_values['average_RH_flat_keys_pressed'] = self.averageFlatNotes(right_hand_stream)


        feature_values['average2_range_for_next_notes_LH'] = self.average2RangeForNextNotes(left_hand_chords)
        feature_values['average2_range_for_next_notes_RH'] = self.average2RangeForNextNotes(right_hand_chords)
        feature_values['average2_range_for_next_notes_RLH'] = self.average2RangeForNextNotes(both_hands_chords)

        feature_values['average_range_for_next_notes_LH'] = self.averageRangeForNextNotes(left_hand_chords)
        feature_values['average_range_for_next_notes_RH'] = self.averageRangeForNextNotes(right_hand_chords)
        feature_values['average_range_for_next_notes_RLH'] = self.averageRangeForNextNotes(both_hands_chords)

        feature_values['average_density_RLH'] = self.averageDensity(both_hands_chords)
        feature_values['average_density_LH'] = self.averageDensity(left_hand_chords)
        feature_values['average_density_RH'] = self.averageDensity(right_hand_chords)

        #average range for top 10% percent of notes
        feature_values['average_range_of_top_x_percent10RLH'] = self.averageRangeOfTopXPercent(both_hands_chords,.1)
        feature_values['average_range_of_top_x_percent10LH'] = self.averageRangeOfTopXPercent(left_hand_chords,.1)
        feature_values['average_range_of_top_x_percent10RH'] = self.averageRangeOfTopXPercent(right_hand_chords,.1)
        #average range for top 20% percent of notes
        feature_values['average_range_of_top_x_percent20RLH'] = self.averageRangeOfTopXPercent(both_hands_chords,.2)
        feature_values['average_range_of_top_x_percent20LH'] = self.averageRangeOfTopXPercent(left_hand_chords,.2)
        feature_values['average_range_of_top_x_percent20RH'] = self.averageRangeOfTopXPercent(right_hand_chords,.2)
        #average range for top 35% percent of notes
        feature_values['average_range_of_top_x_percent35RLH'] = self.averageRangeOfTopXPercent(both_hands_chords,.35)
        feature_values['average_range_of_top_x_percent35LH'] = self.averageRangeOfTopXPercent(left_hand_chords,.35)
        feature_values['average_range_of_top_x_percent35RH'] = self.averageRangeOfTopXPercent(right_hand_chords,.35)
        #average range for top 50% percent of notes
        feature_values['average_range_of_top_x_percent50RLH'] = self.averageRangeOfTopXPercent(both_hands_chords,.5)
        feature_values['average_range_of_top_x_percent50LH'] = self.averageRangeOfTopXPercent(left_hand_chords,.5)
        feature_values['average_range_of_top_x_percent50RH'] = self.averageRangeOfTopXPercent(right_hand_chords,.5)

        feature_values['average_range_of_top_x_percent75RLH'] = self.averageRangeOfTopXPercent(both_hands_chords,.75)
        feature_values['average_range_of_top_x_percent75LH'] = self.averageRangeOfTopXPercent(left_hand_chords,.75)
        feature_values['average_range_of_top_x_percent75RH'] = self.averageRangeOfTopXPercent(right_hand_chords,.75)
        #average range for top 100% percent of notes*******
        feature_values['average_range_of_top_x_percent100RLH'] = self.averageRangeOfTopXPercent(both_hands_chords,1)
        feature_values['average_range_of_top_x_percent100LH'] = self.averageRangeOfTopXPercent(left_hand_chords,1)
        feature_values['average_range_of_top_x_percent100RH'] = self.averageRangeOfTopXPercent(right_hand_chords,1)

        feature_values['fake_range_of_top_x_percent10LH'] = self.fakeRangeOfTopXPercent(left_hand_chords, .1)
        feature_values['fake_range_of_top_x_percent10RH'] = self.fakeRangeOfTopXPercent(right_hand_chords, .1)
        feature_values['fake_range_of_top_x_percent10RLH'] = self.fakeRangeOfTopXPercent(both_hands_chords, .1)

        feature_values['fake_range_of_top_x_percent20LH'] = self.fakeRangeOfTopXPercent(left_hand_chords, .2)
        feature_values['fake_range_of_top_x_percent20RH'] = self.fakeRangeOfTopXPercent(right_hand_chords, .2)
        feature_values['fake_range_of_top_x_percent20RLH'] = self.fakeRangeOfTopXPercent(both_hands_chords, .2)

        feature_values['fake_range_of_top_x_percent35LH'] = self.fakeRangeOfTopXPercent(left_hand_chords, .35)
        feature_values['fake_range_of_top_x_percent35RH'] = self.fakeRangeOfTopXPercent(right_hand_chords, .35)
        feature_values['fake_range_of_top_x_percent35RLH'] = self.fakeRangeOfTopXPercent(both_hands_chords, .35)

        feature_values['fake_range_of_top_x_percent50LH'] = self.fakeRangeOfTopXPercent(left_hand_chords, .5)
        feature_values['fake_range_of_top_x_percent50RH'] = self.fakeRangeOfTopXPercent(right_hand_chords, .5)
        feature_values['fake_range_of_top_x_percent50RLH'] = self.fakeRangeOfTopXPercent(both_hands_chords, .5)

        feature_values['fake_range_of_top_x_percent75LH'] = self.fakeRangeOfTopXPercent(left_hand_chords, .75)
        feature_values['fake_range_of_top_x_percent75RH'] = self.fakeRangeOfTopXPercent(right_hand_chords, .75)
        feature_values['fake_range_of_top_x_percent75RLH'] = self.fakeRangeOfTopXPercent(both_hands_chords, .75)

        feature_values['fake_range_of_top_x_percent100LH'] = self.fakeRangeOfTopXPercent(left_hand_chords, 1)
        feature_values['fake_range_of_top_x_percent100RH'] = self.fakeRangeOfTopXPercent(right_hand_chords, 1)
        feature_values['fake_range_of_top_x_percent100RLH'] = self.fakeRangeOfTopXPercent(both_hands_chords, 1)

        feature_values['range_of_top_x_percent10LH'] = self.rangeOfTopXPercent(left_hand_stream,.1)
        feature_values['range_of_top_x_percent10RH'] = self.rangeOfTopXPercent(right_hand_stream,.1)
        feature_values['range_of_top_x_percent10RLH'] = self.rangeOfTopXPercent(both_hands_stream,.1)

        feature_values['range_of_top_x_percent20LH'] = self.rangeOfTopXPercent(left_hand_stream,.2)
        feature_values['range_of_top_x_percent20RH'] = self.rangeOfTopXPercent(right_hand_stream,.2)
        feature_values['range_of_top_x_percent20RLH'] = self.rangeOfTopXPercent(both_hands_stream,.2)

        feature_values['range_of_top_x_percent35LH'] = self.rangeOfTopXPercent(left_hand_stream,.35)
        feature_values['range_of_top_x_percent35RH'] = self.rangeOfTopXPercent(right_hand_stream,.35)
        feature_values['range_of_top_x_percent35RLH'] = self.rangeOfTopXPercent(both_hands_stream,.35)

        feature_values['range_of_top_x_percent50LH'] = self.rangeOfTopXPercent(left_hand_stream,.50)
        feature_values['range_of_top_x_percent50RH'] = self.rangeOfTopXPercent(right_hand_stream,.50)
        feature_values['range_of_top_x_percent50RLH'] = self.rangeOfTopXPercent(both_hands_stream,.50)

        feature_values['range_of_top_x_percent75LH'] = self.rangeOfTopXPercent(left_hand_stream,.75)
        feature_values['range_of_top_x_percent75RH'] = self.rangeOfTopXPercent(right_hand_stream,.75)
        feature_values['range_of_top_x_percent75RLH'] = self.rangeOfTopXPercent(both_hands_stream,.75)

        feature_values['range_of_top_x_percent100LH'] = self.rangeOfTopXPercent(left_hand_stream,1)
        feature_values['range_of_top_x_percent100RH'] = self.rangeOfTopXPercent(right_hand_stream,1)
        feature_values['range_of_top_x_percent100RLH'] = self.rangeOfTopXPercent(both_hands_stream,1)
        


        #average range for each finger in chord
        # feature_values['average_LRH_2chord_range'] = averageChordRangeForHand(both_hands_chords,2)
        feature_values['average_chord_range_for_hand2LH'] = self.averageChordRangeForHand(left_hand_chords,2)
        feature_values['average_chord_range_for_hand2RH'] = self.averageChordRangeForHand(right_hand_chords,2)

        # feature_values['average_LRH_3chord_range'] = averageChordRangeForHand(both_hands_chords,3)
        feature_values['average_chord_range_for_hand3LH'] = self.averageChordRangeForHand(left_hand_chords,3)
        feature_values['average_chord_range_for_hand3RH'] = self.averageChordRangeForHand(right_hand_chords,3)

        # feature_values['average_LRH_4chord_range'] = averageChordRangeForHand(both_hands_chords,4)
        feature_values['average_chord_range_for_hand4LH'] = self.averageChordRangeForHand(left_hand_chords,4)
        feature_values['average_chord_range_for_hand4RH'] = self.averageChordRangeForHand(right_hand_chords,4)

        # feature_values['average_LRH_5chord_range'] = averageChordRangeForHand(both_hands_chords,5)
        feature_values['average_chord_range_for_hand5LH'] = self.averageChordRangeForHand(left_hand_chords,5)
        feature_values['average_chord_range_for_hand5RH'] = self.averageChordRangeForHand(right_hand_chords,5)



        # feature_values['average_LRH_2chord_range'] = averageChordRangeForHand(both_hands_chords,2)
        feature_values['average_chord_plus_range_for_hand2LH'] = self.averageChordPlusRangeForHand(left_hand_chords,2)
        feature_values['average_chord_plus_range_for_hand2RH'] = self.averageChordPlusRangeForHand(right_hand_chords,2)

        # feature_values['average_LRH_3chord_range'] = averageChordRangeForHand(both_hands_chords,3)
        feature_values['average_chord_plus_range_for_hand3LH'] = self.averageChordPlusRangeForHand(left_hand_chords,3)
        feature_values['average_chord_plus_range_for_hand3RH'] = self.averageChordPlusRangeForHand(right_hand_chords,3)

        # feature_values['average_LRH_4chord_range'] = averageChordRangeForHand(both_hands_chords,4)
        feature_values['average_chord_plus_range_for_hand4LH'] = self.averageChordPlusRangeForHand(left_hand_chords,4)
        feature_values['average_chord_plus_range_for_hand4RH'] = self.averageChordPlusRangeForHand(right_hand_chords,4)

        # feature_values['average_LRH_5chord_range'] = averageChordRangeForHand(both_hands_chords,5)
        feature_values['average_chord_plus_range_for_hand5LH'] = self.averageChordPlusRangeForHand(left_hand_chords,5)
        feature_values['average_chord_plus_range_for_hand5RH'] = self.averageChordPlusRangeForHand(right_hand_chords,5)

        

        # feature_values['average_LRH_2chord_range'] = averageChordRangeForHand(both_hands_chords,2)
        feature_values['weighted_average_chord_range_for_hand2LH'] = self.weightedAverageChordRangeForHand(left_hand_chords,2)
        feature_values['weighted_average_chord_range_for_hand2RH'] = self.weightedAverageChordRangeForHand(right_hand_chords,2)

        # feature_values['average_LRH_3chord_range'] = averageChordRangeForHand(both_hands_chords,3)
        feature_values['weighted_average_chord_range_for_hand3LH'] = self.weightedAverageChordRangeForHand(left_hand_chords,3)
        feature_values['weighted_average_chord_range_for_hand3RH'] = self.weightedAverageChordRangeForHand(right_hand_chords,3)

        # feature_values['average_LRH_4chord_range'] = averageChordRangeForHand(both_hands_chords,4)
        feature_values['weighted_average_chord_range_for_hand4LH'] = self.weightedAverageChordRangeForHand(left_hand_chords,4)
        feature_values['weighted_average_chord_range_for_hand4RH'] = self.weightedAverageChordRangeForHand(right_hand_chords,4)

        # feature_values['average_LRH_5chord_range'] = averageChordRangeForHand(both_hands_chords,5)
        feature_values['weighted_average_chord_range_for_hand5LH'] = self.weightedAverageChordRangeForHand(left_hand_chords,5)
        feature_values['weighted_average_chord_range_for_hand5RH'] = self.weightedAverageChordRangeForHand(right_hand_chords,5)




        # feature_values['average_LRH_2chord_range'] = averageChordRangeForHand(both_hands_chords,2)
        feature_values['weighted_average_chord_plus_range_for_hand2LH'] = self.weightedAverageChordPlusRangeForHand(left_hand_chords,2)
        feature_values['weighted_average_chord_plus_range_for_hand2RH'] = self.weightedAverageChordPlusRangeForHand(right_hand_chords,2)

        # feature_values['average_LRH_3chord_range'] = averageChordRangeForHand(both_hands_chords,3)
        feature_values['weighted_average_chord_plus_range_for_hand3LH'] = self.weightedAverageChordPlusRangeForHand(left_hand_chords,3)
        feature_values['weighted_average_chord_plus_range_for_hand3RH'] = self.weightedAverageChordPlusRangeForHand(right_hand_chords,3)

        # feature_values['average_LRH_4chord_range'] = averageChordRangeForHand(both_hands_chords,4)
        feature_values['weighted_average_chord_plus_range_for_hand4LH'] = self.weightedAverageChordPlusRangeForHand(left_hand_chords,4)
        feature_values['weighted_average_chord_plus_range_for_hand4RH'] = self.weightedAverageChordPlusRangeForHand(right_hand_chords,4)

        # feature_values['average_LRH_5chord_range'] = averageChordRangeForHand(both_hands_chords,5)
        feature_values['weighted_average_chord_plus_range_for_hand5LH'] = self.weightedAverageChordPlusRangeForHand(left_hand_chords,5)
        feature_values['weighted_average_chord_plus_range_for_hand5RH'] = self.weightedAverageChordPlusRangeForHand(right_hand_chords,5)



        #average range for each hand*****
        # feature_values['average_LRH_2chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,2)
        feature_values['average_2_chord_range_for_hand2LH'] = self.average2ChordRangeForHand(left_hand_chords,2)
        feature_values['average_2_chord_range_for_hand2RH'] = self.average2ChordRangeForHand(right_hand_chords,2)

        # feature_values['average_LRH_3chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,3)
        feature_values['average_2_chord_range_for_hand3LH'] = self.average2ChordRangeForHand(left_hand_chords,3)
        feature_values['average_2_chord_range_for_hand3RH'] = self.average2ChordRangeForHand(right_hand_chords,3)

        # feature_values['average_LRH_4chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,4)
        feature_values['average_2_chord_range_for_hand4LH'] = self.average2ChordRangeForHand(left_hand_chords,4)
        feature_values['average_2_chord_range_for_hand4RH'] = self.average2ChordRangeForHand(right_hand_chords,4)

        # feature_values['average_LRH_5chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,5)
        feature_values['average_2_chord_range_for_hand5LH'] = self.average2ChordRangeForHand(left_hand_chords,5)
        feature_values['average_2_chord_range_for_hand5RH'] = self.average2ChordRangeForHand(right_hand_chords,5)


        # feature_values['average_LRH_2chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,2)
        feature_values['weighted_average2_chord_range_for_hand2LH'] = self.weightedAverage2ChordRangeForHand(left_hand_chords,2)
        feature_values['weighted_average2_chord_range_for_hand2RH'] = self.weightedAverage2ChordRangeForHand(right_hand_chords,2)

        # feature_values['average_LRH_3chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,3)
        feature_values['weighted_average2_chord_range_for_hand3LH'] = self.weightedAverage2ChordRangeForHand(left_hand_chords,3)
        feature_values['weighted_average2_chord_range_for_hand3RH'] = self.weightedAverage2ChordRangeForHand(right_hand_chords,3)

        # feature_values['average_LRH_4chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,4)
        feature_values['weighted_average2_chord_range_for_hand4LH'] = self.weightedAverage2ChordRangeForHand(left_hand_chords,4)
        feature_values['weighted_average2_chord_range_for_hand4RH'] = self.weightedAverage2ChordRangeForHand(right_hand_chords,4)

        # feature_values['average_LRH_5chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,5)
        feature_values['weighted_average2_chord_range_for_hand5LH'] = self.weightedAverage2ChordRangeForHand(left_hand_chords,5)
        feature_values['weighted_average2_chord_range_for_hand5RH'] = self.weightedAverage2ChordRangeForHand(right_hand_chords,5)


        # feature_values['average_LRH_2chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,2)
        feature_values['average_2_chord_plus_range_for_hand2LH'] = self.average2ChordPlusRangeForHand(left_hand_chords,2)
        feature_values['average_2_chord_plus_range_for_hand2RH'] = self.average2ChordPlusRangeForHand(right_hand_chords,2)

        # feature_values['average_LRH_3chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,3)
        feature_values['average_2_chord_plus_range_for_hand3LH'] = self.average2ChordPlusRangeForHand(left_hand_chords,3)
        feature_values['average_2_chord_plus_range_for_hand3RH'] = self.average2ChordPlusRangeForHand(right_hand_chords,3)

        # feature_values['average_LRH_4chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,4)
        feature_values['average_2_chord_plus_range_for_hand4LH'] = self.average2ChordPlusRangeForHand(left_hand_chords,4)
        feature_values['average_2_chord_plus_range_for_hand4RH'] = self.average2ChordPlusRangeForHand(right_hand_chords,4)

        # feature_values['average_LRH_5chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,5)
        feature_values['average_2_chord_plus_range_for_hand5LH'] = self.average2ChordPlusRangeForHand(left_hand_chords,5)
        feature_values['average_2_chord_plus_range_for_hand5RH'] = self.average2ChordPlusRangeForHand(right_hand_chords,5)

        # feature_values['average_LRH_2chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,2)
        feature_values['weighted_average_2_chord_plus_range_for_hand2LH'] = self.weightedAverage2ChordPlusRangeForHand(left_hand_chords,2)
        feature_values['weighted_average_2_chord_plus_range_for_hand2RH'] = self.weightedAverage2ChordPlusRangeForHand(right_hand_chords,2)

        # feature_values['average_LRH_3chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,3)
        feature_values['weighted_average_2_chord_plus_range_for_hand3LH'] = self.weightedAverage2ChordPlusRangeForHand(left_hand_chords,3)
        feature_values['weighted_average_2_chord_plus_range_for_hand3RH'] = self.weightedAverage2ChordPlusRangeForHand(right_hand_chords,3)

        # feature_values['average_LRH_4chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,4)
        feature_values['weighted_average_2_chord_plus_range_for_hand4LH'] = self.weightedAverage2ChordPlusRangeForHand(left_hand_chords,4)
        feature_values['weighted_average_2_chord_plus_range_for_hand4RH'] = self.weightedAverage2ChordPlusRangeForHand(right_hand_chords,4)

        # feature_values['average_LRH_5chord_hand_range'] = average2ChordRangeForHand(both_hands_chords,5)
        feature_values['weighted_average_2_chord_plus_range_for_hand5LH'] = self.weightedAverage2ChordPlusRangeForHand(left_hand_chords,5)
        feature_values['weighted_average_2_chord_plus_range_for_hand5RH'] = self.weightedAverage2ChordPlusRangeForHand(right_hand_chords,5)



        #large jumps
        feature_values['large_jumps5RLH'] = self.largeJumps(both_hands_chords,5)
        feature_values['large_jumps5LH'] = self.largeJumps(left_hand_chords,5)
        feature_values['large_jumps5RH'] = self.largeJumps(right_hand_chords,5)

        feature_values['large_jumps7RLH'] = self.largeJumps(both_hands_chords,7)
        feature_values['large_jumps7LH'] = self.largeJumps(left_hand_chords,7)
        feature_values['large_jumps7RH'] = self.largeJumps(right_hand_chords,7)

        feature_values['large_jumps8RLH'] = self.largeJumps(both_hands_chords,8)
        feature_values['large_jumps8LH'] = self.largeJumps(left_hand_chords,8)
        feature_values['large_jumps8RH'] = self.largeJumps(right_hand_chords,8)

        feature_values['large_jumps9RLH'] = self.largeJumps(both_hands_chords,9)
        feature_values['large_jumps9LH'] = self.largeJumps(left_hand_chords,9)
        feature_values['large_jumps9RH'] = self.largeJumps(right_hand_chords,9)

        feature_values['large_jumps10RLH'] = self.largeJumps(both_hands_chords,10)
        feature_values['large_jumps10LH'] = self.largeJumps(left_hand_chords,10)
        feature_values['large_jumps10RH'] = self.largeJumps(right_hand_chords,10)

        #average large jumps*****
        feature_values['average_large_jumps5RLH'] = self.averageLargeJump(both_hands_chords,5)
        feature_values['average_large_jumps5LH'] = self.averageLargeJump(left_hand_chords,5)
        feature_values['average_large_jumps5RH'] = self.averageLargeJump(right_hand_chords,5)

        feature_values['average_large_jumps7RLH'] = self.averageLargeJump(both_hands_chords,7)
        feature_values['average_large_jumps7LH'] = self.averageLargeJump(left_hand_chords,7)
        feature_values['average_large_jumps7RH'] = self.averageLargeJump(right_hand_chords,7)

        feature_values['average_large_jumps8RLH'] = self.averageLargeJump(both_hands_chords,8)
        feature_values['average_large_jumps8LH'] = self.averageLargeJump(left_hand_chords,8)
        feature_values['average_large_jumps8RH'] = self.averageLargeJump(right_hand_chords,8)

        feature_values['average_large_jumps9RLH'] = self.averageLargeJump(both_hands_chords,9)
        feature_values['average_large_jumps9LH'] = self.averageLargeJump(left_hand_chords,9)
        feature_values['average_large_jumps9RH'] = self.averageLargeJump(right_hand_chords,9)

        feature_values['average_large_jumps10RLH'] = self.averageLargeJump(both_hands_chords,10)
        feature_values['average_large_jumps10LH'] = self.averageLargeJump(left_hand_chords,10)
        feature_values['average_large_jumps10RH'] = self.averageLargeJump(right_hand_chords,10)

        #average large jumps*****
        feature_values['average_large_jump_values5RLH'] = self.averageLargeJumpValues(both_hands_chords,5)
        feature_values['average_large_jump_values5LH'] = self.averageLargeJumpValues(left_hand_chords,5)
        feature_values['average_large_jump_values5RH'] = self.averageLargeJumpValues(right_hand_chords,5)

        feature_values['average_large_jump_values7RLH'] = self.averageLargeJumpValues(both_hands_chords,7)
        feature_values['average_large_jump_values7LH'] = self.averageLargeJumpValues(left_hand_chords,7)
        feature_values['average_large_jump_values7RH'] = self.averageLargeJumpValues(right_hand_chords,7)

        feature_values['average_large_jump_values8RLH'] = self.averageLargeJumpValues(both_hands_chords,8)
        feature_values['average_large_jump_values8LH'] = self.averageLargeJumpValues(left_hand_chords,8)
        feature_values['average_large_jump_values8RH'] = self.averageLargeJumpValues(right_hand_chords,8)

        feature_values['average_large_jump_values9RLH'] = self.averageLargeJumpValues(both_hands_chords,9)
        feature_values['average_large_jump_values9LH'] = self.averageLargeJumpValues(left_hand_chords,9)
        feature_values['average_large_jump_values9RH'] = self.averageLargeJumpValues(right_hand_chords,9)

        feature_values['average_large_jump_values10RLH'] = self.averageLargeJumpValues(both_hands_chords,10)
        feature_values['average_large_jump_values10LH'] = self.averageLargeJumpValues(left_hand_chords,10)
        feature_values['average_large_jump_values10RH'] = self.averageLargeJumpValues(right_hand_chords,10)


        feature_values['weighted_average_large_jump_values5RLH'] = self.weightedAverageLargeJumpValues(both_hands_chords,5)
        feature_values['weighted_average_large_jump_values5LH'] = self.weightedAverageLargeJumpValues(left_hand_chords,5)
        feature_values['weighted_average_large_jump_values5RH'] = self.weightedAverageLargeJumpValues(right_hand_chords,5)

        feature_values['weighted_average_large_jump_values7RLH'] = self.weightedAverageLargeJumpValues(both_hands_chords,7)
        feature_values['weighted_average_large_jump_values7LH'] = self.weightedAverageLargeJumpValues(left_hand_chords,7)
        feature_values['weighted_average_large_jump_values7RH'] = self.weightedAverageLargeJumpValues(right_hand_chords,7)

        feature_values['weighted_average_large_jump_values8RLH'] = self.weightedAverageLargeJumpValues(both_hands_chords,8)
        feature_values['weighted_average_large_jump_values8LH'] = self.weightedAverageLargeJumpValues(left_hand_chords,8)
        feature_values['weighted_average_large_jump_values8RH'] = self.weightedAverageLargeJumpValues(right_hand_chords,8)

        feature_values['weighted_average_large_jump_values9RLH'] = self.weightedAverageLargeJumpValues(both_hands_chords,9)
        feature_values['weighted_average_large_jump_values9LH'] = self.weightedAverageLargeJumpValues(left_hand_chords,9)
        feature_values['weighted_average_large_jump_values9RH'] = self.weightedAverageLargeJumpValues(right_hand_chords,9)

        feature_values['weighted_average_large_jump_values10RLH'] = self.weightedAverageLargeJumpValues(both_hands_chords,10)
        feature_values['weighted_average_large_jump_values10LH'] = self.weightedAverageLargeJumpValues(left_hand_chords,10)
        feature_values['weighted_average_large_jump_values10RH'] = self.weightedAverageLargeJumpValues(right_hand_chords,10)

    

        #note type total count
        feature_values['total_LRHwhole_notes'] = self.totalWholeNotes(both_hands_stream)
        feature_values['total_LRHhalf_notes'] = self.totalHalfNotes(both_hands_stream)
        feature_values['total_LRHquarter_notes'] = self.totalQuarterNotes(both_hands_stream)
        feature_values['total_LRHeighth_notes'] = self.totalEighthNotes(both_hands_stream)
        feature_values['total_LRH16th_notes'] = self.total16thNotes(both_hands_stream)
        feature_values['total_LRH32nd_notes'] = self.total32ndNotes(both_hands_stream)
        feature_values['total_LRH64th_notes'] = self.total64thNotes(both_hands_stream)
        feature_values['total_LHwhole_notes'] = self.totalWholeNotes(left_hand_stream)
        feature_values['total_LHhalf_notes'] = self.totalHalfNotes(left_hand_stream)
        feature_values['total_LHquarter_notes'] = self.totalQuarterNotes(left_hand_stream)
        feature_values['total_LHeighth_notes'] = self.totalEighthNotes(left_hand_stream)
        feature_values['total_LH16th_notes'] = self.total16thNotes(left_hand_stream)
        feature_values['total_LH32nd_notes'] = self.total32ndNotes(left_hand_stream)
        feature_values['total_LH64th_notes'] = self.total64thNotes(left_hand_stream)
        feature_values['total_RHwhole_notes'] = self.totalWholeNotes(right_hand_stream)
        feature_values['total_RHhalf_notes'] = self.totalHalfNotes(right_hand_stream)
        feature_values['total_RHquarter_notes'] = self.totalQuarterNotes(right_hand_stream)
        feature_values['total_RHeighth_notes'] = self.totalEighthNotes(right_hand_stream)
        feature_values['total_RH16th_notes'] = self.total16thNotes(right_hand_stream)
        feature_values['total_RH32nd_notes'] = self.total32ndNotes(right_hand_stream)
        feature_values['total_RH64th_notes'] = self.total64thNotes(right_hand_stream)

        #note type average
        feature_values['average_LRHwhole_notes'] = self.averageWholeNotes(both_hands_stream)
        feature_values['average_LRHhalf_ntoes'] = self.averageHalfNotes(both_hands_stream)
        feature_values['average_LRHquarter_notes'] = self.averageQuarterNotes(both_hands_stream)
        feature_values['average_LRHeighth_notes'] = self.averageEighthNotes(both_hands_stream)
        feature_values['average_LRH16th_notes'] = self.average16thNotes(both_hands_stream)
        feature_values['average_LRH32nd_notes'] = self.average32ndNotes(both_hands_stream)
        feature_values['average_LRH64th_notes'] = self.average64thNotes(both_hands_stream)
        feature_values['average_LHwhole_notes'] = self.averageWholeNotes(left_hand_stream)
        feature_values['average_LHhalf_ntoes'] = self.averageHalfNotes(left_hand_stream)
        feature_values['average_LHquarter_notes'] = self.averageQuarterNotes(left_hand_stream)
        feature_values['average_LHeighth_notes'] = self.averageEighthNotes(left_hand_stream)
        feature_values['average_LH16th_notes'] = self.average16thNotes(left_hand_stream)
        feature_values['average_LH32nd_notes'] = self.average32ndNotes(left_hand_stream)
        feature_values['average_LH64th_notes'] = self.average64thNotes(left_hand_stream)
        feature_values['average_RHwhole_notes'] = self.averageWholeNotes(right_hand_stream)
        feature_values['average_RHhalf_ntoes'] = self.averageHalfNotes(right_hand_stream)
        feature_values['average_RHquarter_notes'] = self.averageQuarterNotes(right_hand_stream)
        feature_values['average_RHeighth_notes'] = self.averageEighthNotes(right_hand_stream)
        feature_values['average_RH16th_notes'] = self.average16thNotes(right_hand_stream)
        feature_values['average_RH32nd_notes'] = self.average32ndNotes(right_hand_stream)
        feature_values['average_RH64th_notes'] = self.average64thNotes(right_hand_stream)

        paths = []

        #score contains both left and right hand
        scoreRL = stream.Score()
        scoreR = stream.Score()

        scoreL = None
        scoreR.insert(0,right_hand_stream)
        scoreRL.insert(0,right_hand_stream)
        
        if left_hand_stream is not None:
            scoreL = stream.Score()
            scoreL.insert(0,left_hand_stream)
            scoreRL.insert(0,left_hand_stream)
    
        #scoreL.show()
        # feature_values["Right Hand Similarity"] = similarityBetween1Score(scoreR,file)
        
    
        #right_hand_chords.show()
        feature_values["total_x_chord_plus_notes2RH"] = self.totalXChordPlusNotes(right_hand_chords,2)
        feature_values["total_x_chord_plus_notes3RH"] = self.totalXChordPlusNotes(right_hand_chords,3)
        feature_values["total_x_chord_plus_notes4RH"] = self.totalXChordPlusNotes(right_hand_chords,4)
        feature_values["total_x_chord_plus_notes5RH"] = self.totalXChordPlusNotes(right_hand_chords,5)
        feature_values["total_x_chord_plus_notes2LH"] = self.totalXChordPlusNotes(left_hand_chords,2)
        feature_values["total_x_chord_plus_notes3LH"] = self.totalXChordPlusNotes(left_hand_chords,3)
        feature_values["total_x_chord_plus_notes4LH"] = self.totalXChordPlusNotes(left_hand_chords,4)
        feature_values["total_x_chord_plus_notes5LH"] = self.totalXChordPlusNotes(left_hand_chords,5)

        feature_values["average_x_chord_plus_notes2RH"] = self.averageXChordPlusNotes(right_hand_chords,2)
        feature_values["average_x_chord_plus_notes3RH"] = self.averageXChordPlusNotes(right_hand_chords,3)
        feature_values["average_x_chord_plus_notes4RH"] = self.averageXChordPlusNotes(right_hand_chords,4)
        feature_values["average_x_chord_plus_notes5RH"] = self.averageXChordPlusNotes(right_hand_chords,5)
        feature_values["average_x_chord_plus_notes2LH"] = self.averageXChordPlusNotes(left_hand_chords,2)
        feature_values["average_x_chord_plus_notes3LH"] = self.averageXChordPlusNotes(left_hand_chords,3)
        feature_values["average_x_chord_plus_notes4LH"] = self.averageXChordPlusNotes(left_hand_chords,4)
        feature_values["average_x_chord_plus_notes5LH"] = self.averageXChordPlusNotes(left_hand_chords,5)

        feature_values["total_x_chord_notes2RH"] = self.totalXChordNotes(right_hand_chords,2)
        feature_values["total_x_chord_notes3RH"] = self.totalXChordNotes(right_hand_chords,3)
        feature_values["total_x_chord_notes4RH"] = self.totalXChordNotes(right_hand_chords,4)
        feature_values["total_x_chord_notes5RH"] = self.totalXChordNotes(right_hand_chords,5)
        feature_values["total_x_chord_notes2LH"] = self.totalXChordNotes(left_hand_chords,2)
        feature_values["total_x_chord_notes3LH"] = self.totalXChordNotes(left_hand_chords,3)
        feature_values["total_x_chord_notes4LH"] = self.totalXChordNotes(left_hand_chords,4)
        feature_values["total_x_chord_notes5LH"] = self.totalXChordNotes(left_hand_chords,5)

        feature_values["average_x_chord_notes2RH"] = self.averageXChordNotes(right_hand_chords,2)
        feature_values["average_x_chord_notes3RH"] = self.averageXChordNotes(right_hand_chords,3)
        feature_values["average_x_chord_notes4RH"] = self.averageXChordNotes(right_hand_chords,4)
        feature_values["average_x_chord_notes5RH"] = self.averageXChordNotes(right_hand_chords,5)
        feature_values["average_x_chord_notes2LH"] = self.averageXChordNotes(left_hand_chords,2)
        feature_values["average_x_chord_notes3LH"] = self.averageXChordNotes(left_hand_chords,3)
        feature_values["average_x_chord_notes4LH"] = self.averageXChordNotes(left_hand_chords,4)
        feature_values["average_x_chord_notes5LH"] = self.averageXChordNotes(left_hand_chords,5)

    
        if scoreL is not None:
            # feature_values["Left Hand Similarity"] = similarityBetween1Score(scoreL,file)
            #similarity of both hands at the same time

            # feature_values["Both Hand Similarity"] = similarityBetween1Score(scoreRL,file)
            #similarity of left hand with right hand
            # feature_values["Left Right Hand Similarity"] = similarityBetween2Score(scoreL,scoreR,file)
            #rhythmic similarity
            feature_values["rhythm_similarityRLH"] = self.rhythmSimilarity(scoreL,scoreR)
            #advanced rhythmic similarity
            feature_values["advanced_rhythmic_similarityR"] = self.advancedRhythmSimilarity(scoreR)
            feature_values["advanced_rhythmic_similarityLH"] = self.advancedRhythmSimilarity(scoreL)
            #advanced rhythmic similarity for left and right hand,score1 search for, score 2 search
            feature_values["advanced_rhythmic_similarityRLH"] = self.advancedRhythm2Similarity(scoreL,scoreR)
            #total X notes in left hand
            
        else:
            feature_values["rhythm_similarityRLH"] = 0
            #advanced rhythmic similarity
            feature_values["advanced_rhythmic_similarityLH"] = 0
            #advanced rhythmic similarity for left and right hand,score1 search for, score 2 search
            feature_values["advanced_rhythmic_similarityRLH"] = 0
            #total X notes in right hand
        

        try:
            feature_values['UniqueSetClassSimultaneities'] = features.native.UniqueSetClassSimultaneities(score).extract().vector[0]
        except:
            feature_values['UniqueSetClassSimultaneities']= 0
        try:
            feature_values['UniquePitchClassSetSimultaneities'] = features.native.UniquePitchClassSetSimultaneities(score).extract().vector[0]
        except:
            feature_values['UniquePitchClassSetSimultaneities']= 0
        try:
            feature_values['UniqueNoteQuarterLengths'] = features.native.UniqueNoteQuarterLengths(score).extract().vector[0]
        except:
            feature_values['UniqueNoteQuarterLengths']= 0
        try:
            feature_values['TriadSimultaneityPrevalence'] = features.native.TriadSimultaneityPrevalence(score).extract().vector[0]
        except:
            feature_values['TriadSimultaneityPrevalence']= 0
        try:
            feature_values['TonalCertainty'] = features.native.TonalCertainty(score).extract().vector[0]
        except:
            feature_values['TonalCertainty']= 0
        try:
            feature_values['RangeOfNoteQuarterLengths'] = features.native.RangeOfNoteQuarterLengths(score).extract().vector[0]
        except:
            feature_values['RangeOfNoteQuarterLengths']= 0
        try:
            feature_values['MostCommonSetClassSimultaneityPrevalence'] = features.native.MostCommonSetClassSimultaneityPrevalence(score).extract().vector[0]
        except:
            feature_values['MostCommonSetClassSimultaneityPrevalence']= 0
        try:
            feature_values['MostCommonPitchClassSetSimultaneityPrevalence'] = features.native.MostCommonPitchClassSetSimultaneityPrevalence(score).extract().vector[0]
        except:
            feature_values['MostCommonPitchClassSetSimultaneityPrevalence']= 0
        try:
            feature_values['MostCommonNoteQuarterLengthPrevalence'] = features.native.MostCommonNoteQuarterLengthPrevalence(score).extract().vector[0]
        except:
            feature_values['MostCommonNoteQuarterLengthPrevalence']= 0
        try:
            feature_values['MostCommonNoteQuarterLength'] = features.native.MostCommonNoteQuarterLength(score).extract().vector[0]
        except:
            feature_values['MostCommonNoteQuarterLength']= 0
        try:
            feature_values['MinorTriadSimultaneityPrevalence'] = features.native.MinorTriadSimultaneityPrevalence(score).extract().vector[0]
        except:
            feature_values['MinorTriadSimultaneityPrevalence']= 0
        try:
            feature_values['MajorTriadSimultaneityPrevalence'] = features.native.MajorTriadSimultaneityPrevalence(score).extract().vector[0]
        except:
            feature_values['MajorTriadSimultaneityPrevalence']= 0
        try:
            feature_values['DominantSeventhSimultaneityPrevalence'] = features.native.DominantSeventhSimultaneityPrevalence(score).extract().vector[0]
        except:
            feature_values['DominantSeventhSimultaneityPrevalence']= 0
        try:
            feature_values['DiminishedTriadSimultaneityPrevalence'] = features.native.DiminishedTriadSimultaneityPrevalence(score).extract().vector[0]
        except:
            feature_values['DiminishedTriadSimultaneityPrevalence']= 0
        try:
            feature_values['DiminishedSeventhSimultaneityPrevalence'] = features.native.DiminishedSeventhSimultaneityPrevalence(score).extract().vector[0]
        except:
            feature_values['DiminishedSeventhSimultaneityPrevalence']= 0
        try:
            feature_values['VariabilityOfNumberOfIndependentVoicesFeature'] = features.jSymbolic.VariabilityOfNumberOfIndependentVoicesFeature(score).extract().vector[0]
        except:
            feature_values['VariabilityOfNumberOfIndependentVoicesFeature']= 0
        try:
            feature_values['VariabilityOfTimeBetweenAttacksFeature'] = features.jSymbolic.VariabilityOfTimeBetweenAttacksFeature(score).extract().vector[0]
        except:
            feature_values['VariabilityOfTimeBetweenAttacksFeature']= 0
        try:
            feature_values['VariabilityOfNoteDurationFeature'] = features.jSymbolic.VariabilityOfNoteDurationFeature(score).extract().vector[0]
        except:
            feature_values['VariabilityOfNoteDurationFeature']= 0
        try:
            feature_values['StrongestRhythmicPulseFeature'] = features.jSymbolic.StrongestRhythmicPulseFeature(score).extract().vector[0]
        except:
            feature_values['StrongestRhythmicPulseFeature']= 0
        try:
            feature_values['StrengthRatioOfTwoStrongestRhythmicPulsesFeature'] = features.jSymbolic.StrengthRatioOfTwoStrongestRhythmicPulsesFeature(score).extract().vector[0]
        except:
            feature_values['StrengthRatioOfTwoStrongestRhythmicPulsesFeature']= 0
        try:
            feature_values['StrengthOfStrongestRhythmicPulseFeature'] = features.jSymbolic.StrengthOfStrongestRhythmicPulseFeature(score).extract().vector[0]
        except:
            feature_values['StrengthOfStrongestRhythmicPulseFeature']= 0
        try:
            feature_values['StrengthOfSecondStrongestRhythmicPulseFeature'] = features.jSymbolic.StrengthOfSecondStrongestRhythmicPulseFeature(score).extract().vector[0]
        except:
            feature_values['StrengthOfSecondStrongestRhythmicPulseFeature']= 0
        try:
            feature_values['StepwiseMotionFeature'] = features.jSymbolic.StepwiseMotionFeature(score).extract().vector[0]
        except:
            feature_values['StepwiseMotionFeature']= 0
        try:
            feature_values['StaccatoIncidenceFeature'] = features.jSymbolic.StaccatoIncidenceFeature(score).extract().vector[0]
        except:
            feature_values['StaccatoIncidenceFeature']= 0
        try:
            feature_values['SizeOfMelodicArcsFeature'] = features.jSymbolic.SizeOfMelodicArcsFeature(score).extract().vector[0]
        except:
            feature_values['SizeOfMelodicArcsFeature']= 0
        try:
            feature_values['SecondStrongestRhythmicPulseFeature'] = features.jSymbolic.SecondStrongestRhythmicPulseFeature(score).extract().vector[0]
        except:
            feature_values['SecondStrongestRhythmicPulseFeature']= 0
        try:
            feature_values['RepeatedNotesFeature'] = features.jSymbolic.RepeatedNotesFeature(score).extract().vector[0]
        except:
            feature_values['RepeatedNotesFeature']= 0
        try:
            feature_values['RelativeStrengthOfTopPitchesFeature'] = features.jSymbolic.RelativeStrengthOfTopPitchesFeature(score).extract().vector[0]
        except:
            feature_values['RelativeStrengthOfTopPitchesFeature']= 0
        try:
            feature_values['RelativeStrengthOfTopPitchClassesFeature'] = features.jSymbolic.RelativeStrengthOfTopPitchClassesFeature(score).extract().vector[0]
        except:
            feature_values['RelativeStrengthOfTopPitchClassesFeature']= 0
        try:
            feature_values['RelativeStrengthOfMostCommonIntervalsFeature'] = features.jSymbolic.RelativeStrengthOfMostCommonIntervalsFeature(score).extract().vector[0]
        except:
            feature_values['RelativeStrengthOfMostCommonIntervalsFeature']= 0
        try:
            feature_values['RangeFeature'] = features.jSymbolic.RangeFeature(score).extract().vector[0]
        except:
            feature_values['RangeFeature']= 0
        try:
            feature_values['PrimaryRegisterFeature'] = features.jSymbolic.PrimaryRegisterFeature(score).extract().vector[0]
        except:
            feature_values['PrimaryRegisterFeature']= 0
        try:
            feature_values['PitchVarietyFeature'] = features.jSymbolic.PitchVarietyFeature(score).extract().vector[0]
        except:
            feature_values['PitchVarietyFeature']= 0
        try:
            feature_values['PitchClassVarietyFeature'] = features.jSymbolic.PitchClassVarietyFeature(score).extract().vector[0]
        except:
            feature_values['PitchClassVarietyFeature'] = 0
        try:
            feature_values['NumberOfCommonPitchesFeature'] = features.jSymbolic.NumberOfCommonPitchesFeature(score).extract().vector[0]
        except:
            feature_values['NumberOfCommonPitchesFeature'] = 0
        try:
            feature_values['NumberOfCommonMelodicIntervalsFeature'] = features.jSymbolic.NumberOfCommonMelodicIntervalsFeature(score).extract().vector[0]
        except:
            feature_values['NumberOfCommonMelodicIntervalsFeature'] = 0
        try:
            feature_values['NoteDensityFeature'] = features.jSymbolic.NoteDensityFeature(score).extract().vector[0]
        except:
            feature_values['NoteDensityFeature'] = 0
        try:
            feature_values['MostCommonPitchPrevalenceFeature'] = features.jSymbolic.MostCommonPitchPrevalenceFeature(score).extract().vector[0]
        except:
            feature_values['MostCommonPitchPrevalenceFeature'] = 0
        try:
            feature_values['MostCommonPitchFeature'] = features.jSymbolic.MostCommonPitchFeature(score).extract().vector[0]
        except:
            feature_values['MostCommonPitchFeature'] = 0
        try:
            feature_values['MostCommonPitchClassPrevalenceFeature'] = features.jSymbolic.MostCommonPitchClassPrevalenceFeature(score).extract().vector[0]
        except:
            feature_values['MostCommonPitchClassPrevalenceFeature'] = 0
        try:
            feature_values['MostCommonPitchClassFeature'] = features.jSymbolic.MostCommonPitchClassFeature(score).extract().vector[0]
        except:
            feature_values['MostCommonPitchClassFeature'] = 0
        try:
            feature_values['MostCommonMelodicIntervalPrevalenceFeature'] = features.jSymbolic.MostCommonMelodicIntervalPrevalenceFeature(score).extract().vector[0]
        except:
            feature_values['MostCommonMelodicIntervalPrevalenceFeature'] = 0
        try:
            feature_values['MostCommonMelodicIntervalFeature'] = features.jSymbolic.MostCommonMelodicIntervalFeature(score).extract().vector[0]
        except:
            feature_values['MostCommonMelodicIntervalFeature'] = 0
        try:
            feature_values['MinimumNoteDurationFeature'] = features.jSymbolic.MinimumNoteDurationFeature(score).extract().vector[0]
        except:
            feature_values['MinimumNoteDurationFeature'] = 0
        try:
            feature_values['MelodicTritonesFeature'] = features.jSymbolic.MelodicTritonesFeature(score).extract().vector[0]
        except:
            feature_values['MelodicTritonesFeature'] = 0
        try:
            feature_values['MelodicThirdsFeature'] = features.jSymbolic.MelodicThirdsFeature(score).extract().vector[0]
        except:
            feature_values['MelodicThirdsFeature'] = 0
        try:
            feature_values['MelodicOctavesFeature'] = features.jSymbolic.MelodicOctavesFeature(score).extract().vector[0]
        except:
            feature_values['MelodicOctavesFeature'] = 0
        try:
            feature_values['MelodicFifthsFeature'] = features.jSymbolic.MelodicFifthsFeature(score).extract().vector[0]
        except:
            feature_values['MelodicFifthsFeature'] = 0
        
        try:
            feature_values['MaximumNoteDurationFeature'] = features.jSymbolic.MaximumNoteDurationFeature(score).extract().vector[0]
        except:
            feature_values['MaximumNoteDurationFeature'] = 0
        
        try:
            feature_values['IntervalBetweenStrongestPitchesFeature'] = features.jSymbolic.IntervalBetweenStrongestPitchesFeature(score).extract().vector[0]
        except:
            feature_values['IntervalBetweenStrongestPitchesFeature'] = 0
        try:
            feature_values['IntervalBetweenStrongestPitchClassesFeature'] = features.jSymbolic.IntervalBetweenStrongestPitchClassesFeature(score).extract().vector[0]
        except:
            feature_values['IntervalBetweenStrongestPitchClassesFeature'] = 0
        
        try:
            feature_values['InitialTempoFeature'] = features.jSymbolic.InitialTempoFeature(score).extract().vector[0]
        except:
            feature_values['InitialTempoFeature'] = 0 
        try:
            feature_values['ImportanceOfMiddleRegisterFeature'] = features.jSymbolic.ImportanceOfMiddleRegisterFeature(score).extract().vector[0]
        except:
            feature_values['ImportanceOfMiddleRegisterFeature'] = 0
        try:
            feature_values['ImportanceOfHighRegisterFeature'] = features.jSymbolic.ImportanceOfHighRegisterFeature(score).extract().vector[0]
        except:
            feature_values['ImportanceOfHighRegisterFeature'] = 0
        try:
            feature_values['ImportanceOfBassRegisterFeature'] = features.jSymbolic.ImportanceOfBassRegisterFeature(score).extract().vector[0]
        except:
            feature_values['ImportanceOfBassRegisterFeature'] = 0
        try:
            feature_values['HarmonicityOfTwoStrongestRhythmicPulsesFeature'] = features.jSymbolic.HarmonicityOfTwoStrongestRhythmicPulsesFeature(score).extract().vector[0]
        except:
            feature_values['HarmonicityOfTwoStrongestRhythmicPulsesFeature'] = 0
            print("error")   
        try:
            feature_values['DurationOfMelodicArcsFeature'] = features.jSymbolic.DurationOfMelodicArcsFeature(score).extract().vector[0]
        except:
            feature_values['DurationOfMelodicArcsFeature'] = 0
            print("error")
        try:
            feature_values['DurationFeature'] = features.jSymbolic.DurationFeature(score).extract().vector[0]
        except:
            feature_values['DurationFeature'] = 0
            print("error")
        try:
            feature_values['AverageNumberOfIndependentVoicesFeature'] = features.jSymbolic.AverageNumberOfIndependentVoicesFeature(score).extract().vector[0]
        except:
            feature_values['AverageNumberOfIndependentVoicesFeature'] = 0
            print("error")
        try:
            feature_values['AverageTimeBetweenAttacksFeature'] = features.jSymbolic.AverageTimeBetweenAttacksFeature(score).extract().vector[0]
        except:
            feature_values['AverageTimeBetweenAttacksFeature'] = 0
            print("error")
        try:
            feature_values['AverageTimeBetweenAttacksForEachVoiceFeature'] = features.jSymbolic.AverageTimeBetweenAttacksForEachVoiceFeature(score).extract().vector[0]
        except:
            feature_values['AverageTimeBetweenAttacksForEachVoiceFeature'] = 0
            print("error")
        try:
            feature_values['AverageVariabilityOfTimeBetweenAttacksForEachVoiceFeature'] = features.jSymbolic.AverageVariabilityOfTimeBetweenAttacksForEachVoiceFeature(score).extract().vector[0]
        except:
            feature_values['AverageVariabilityOfTimeBetweenAttacksForEachVoiceFeature'] = 0
            print("error")
        try:
            feature_values['BrassFractionFeature'] = features.jSymbolic.BrassFractionFeature(score).extract().vector[0]
        except:
            feature_values['BrassFractionFeature'] = 0
            print("error")
        try:
            feature_values['ChromaticMotionFeature'] = features.jSymbolic.ChromaticMotionFeature(score).extract().vector[0]
        except:
            feature_values['ChromaticMotionFeature'] = 0
            print("error")
        try:
            feature_values['CombinedStrengthOfTwoStrongestRhythmicPulsesFeature'] = features.jSymbolic.CombinedStrengthOfTwoStrongestRhythmicPulsesFeature(score).extract().vector[0]
        except:
            feature_values['CombinedStrengthOfTwoStrongestRhythmicPulsesFeature'] = 0
            print("error")
        try:
            feature_values['DirectionOfMotionFeature'] = features.jSymbolic.DirectionOfMotionFeature(score).extract().vector[0]
        except:
            feature_values['DirectionOfMotionFeature'] = 0
            print("error")
        try:
            feature_values['DistanceBetweenMostCommonMelodicIntervalsFeature'] = features.jSymbolic.DistanceBetweenMostCommonMelodicIntervalsFeature(score).extract().vector[0]
        except:
            feature_values['DistanceBetweenMostCommonMelodicIntervalsFeature'] = 0
            print("error")



        #replace all commas in file name
        file_name = str(file).replace(",","")
        feature_values['Name'] = file_name
        if(feature_index==0):
            labels_file = open("temp2.txt","w")
            f = open("temp2.csv","w")

        write_index = 0
        #print("feature values: ",feature_values)
        for key,feature_value in feature_values.items():
            # if(feature_value is None):
            #     print(key,"  ",feature_value)
            #write feature string
            if feature_index==0:
                if write_index<len(feature_values)-1:
                    labels_file.write(str(key)+",")
                    f.write(str(key)+",")
                else:
                    labels_file.write(str(key))
                    f.write(str(key))
            if feature_index not in songs_features:
                songs_features[feature_index] = []
                songs_features[feature_index].append(feature_value)
            else:
                songs_features[feature_index].append(feature_value)
            write_index+=1
        print("song index: ",feature_index)
        feature_index+=1
        f.write("\n")

        print("music processed...Now adding features")


        for key,song_features in songs_features.items():
            i = 0
            write_index = 0
            for feature in song_features:
                if i<len(song_features)-1:
                    f.write(str(feature)+",")
                else:
                    f.write(str(feature))
                i+=1
                write_index +=1
            f.write("\n")#
        print("feature values added")
        f.flush()
        f.seek(0)
        ###################################################################predict values of unknown features
        #fit original data
        from sklearn.preprocessing import StandardScaler
        from sklearn import datasets, cluster
        
        data = pd.read_csv(data_name)
        data = data.sample(frac=1).reset_index(drop=True)
        data = data[data.Grade<less_than_grade]
        data = data.groupby('Grade')\
            .apply(lambda x: x[:N])
        X = data.drop(['Grade'],axis = 1)
        scaler = StandardScaler()
        scaler.fit(X)
        scaledX = scaler.transform(X)



        #read in new data
        data = pd.read_csv("temp2.csv")
        data = data.replace(to_replace="None", value="0")
        labels=data['Name']
        new_X = data.drop(['Name'],axis=1)
        if(scaleData):
            # scaler.fit(new_X)
            new_X = scaler.transform(new_X)
            print("data is scaled :)")
        if(reduceFeatures):
            agglo = cluster.FeatureAgglomeration(n_clusters=128)
            agglo.fit(new_X)
            new_X = agglo.transform(new_X)
            print("data features are reduced");

        #fit new data using fitted scaler
        filename = model_name
        # loaded_model = None
        loaded_model = joblib.load(filename)
        #print predictions
        # predictions = loaded_model.predict(new_X_reduced)
        predictions = loaded_model.predict(new_X)
        print("predictions: ", predictions)
        i = 0
        level_of_song = 0
        for grade in predictions:
            # print(labels[i],":",grade)
            level_of_song = float(grade)#math.floor(grade)
            i+=1
        print("level of song: ", level_of_song)
        return level_of_song
