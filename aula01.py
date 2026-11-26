import cv2
imagem = cv2.imread('image.jpg')  # Load an image from file
cv2.imshow('CHARLIE BROWN JR', imagem)  # Display the image in a window
cv2.waitKey(0)  # Wait indefinitely for a key press
cv2.destroyAllWindows()  # Close all OpenCV windows
# Print a success message, mostrar linhas e colunas dos pixels da imagem
print(imagem.shape)
