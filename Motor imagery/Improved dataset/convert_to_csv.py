import numpy as np
import pandas as pd
import os
def npy_to_csv(input_file, output_file, labels):
    data = np.load(input_file)
    df = pd.DataFrame(data.T, columns=labels)
    df.to_csv(output_file, index=False)
input_dir = '.'
output_dir = './to_csv'
os.makedirs(output_dir, exist_ok=True)
labels = ['FC6', 'C4', 'CP6', 'CP5', 'FC5', 'C3']
for i in range(1, 51):
    input_file = os.path.join(input_dir, f'l_{i}.npy')
    output_file = os.path.join(output_dir, f'l_{i}.csv')
    npy_to_csv(input_file, output_file, labels)
