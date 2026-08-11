from use_croma import PretrainedCROMA
import torch

"""
this is an experiment at using the pretrained CROMA model for SAR images.
I am adding comments at each step for what will need to be updated/modified when we get our training data.
I might have to finetune CROMA on our dataset, but I will use it as is to understand it better.
"""
# To experiment with CROMA, I downloaded the model weights from https://huggingface.co/antofuller/CROMA/tree/main
model = PretrainedCROMA(pretrained_path='CROMA_base.pt', size='base', modality='SAR', image_resolution=120)
# The model will not work if the input images are of a different size than the one specified here. 

# sentinel_SAR_image = torch.rand(1, 1, 120, 120)
# The model expects the input to be a tensor of shape (batch_size, channels, height, width). with channels== 1 for SAR images.
print("model loaded ✅!")

#sample dummy input to test the model
N = 4

sentinel_1 = torch.randn(N, 2, 120, 120)
print(f"input transformsation:\n shape: {sentinel_1.shape}\n type: {type(sentinel_1)}\n dtype: {sentinel_1.dtype}")

with torch.no_grad():
    outputs = model(sentinel_1)
# print model output information