import tqdm

class ProgressBar:
    def __init__(self, total, text):
        self.total = total
        self.pd = tqdm.tqdm(
            desc=text,
            total=self.total,
            miniters=1,
            ncols=100,
            unit='it',
            unit_scale=True,
            unit_divisor=1024,
        )
    def update_pd(self):
        self.pd.update(1)
    def close_pd(self):
        self.pd.close()