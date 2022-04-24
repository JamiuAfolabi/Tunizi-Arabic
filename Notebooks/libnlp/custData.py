from torch.utils.data import Dataset
from libnlp.env import Env
import torch

E=Env()

class ArabiziDataset(Dataset):
    def __init__(self,df,tokenizer,max_len,train=True):
        self.train=train
        self.tokenizer=tokenizer
        self.max_len=max_len
        self.text=df.text.values
        if train:
            self.labels=df.label.values
        
    def __len__(self):
        return len(self.text)  
    
    def __getitem__(self,idx):
        token,mask,len_token=self.token_mask(self.text[idx],self.max_len)
        if self.train:
            label=self.labels[idx]
            return token,mask,len_token,label
        return token,mask,len_token
    def token_mask(self,text,max_len):
        if max_len in range(511,513):
            len_text=min(max_len-2,len(text))
        else:
            len_text=min(max_len,len(text))
        text=text[:len_text]
        token=self.custTokenizer(self.tokenizer,text)
        len_token=len(token)
        mask= [1] * len_token
        return token,mask,len_token
    
    def custTokenizer(self,tokenizer,text):
        return tokenizer.encode(text)
    
def customPadding(batch,tokenizer=E.tokenizer):
    comp=list(zip(*batch))
    tokens=comp[0]
    masks=comp[1]
    len_tokens=comp[2]      
    max_len=max(len_tokens)
    tokens_ret=[]
    masks_ret=[]
    
    for idx in range(len(tokens)):
        pad_len=max_len-min(len_tokens[idx],max_len)
        padding=[tokenizer.pad_token_id] * pad_len
        token=tokens[idx] + padding
        mask=masks[idx] + [0] * pad_len
        tokens_ret.append(token)
        masks_ret.append(mask)
        
    if len(comp)==4:
        labels=comp[3]
        return torch.tensor(tokens_ret),torch.tensor(masks_ret),torch.tensor(labels)
    return torch.tensor(tokens_ret),torch.tensor(masks_ret)
