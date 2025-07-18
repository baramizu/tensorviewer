import numpy as np

def load_data(filename):
  if filename.endswith('.npy') or filename.endswith('.np'):
    return np.load(filename, allow_pickle=True), ""
  if filename.endswith('.npz'):
    try:
      data = np.load(filename, allow_pickle=True)
      return {k: v for k, v in data.items()}, ""
    except Exception as e:
      return None, f"Error loading .npz file: {str(e)}"
  if filename.endswith('.csv'):
    return np.loadtxt(filename, delimiter=','), ""
  if filename.endswith('.txt'):
    return np.loadtxt(filename), ""
  if filename.endswith('.pt') or filename.endswith('.pth'):
    try:
      import torch
      return torch.load(filename, map_location='cpu').numpy()
    except ImportError:
      return None, "PyTorch is not installed. Cannot load .pt or .pth files."
  return None, "Unsupported file format."