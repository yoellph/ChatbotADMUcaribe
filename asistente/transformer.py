import numpy as np

import typing
from typing import Any, Tuple

import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing

import tensorflow_text as tf_text

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
reloaded = tf.saved_model.load('translator')

def trans(text):
    three_input_text=tf.constant([text])
    result = reloaded.tf_translate(three_input_text)
    for tr in result['text']:
        return tr.numpy().decode()
