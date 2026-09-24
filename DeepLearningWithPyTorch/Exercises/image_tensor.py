import imageio.v2 as imageio
import torch

img_arr = imageio.imread('DeepLearningWithPyTorch/Documents/golden-retriever-tongue-out.jpg')
print(img_arr.shape)

img = torch.from_numpy(img_arr)
out = img.permute(2, 0, 1)

print(out.shape)