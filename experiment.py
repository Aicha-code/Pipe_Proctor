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

"""
    Test to see if CROMA gives me different results when I pass the same input twice to represnet the case where a place is being monitored but nothing has changed. 
    I expect the output to be the same in this case. 
"""
N = 4

sentinel_1 = torch.randn(N, 2, 120, 120)
# print(f"input transformsation:\n shape: {sentinel_1.shape}\n type: {type(sentinel_1)}\n dtype: {sentinel_1.dtype}")
sentinel_1_2 = sentinel_1.clone()
with torch.no_grad():
    outputs = model(sentinel_1, sentinel_1_2)


# print model output information
for output in outputs:
    try:
        print(f"model output 👀:\n shape: {output.shape}\n type: {type(output)}\n dtype: {output.dtype}")
    except AttributeError:
        print(f"model output 🥹:\n type: {type(outputs)}")
        if isinstance(outputs, dict):
            print("output keys:")
            for key in outputs:
                print(f"  {key}")
            print("output shapes:")
            for key, value in outputs.items():
                if torch.is_tensor(value):
                    print(f"  {key}: {value.shape}")
                else:
                    print(f"  {key}: {type(value)}")
            print("output values:")
            for key, value in outputs.items():
                print(f"  {key}: {value}")
        else:
            print(f"oups, teh output is not of teh expected shape, see it below:\n {outputs}")
