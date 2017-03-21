# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:09:16 2017

@author: Jack Tan

Collect reviews of a product from Amazon. Append the reviews to a file called "reviews.txt". The file should include the 
following TAB-separated columns:

column 1: the review's rating
column 2: the review's title
column 3: the review's date of submission, as it appears on the website
column 4: the FULL review text, exactly as it appears on the website
"""

import urllib2, re, time

# enter a product url, for example: https://www.amazon.com/Venom-Meagan-Good/product-reviews/B00ALXHPFE/ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=avp_only_reviews 
# look at this example url, in the following step, we need to extract "https://www.amazon.com/Venom-Meagan-Good/" and "B00ALXHPFE". these two parts are what matters.
    
url = raw_input("Please enter the pruduct url: ")
url_info = re.findall('(https://www.amazon.com/.+?/).+?/(.+?)/', url)

# a boolean to tell if it has reached the end of all reviews
noMorePages = False

# number of review pages
pageNo = 1

# initiate a browswer
browser = urllib2.build_opener()
browser.addheaders = [('User-agent', 'Mozilla/5.0')]

# set up a file object to write the output later
fileWriter = open('reviews.txt','a')

while True: 
    # build the actual review url
    url_reviews = url_info[0][0] + 'product-reviews/' + url_info[0][1] + '/ref=cm_cr_getr_d_paging_btm_' + str(pageNo) + '?pageNumber=' + str(pageNo) + '&sortBy=helpful'
    
    while True: 
        try: 
            #Use the browser to open url_reviews
            response = browser.open(url_reviews)
        except Exception as e: 
            print "Error url: ", url_reviews
            print type(e).__name__
            print e
            continue
        
        # read the HTML source
        pageSource = response.read()
        if re.search('Sorry, no reviews match your current selections',pageSource):
            noMorePages = True
            print 'Finished downloading reviews for this product!'
            #When we find this sentence, it should be the page right after the last review page. We should break here
            break
        # since this pattern is long and it probably span multiple lines, add re.S flag to let dot(.) match newline characters
        reviews = re.findall('<i data-hook="review-star-rating".+?<span class="a-icon-alt">(.+?) stars</span>.+?<a data-hook="review-title" class="a-size-base a-link-normal review-title a-color-base a-text-bold" href=.+?>(.+?)</a>.+?<span data-hook="review-date" class="a-size-base a-color-secondary review-date">on (.+?)</span></div>.+?<span data-hook="review-body" class="a-size-base review-text">(.+?)</span>', pageSource, re.S)
        # set a time delay to allow more time to load page source
        time.sleep(2)
        # Normally the number of reviews is greater than 0, page is loaded successfully, break the loading process      
        if len(reviews) > 0:
            break
        print 'Page not loaded successfully, load again.'
        
    #If noMorePages, break the first "while" loop
    if noMorePages:
        break
    
    # the variable reviews is a list of review blocks(rev), and each review block(rev) is a tuple of the demanded content, like rev[0]: rating, rev[1]: title, rev[2]: data, rev[3]: content
    # We also need to remove HTML tag contents, when the review contains a video block
    for rev in reviews:
        # the contect of this review block
        content = rev[3]
        content = re.sub('<div.*?>|<input.*?>|</.*?>|<br.*?>', '', content)
        content = re.sub('\n', '', content)
        content = re.sub('&nbsp;', ' ', content)
        content = re.sub('&#34;', '\"', content)
        content = re.sub('&#60;', '<', content)
        content = re.sub('&#62;', '>', content)
        fileWriter.write(rev[0] + '\t' + rev[1] + '\t' + rev[2] + '\t' + rev[3] + '\n')
        
    print 'Page', pageNo, 'done.'
    pageNo = pageNo + 1
    
fileWriter.close()  