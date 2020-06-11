import numpy as np
import matplotlib.pyplot as plt
import os

def read_image(imagefile):
    # Reads image in imagefile and returns color and gray-level images
    #
    img = (plt.imread(img_dir+file)*255).astype(int)
    img = img[:,:,:3]  # Remove transparency channel
    img_gl = np.mean(img,axis=2).astype(int)
    return img, img_gl
"""/////////////////////////////////////////////////////////////////////////////////////"""
def drawRectangle(I, r, c, h, w):
    
    p = np.array([[r,c],[r+h,c],[r+h,c+w],[r, c+w],[r,c]])
    """Here i create an array with the 4 points of the rectangle"""
    """The first point is represented by [r,c] and the other points modify r and c by adding h and w to them"""
    """w which represents width of the desired area is added to c which represents the column"""
    """h which represents the height of the desired area is added to r which represents the row"""
    fig, ax = plt.subplots(nrows = 1, ncols=1) #this line opens up an ax plot
    
    ax.plot(p[:,0],p[:,1],linewidth=1,color='blue') #this line plots the rectangle on the picture
    ax.imshow(I, cmap='gray') #this line puts the image on the ax plot
    plt.show()
    

def brightestPixel(I):
    r = 0 #represents rows
    c = 0  #represents columns
    brightestValue = -200 
    h = 10
    w = 10
    for i in range(len(I)):
        for j in range(len(I[0])):
            if I[i][j] > brightestValue:
                r = i
                c = j
                brightestValue = I[i][j]
            #the if statement replaces the current brightestValue if the current pixel has a higher value then 
            #the current value stored in brightestValue
    p = np.array([[r-h,c-w],[r+h,c-w],[r+h,c+w],[r-h, c+w],[r-h,c-w]]) 
    #draws a rectangle around the brightest pixel
    #the rectangle has the pixel at its center, not in its upper left corner
    fig, ax = plt.subplots(nrows = 1, ncols=1)
    ax.plot(p[:,0],p[:,1],linewidth=1,color='blue')
    ax.imshow(I, cmap='gray')
    plt.show()

def naiveAlgorithmVersion1Point1(I, h, w):
    largestRegionTotal = -255
    sumX = 0
    X = 0
    Y = 0
    for row in range(len(I) - h +1):
        for column in range (len(I[0]) - w +1):
            #the 2 for loops below will break the big array into smaller segments of a given height and range 
            for rowModifier in range (h):
                for columnModifier in range (w):
                    sumX += I[row + rowModifier, column + columnModifier] 
                    #I add rowModifier and columnModifier to row and column in order to get a segment of the 
                    #proper size and shape 
            #if sumX is larger than the current largest region total then X and Y are updated
            if sumX > largestRegionTotal:
                X = row
                Y = column 
                #X and Y become row and column without any modifiers because row and column are the upper 
                #left corners of the rectangle, which is the parameter drawRectangle needs to function properly
                largestRegionTotal = sumX
            sumX = 0 #sumX gets reset so after the sum of each segment is found, this way the sum doesnt keep increasing
            
                 
    drawRectangle(I, Y, X, h, w)
    return Y,X

def naiveAlgorithmVersion1Point2(I, h, w):
    largestRegionTotal = -255; 
    sumX = 0
    X = 0
    Y = 0
    for i in range(len(I) - h +1):
        for j in range (len(I[0]) - w +1):
            #where before added each array index to another variable here I create a new array and use a built in function
            #to add them more quickly
            tempArray = I[i:i+h,j:j+w] #creates an array of height h and width w, values are taken from the oringal image
            sumX = np.sum(tempArray) #adds together every value in the previously created array
            if sumX > largestRegionTotal: #will replace largestRegionTotal only if sumX is greater
                largestRegionTotal = sumX
                X = i
                Y =j
                sumX = 0
            
    drawRectangle(I, Y, X, h, w)
    return Y,X

