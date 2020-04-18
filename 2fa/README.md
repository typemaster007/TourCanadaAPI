# Registration and email verification.

To run the registration api on localhost:<br>
>Note: even if you run it, you need to change the port number to run it along with the API module
* `pip install -r requirements.txt`
* `python app.py`

To run it on EC2 install `(unbuntu 18.04)`:
* Create an *ubuntu 18.04* instance on EC2.
* Follow the steps mentioned in the file  [mongo-docker-aws-ubuntu.txt](./mongo-docker-aws-ubuntu.txt)
* Once mongodb, docker and docker-compose starts running, replace the host ip at [line 19 in app.py](https://git.cs.dal.ca/daksh/tourcanada-api/-/blob/master/2fa/app.py#L19) by your EC2 instance's public ip. <small>Note: You need to open following ports in your security group: 27017, 27018, 27019 and 5000.
* zip the current folder and upload it to your EC2 instance. (Eg: Use `scp -i "your_key.pem" 2fa.zip ubuntu@ec2-your-public-ip-here.compute-1.amazonaws.com:~`)
* unzip the folder on EC2.
* `cd 2fa`
* Run `docker-compose build`
* Run `docker-compose up -d`