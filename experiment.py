from use_croma import PretrainedCROMA
import torch 
import torch.nn.functional as F

"""
this is an experiment at using the pretrained CROMA model for SAR images.
I am adding comments at each step for what will need to be updated/modified when we get our training data.
I might have to finetune CROMA on our dataset, but I will use it as is to understand it better.
"""
# To experiment with CROMA, I downloaded the model weights from https://huggingface.co/antofuller/CROMA/tree/main
model = PretrainedCROMA(pretrained_path='CROMA_base.pt', size='base', modality='SAR', image_resolution=120)
# The input images should not be of a different size than the one specified here. 

# The model expects the input to be a tensor of shape (batch_size, channels, height, width). with channels== 1 for SAR images.
print("model loaded ✅!")

"""
    Test to see if CROMA gives me different results when I pass the same input twice to represnet the case where a place is being monitored but nothing has changed. 
    I expect the output to be the same in this case. 
"""
N = 4

sentinel_1_t1 = torch.randn(N, 2, 120, 120)
# print(f"input transformsation:\n shape: {sentinel_1.shape}\n type: {type(sentinel_1)}\n dtype: {sentinel_1.dtype}")
sentinel_1_t2 = sentinel_1_t1.clone()

# Simulate sentinel-1 data with some noise added to the original image to represent a change in the scene.
noise = torch.randn_like(sentinel_1_t1) * 0.5

sentinel_1_t2_A = sentinel_1_t1 + noise


#compute outputs for all tests
with torch.no_grad():

    # Experiment A
    output_t1 = model(sentinel_1_t1)
    output_t2 = model(sentinel_1_t2)

    # Experiment B
    output_t1_change = model(sentinel_1_t1)
    output_t2_change = model(sentinel_1_t2_A)


# print experiments results with statistics about the similarity between the encodings of the two images.
def compare_encodings(output_t1, output_t2, experiment_name):
    """
    Compare the SAR encodings and print statistics about their similarity.
    """

    encoding_t1 = output_t1["SAR_encodings"]
    encoding_t2 = output_t2["SAR_encodings"]

    # Cosine similarity between corresponding spatial patches
    similarity = F.cosine_similarity(
        encoding_t1,
        encoding_t2,
        dim=-1
    )

    # Convert similarity to a change score
    change = 1 - similarity

    print("\n")
    print(f"Results: {experiment_name}")
    print("=" * 40)

    print(f"Encoding T1 shape: {encoding_t1.shape}")
    print(f"Encoding T2 shape: {encoding_t2.shape}")

    print(f"Mean change: {change.mean().item():.6f}")
    print(f"Maximum change: {change.max().item():.6f}")
    print(f"Minimum change: {change.min().item():.6f}")

compare_encodings(
    output_t1,
    output_t2,
    "A - No anomaly"
)

compare_encodings(
    output_t1_change,
    output_t2_change,
    "B - Simulated anomaly at T2"
)

"""
    Write code to set a similarity threshold that will help in identifying changes to patch P at time tx
"""