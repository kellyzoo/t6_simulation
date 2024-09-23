import numpy as np
import cv2
from utils import _write_as_png, _generate_test_image

def reshuffle_mosaic2vid(image, K):
    """
    Vectorized conversion of a mosaic image into K^2 low-resolution frames.
    
    Args:
    - image (numpy array): Input mosaic image of shape (H, W).
    - K (int): Size of each KxK tile.
    
    Returns:
    - frames (numpy array): Reshuffled frames of shape (K^2, H//K, W//K).
    """
    
    H, W = image.shape
    assert H % K == 0 and W % K == 0, "Image dimensions must be divisible by K"
    
    # Reshape the image to extract KxK tiles
    # (H//K, K, W//K, K): reshapes into submatrices where each is KxK
    reshaped_image = image.reshape(H // K, K, W // K, K)
    
    # Transpose to get the KxK tile dimensions aligned for reshuffling
    # Now shape is (H//K, W//K, K, K)
    transposed_image = reshaped_image.transpose(0, 2, 1, 3)
    
    # Reshape to combine the KxK tiles into K^2 separate frames
    # (H//K, W//K, K^2): each KxK tile is now flattened into K^2 and frames are across the grid
    flattened_image = transposed_image.reshape(H // K, W // K, K * K)
    
    # Transpose to get the final frame structure
    # (K^2, H//K, W//K): now we have K^2 frames of size H//K x W//K
    frames = flattened_image.transpose(2, 0, 1)
    
    return frames


if __name__ == "__main__":
    # Example usage
    image_path = "/home/daniel/t6_simulation/outputs/coded_exposure_2x2_00000.png"
    K = 2
    # # Presume 320 x 640 image
    image = cv2.imread(image_path, 0)
    image = (image.astype(float) * 16)
    # image = np.tile(_generate_test_image(K, 320), (1, 2)) * 256 * 16
    print(f"Input image shape: {image.shape}")
    # Each bucket individually
    size = image.shape[0]
    image_0 = image[:, :size]
    image_1 = image[:, size:]

    _write_as_png(f"./outputs/frame.png", image)
    _write_as_png(f"./outputs/frame_0.png", image_0)
    _write_as_png(f"./outputs/frame_1.png", image_1)

    frames_0 = reshuffle_mosaic2vid(image_0, K)
    frames_1 = reshuffle_mosaic2vid(image_1, K)

    print(f"Reshuffled frames shape: {frames_0.shape}")
    # print(f"Reshuffled frames shape: {frames.shape}")

    # # Save the frames as .npy and .png files
    # Show base images
    for i, frame in enumerate(frames_0):
        # The output folder in inverse_solvers
        _write_as_png(f"./outputs/frame_0_{i:05d}.png", frame)
    for i, frame in enumerate(frames_1):
        # The output folder in inverse_solvers
        _write_as_png(f"./outputs/frame_1_{i:05d}.png", frame)
