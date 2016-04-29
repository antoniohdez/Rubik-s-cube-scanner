

   def filter_shapes(self, contours, min_size = 10):
        filtered_contours = []
        for cnt in contours:
            if len(cnt) == 4:
                a, b = cnt[0][0], cnt[2][0]
                size = math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))
                if size > min_size:
                    filtered_contours.append(cnt)

        return filtered_contours




    def detect_shapes(self, frame):
        # Detecting shapes...
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray_frame = cv2.bilateralFilter(gray_frame, 7, 1, 1)
        edged = cv2.Canny(gray_frame, 20, 20)
        cv2.imshow('threshold', edged)


        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
        screenCnt = None

        # loop over our contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.01 * peri, True)

            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                orig = gray_frame.copy()
                cv2.drawContours(gray_frame, [screenCnt], -1, (255, 255, 255), 3)
                
        cv2.imshow("Screen", gray_frame)
        
        thresh = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        #cv2.imshow('threshold', thresh)

        contours, h = cv2.findContours(thresh, cv2.cv.CV_RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        contours = self.filter_shapes(contours, 1)

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            # print len(approx)
            if len(approx) == 4:
                pass
                # print "square"
                # print cnt
                #if cnt[0][0][0] > 5 and cnt[0][0][1] > 5:
                #    cv2.drawContours(frame,[cnt],0,(255,255,255),-1)
                
            cv2.drawContours(frame,[cnt],0,(255,255,255),-1)