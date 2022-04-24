import torch
import os
import random

class Env:
    def __init__(self,tokenizer_model='bert-base-multilingual-uncased',max_len=120,seed=42):
        
        #Defining the paths
        self.data_path='../Data'
        self.train_path='Train.csv'
        self.test_path='Test.csv'
        self.ppd_path='../ppd'
        
        #Definining the tokenizer
        self.tokenizer_name=tokenizer_model
        self.tokenizer=torch.hub.load('huggingface/pytorch-transformers', 'tokenizer',tokenizer_model )
        self.model=torch.hub.load('huggingface/pytorch-transformers', 'model',tokenizer_model )
        self.tokenizer_max_len=max_len
        self.cls_token=self.tokenizer.cls_token_id
        self.sep_token=self.tokenizer.sep_token_id
        self.pad_token=self.tokenizer.pad_token_id
        self.unk_token=self.tokenizer.unk_token_id
        
        #Setting the Seed Value
        if torch.cuda.is_available():
            self.device='cuda'
        else:
            self.device='cpu'
        torch.manual_seed(seed)
        os.environ['PYTHONHASHSEED']=str(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic=True
        torch.backends.cudnn.benchmark=False
        random.seed(seed)