def computeIntegralImage(I):
    S = np.zeros((len(I) + 1, len(I[0] )+ 1), dtype = int) 
    #creates an array the same size as the integral image array
    #not the integral image array yet, since it's currently filled with zeroes    
    for row in range(1,len(S)):
        for column in range (1,len(S[0])):
            #I start row and column at 1 because the integral image will have only zeros in row 0 and column 0
            S[row,column]= np.sum(I[:row,:column]) 
            """
            -use array splicing to create an array from I that starts above and to the left of row and column 
            -use np.sum to add the contents of the array into a single value
            -add that value to S at position [row,column]
            -repeat until S is full and now S is the integral image
            """
    
    return S
 
def naiveAlgorithmVersion2Point1(I, h, w):
    S = computeIntegralImage(I)
    sumX = 0
    storage = np.array([])
    for row in range(len(I) - h + 1):
        for column in range(len(I[0] ) -w + 1):
            sumX = S[row+h,column+w] - S[row][column+w] - S[row+h][column] + S[row][column]
            #S[row+h,column+w] gives me the summation of every single element above and to the left 
            #S[row,column+w] subtracts the values located on the top that should be subtracted
            #S[row+h,column] subtracts the values located on the left that should be subtracted
            #S[row,column] ads the values located above and to the left 
            print(sumX)
            #I'm choosing to print it even though it'll take forever to finish
    
            
def naiveAlgorithmVersion2point2(I, h, w, row, column):
    S = computeIntegralImage(I)
    sumX = S[row+h,column+w] - S[row][column+w] - S[row+h][column] + S[row][column]
    
    
      
