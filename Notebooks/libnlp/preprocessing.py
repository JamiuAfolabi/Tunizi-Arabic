from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import numpy as np

def preprocess(tweet):
    """
    preprocesses tweet using regex expressions
    
    PARAMETER
    ---------
    tweet
    
    RETURNS
    ------
    Cleaned_tweet
    """
    #tweet=BeautifulSoup(tweet,'lxml')
    tweet=re.sub(r'(\w)(\1){2,}',r'\1\1',tweet)
    tweet=re.sub(r'[^\w](?:(\w)(\w))(\1\2){2,}',r'\1\2\1\2\1\2',tweet)
    tweet=re.sub(r'(?:(\w)(\w)(\w))(\1\2\3){2,}',r'\1\2\3\1\2\3\1\2\3',tweet)
    tweet=re.sub(r'h[ha]{3,}',r'hahahaha',tweet)
    tweet=re.sub(r'^\d+\s|\s\d+\s|\s\d+$',r' ',tweet)
    tweet=re.sub(r'(\d)(\1){1,}',r'\1',tweet)
    tweet=re.sub(r"[^\w ]",r'',tweet)
    tweet=re.sub(r'(\w)',lambda x: x.group(0).lower(),tweet)
    tweet=re.sub(r' +',r' ',tweet)
    
    return tweet

def check_dir(path):
    """
    check if directory path exists
    
    PARAMETERS
    ----------
    path:
    
    RETURNS
    -------
    path
    """
    if not os.path.exists(path):
        os.mkdir(path)
        
def preprocessed_df(data_path,csv_p,ppd_p,train=True):
    """
    generate preprocessed dataframe
    PARAMETERS
    ----------
    data_path: path of the csv file
    csv_p: csv name
    ppd_p: path to save the preprocessed file
    
    RETURNS
    -------
    csv file
    """
    p_csv=os.path.join(data_path,csv_p)
    df=pd.read_csv(p_csv,encoding='utf-8')
    df['text']=df.text.apply(lambda x: preprocessing.preprocess(x))
    if train:
        ls1=set(df.label)
        # {0: 0, 1: 1, -1: 2}
        df['label']=df.label.map(dict([(key,val) for val,key in enumerate(ls1)]))
    df.drop(['ID'],axis=1,inplace=True)
    f_name=csv_p.split('.')[0]
    check_dir(ppd_p)
    df.to_csv(f'{ppd_p}/{f_name}.csv',index=False)
    
def ppShortenedSentence(df_obj):
    """
    Split sentence based if length of string is greater than by 512
    PARAMETERS
    -----------
    df_obj: Dataframe object
    
    RETURNS
    -------
    array: Array object of Splitted strings
    
    """
    minority_sentence=[ret_shortened_sentence(x) for x in df_obj.text.values]
    split_sentence=[]
    for x in minority_sentence:
        if len(x[-1])>7:
            split_sentence.extend(x)
    return np.array(split_sentence)

def ret_shortened_sentence(text,max_length=120):
    """
    Returns shortened sentence if sentence greater than max_length
    """
    split_string=[]
    length_text=len(text)
    num_string=length_text // max_length
    rems= length_text-num_string * max_length
    
    if num_string >=1:
        for i in range(num_string):
            split_string.append(text[i*max_length:(i+1)*max_length])
        
    split_string.append(text[num_string*max_length:(num_string*max_length)+rems])
    return split_string 