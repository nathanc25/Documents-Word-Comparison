#turn file into string
def filestring(file):
    fstr=''
    for line in file:
        fstr+=line
    return fstr

#get parsed list from a string
def parseline(line):
    line=line.replace('\n', ' ')
    line=line.replace('\t', ' ')
    line=line.replace('\r', ' ')
    line=line.split(' ')
    
    strlist=[]
    for i in line:
        if i=='':
            continue
        
        alpha=False
        for j in i:
            if j.isalpha():
                alpha=True
        
        if alpha:
            word=''
            for j in i:
                if j.isalpha():
                    word+=j
            word=word.lower()
            strlist.append(word)
        
    return strlist

#calculate how many white spaces
def whitespace(char):
    return (' '*(4-len(str(char))))


#calculate average word length
def avglen(wordlist):
    words=0
    totallen=0
    for i in wordlist:
        words+=1
        totallen+=len(i)
    output=round(totallen/words,2)
    return output

#calculate ratio between distinct and total words
def variety(wordlist):
    wordset=set()
    for i in wordlist:
        wordset.add(i)
    ratio=round(len(wordset)/len(wordlist),3)
    return ratio

def wordlengths(wordlist):
    #find max word len
    maxlen=0
    for i in wordlist:
        if len(i)>maxlen:
            maxlen=len(i)
    
    #makes dict from 1 to max word len
    wordslen=dict()
    for i in range(1,maxlen+1):
        wordslen[i]=set()
    
    #adds word to correct key of dict
    for i in wordlist:
        wordslen[len(i)].add(i)
    return wordslen


def printlengths(wdict):
    #print output
    for i in range(1,len(wdict)+1):
        lenvalue=len(wdict[i])
        if lenvalue==0:
            print('{}{}:   0:'.format(whitespace(i),i))
        else:
            if lenvalue<=6:
                words=''
                count=0
                for j in sorted(wdict[i]):
                    count+=1
                    if count==1:
                        words+=j
                    else:
                        words+=' '+j
                print('{}{}:{}{}: {}'.format(whitespace(i),i,whitespace(lenvalue),lenvalue,words))
            elif lenvalue>6:
                words=sorted(wdict[i])
                print('{}{}:{}{}: {} {} {} ... {} {} {}'.format(whitespace(i),i,whitespace(lenvalue),lenvalue,words[0],words[1],words[2],words[-3],words[-2],words[-1],))

#find distinct word pairs
def wordpairs(wordlist,sep):
    pairs=[]
    for i in range(len(wordlist)-sep):
        word1=wordlist[i]
        for j in range(1,sep+1):
            word2=wordlist[i+j]
            if (word2,word1) not in pairs and (word1,word2) not in pairs:
                if word1<word2:
                    pairs.append((word1,word2))
                else:
                    pairs.append((word2,word1))
    for i in range(-1,sep*-1-1,-1):
        word1=wordlist[-1]
        word2=wordlist[i-1]
        if (word2,word1) not in pairs and (word1,word2) not in pairs:
            if word1<word2:
                pairs.append((word1,word2))
            else:
                pairs.append((word2,word1))
    psort=sorted(pairs)
    return psort

#total word pairs
def totalpairs(wordlist,sep):
    pairs=[]
    for i in range(len(wordlist)-sep):
        word1=wordlist[i]
        for j in range(1,sep+1):
            word2=wordlist[i+j]
            if word1<word2:
                pairs.append((word1,word2))
            else:
                pairs.append((word2,word1))
                
    for i in range(-1,sep*-1-1,-1):
        word1=wordlist[-1]
        word2=wordlist[i-1]
        if word1<word2:
            pairs.append((word1,word2))
        else:
            pairs.append((word2,word1))
    psort=sorted(pairs)
    return psort    

def printpairs(pairs):  
    #output
    print('  {} distinct pairs'.format(len(pairs)))
    for i in range(5):
        print('  {} {}'.format(pairs[i][0],pairs[i][1]))
    if len(pairs)>5:
        print('  ...')
        for i in range(-5,0):
            print('  {} {}'.format(pairs[i][0],pairs[i][1]))

#find how distinct word pairs are
def distinctpair(wordpairs,total):
    ratio=len(wordpairs)/len(total)
    return ratio

#evaluated document
def evaluate(file,parse,sep):
    print('')
    print('Evaluating document {}'.format(file))
    print('1. Average word length: {:.2f}'.format(avglen(parse)))
    print('2. Ratio of distinct words to total words: {:.3f}'.format(variety(parse)))
    print('3. Word sets for document {}:'.format(file))
    printlengths(wordlengths(parse))
    print('4. Word pairs for document {}'.format(file))
    pair=wordpairs(parse,sep)
    printpairs(pair)
    total=totalpairs(parse,sep)
    print('5. Ratio of distinct word pairs to total: {:.3f}'.format(distinctpair(pair,total)))

#finds jaccard similarity
def similar(s1,s2):
    if len(s1|s2)==0:
        return 0
    return len(s1&s2)/len(s1|s2)

#find jaccard similarity for each word length
def similarlen(dict1,dict2):
    small=len(dict2)
    big=len(dict1)
    if len(dict1)<len(dict2):
        small=len(dict1)
        big=len(dict2)
    
    count=1
    for i in range(1,small+1):
        sim=similar(dict1[i],dict2[i])
        print('{}{}: {:.4f}'.format(whitespace(i),i,sim))
        count+=1
    if small!=big:
        for i in range(big-small):
            print('{}{}: 0.0000'.format(whitespace(count),count))
            count+=1

if __name__=='__main__':
    #get inputs from user
    file1=input('Enter the first file to analyze and compare ==> ').strip()
    print(file1)
    file2=input('Enter the second file to analyze and compare ==> ').strip()
    print(file2)
    maxsep=input('Enter the maximum separation between words in a pair ==> ').strip()
    print(maxsep)
    maxsep=int(maxsep)
    
    #open stop file
    stop=open('stop.txt')
    stopstr=filestring(stop)
    #create set of words in stop
    stopset=set()
    for i in parseline(stopstr):
        stopset.add(i)
    
    #get parsed list for file 1
    f1=open(file1)
    line1=filestring(f1)
    parse1filter=parseline(line1)
    parse1=[]
    for i in parse1filter:
        if i not in stopset:
            parse1.append(i)
    set1=set()
    for i in parse1:
        set1.add(i)
    
    #get parsed for file 2
    f2=open(file2)
    line2=filestring(f2)
    parse2filter=parseline(line2)
    parse2=[]
    for i in parse2filter:
        if i not in stopset:
            parse2.append(i)
    set2=set()
    for i in parse2:
        set2.add(i)
        
    
    evaluate(file1,parse1,maxsep)
    evaluate(file2,parse2,maxsep)
    
    #comparing files
    print('\nSummary comparison')
    #find average longer words
    if avglen(parse1)>avglen(parse2):
        longer=file1
        short=file2
    else:
        longer=file2
        short=file1
    print('1. {} on average uses longer words than {}'.format(longer,short))
    
    #find overall similarity
    print('2. Overall word use similarity: {:.3f}'.format(similar(set1,set2)))
    
    #find similarity by length
    print('3. Word use similarity by length:')
    similarlen(wordlengths(parse1),wordlengths(parse2))
    
    #find word pair similarity
    pairsim=similar(set(wordpairs(parse1,maxsep)),set(wordpairs(parse2,maxsep)))
    print('4. Word pair similarity: {:.4f}'.format(pairsim))