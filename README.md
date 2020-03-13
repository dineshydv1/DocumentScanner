# DocumentScanner
Create Document Scanner using Computer Vision, OpenCV and Python

I published this in Medium article: 
Link: https://towardsdatascience.com/document-scanner-using-computer-vision-opencv-and-python-20b87b1cbb06


Basic steps:

Step 1: Read the photograph or image

Step 2: Identify the edges

Step 3: Detect document edges in the image:

Step 4: Identify and extract document boundary/edges:

Step 5: Apply perspective transform:

About files:

1. File scanner_wb.ipynb is a interactive jupyter notebook. 
2. prod folder has python scripts to run from command line. These scripts can be used to integrate this with flask/docker to run on the fly. 
3. Script prod/scanner.py inputs 2 argument: (photo-name, BWflag)
