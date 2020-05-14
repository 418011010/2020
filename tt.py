import pandas as pd
import numpy as np
import time
from tqdm import tqdm

df = pd.DataFrame(np.random.randint(0, 100, (10000000, 6)))
tqdm.pandas(desc="my bar！")
df.progress_apply(lambda x: x ** 2)


