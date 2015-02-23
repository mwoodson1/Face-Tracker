import cv2

def outlineRect(image,rect,color):
    if rect is None:
        return
    x, y, w, h = rect;
    cv2.rectangle(image,(x,y),(x+w,y+h),color)

def copyRect(src, dst, srcRect, dstRect, interpolation = cv2.INTER_LINEAR):
    """Copy part of the cource to part of the destination"""
    x0, y0, w0, h0 = srcRect
    x1, y1, w1, h1 = dstRect

    #Resize the contents of the source rectangle
    dst[y1:y1+h1,x1:x1+w1] = cv2.resize(src[y0:y0+h0,x0:x0+w0], (w1,h1),interpolation = interpolation)

def swapRects(src, dst,rects, interpolation = cv2.INTER_LINEAR):
    """Copy the source with two or more rectangles swapped"""
    if dst is not src:
        dst[:] = src

    numRects = len(rects)
    if numRects < 2:
        return

    x, y, w, h = rects[numRects - 1]
    temp = src[y:y+h,x:x+w].copy()

    i = numRects - 2;
    while i >= 0:
        copyRect(src, dst, rects[i], rects[i+1], interpolation)
        i -= 1

    copyRect(temp, dst, (0,0,w,h), rects[0], interpolation)