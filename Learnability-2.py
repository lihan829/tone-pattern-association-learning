# -*- coding: utf-8 -*-

# -- Sheet --

# data import
# Hausa dictionary data was retreived from Montreal Forced Aligner 
# https://mfa-models.readthedocs.io/en/latest/g2p/index.html#g2p

f = open("Book1.csv", "r")
entry = []

for line in f:
    line = f.readline()
    entry.append(line)

# raw data contains:
## IPA transcription
## semgents
## vowel length (u:, a:)
## tones (˥- High; ˩-Low; ˥˦ - Falling )

#Here is an example
print(entry[:5]) 

#get each lexical items (the orthographic transcrpitions are excluded)

words = []
for item in entry:
    item = item.replace(" ", "")
    item = item.replace("˥˦", "˦")
    words.append(item.split(",")[-1][:-1])

# E.g words[0] output 'ʔduː˥nɪ˥jɛ˩'
words[0]

# the extracted "words" contain extra white spaces, and the F tone markers which takes two characters are causing many inconviniences. 
# the tone representations at this step is before OCP is applied
words = []
t1 = ""
tone = []
tones = []


for item in entry:
    item = item.replace(" ", "")    #exclude the space between segments
    item = item.replace("˥˦", "˦")  #use a one-character representation for falling tones for the convinience
    words.append(item.split(",")[-1][:-1])


print(words[0]) # now it looks better :3



# get the patterns of tones (before the OCP is applied)
# Here, the symbols in the uppercase indicate a long vowel; the symbols in the lowercase a short vowel.
# Long vowels include: monothong long vowels, diphthongs vowels (ended with aw, aj)
# Since Falling tones can only occur on long vowels, hence the uppercase is used for F

for item in words:
    t1 = ""
    for i in range(len(item)):
        if item[i] == "˩":
            if item[i - 1] in ["ː", "j", "w"]: 
                t1 = t1 + "L" 
            else:
                t1 = t1 + "l"
        elif item[i] == "˥":
            if item[i - 1] in ["ː", "j", "w"]:
                t1 = t1 + "H"
            else:
                t1 = t1 + "h"
        if item[i] == "˦":
            t1 = t1 + "F"
    tones.append(t1)


print(tones[0])

# the tone sequence for ʔduː˥nɪ˥jɛ˩ is HhL. More specifically:
## the word contains three syllables
## syllable 1 is associated with H tone on a long vowel
## Syllable 2 is associated with h tone on a short vowel
## Syllable 3 is associated with l tone on a short vowel

# for a brief display of the data so far

for n in range(20):
    print(words[n], "\t", tones[n])

# Get the number of syllables in each lexical item

syllables = [] # create a empty list for storing all syllable info of the dict
for tone in tones:
    sylnum = len(tone)
    syllables.append(sylnum) 

print("The word ", words[0]," has", syllables[0] ,"syllables", "with a",tones[0], "tone sequence") 
#The word  ʔduː˥nɪ˥jɛ˩  has 3 syllables with a Hhl tone sequence


#Get the number of moras in each syllable


moralist = []
moraslist = []
morassum = []

for tone in tones: # for hHL
    moralist = []
    for i in tone:  #for h in hL
        moranum = 0 # moranum is a tally of mora number in each syllable
        if i in ["h", "l"]: #if the vowel is short, then the the vowel only contributes to 1 mora to the syllable
            moranum = moranum + 1
        else:
            moranum = moranum + 2 #if the vowel is long, then the the vowel contributes to 2 moras 
        moralist.append(moranum) # a list of mora numbers of each syllable
        morasum = sum(moralist) # the sum of mora in each lexical word
    moraslist.append(moralist)
    morassum.append(morasum)

print(words[0], tones[0], moraslist[0], morassum[0]) 

#Hhl [2, 1, 1] 4 
# 3-syllable word
#syl1 - 2 mora 
#syl2 - 1 mora
#syl3 - 1 mora
#total mora num = 4




# Now we need to apply OCP rules to the tone sequences
# After the OCP - all tone symbols are in uppercase
# The tones after the ocp rules are named "newtones" - sounds like Newton...
#For example, hHl --> HL; Llh -->LH; lHl-->LHL


