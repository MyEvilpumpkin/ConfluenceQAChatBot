from enum import Enum
from transformers import pipeline as pipe


# Define an enumeration for different loading policies
class LoadingPolicy(Enum):
    EAGER = 1
    LAZY = 2
    DISPOSABLE = 3


# Set the default loading policy to LAZY
loading_policy = LoadingPolicy.LAZY


# Define a function that acts as a factory for creating pipelines based on the current loading policy
def pipeline(*args, **kwargs):
    lazy_model = None

    def lazy_load(*model_args, **model_kwargs):
        nonlocal lazy_model
        if lazy_model is None:
            lazy_model = pipe(*args, **kwargs)
        return lazy_model(*model_args, **model_kwargs)

    if loading_policy == LoadingPolicy.EAGER:
        return pipe(*args, **kwargs)
    elif loading_policy == LoadingPolicy.LAZY:
        return lazy_load
    elif loading_policy == LoadingPolicy.DISPOSABLE:
        return lambda *model_args, **model_kwargs: pipe(*args, **kwargs)(*model_args, **model_kwargs)
