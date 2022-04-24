def children(m):
    return m if isinstance(m, (list, tuple)) else list(m.children())


def set_trainable_attr(m, b):
    m.trainable = b
    for p in m.parameters():
        p.requires_grad = b


def apply_leaf(m, f):
    c = children(m)
    if isinstance(m, nn.Module):
        f(m)
    if len(c) > 0:
        for l in c:
            apply_leaf(l, f)

def set_trainable(l, b):
    apply_leaf(l, lambda m: set_trainable_attr(m, b))
    
    

class Run:
    def __init__(self,train_loader,validation_loader,model,criterion,optimizer):
        self.train_loader=train_loader
        self.validation_loader=validation_loader
        self.model=model
        self.criterion=criterion
        self.optimizer=optimizer
        
    def _batch(batch,train=True):
        if train:
            input_token,attention_mask,targets=batch
            return input_token.to(E.device),attention_mask.to(E.device),targets.to(E.device)
        else:
            input_token,attention_mask=batch
            return input_token.to(E.device),attention_mask.to(E.device)

    def trainer_update(engine,batch):
        self.model.train()
        self.optimizer.zero_grad()
        input_token,attention_mask,y=self._batch(batch)
        #Forward pass
        out=self.model(input_token,attention_mask)
        loss=self.criterion(out,y)
        #backward pass
        loss.backward()
        self.optimizer.step()
        #print('Done')
        return loss.item()

    def eval_update(engine,batch):
        model.eval()
        with torch.no_grad():
            input_token,attention_mask,y=self._batch(batch)
            out=model(input_token,attention_mask)
            y_pred=torch.round(out)
            return y_pred,y
    self.trainer=Engine(self.trainer_update)
    self.train_evaluator=Engine(self.eval_update)
    
    #metrics
    RunningAverage(output_transform=lambda x: x).attach(self.trainer,'loss')
    Loss(criterion).attach(self.train_evaluator,'crossentropy')
    Accuracy().attach(self.train_evaluator,'accuracy')
    pbar=ProgressBar(persist=True,bar_format="")
    pbar.attach(self.trainer,['loss'])
    
    def score_func(engine):
    val_loss=engine.state.metrics['crossentropy']
    return -val_loss

    self.handler=EarlyStopping(patience=5,score_function=self.score_func,trainer=self.trainer)
    self.train_evaluator.add_event_handler(Events.COMPLETED,self.handler)
    
    
    @self.trainer.on(Events.EPOCH_COMPLETED)
    
    def log_training_res():
        self.train_evaluator.run(self.train_loader)
        metrics=self.train_evaluator.state.metrics
        accuracy=metrics['accuracy']
        loss=metrics['crossentropy']
        pbar.log_message(f'Training_loss: {loss}, Accuracy: {accuracy}')

    @self.trainer.on(Events.EPOCH_COMPLETED)
    def log_validation_res():
        self.train_evaluator.run(self.validation_loader)
        metrics=self.train_evaluator.state.metrics
        accuracy=metrics['accuracy']
        loss=metrics['crossentropy']
        pbar.log_message(f'Validation_loss: {loss}, Accuracy: {accuracy}')

    checkpoint=ModelCheckpoint('/tmp/modeltest','bert_model',n_saved=3,require_empty=False)
    self.trainer.add_event_handler(Events.EPOCH_COMPLETED,checkpoint,{'bertmodel':model})

    
    
    
        
    