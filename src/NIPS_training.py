import os
import sys
import csv
import math
import pickle
import shutil
from collections import Counter
from datetime import datetime
from scoring_wip import*
from graphs import*
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split
# from torchsummary import summary

# region
from torch import cuda
import torch
from torch import LongTensor
from torch import nn
from torch.utils.data import DataLoader
from network import TweetyNet
import librosa
from librosa import display
import scipy.signal as scipy_signal
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
from glob import glob
#endregion

#from microfaune.audio import wav2spc, create_spec, load_wav
from TweetyNetAudio import wav2spc, create_spec, load_wav
import random
from CustomAudioDataset import CustomAudioDataset
from TweetyNetModel import TweetyNetModel


def get_frames(x, frame_size, hop_length):
    return ((x) / hop_length) + 1 #(x - frame_size)/hop_length + 1
def frames2seconds(x, sr):
    return x/sr
def find_tags(data_path, folder):
    fnames = os.listdir(os.path.join(data_path, "temporal_annotations_nips4b"))
    csvs = []
    for f in fnames:
        #print(f)
        csvs.append(pd.read_csv(os.path.join(data_path, "temporal_annotations_nips4b", f), index_col=False, names=["start", "duration", "tag"]))
    return csvs


# works
def find_pyrenote_tags(data_path, folder):
    # fnames = os.listdir(os.path.join(data_path, "temporal_annotations_nips4b"))
    Pyre = pd.read_csv(os.path.join(data_path, "for_data_science_newline_fixed.csv"), index_col=False, usecols=["IN FILE","OFFSET", "DURATION", "MANUAL ID","SAMPLE RATE"])

    # for_data_science_newline_fixed.csv
    # csvs = []
    # for f in fnames:
        #print(f)
        # csvs.append(pd.read_csv(os.path.join(data_path, "temporal_annotations_nips4b", f), index_col=False, names=["OFFSET", "DURATION", "MANUAL ID"]))
        # instead of doing this we just get that info from one dataframe.! WIP
    Pyre = Pyre[Pyre["SAMPLE RATE"] == 44100]
    # print(Pyre)
    # return
    return Pyre
# works
def create_pyrenote_tags(data_path, folder):

    csv = find_pyrenote_tags(data_path, folder) # one dataframe
    # print()

    tags = csv["MANUAL ID"] # tags column

    tag = [] 
    for t in tags:# for each column/series
        # for a in t: # for each species in the individual column/series
        tag.append(t)
    tag = set(tag) # remove duplicates
    # tags = {"None": 0} # dictionary counting the number of species
    tags = {}
    for i, t in enumerate(sorted(tag)): # adding to dictionary and updating species counts
        tags[t] = i + 1
    # print(tags)
    return tags # returns a dictionary of species and their counts
