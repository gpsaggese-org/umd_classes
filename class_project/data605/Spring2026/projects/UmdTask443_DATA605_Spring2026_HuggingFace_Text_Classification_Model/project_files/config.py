#Dataset
DATASET_NAME = "ag_news"
NUM_LABELS = 4
LABEL_NAMES = ["World", "Sports", "Business", "Sci/Tech"]
LABEL2ID = {name: i for i, name in enumerate(LABEL_NAMES)}
ID2LABEL = {i: name for i, name in enumerate(LABEL_NAMES)}

#Model
DEFAULT_MODEL = "distilbert-base-uncased"
BERT_MODEL    = "bert-base-uncased"      
ROBERTA_MODEL = "roberta-base"             

#Training
OUTPUT_DIR       = "models/distilbert-ag-news"
EPOCHS           = 3
BATCH_SIZE       = 16
LEARNING_RATE    = 2e-5
WEIGHT_DECAY     = 0.01
WARMUP_STEPS     = 500
MAX_LENGTH       = 128          #Max token length per article
TRAIN_SUBSET     = None        
EVAL_SUBSET      = None     

#Evaluation
RESULTS_DIR = "results"

#Reproducibility
SEED = 42
