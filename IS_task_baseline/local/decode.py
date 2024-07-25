import os
from pathlib import Path
from desed_task.utils.encoder import ManyHotEncoder

import numpy as np
import pandas as pd
import scipy
import torch

from desed_task.evaluation.evaluation_measures import compute_sed_eval_metrics
import json
import re

import soundfile
import glob
from thop import profile, clever_format

from sed_scores_eval.utils.scores import create_score_dataframe

def read_audio_lengths(duration_file):
    """
    Read the audio lengths from the duration file.

    Args:
        duration_file (str): Path to the duration file.

    Returns:
        dict: A dictionary mapping file names to their respective durations.
    """
    audio_lengths = {}
    # 使用pandas读取tsv文件
    df = pd.read_csv(duration_file, sep='\t', header=0)
    for index, row in df.iterrows():
        audio_lengths[row[0]] = float(row[1])
    return audio_lengths


def batched_decode_from_files(
    pred_folder, filenames, encoder, thresholds=[0.5], median_filter=7, pad_indx=None,
):
    """ Decode a batch of predictions to dataframes. Each threshold gives a different dataframe and stored in a
    dictionary

    Args:
        strong_preds: torch.Tensor, batch of strong predictions.
        filenames: list, the list of filenames of the current batch.
        encoder: ManyHotEncoder object, object used to decode predictions.
        thresholds: list, the list of thresholds to be used for predictions.
        median_filter: int, the number of frames for which to apply median window (smoothing).
        pad_indx: list, the list of indexes which have been used for padding.

    Returns:
        dict of predictions, each keys is a threshold and the value is the DataFrame of predictions.
    """
    # Init a dataframe per threshold
    prediction_dfs = {}
    for threshold in thresholds:
        prediction_dfs[threshold] = pd.DataFrame()

    for j, filename in enumerate(filenames):
        audio_id_match = re.search(r'strong_(\w+)_\d+\.tsv', filename)
        if audio_id_match:
            dynamic_part1 = audio_id_match.group(1)
            dynamic_part2 = audio_id_match.group(2) if len(audio_id_match.groups()) > 1 else None
            c_scores = pd.read_csv(Path(pred_folder) / filename, sep='\t')
        
        if pad_indx is not None:
            true_len = int(c_scores.shape[-1] * pad_indx[j].item())
            c_scores = c_scores.iloc[:, :true_len]

        #c_scores = c_scores.transpose().to_numpy()
        #c_scores = scipy.ndimage.median_filter(c_scores, (median_filter, 1))
        #labels=getattr(encoder, 'labels', np.array([]))

        labels = encoder.labels
        #print(labels)
        #exit()

        for c_th in thresholds:
            pred = c_scores > c_th
            #print(c_scores,pred)
            #exit()
            #pred = encoder.decode_strong(pred, labels=getattr(encoder, 'labels', np.array([])))
            #pred = pd.DataFrame(pred, columns=["event_label", "onset", "offset"])
            #pred["filename"] = filename
            #prediction_dfs[c_th] = pd.concat([prediction_dfs[c_th], pred], ignore_index=True)
            try:
                pred = encoder.decode_strong(pred,labels=labels)
            except Exception as e:
                print(f"Error decoding at threshold {c_th}: {e}")
                continue
            pred = pd.DataFrame(pred, columns=["event_label", "onset", "offset"])
            pred["filename"] = filename
            prediction_dfs[c_th] = pd.concat([prediction_dfs[c_th], pred], ignore_index=True)

    return prediction_dfs

test_thresholds = np.arange(1 / (50 * 2), 1, 1 / 50)

pred_folder = "/Share/slf/IS_task/IS_task_baseline/exp/IStask_baseline/student/scenario1/real_scores"
all_files = os.listdir(pred_folder)
matching_files = [file for file in all_files if re.match(r'strong_(\w+)_\d+\.tsv', file)]

# 读取音频长度信息
duration_file = "/Share/slf/IS_task/IS_task_baseline/exp/IStask_baseline/student/test_durations_strong.tsv"
audio_lengths = read_audio_lengths(duration_file)


#encoder_instance= ManyHotEncoder()

encoder_instances = {}
for audio_file, duration in audio_lengths.items():
    # 计算音频文件的帧数
    total_frames = int(duration * 16000)
    # 初始化ManyHotEncoder
    encoder_instance = ManyHotEncoder(labels=['Infantcry', 'Snoring'], audio_len=total_frames, frame_len=2048, frame_hop=256)
    

prediction_dfs_student = batched_decode_from_files(
    pred_folder=pred_folder,
    filenames=[f for f in matching_files if f.startswith(f'strong_{audio_file}')],
    encoder=encoder_instance,
    median_filter=7,
    thresholds=test_thresholds.tolist() + [0.5],
)

# Extract the decoded results
decoded_student_strong = prediction_dfs_student[0.5]  

output_folder = "/Share/slf/IS_task/IS_task_baseline/exp/IStask_baseline/student/scenario1/decoded"
os.makedirs(output_folder, exist_ok=True)

# Save the decoded results to a TSV file in the specified folder
output_path_tsv = os.path.join(output_folder, "results.tsv")
decoded_student_strong.to_csv(output_path_tsv, sep='\t', index=False)