if __name__ == "__main__":  


    img_dir = r'C:\Users\ldd77\Desktop\Computer Science\Data Structures\Lab 2\lab2imgs\\' # Directory where images are stored
    img_files = os.listdir(img_dir)  # List of files in directory
    plt.close('all')
    

    i = 1
    for file in img_files:
        print(file)
        if file[-4:] == '.png': # File contains an image
            img, img_gl = read_image(img_dir+file)    
            drawRectangle(img_gl, 0,0,1000,1000)
            print('This is the photo for drawRectangle')
            brightestPixel(img_gl)
            print('This is the photo for brightestPixel')
            X, Y = naiveAlgorithmVersion1Point1(img_gl, 20,20)
            print('This is the photo for naiveAlgorithmVersion1Point1')
            X , Y = naiveAlgorithmVersion1Point2(img_gl, 20,20)
            print('This is the photo for naiveAlgorithmVersion1Point2')
            naiveAlgorithmVersion2Point1(img_gl, 20,20)
            print('This is the calculations for naiveAlgorithmVersion2Point1')
            naiveAlgorithmVersion2Point1(img_gl, X, Y, 20,20)
            print('This is the calculations for naiveAlgorithmVersion2Point2')
            plt.show()
            
            print(i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)
            i+=1

    i = 1
    for file in img_files:
        print(file)
        if file[-4:] == '.png': # File contains an image
            img, img_gl = read_image(img_dir+file)    
            drawRectangle(img_gl, 0,0,1000,1000)
            print('This is the photo for drawRectangle')
            brightestPixel(img_gl)
            print('This is the photo for brightestPixel')
            X, Y = naiveAlgorithmVersion1Point1(img_gl, 30,30)
            print('This is the photo for naiveAlgorithmVersion1Point1')
            X , Y = naiveAlgorithmVersion1Point2(img_gl, 30,30)
            print('This is the photo for naiveAlgorithmVersion1Point2')
            naiveAlgorithmVersion2Point1(img_gl, 30,30)
            print('This is the calculations for naiveAlgorithmVersion2Point1')
            naiveAlgorithmVersion2Point1(img_gl, X, Y, 30,30)
            print('This is the calculations for naiveAlgorithmVersion2Point2')
            plt.show()
            
            print(i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)
            i+=1
    i = 1
    for file in img_files:
        print(file)
        if file[-4:] == '.png': # File contains an image
            img, img_gl = read_image(img_dir+file)    
            drawRectangle(img_gl, 0,0,1000,1000)
            print('This is the photo for drawRectangle')
            brightestPixel(img_gl)
            print('This is the photo for brightestPixel')
            X, Y = naiveAlgorithmVersion1Point1(img_gl, 30,60)
            print('This is the photo for naiveAlgorithmVersion1Point1')
            X , Y = naiveAlgorithmVersion1Point2(img_gl, 30,60)
            print('This is the photo for naiveAlgorithmVersion1Point2')
            naiveAlgorithmVersion2Point1(img_gl, 30,60)
            print('This is the calculations for naiveAlgorithmVersion2Point1')
            naiveAlgorithmVersion2Point1(img_gl, X, Y, 30,60)
            print('This is the calculations for naiveAlgorithmVersion2Point2')
            plt.show()
            
            print(i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)
            i+=1

    i = 1
    for file in img_files:
        print(file)
        if file[-4:] == '.png': # File contains an image
            img, img_gl = read_image(img_dir+file)    
            drawRectangle(img_gl, 0,0,1000,1000)
            print('This is the photo for drawRectangle')
            brightestPixel(img_gl)
            print('This is the photo for brightestPixel')
            X, Y = naiveAlgorithmVersion1Point1(img_gl, 60,60)
            print('This is the photo for naiveAlgorithmVersion1Point1')
            X , Y = naiveAlgorithmVersion1Point2(img_gl, 60,60)
            print('This is the photo for naiveAlgorithmVersion1Point2')
            naiveAlgorithmVersion2Point1(img_gl, 60,60)
            print('This is the calculations for naiveAlgorithmVersion2Point1')
            naiveAlgorithmVersion2Point1(img_gl, X, Y, 60,60)
            print('This is the calculations for naiveAlgorithmVersion2Point2')
            plt.show()
            
            print(i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)
            i+=1

    i = 1
    for file in img_files:
        print(file)
        if file[-4:] == '.png': # File contains an image
            img, img_gl = read_image(img_dir+file)    
            drawRectangle(img_gl, 0,0,1000,1000)
            print('This is the photo for drawRectangle')
            brightestPixel(img_gl)
            print('This is the photo for brightestPixel')
            X, Y = naiveAlgorithmVersion1Point1(img_gl, 60,100)
            print('This is the photo for naiveAlgorithmVersion1Point1')
            X , Y = naiveAlgorithmVersion1Point2(img_gl, 60,100)
            print('This is the photo for naiveAlgorithmVersion1Point2')
            naiveAlgorithmVersion2Point1(img_gl, 60,100)
            print('This is the calculations for naiveAlgorithmVersion2Point1')
            naiveAlgorithmVersion2Point1(img_gl, X, Y, 60,100)
            print('This is the calculations for naiveAlgorithmVersion2Point2')
            plt.show()
            
            print(i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)
            i+=1
            
    i = 1
    for file in img_files:
        print(file)
        if file[-4:] == '.png': # File contains an image
            img, img_gl = read_image(img_dir+file)    
            drawRectangle(img_gl, 0,0,1000,1000)
            print('This is the photo for drawRectangle')
            brightestPixel(img_gl)
            print('This is the photo for brightestPixel')
            X, Y = naiveAlgorithmVersion1Point1(img_gl, 100,100)
            print('This is the photo for naiveAlgorithmVersion1Point1')
            X , Y = naiveAlgorithmVersion1Point2(img_gl, 100,100)
            print('This is the photo for naiveAlgorithmVersion1Point2')
            naiveAlgorithmVersion2Point1(img_gl, 100,100)
            print('This is the calculations for naiveAlgorithmVersion2Point1')
            naiveAlgorithmVersion2Point1(img_gl, X, Y, 100,100)
            print('This is the calculations for naiveAlgorithmVersion2Point2')
            plt.show()
            
            print(i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)
            i+=1