newtones = []
for tone in tones:
    tone = tone.upper()
    i = 0
    newtone = ' '
    while i < len(tone):
        if tone[i] != newtone[-1]: #fixme: i think there are some index error going on here since all newtones will have an extra space at the beginning 
            newtone = newtone + tone[i]
        else:
            newtone = newtone
            #   print("stop")
        i = i + 1
        #print(i,newtone)
        #  print(newtone)

    newtones.append(newtone)

list = []
for i in newtones:
    item = i.replace(" ", "") # did a workaround to fix the space - but should change it later 
    list.append(item)

print("tones are", tones[:10])
print("newtones are", list[:10])

#tones are ['Hhl', 'hL', 'LhH', 'hF', 'F', 'hl', 'h', 'L', 'l', 'Hlhl'] before ocp
#newtones are ['HL', 'HL', 'LH', 'HF', 'F', 'HL', 'H', 'L', 'L', 'HLHL']after ocp


# establish syllable-mora association
## for the word ʔja˥ntʃɪ˩ŋ the syllable-mora association is [(1, 1), (2, 2)]
## for the word ʔduː˥nɪ˥jɛ˩ the syllable-mora association is [(1, 1), (1, 2), (2, 3), (3, 4)]

syl_mora_list = []
for n in range(len(words)):
    syl_mora = []
    #print("for words",n,"is",words[n])
    m = 1
    for i in range(syllables[n]):  # (0 ,1, 2 3 
        #print("i=", i)
        p = 1
        while p <= moraslist[n][i]:  #1<=2 2 <= 2 1<=1
            syl_mora.append((i + 1, m))  #(1,1) (1,2) (2,1)
            #print("syl_mora = ",syl_mora)
            #print(i+1,m)
            p += 1
            m += 1
    syl_mora_list.append(syl_mora)
    #print("syl_mora_list",syl_mora_list)

print("for the word", words[0], "the syllable-mora association is", syl_mora_list[0])

# establish tone(before ocp applied)-syllable association
#(maybe there is a better to establish the association with tones after ocp - will consider this later)

# for the word ʔja˥ntʃɪ˩ŋ the syllable-mora association is [(1, 1), (2, 2)]
# for the word ʔduː˥nɪ˥jɛ˩ the syllable-mora association is [(1, 1), (1, 2), (2, 3), (3, 4)]

t_syl_list = []
for n in range(len(words)):
    #print(words[n], tones[n], newtones[n])
    t_syl = []
    m = 0
    for j in range(1, len(newtones[n])):  # 0 1 2
        #print(tones[n][m],newtones[n][j])
        while tones[n][m].upper() == newtones[n][j]:  #h->(H) == H
            t_syl.append((j, m + 1))
            #print(t_syl)
            m += 1
            if m == len(tones[n]):
                break
        #if tones[n][-1] in ["H","L"]:
        #   t_syl.append((j,m+2)) 
        #print(newtones[n][j])
    t_syl_list.append(t_syl)

print(words[:2],tones[:2],t_syl_list[:2])


#All information about a lexical item 

for n in range(2):
    print(words[n], "\t", tones[n], "\t", list[n], "\t", syllables[n], "\t", moraslist[n], "\t",
          morassum[n], "\t", t_syl_list[n], '\t', syl_mora_list[n])
    
#ʔduː˥nɪ˥jɛ˩    Hhl     HL      3       [2, 1, 1]       4       [(1, 1), (1, 2), (2, 3)]        [(1, 1), (1, 2), (2, 3), (3, 4)]
#ʔɪ˥naː˩        hL      HL      2       [1, 2]          3       [(1, 1), (2, 2)] 	            [(1, 1), (2, 2), (2, 3)]
    
    
# I tried to create a class but haven't figured it out very clearly
# Will try the class object method later

class Pattern:
    def __init__(self, tone, newtone, tsig, sigmu):
        self.tone = tone
        self.newtone = newtone
        self.tsig = tsig
        self.sigmu = sigmu
p1 = Pattern(tones[0],list[0],t_syl_list[0],syl_mora_list[0])

p1.tone
p1.newtone
p1.tsig



# -- Sheet 2 --



