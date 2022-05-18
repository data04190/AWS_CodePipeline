import os
import sys
import pandas as pd
import numpy as np
from scipy import signal
import mne
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


bucket = "kmk-practice" 
file_name = "20211018_1_jhkwon_gum/S1.csv"

s3 = boto3.client('s3')
obj = s3.get_object(Bucket= bucket, Key= file_name)
df = pd.read_csv(obj['Body'])
print(df)


def lambda_handler(event, context):
    print("test")
