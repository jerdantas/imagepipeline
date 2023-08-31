import numpy as np
import torch
from datasets import load_dataset, load_metric
from transformers import ViTImageProcessor, ViTForImageClassification, TrainingArguments, Trainer
from time import time
import os


def collate_fn(batch):
    return {
        'pixel_values': torch.stack([x['pixel_values'] for x in batch]),
        'labels': torch.tensor([x['labels'] for x in batch])
    }


metrics = load_metric("accuracy")
# FutureWarning: load_metric is deprecated and will be removed in the next major version of datasets.
# Use 'evaluate.load' instead, from the new library 🤗 Evaluate: https://huggingface.co/docs/evaluate
#   metrics = load_metric("accuracy")


def compute_metrics(p):
    return metrics.compute(predictions=np.argmax(p.predictions, axis=1), references=p.label_ids)


model_name_or_path = 'google/vit-base-patch16-224-in21k'
feature_extractor = ViTImageProcessor.from_pretrained(model_name_or_path)


def transform(example_batch):
    inputs = feature_extractor([x for x in example_batch['image']], return_tensors='pt')
    inputs['labels'] = example_batch['label']
    return inputs


# ----- prepare dataset -------------------------------------------------------------
root_dir = os.getcwd()
ds = load_dataset(path="imagefolder", data_dir=os.path.join(root_dir, "dddd"))
prepared_ds = ds.with_transform(transform)
labels = ds['train'].features['label'].names

# ----- finetune pretrained model -------------------------------------------------------------
model = ViTForImageClassification.from_pretrained(
    model_name_or_path,
    num_labels=len(labels),
    id2label={str(i): c for i, c in enumerate(labels)},
    label2id={c: str(i) for i, c in enumerate(labels)}
)
training_args = TrainingArguments(
  output_dir="./vit-base-dddd",
  per_device_train_batch_size=16,
  evaluation_strategy="steps",
  num_train_epochs=4,
  fp16=True,
  save_steps=100,
  eval_steps=100,
  logging_steps=10,
  learning_rate=2e-4,
  save_total_limit=2,
  remove_unused_columns=False,
  push_to_hub=False,
  report_to='tensorboard',
  load_best_model_at_end=True,
)
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=collate_fn,
    compute_metrics=compute_metrics,
    train_dataset=prepared_ds["train"],
    eval_dataset=prepared_ds["validation"],
    tokenizer=feature_extractor,
)

start = time()
train_results = trainer.train()
duration = (time() - start) * 1000
print(f'Duration: {duration:7.3f} ms')

# ----- save model -------------------------------------------------------------
trainer.save_model()
trainer.log_metrics("train", train_results.metrics)
trainer.save_metrics("train", train_results.metrics)
trainer.save_state()
