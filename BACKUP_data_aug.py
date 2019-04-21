import random
from scipy import ndarray
import random
import os
import skimage as sk
from skimage import transform
from skimage import util
from skimage import io
import shutil

def random_rotation(original_image_array: ndarray, gt_image_array: ndarray,):
    # pick a random degree of rotation between 100% on the left and 100% on the right
    random_degree = random.uniform(-100, 100)
    return sk.transform.rotate(original_image_array, random_degree), sk.transform.rotate(gt_image_array, random_degree)
    
# Do not augment GT
def random_noise(image_array: ndarray):
    # add random noise to the image
    return sk.util.random_noise(image_array)

def horizontal_flip(image_array: ndarray):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]
    
def vertical_flip(image_array: ndarray):
    # vertical flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, :-1:]


# our folder path containing some images
original_image_folder_path = '/home/ranjith/Desktop/updated_img/vessel_raw'
gt_image_folder_path = '/home/ranjith/Desktop/updated_img/vessel_gt'

original_image_save_folder_path = '/home/ranjith/Desktop/updated_img/augmented/vessel_raw'
gt_image_save_folder_path = '/home/ranjith/Desktop/updated_img/augmented/vessel_gt'

#if os.path.exists("/home/ranjith/Desktop/updated_img/augmented"):
#    shutil.rmtree("/home/ranjith/Desktop/updated_img/augmented")
#else:
#    os.makedirs("/home/ranjith/Desktop/updated_img/augmented")
    
#if not os.path.exists("/home/ranjith/Desktop/updated_img/augmented/X"):
#    os.makedirs("/home/ranjith/Desktop/updated_img/augmented/X")
    
#if not os.path.exists("/home/ranjith/Desktop/updated_img/augmented/y"):
#    os.makedirs("/home/ranjith/Desktop/updated_img/augmented/y")    


# the number of file to generate
num_files_desired = 200

# loop on all files of the folder and build a list of files paths
original_images = [os.path.join(original_image_folder_path, f) for f in os.listdir(original_image_folder_path) if os.path.isfile(os.path.join(original_image_folder_path, f))]
gt_images = [os.path.join(gt_image_folder_path, f) for f in os.listdir(gt_image_folder_path) if os.path.isfile(os.path.join(gt_image_folder_path, f))]

num_generated_files = 0
while num_generated_files <= num_files_desired:

    # random images from the folder
    original_image_path = random.choice(original_images)
    gt_image_path = os.path.join(gt_image_folder_path, original_image_path.split('/')[-1])
    
    # read images as a two dimensional array of pixels
    original_image_to_transform = io.imread(original_image_path)
    gt_image_to_transform = io.imread(gt_image_path)
    
    # dictionary of the transformations functions we defined earlier
    available_transformations = {
        'rotate': random_rotation,
        'noise': random_noise,
        'horizontal_flip': horizontal_flip,
        'vertical_flip': vertical_flip,
    }
    
    # random num of transformations to apply
    num_transformations_to_apply = random.randint(1, len(available_transformations))
    
    num_transformations = 0
    transformed_image = None
    while num_transformations <= num_transformations_to_apply:
        # choose a random transformation to apply for a single image
        key = random.choice(list(available_transformations))
        
        if key == 'noise' :
            original_transformed_image = available_transformations[key](original_image_to_transform)
            gt_transformed_image = gt_image_to_transform
            
        elif key == 'rotate' :
            original_transformed_image, gt_transformed_image = available_transformations[key](original_image_to_transform, gt_image_to_transform)
        
        else:
            original_transformed_image = available_transformations[key](original_image_to_transform)
            gt_transformed_image = available_transformations[key](gt_image_to_transform)
        
        num_transformations += 1
        
        # define a name for our new file
        original_file_path = '%s/augmented_image_%s.png' % (original_image_save_folder_path, num_generated_files)
        gt_file_path = '%s/augmented_image_%s.png' % (gt_image_save_folder_path, num_generated_files)

        # write images to the disk
        io.imsave(original_file_path, original_transformed_image)
        io.imsave(gt_file_path, gt_transformed_image)
    
    num_generated_files+=1