# works
def compute_pyrenote_feature(data_path, folder, SR, n_mels, frame_size, hop_length, windowsize):
    print(f"Compute features for dataset {os.path.basename(data_path)}")
    
    features = {"uids": [], "X": [], "Y": []}
    '''
    # print(data_path)
    # folder = 
    # print(os.path.join(data_path, folder))
    # cwd = os.getcwd() 
    # print(cwd)
    '''
    pyre_notes = find_pyrenote_tags(data_path,folder)
    valid_filenames = pyre_notes["IN FILE"].drop_duplicates().values.tolist() 
    '''
    # print(valid_filnames)
    # return
    '''
    file_path = os.path.join(data_path,"Mixed_Bird-20220126T212121Z-003","Mixed_Bird")
    # print(file_path)
    filenames = os.listdir(file_path)
    # print(filenames)
    true_wavs = [i for i in filenames if i in valid_filenames] # keep in mind not all wavs have been downloaded yet.
    
    #region
    # print(os.path.join(data_path,'birdwavs.txt'))
    #C:\Users\lianl\Repositories\Q1-Project-Code\data\PYRE\ birdwavs.txt
    # with open(os.path.join(data_path,'birdwavs.txt'), 'w') as filehandle: # for getting the stats in this set of data., makes an extra new line in txt.
    #     for listitem in true_wavs:
    #         filehandle.write('%s\ n' % listitem)
    # return 
    # print(true_wavs)
    # print(len(true_wavs))
    # print(type(true_wavs))
     # filter out the non-44100 sampling rates frequencies
    # return
    "Recordings in the format of nips4b_birds_{folder}filexxx.wav"
    
    "annotations in the format annotation_{folder}xxx.csv"
    #endregion
    
    tags = create_pyrenote_tags(data_path, folder)
    '''
    # print(tags)
    # return
    ''' 
    
    for f in true_wavs:
        '''
        #signal, SR = downsampled_mono_audio(signal, sample_rate, SR)
        # print(f)
        '''
        wav = os.path.join(file_path, f)
        spc,len_audio = wav2spc(wav, fs=SR, n_mels=n_mels) # returns array for display melspec (216,72)
       
        '''
        # spec_1 = librosa.display.specshow(spc, hop_length = hop_length, sr = SR, y_axis = 'mel', x_axis='time')
        # print(spc)
        # print(spec_1)
        # plt.show()
        # print(f'spec shape {spc.shape}')
        # window = frames2seconds(spc.shape[1],SR) # seconds also, model has
        # print(f'window size {window}')
        # print(f'length of audio {len_audio}')
        # print(f'time bins in seconds {len_audio/spc.shape[1]}')
        '''

        time_bins = len_audio/spc.shape[1] # in seconds

        '''
        # curr have seconds we want for winds
        # now we need to calc how many time bins we need to meet the number of seconds.
        # able to slice the matrix, to balance the windows.
        # return 
        # print(wav)
        # spec = librosa.display.specshow(spc,sr = SR, hop_length = hop_length, y_axis='mel', x_axis='time') # 72 is freq bin, second is time bins
        # print(spec)
        # plt.show()
        # return
        # return
        # print(type(spc))
        '''

        Y = compute_pyrenote_Y(wav,f, spc, tags, data_path, folder, SR, frame_size, hop_length) # fix this
        computed = windowsize//time_bins #verify, big assumption. are time bins consistant?
        # print(computed*(Y.shape[0]//computed))
        time_axis = int(computed*(Y.shape[0]//computed))
        '''
        # print(time_axis)
        # print(type(time_axis))
        # print(Y.shape[0]//computed)
        '''
        freq_axis = int(Y.shape[0]//computed) # 31, 2, 19
        '''
        # print(f'freq_axis {freq_axis}')
        # print(f'freq_axis type {type(freq_axis)}')
        # # return 
        # print(f'spc split spc[:time_axis,:] shape {spc[:,:time_axis].shape}')
        # print(f'Y split Y[:time_axis] shape {Y[:time_axis].shape}')
        '''

        spc_split = np.split(spc[:,:time_axis],freq_axis,axis = 1)
        Y_split = np.split(Y[:time_axis],freq_axis)

        spc_split_zero = spc_split[0]
        print(f)
        print(spc_split_zero.shape)

        '''
        # print(type(spc_split_zero))
        # print(spc_split_zero)
        # spec_2 = librosa.display.specshow(spc_split_zero, hop_length = hop_length, sr = SR, y_axis = 'mel', x_axis='time')
        # print(spec_2)
        # plt.show()
        # return 

        # spc.shape[0]
        # print(len(spc_split))
        # print(len(Y_split))
        # print(spc_split[0].shape)
        # print(Y_split[0].shape)
        # return 

        # for i in spc:
        '''

        '''
        # compute_windows(spc,Y)--> array of spc's and their corresponding windows.
        #compute the seconds, for window length
        #spc matrix and labels array window spcs to match up with the labels
        # return
        '''

        features["uids"].extend([f]*freq_axis) # need 31 of f
        features["X"].extend(spc_split)#.append(spc)
        features["Y"].extend(Y_split)#.append(Y)
        '''
        # features["time_bins"].append(time_bins)

    # print(filenames)
    # return
    '''
    return features
#testing
def compute_pyrenote_Y(wav, f, spc, tags, data_path, folder, SR, frame_size, hop_length):
    # file_num = f.split("file")[-1][:3]
    # print(wav)
    # print(os.path.isfile(wav))
    infile = f # wav file name
    # print(f)
    Pyre_notes = find_pyrenote_tags(data_path, folder)

    wav_notes = Pyre_notes[Pyre_notes['IN FILE'] == f ]
    # print(wav_notes)
    # print(type(wav_notes))
    # print(wav_notes.shape)
    # return

    if os.path.isfile(wav):

        x, sr = librosa.load(wav, sr=SR)
        # print(x)
        # print(sr)
        # return

        annotation = wav_notes[['OFFSET','DURATION','MANUAL ID']].reset_index(drop = True)#pd.read_csv(Pyre_notes, index_col=False, names=["start", "duration", "tag"])
        # print(annotation)
        # print(type(annotation))
        # print(annotation.shape)
        # return

        y = calc_pyrenote_Y(x, sr, spc, annotation, tags, frame_size, hop_length)
        # return

        return np.array(y)
    else:
        print("file does not exist: ", f)
    return [0] * spc.shape[1]
# wip
def calc_pyrenote_Y(x, sr, spc, annotation, tags, frame_size, hop_length):
    y = [0] * spc.shape[1] # array of zeros
    # print(y)
    # return
    for i in range(len(annotation)):
        # print(len(annotation))
        # return
        # print(i)
        # print(annotation.loc[i, "OFFSET"])
        # return
        # print(annotation.loc[i, "OFFSET"] * sr)
        # return
        start = get_frames(annotation.loc[i, "OFFSET"] * sr, frame_size, hop_length)
        # print(start)
        # return
        end = get_frames((annotation.loc[i, "OFFSET"] + annotation.loc[i, "DURATION"]) * sr, frame_size, hop_length)
        # print(end)
        # return
        #print(annotation["tag"], len(annotation["tag"]))

        # if annotation["tag"][i] not in nonBird_labels:
        for j in range(math.floor(start), math.floor(end)): #CORRECT WAY TO ADD TRUE LABELS?
            # print(f'spc shape {spc.shape}') # (72, 1)
            # print(f'Manual ID{annotation.loc[0, "MANUAL ID"]}') # Alopochelidon fucata Tawny-headed Swallow
            # print(f'length of labels {len(y)}') #1
            # print(f'indexing label {j}')      #81 which file? maybe the wav_file has not been annotated?
            y[j] = 1 # For binary use. add if statement later tags[annotation.loc[i, "tag"]]
        # else: 
        #     #print(str(annotation["tag"][i]))
        #     found[str(annotation["tag"][i])] += 1
        # print(y) #COMPARE TO SPECTROGRAM Accipiter-superciliosus-329800.wav
        # return
    return y
#WIP
def load_pyrenote_dataset(data_path, folder, SR, n_mels, frame_size, hop_length, windowsize, use_dump=True):
    mel_dump_file = os.path.join(data_path, "downsampled_{}_bin_mel_dataset.pkl".format(folder))
    if os.path.exists(mel_dump_file) and use_dump:
        with open(mel_dump_file, "rb") as f:
            dataset = pickle.load(f)
    else:
        dataset = compute_pyrenote_feature(data_path, folder, SR, n_mels, frame_size, hop_length, windowsize)
        with open(mel_dump_file, "wb") as f:
            pickle.dump(dataset, f)
    # print(f'dataset is {dataset}')
    # print(dataset)
    #this section here has me confused, rotates the spectrograms, microfaune implementation.
    # inds = [i for i, x in enumerate(dataset["X"]) if x.shape[1] == 216]
    inds = [i for i, x in enumerate(dataset["X"]) if x.shape[1] >= 0] # consider monophonic, start windowing
    # inds = [i for i, x in enumerate(dataset["X"])]
    # X = np.array([dataset["X"][i].transpose() for i in inds]).astype(np.float32)/255

    # X = np.array([np.rot90(dataset["X"][i].astype(np.float32)/255,3) for i in inds], dtype=object)#.astype(np.float32)/255
    # X = np.array([np.rot90(dataset["X"][i],3) for i in inds]).astype(np.float32)/255 rotation causes frequency prediction outputs instead of timebins
    X = np.array([dataset["X"][i] for i in inds]).astype(np.float32)/255
    X = X.reshape(X.shape[0], 1, X.shape[1], X.shape[2])
    Y = np.array([dataset["Y"][i] for i in inds]).astype(np.longlong)
    uids = np.array([dataset["uids"][i] for i in inds])
    # X = dataset['X']
    # Y = dataset['Y']
    # uids = dataset['uids']
    return X, Y, uids




def create_tags(data_path, folder):
    csvs = find_tags(data_path, folder)
    tags = [csv["tag"] for csv in csvs]
    tag = []
    for t in tags:
        for a in t:
            tag.append(a)
    tag = set(tag)
    tags = {"None": 0}
    for i, t in enumerate(sorted(tag)):
        tags[t] = i + 1
    return tags

def compute_feature(data_path, folder, SR, n_mels, frame_size, hop_length, nonBird_labels, found):
    print(f"Compute features for dataset {os.path.basename(data_path)}")
    
    features = {"uids": [], "X": [], "Y": []}
    
    filenames = os.listdir(os.path.join(data_path, folder))
    
    "Recordings in the format of nips4b_birds_{folder}filexxx.wav"
    
    "annotations in the format annotation_{folder}xxx.csv"
    
    tags = create_tags(data_path, folder)
    
    for f in filenames:
		#signal, SR = downsampled_mono_audio(signal, sample_rate, SR)
        spc = wav2spc(os.path.join(data_path, folder, f), fs=SR, n_mels=n_mels)
        Y = compute_Y(f, spc, tags, data_path, folder, SR, frame_size, hop_length, nonBird_labels, found)
        features["uids"].append(f)
        features["X"].append(spc)
        features["Y"].append(Y)
    return features

def compute_Y(f, spc, tags, data_path, folder, SR, frame_size, hop_length, nonBird_labels, found):
    file_num = f.split("file")[-1][:3]
    fpath = os.path.join(data_path, "temporal_annotations_nips4b", "".join(["annotation_", folder, file_num, ".csv"]))
    if os.path.isfile(fpath):
        x, sr = librosa.load(os.path.join(data_path, folder, f), sr=SR)
        annotation = pd.read_csv(fpath, index_col=False, names=["start", "duration", "tag"])
        y = calc_Y(x, sr, spc, annotation, tags, frame_size, hop_length, nonBird_labels, found)
        return np.array(y)
    else:
        print("file does not exist: ", f)
    return [0] * spc.shape[1]

def calc_Y(x, sr, spc, annotation, tags, frame_size, hop_length, nonBird_labels, found):
    y = [0] * spc.shape[1]
    for i in range(len(annotation)):
        start = get_frames(annotation.loc[i, "start"] * sr, frame_size, hop_length)
        end = get_frames((annotation.loc[i, "start"] + annotation.loc[i, "duration"]) * sr, frame_size, hop_length)
        #print(annotation["tag"], len(annotation["tag"]))
        if annotation["tag"][i] not in nonBird_labels:
            for j in range(math.floor(start), math.floor(end)):
                y[j] = 1 # For binary use. add if statement later tags[annotation.loc[i, "tag"]]
        else: 
            #print(str(annotation["tag"][i]))
            found[str(annotation["tag"][i])] += 1
    return y

def split_dataset(X, Y, test_size=0.2, random_state=0):
    split_generator = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    ind_train, ind_test = next(split_generator.split(X, Y))
    X_train, X_test = X[ind_train, :, :], X[ind_test, :, :] # questionable
    Y_train, Y_test = Y[ind_train], Y[ind_test] # questionable
    return ind_train, ind_test

def get_pos_total(Y):
    pos, total = 0,0
    for y in Y:
        pos += sum(y)
        total += len(y)
    #print(pos, total, pos/total, len(Y))
    return pos, total

def random_split_to_fifty(X, Y, uids):
    pos, total = get_pos_total(Y)
    j = 0
    while (pos/total < .50):
        idx = random.randint(0, len(Y)-1)
        if (sum(Y[idx])/Y.shape[1] < .5):
            #print(uids[idx],(sum(Y[idx])/Y.shape[1]))
            X = np.delete(X, idx, axis=0)
            Y = np.delete(Y, idx, axis=0)
            uids = np.delete(uids, idx, axis=0)
            #print(j, pos/total)
            j += 1

        pos, total = get_pos_total(Y)
    return X, Y, uids

def load_dataset(data_path, folder, SR, n_mels, frame_size, hop_length, nonBird_labels, found, use_dump=True):
    mel_dump_file = os.path.join(data_path, "downsampled_{}_bin_mel_dataset.pkl".format(folder))
    if os.path.exists(mel_dump_file) and use_dump:
        with open(mel_dump_file, "rb") as f:
            dataset = pickle.load(f)
    else:
        dataset = compute_feature(data_path, folder, SR, n_mels, frame_size, hop_length, nonBird_labels, found)
        with open(mel_dump_file, "wb") as f:
            pickle.dump(dataset, f)

    inds = [i for i, x in enumerate(dataset["X"]) if x.shape[1] == 216]
    # X = np.array([dataset["X"][i].transpose() for i in inds]).astype(np.float32)/255 # tune
    # X = np.array([dataset["X"][i] for i in inds]).astype(np.float32)/255
    X = np.array([dataset["X"][i] for i in inds]).astype(np.float32)/255 # over training, with norm label, .005 lr, 5, bs, 500 E
    X = X.reshape(X.shape[0], 1, X.shape[1], X.shape[2])
    Y = np.array([dataset["Y"][i] for i in inds]).astype(np.longlong)
    uids = np.array([dataset["uids"][i] for i in inds])

    # to tensor
    # X = torch.LongTensor(X).cuda()
    # Y = torch.LongTensor(Y).cuda()
    # uids = torch.LongTensor(uids).cuda()

    return X, Y, uids

def apply_features(datasets_dir, folder, SR, n_mels, FRAME_SIZE, HOP_LENGTH, nonBird_labels, found):
    
    print("----------------------------------------------------------------------------------------------")
    print("\n")
    print("IGNORE MISSING WAV FILES - THEY DONT EXIST")
    # load_data_set returns variables which get fed into model builder 
    # X, Y, uids = load_pyrenote_dataset(datasets_dir, folder, SR, n_mels, FRAME_SIZE, HOP_LENGTH, nonBird_labels, found, use_dump=True)
    
    folder = 'Train'
    X, Y, uids = load_dataset(datasets_dir, folder, SR, n_mels, FRAME_SIZE, HOP_LENGTH, 2)
    '''# print(f'X shape {X.shape}') #number of birds, rows of each data column of each data.
    # print(f'len of X {len(X)}')
    # bird1 = X[0] #data point, [0][0] feature value of dp, yes
    # print(bird1)
    # print(f'len of bird1 {len(bird1)}') # 216
    # print(f'shape of bird1 {bird1.shape}') # 216,72, r,c frequency bins, time bins
    # print(f'arrays inside bird1 {len(X[0][0])}') # 72
    # print(f'shape of bird1 first array {X[0][0].shape}')
    # print(f'bird1 uid {uids[0]}')
    # print(f'number of different birds {len(uids)}')
    # spec = librosa.display.specshow(bird1, hop_length = HOP_LENGTH,sr = SR, y_axis='mel', x_axis='time') # displays rotated
    # print(spec)
    # plt.show()
    # return'''


    print("\n")
    print("----------------------------------------------------------------------------------------------")
    # test_dataset = CustomAudioDataset(X, Y, uids)

    '''# pos, total = 0,0
    #remove green and red labels
    #for k in found:
        #print(k, found[k])'''

    # Prolonged time complexity
    # X, Y, uids =  random_split_to_fifty(X, Y, uids)

    '''# for y in Y:
    #     pos += sum(y)
    #     total += len(y)
    # print(pos, total, pos/total, len(Y))

    #features above feed into below

    #all_tags = create_tags(datasets_dir, folder)'''
    all_tags = [0,1]
    '''#print(len(Counter(all_tags)))
    #for c in range(10):
    #    print(Y[c])
    #return'''
    
    X_train, X_val, Y_train, Y_val, uids_train, uids_val = train_test_split(X, Y, uids, test_size=.3)

    X_val, X_test, Y_val, Y_test, uids_val, uids_test = train_test_split(X_val, Y_val, uids_val, test_size=.33)

    # print(X_train.shape, Y_train.shape, uids_train.shape)
    # print(X_val.shape, Y_val.shape, uids_val.shape)
    #create tensors
    # print(X_train.shape) #100, 216, 72
    # return 

    #if torch.cuda.is_available(): #get this to work, does not detect gpu. works on tweety env(slow)
    device = torch.cuda.device('cuda:0')
    # print(f'device {device.get_device_name()}')
    print(f'using device {torch.cuda.get_device_name(torch.cuda.current_device())}')
    name = torch.cuda.get_device_name(device)
    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using {name} ")# torch.cuda.get_device_name(0)
    
    #1) batch the X_train
    #For ex, batch_size=5 means that each batch is gonna be (5, 216, 72)
    #2) specify in the model that the input is (216, 72)

    X_train = torch.FloatTensor(X_train).to(torch.cuda.current_device())#.cuda()
    X_val = torch.FloatTensor(X_val).to(torch.cuda.current_device())#.cuda()

    Y_train = torch.LongTensor(Y_train).to(torch.cuda.current_device())#.cuda()
    Y_val = torch.LongTensor(Y_val).to(torch.cuda.current_device())#.cuda()

    X_test = torch.FloatTensor(X_test).to(torch.cuda.current_device())#.cuda()
    Y_test = torch.LongTensor(Y_test).to(torch.cuda.current_device())#.cuda()

    print(f'is X_train on GPU? {X_train.is_cuda}')
    print(f'is X_val on GPU? {X_val.is_cuda}')

    print(f'is Y_train on GPU? {Y_train.is_cuda}')
    print(f'is Y_val on GPU? {Y_val.is_cuda}')

    print(f'is X_test on GPU? {X_test.is_cuda}')
    print(f'is Y_test on GPU? {Y_test.is_cuda}')

    print(f'using device {torch.cuda.get_device_name(torch.cuda.current_device())}')
    
    # print('---------------------------------')
    # print('\n')
    # print(X_train)
    # print('\n')
    # print(X_val)
    # print('\n')
    # print(Y_train)
    # print('\n')
    # print(Y_val)
    # print('\n')
    # print('---------------------------------')

    #uids_train = torch.LongTensor(uids_train).cuda()
    #uids_val = torch.LongTensor(uids_val).cuda()
    

    train_dataset = CustomAudioDataset(X_train, Y_train, uids_train)
    #test_dataset = CustomAudioDataset(X_test[:6], Y_test[:6], uids_test[:6])

    X, Y, uid = train_dataset.__getitem__(0)
    # print(X.detach().cpu().numpy())
    # # return...
    # print('\n')
    # print(X[0].detach().cpu().numpy())
    # print('\n')
    # print(Y[0].detach().cpu().numpy())
    # print('\n')
    # print(uid)
    # print('\n')

    # bird1 = X[0].detach().cpu().numpy()
    # spec1 = librosa.display.specshow(bird1, hop_length = HOP_LENGTH,sr = SR, y_axis='time', x_axis='mel')
    # plt.show()
    # return

    val_dataset = CustomAudioDataset(X_val, Y_val, uids_val)

    # X, Y, uid = val_dataset.__getitem__(0)
    # print('\n')
    # print(X[0].detach().cpu().numpy())
    # print('\n')
    # print(Y[0].detach().cpu().numpy())
    # print('\n')
    # print(uid)
    # print('\n')

    # bird2 = X[0].detach().cpu().numpy()
    # spec2 = librosa.display.specshow(bird2, hop_length = HOP_LENGTH,sr = SR, y_axis='time', x_axis='mel')
    # plt.show()
    # return

    test_dataset = CustomAudioDataset(X_test, Y_test, uids_test)

    # X, Y, uid = test_dataset.__getitem__(0)
    # print('\n')
    # print(X[0].detach().cpu().numpy())
    # print('\n')
    # print(Y[0].detach().cpu().numpy())
    # print('\n')
    # print(uid)
    # print('\n')

    # bird3 = X[0].detach().cpu().numpy()
    # spec3 = librosa.display.specshow(bird3, hop_length = HOP_LENGTH,sr = SR, y_axis='time', x_axis='mel')
    # plt.show()
    # return

    # train_dataset.to(device)
    # val_dataset.to(device)

    # print(f'is train_dataset on GPU? {train_dataset.is_cuda}')
    # print(f'is val_dataset on GPU? {train_dataset.is_cuda}')

    # print('\n')
    # print('---------------------------------')
    # #print(train_dataset[:])
    # print('\n')
    # #print(val_dataset[:])
    # print('\n')
    # print('---------------------------------')

    # train_dataset = (train_dataset)
    # val_dataset = (val_dataset)

    return all_tags, n_mels, train_dataset, val_dataset, test_dataset, HOP_LENGTH, SR

def model_build(all_tags, n_mels, train_dataset, val_dataset, Skip, lr, batch_size, epochs, outdir):
    
    if Skip:
        for f in os.listdir(outdir):
            shutil.rmtree(os.path.join(outdir, f),ignore_errors=True)
        for f in os.listdir(outdir):
            os.remove(os.path.join(outdir, f))
    else:   
        pass
    
    #device = 'cuda' if torch.cuda.is_available() else 'cpu'

    cwd = os.getcwd() 
    os.chdir(outdir)

    #if torch.cuda.is_available(): #get this to work, does not detect gpu. works on tweety env(slow)
    device = torch.cuda.device('cuda')
    print(f'device {torch.cuda.get_device_name(device)}')
    name = torch.cuda.get_device_name(device)
    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using {name} ")# torch.cuda.get_device_name(0)
    
    model = TweetyNetModel(len(Counter(all_tags)), (1, n_mels, 216), device, batchsize = batch_size, binary=False)
    # model = 
    # model.cuda()
    model.to(torch.cuda.current_device())#()
    model.train()
    # summary(model.to(torch.cuda.current_device()),(1, n_mels, 216))

    # print(f'is model in GPU? {model.is_cuda}')

    print(torch.cuda.get_device_name(model.device))
    for i in model.parameters():
        # print('model param')
        # print(i)
        print(i.is_cuda)
    next(model.parameters()).to(torch.cuda.current_device())#.cuda()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    print(dt_string)

    train_dataset = train_dataset #(train_dataset).cuda()
    val_dataset = val_dataset#(val_dataset).cuda()

    history, test_out, start_time, end_time, date_str = model.train_pipeline(train_dataset,val_dataset, None,
                                                                       lr=lr, batch_size=batch_size,epochs=epochs, save_me=True,
                                                                       fine_tuning=False, finetune_path=None, outdir=outdir)#.cuda()
    print("Training time:", end_time-start_time)

    os.chdir(cwd)

    with open(os.path.join(outdir,"nips_history.pkl"), 'wb') as f:   # where does this go??? it has to end up in data/out
        pickle.dump(history, f, pickle.HIGHEST_PROTOCOL) 

    return model, date_str

def evaluate(model,test_dataset, date_str, hop_length, sr, outdir,temporal_graphs): # How can we evaluauate on a specific wav file though?? and show time in the csv? and time on a spectrorgam? ¯\_(ツ)_/¯
    
    model_weights = os.path.join(outdir,f"model_weights-{date_str}.h5") # time sensitive file title
    tweetynet = model
    test_out, time_segs = tweetynet.test_load_step(test_dataset, hop_length, sr, model_weights=model_weights) 
    test_out.to_csv(os.path.join(outdir,"Evaluation_on_data.csv"))
    time_segs.to_csv(os.path.join(outdir,"Time_intervals.csv"))
    
    # orig_stdout = sys.stdout

    # sys.stdout = open(os.path.join('data/out','file_score_rates.txt'), 'w')
    file_score(temporal_graphs)
    # sys.stdout.close()

    # sys.stdout = orig_stdout
    file_graph_temporal(temporal_graphs) 
    file_graph_temporal_rates(temporal_graphs) 
    
    return print("Finished Classifcation")