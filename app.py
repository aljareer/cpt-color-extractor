import streamlit as st
from PIL import Image
import numpy as np
import io

# Function to extract colors from the image
def extract_colors(image, num_colors=5):
    # Convert image to RGB
    image = image.convert('RGB')
    # Resize image for faster processing
    image = image.resize((150, 150))
    # Convert image data to a flat array of RGB values
    pixels = np.array(image).reshape(-1, 3)
    # Cluster the pixels to find the dominant colors
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    # Sort colors by frequency
    sorted_colors = unique_colors[np.argsort(-counts)]
    # Return the most frequent colors
    return sorted_colors[:num_colors]

# Function to save colors to CPT format
def save_cpt(colors, filename):
    with open(filename, 'w') as f:
        f.write('# COLOR_MODEL = RGB\n')
        for i, color in enumerate(colors):
            r, g, b = color
            f.write(f'{i} {r} {g} {b} {i} {r} {g} {b}\n')

# Streamlit app
st.title('Color Palette Generator')

st.write('Upload an image, and this tool will extract the dominant colors and allow you to save them in CPT format.')

uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Open the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Extract colors
    num_colors = st.slider('Number of Colors', 1, 20, 5)
    colors = extract_colors(image, num_colors)
    
    # Display color palette
    st.write('Color Palette:')
    palette = np.zeros((50, num_colors * 50, 3), dtype=np.uint8)
    for i, color in enumerate(colors):
        palette[:, i*50:(i+1)*50] = color
    st.image(palette, width=300)
    
    # Dynamic color adjustment (simplified)
    st.write('Adjust the color gradients using the sliders below:')
    adjusted_colors = []
    for i, color in enumerate(colors):
        r, g, b = color
        r = st.slider(f'Red {i+1}', 0, 255, r)
        g = st.slider(f'Green {i+1}', 0, 255, g)
        b = st.slider(f'Blue {i+1}', 0, 255, b)
        adjusted_colors.append([r, g, b])
    
    # Save CPT file
    filename = st.text_input('Enter filename to save as CPT', 'colors.cpt')
    if st.button('Save CPT File'):
        save_cpt(adjusted_colors, filename)
        st.success(f'File saved as {filename}')
    
    # Option for automatic save (example implementation)
    if st.checkbox('Auto-Save'):
        save_cpt(adjusted_colors, filename)
        st.success(f'File automatically saved as {filename}')
