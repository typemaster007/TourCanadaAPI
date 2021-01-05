# TourCanada

## Authors:
* Amogh Adithya Bangalore
* Daksh Patel

> The folder "frontend" contains the code of the website's frontend.
 
> The folder "2fa" contains the code of the for registration module and email verification.
><br><small>Note: "2fa" module is independent module. To run it, follow its readMe.

To run the api on localhost:
* `clone the repo`
* `cd 'TourCanada-API`
* `pip install -r requirements.txt`
* `python app.py`

<b>Link to website:</b> https://s3.amazonaws.com/www.tourcanada.ca/index.html

## If you are opening the above website for the first time you need to make the following changes in the browser settings(preferably Google Chrome):
```
The reason we need to do this is because the frontend of the website is HTTPS certified and the APIs which are 
hosted on Elastic Beanstalk are not HTTPS certified.
```
 * Open https://s3.amazonaws.com/www.tourcanada.ca/index.html.
 * Click on the lock and then click on the site settings as show in the image below
 ![Step 1 and 2](imgs/step1_2.png)
 * Scroll all the way down to the page opened after step 1.
 * Change `Insecure content` to `Allow`.
 ![Step 3](imgs/step3.png)
 * Close the tab and then refresh the page.
 Now you can use all the functionalities of the website.
 
 
## API endpoints for Tour Canada.

```
Endpoint: /register
Type: POST
Parameters: username, name, email
On success response: {
    'status': True,
    'code': 200,
    'message': “Success message”,
    'result': {}
}
```
```
<b>Endpoint: /getUserDetails
Type: GET
Parameters: username
On success response: {
    “status”: True,
    “code”: 200,
    'message': “Success message”,
    “result”: {
    “name”: “John Doe”, 
    “email”: 
    ”johndoe@example.com”,
       }
}
``` 
```
<b>Endpoint</b>: /getTrendingLocations
Type: GET
Parameters: N/A
On success response: {
  "status": true,
  "code": 200,
  "message": "Trending locations fetched successfully",
  "result": [
    [
      {
        "photoURL": url_to_photo",
        "location": "Halifax"
      },
      {
        "photoURL": url_to_photo",
        "location": "Vancouver"
      },
      {
        "photoURL": " url_to_photo",
        "location": "Toronto"
      }
    ],
    [
      {
        "photoURL": " url_to_photo ",
        "location": "Cape Breton"
      },
      {
        "photoURL": " url_to_photo",
        "location": "Waterloo"
      },
      {
        "photoURL": " url_to_photo ",
        "location": "Montreal"
      }
    ]
  ]
}
Note: In results, there is a 2-D list (where inner one is of length 3) which contains dictionary of search results for location.
```
```
<b>Endpoint</b>: /destinations
Type: GET
Parameters: location (eg: halifax)
On success response: {
  "status": true,
  "code": 200,
  "message": "Trending locations fetched successfully",
  "result": [
    [
      {
        "photoURL": url_to_photo",
        "location": "Point Pleasant Park"
      },
      {
        "photoURL": url_to_photo",
        "location": "Halifax Citadel"
      },
      {
        "photoURL": " url_to_photo",
        "location": "Black Rock Beach"
      }
    ]
  ]
}
Note: In results, there is a 2-D list( where inner one is of length 3) which contains dictionary of search results for location.
```
```
<b>Endpoint</b>: /make_payment</b>
Type: POST
Parameters: user_id, username, location, place, numTickets, amount, date
On success response: {
  "status": true,
  "code": 200,
  "message": "Booking inserted successfully!",
  "result": {
    "uid": 126948,
    }
}
```
```
<b>Endpoint</b>: /get_image_url
Type: GET
Parameters: username
On success response: {
    "status": true,
    "code": 200,
    "message": "Image fetched successfully!",
  "result": {
      “img_url”: base64 encoded url
     for the image of qrcode stored
    in s3.
    }
}
```
```
<b>Endpoint</b>: /get_my_bookings
Type: GET
Parameters: username
On success response: {
  "status": true,
  "code": 200,
  "message": "Bookings fetched Successful!",
  "result": [
    [
      {
        "date_ticket": "2020-04-15",
        "ticket_location": "Point Pleasant Park",
        "user_id": "3aa2f70d-30d6-46a7-aa13-
        e688f4fe468d",
        "numTickets": "1",
        "img_url": base64 encoded url
        for the image of qrcode stored
        in s3.,
        "ticket_city": "Halifax",
        "username": "daksh2298",
        "amount_ticket": "$12",
        "id": 126948
      },
    ]
  ]
}
Note: In results, there is a 2-D list( where inner one is of length 3) which contains dictionary of search results for location.
```
