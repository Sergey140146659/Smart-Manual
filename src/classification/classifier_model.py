from torch.utils.data import Dataset
from transformers import AutoTokenizer, DataCollatorWithPadding, AutoModelForSequenceClassification
import torch

model_path = "../src/classification/bert_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)

class ChatBotDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

id2label = {0: "NEGATIVE", 1: "POSITIVE"}

label2id = {"NEGATIVE": 0, "POSITIVE": 1}

model = AutoModelForSequenceClassification.from_pretrained(
    model_path, num_labels=2, id2label=id2label, label2id=label2id
)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


def classifier(text):
    inputs = tokenizer(text, return_tensors="pt").to(device)
    output = model(**inputs, output_hidden_states=True)
    logits = output.logits
    probability = torch.nn.Softmax(dim=1)(logits)
    predicted_class_id = logits.argmax().item()
    return predicted_class_id


