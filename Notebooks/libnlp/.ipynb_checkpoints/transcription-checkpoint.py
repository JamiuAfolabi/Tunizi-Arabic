arabizi_dict={'2':[u"\u0621",u"\u0622",u"\u0623",u"\u0624",u"\u0625",u"\u0626"],
              'b':u"\u0628",
              'p':u"\u0628",
              't':u"\u062A",
              's':[u"\u062B",u"\u0633",u"\u0635"],
              'th':[u"\u062B",u"\u0630",u"\u0638"],
              'a':[u"\u0627",u"\u0647",u"\u0629"],
              'e':[u"\u0627",u"\u0647",u"\u0629"],
              u"\u00e9":[u"\u0627",u"\u0647",u"\u0629"],
              'j':u"\u062C",
              'dj':u"\u062C",
              'g':[u"\u062C",u"\u0642",u"\u0643"],
              '7':u"\u062D",
              "7'":u"\u062E",
              'kh':u"\u062E",
              '5':u"\u062E",
              'd':[u"\u062F",u"\u0636"],
              'z':[u"\u0630",u"\u0632"],
                'dh':[u"\u0630",u"\u0636",u"\u0638"],
                'sh': u"\u0634",
                'ch': u"\u0634",
                '9': u"\u0635",
                "9'": u"\u0636",
                '6': u"\u0637",
                "6'": u"\u0638",
                '3': u"\u0639",
                "3'": u"\u063A",
                'gh': u"\u063A",
                'f' : u"\u0641",
                'v' : u"\u0641",
                '8' : u"\u0642",
                '9' : u"\u0642",
                'q' : u"\u0642",
                'k' : u"\u0643",
                'l' : u"\u0644",
                'm' : u"\u0645",
                'n' : u"\u0646",
                'w' : u"\u0648",
                  'ou': u"\u0648",
                'o' : u"\u0648",
                
                'oo': u"\u0648",
                'u' : u"\u0648",
                'y' : u"\u064A",
                'i' : u"\u064A",
                'ee': u"\u064A",
                'ei' : u"\u064A",
                'ai' : u"\u064A",
                'ah':[u"\u0647",u"\u0629"],
                'eh': [u"\u0647",u"\u0629"],
                'et': u"\u0629",
              "r": u"\u0631", 
              'h' : u"\u062D"

             }

special_dict={
            r'ia$' : u"\u064A"u"\u0647",
            r'y[aeio]$': u"\u064A",
            r'a$': u"\u0627",
            r'a([32])' : r'\1',
            r'et$': u"\u0629",
            r'eh[a-z]?$': u"\u0639"u"\u0647",
            r'^e': u"\u0639",
            r'^[ie]': u"\u0627",
            r'([3g2twy])([aeo])' : r'\1',
            r'k([ou])(\1){2}' : u"\u0642",
            r'k[aoe]': u"\u0643",
            r'a' : u"\u0627",
            'd': u"\u062F",
            's' : u"\u0633",
            'e' : '',   
            'g' : u"\u0642",
            r'th[o]' : u"\u0630",
            r'th[a]' : u"\u062B",
            r'dh[ao]' : u"\u0638",
            r'z[a]?' : u"\u0632",
            r'2' : u"\u0623"
            
            }

import regex as re
import random
class Transcribe:
    """
    class to convert arabizi to arabic
    """
    def __init__(self,arabizi_dict=arabizi_dict,special_dict=special_dict):
        """
        PARAMETERS
        ----------
        arabizi_dict: transcription rule
        special_dict: transcription rule
        
        RETURNS
        -------
        transcription: tokenized arabic text
        b: string joined together
        """
        self.special_dict=special_dict
        self.arabizi_dict=arabizi_dict
        self.dict_double_key={k:v for k,v in self.arabizi_dict.items() if len(k)==2}
        self.dict_multiple_label={k:v for k,v in self.arabizi_dict.items() if isinstance(v,list)}
        self.dict_single={k:v for k,v in self.arabizi_dict.items() if not isinstance(v,list)}
        
    def tokenize_text(self,text):
        return text.split()
    
    def replace_dict_single(self,token):
        regex = re.compile("(%s)" % "|".join(map(re.escape, self.dict_single.keys())))
        string=lambda mo:self.dict_single.get(mo.group(1),mo.group(1))
        return regex.sub(string,token)
    
    def replace_dict_special(self,token):
        for k,v in self.special_dict.items():
            token=re.sub(k,v,token)
        return token
    
    def replace_dict_list(self,token):
        new_dict={k:v[random.choice(range(len(v)))] for k,v in self.dict_multiple_label.items()}
        for k,v in new_dict.items():
            token=token.replace(k,v)
        return token

    def transcription_rule(self,text):
        tokenize_text=self.tokenize_text(text)
        transcribe=[]
        for token in tokenize_text:  
            token=self.replace_dict_special(token)
            token=self.replace_dict_single(token)
            #token=self.replace_dict_list(token)
            transcribe.append(token)
            
        string=' '.join(x for x in transcribe)
        return transcribe,string