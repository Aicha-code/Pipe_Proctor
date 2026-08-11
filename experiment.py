from use_croma import PretrainedCROMA

"""
this is an experiment at using the pretrained CROMA model for SAR images.
I am adding comments at each step for what will need to be updated/modified when we get our training data.
Depending on the dataset's size, I might have to finetune the model on our dataset, but I will first try to use it as is and see how it performs.
"""
# To experiment with CROMA, O downloaded the model weights from https://huggingface.co/antofuller/CROMA/tree/main
model = PretrainedCROMA(pretrained_path='CROMA_base.pt', size='base', modality='SAR', image_resolution=120)
# The model will not work if the input images are of a different size than the one specified here. 
