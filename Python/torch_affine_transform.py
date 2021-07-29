import torch
import numpy as np
import matplotlib.pyplot as plt
import torchvision


# Create an image.
w = 256
h = 256
a = torch.zeros(1, 3, h, w)
# a[:, :, :, :] = 0.5
a[:, :, int(0.0*h):int(0.25*h), int(0.0*w):int(0.25*w)] = 1

# Apply affine transform.
shiftx = -1
shifty = -1
theta = torch.tensor(
    [1, 0, shiftx, 0, 1, shifty],
    dtype=torch.float).view(-1, 2, 3)
grid = torch.nn.functional.affine_grid(theta, a.size())
x = torch.nn.functional.grid_sample(a, grid)

# Apply invert affine transform.
_theta = torch.tensor(
    [1, 0, -shiftx, 0, 1, -shifty],
    dtype=torch.float).view(-1, 2, 3)
_grid = torch.nn.functional.affine_grid(_theta, x.size())
_a = torch.nn.functional.grid_sample(x, _grid)

# Show images.
a_img = np.transpose(a.squeeze().numpy(), (1,2,0))
x_img = np.transpose(x.squeeze().numpy(), (1,2,0))
_a_img = np.transpose(_a.squeeze().numpy(), (1,2,0))

plt.subplot(131)
plt.imshow(a_img)
plt.xticks(np.arange(0, w+1, w/8))
plt.yticks(np.arange(0, h+1, h/8))
plt.title('a')

plt.subplot(132)
plt.imshow(x_img)
plt.xticks(np.arange(0, w+1, w/8))
plt.yticks(np.arange(0, h+1, h/8))
plt.title('x')

plt.subplot(133)
plt.imshow(_a_img)
plt.xticks(np.arange(0, w+1, w/8))
plt.yticks(np.arange(0, h+1, h/8))
plt.title('_a')

plt.show()
