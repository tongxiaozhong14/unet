import os
import glob
import numpy as np

from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms
import pandas as pd

import pdb


class IsicDataset(Dataset):
    def __init__(self, opt):
        data_files = sorted(glob.glob(opt.data_dir + "/*.*"))
        mask_files = sorted(glob.glob(opt.mask_dir + "/*.*"))

        try:
            table_df = pd.read_csv(os.path.dirname(os.path.dirname(opt.data_dir)) + '/train_test_split.csv')
            print('Using existing train/test split')
        except:
            print('Generating new train/test split')
            table_df = pd.DataFrame(list(zip(data_files, mask_files)), columns=['data_files', 'mask_files'])
            mask = np.random.rand(len(table_df)) < 0.8
            table_df['test'] = mask
            table_df.to_csv(os.path.dirname(os.path.dirname(opt.data_dir)) + '/train_test_split.csv')

        if opt.test:
            self.data_files = table_df[~table_df.test].data_files.tolist()
            self.mask_files = table_df[~table_df.test].mask_files.tolist()
        else:
            self.data_files = table_df[table_df.test].data_files.tolist()
            self.mask_files = table_df[table_df.test].mask_files.tolist()

        img = Image.open(self.data_files[0])
        h, w = img.size

        self.transform = transforms.Compose(
            [
                transforms.Resize((int(h * opt.scale), int(w * opt.scale)), Image.BICUBIC),
                # transforms.ToTensor(),
                # transforms.Normalize(mean, std),
            ]
        )