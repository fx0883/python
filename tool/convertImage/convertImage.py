import cv2
import logging

imageSizeList = [20, 29, 40, 48,50,57,58,60,72,76,80,87,96,100,144,148,152,167,192,256,512,1024]
img = cv2.imread("source.png")


for sizeItem in imageSizeList:
    res=cv2.resize(img,(sizeItem,sizeItem))
    cv2.imwrite("retIonic/"+str(sizeItem)+".png", res)

print("finish")

# cv2.imshow('iker',res)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# cv2.imwrite("retIonic/72.png", res)
# cv2.imwrite("retIonic/172.png", res2)

# cv2.waitKey(0)