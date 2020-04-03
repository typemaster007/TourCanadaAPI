__author__ = "Daksh Patel"

from project.model.LocationModel import Location
from project.model.LoginModel import Login
from project.model.forms import *
from utils import capitalizeAll, createNested, createResponse
from project import app

@app.route('/destinations', methods=['GET'])
def destinations():
    location = Location()
    login = Login()
    key = 'user'
    user = login.getUserDetails(session.get(key)).get('Items')[0]
    loc = request.args.get('location').lower()
    destinations_loc = capitalizeAll(location.getDestinations(loc))
    for i in range(len(destinations_loc)):
        del destinations_loc[i]['id']
    finalDestinations = createNested(destinations_loc)
    code = 200
    status = True
    message = 'Search successful!'
    result = finalDestinations
    resp = createResponse(
        status_value=status,
        code=code,
        message=message,
        result=result
    )
    print('here', resp)
    return resp


@app.route('/make_booking', methods=['GET', 'POST'])
def make_booking():
    form = PaymentForm()
    return render_template('payment.html', form=form, title='Payment')


@app.route('/getTrendingLocations', methods=['GET', 'POST'])
def getTrendingLocations():
    location = Location()
    trendingLocations = capitalizeAll(location.getLocations())
    print(trendingLocations)
    trendingLocations = sorted(trendingLocations, key=lambda t: t['id'])[:6]
    for i in range(len(trendingLocations)):
        del trendingLocations[i]['id']
    finalTrends = createNested(trendingLocations)
    code = 200
    status = True
    message = 'Trending locations fetched successfully'
    result = finalTrends
    resp = createResponse(
        status_value=status,
        code=code,
        message=message,
        result=result)
    return resp
