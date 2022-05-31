import os
import sys
import boto3
import json
import pandas as pd
import numpy as np
from scipy import signal
import mne
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def lambda_handler(event, context):
    
    #bucket_name = 'nmlt201021'
    n_channels = 16
    sampling_freq = 128  # in Hertz
    ch_names = ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2', 'F7', 'F8', 'T7', 'T8', 'F3', 'F4', 'P3', 'P4']
    ch_types = ['eeg'] * n_channels
    all_ch_names = ch_names + ['Task','STM']
    all_ch_types = ch_types + ['misc','misc']
    p_detrend = 1 # 0: OFF, 1: On
    p_normalization = 1 # 0: do not, 1: [0, 1] scaling, 2: standardization (x-mean)/var
    p_n_filenames = 7
    p_ica_flag = 1
    p_ts_psd_flag = 0
    l_freqs = 1
    h_freqs = 60

    bucket_name = 'eeg-platform'
    file_name = 'S1.csv'

    s3 = boto3.client('s3')
    resp = s3.get_object(Bucket=bucket_name, Key= file_name)
    temp_pd = pd.read_csv(resp['Body'])
    temp_pd=temp_pd.drop(columns=['Unnamed: 0','time','event'])
    temp_pd=temp_pd.drop(range(0,sampling_freq*5)) # remove first 5sec data
    
    ## Detrend
    if p_detrend == 1:
        temp_pd = pd.DataFrame(signal.detrend(temp_pd, axis=0))
    
    ## Normalization
    if p_normalization == 1:
        temp_pd = (temp_pd - temp_pd.min()) / (temp_pd.max() - temp_pd.min())
    elif p_normalization == 2:
        temp_pd = (temp_pd - temp_pd.mean()) / temp_pd.std()
        
    ## Task marking by filenames
    temp_pd['Task']=0+1   
    temp_pd['STM']=0
    
    for STM_i in range(0,temp_pd.shape[0],sampling_freq):
        temp_pd['STM'].iat[STM_i] = temp_pd['Task'].iat[STM_i]  
        
    ## channels X times
    temp_pd = temp_pd.transpose()
    
    
    ## MNE object
    info = mne.create_info(n_channels, sfreq=sampling_freq)
    info = mne.create_info(all_ch_names, ch_types=all_ch_types, sfreq=sampling_freq)
    info.set_montage('standard_1020')
    
    info['description'] = 'OpenBCI'
    info['bads'] = []  # Names of bad channels

    ## Filtering  
    mne_raw = mne.io.RawArray(temp_pd, info)
    data_lp_hp = mne_raw.filter(l_freq=60,h_freq=1,picks='eeg', method='fir')
    mne_raw_filtered = data_lp_hp.copy().notch_filter(freqs=60, picks='eeg')
    
        
    df = mne_raw_filtered.to_data_frame()
    print(df)
