from sklearn.datasets import fetch_california_housing
import ray
from ray import data

def load_data():
    ray.init(ignore_reinit_error=True)
    
    data_raw = fetch_california_housing(as_frame=True)
    df = data_raw.frame

    ray_ds = data.from_pandas(df)
    
    return ray_ds.to_pandas()