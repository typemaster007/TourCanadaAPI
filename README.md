# TourCanada

> The folder "frontend" contains the code of the website's frontend.

To run the api on localhost:
* `clone the repo`
* `cd 'TourCanada-API`
* `python app.py`.

<b>Link to website:</b> https://s3.amazonaws.com/www.tourcanada.ca/index.html

## If you are opening the above website for the first time you need to make the following changes in the browser settings(preferably Google Chrome):
```
The reason we need to do this is because the frontend of the website is HTTPS certified and the APIs which are hosted on Elastic Beanstalk
 are not HTTPS certified.
```
 * Open https://s3.amazonaws.com/www.tourcanada.ca/index.html.
 * Click on the lock and then click on the site settings as show in the image below
 ![Step 1 and 2](imgs/step1_2.png)
 * Scroll all the way down to the page opened after step 1.
 * Change `Insecure content` to `Allow`.
 ![Step 3](imgs/step3.png)
 * Close the tab and then refresh the page.
 Now you can use all the functionalities of the website.
 
 
 




