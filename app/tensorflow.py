
import tensorflow as tf

import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns

from bs4 import BeautifulSoup
from markdown import markdown
import re

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
model = hub.load(module_url)
print ("module %s loaded" % module_url)
def embed(input):
  return model(input)




word = "Elephant"
sentence = "I am a sentence for which I would like to get its embedding."
paragraph = (
    "Universal Sentence Encoder embeddings also support short paragraphs. "
    "There is no hard limit on how long the paragraph is. Roughly, the longer "
    "the more 'diluted' the embedding will be.")
messages = [word, sentence, paragraph]

# Reduce logging output.
logging.set_verbosity(logging.ERROR)

message_embeddings = embed(messages)

for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
  print("Message: {}".format(messages[i]))
  print("Embedding size: {}".format(len(message_embedding)))
  message_embedding_snippet = ", ".join(
      (str(x) for x in message_embedding[:20]))
  print("Embedding: [{}, ...]\n".format(message_embedding_snippet))
    
    
def plot_similarity(labels, features, rotation):
  corr = np.inner(features, features)
  sns.set(font_scale=1.2)

  shortened_array = []
  for string in labels:
    shortened_array.append(string[:1])
    
  g = sns.heatmap(
      corr,
      xticklabels=shortened_array,
      yticklabels=shortened_array,
      vmin=0,
      vmax=1,
      cmap="YlOrRd")
  
  g.set_xticklabels(labels, rotation=rotation)
  g.set_title("Semantic Textual Similarity")

def run_and_plot(messages_):
  message_embeddings_ = embed(messages_)
  plot_similarity(messages_, message_embeddings_, 90)


dir_path = './docs/'
file_contents = []

for root, dirs, files in os.walk(dir_path):
    for file_name in files:
        if file_name.endswith('.md'):
            with open(os.path.join(root, file_name), 'r') as file:
                contents = file.read()
                # md -> html -> text since BeautifulSoup can extract text cleanly
                html = markdown(contents)

                # remove code snippets
                html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
                html = re.sub(r'<code>(.*?)</code >', ' ', html)

                # extract text
                soup = BeautifulSoup(html, "html.parser")
                text = ''.join(soup.findAll(string=True))
                file_contents.append(text)


run_and_plot(file_contents)