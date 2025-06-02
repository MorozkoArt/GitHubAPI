from tqdm import tqdm
import time

class ProgressBar:
    def __init__(self, total, text, color='green'):
        self.total = total
        self.text = text
        self.color = color
        
        
        self.pd = tqdm(
            desc=self.text,
            total=self.total,
            ncols=80,
            colour=self.color,
            leave=True,          
        )
        
        self.start_time = time.time()
        
    def update_pd(self, amount=1):
        self.pd.update(amount)
        
    def set_description(self, text):
        self.pd.set_description_str(text)
        
    def set_postfix(self, **kwargs):
        self.pd.set_postfix(**kwargs)
        
    def close_pd(self):
        self.pd.close()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_pd()