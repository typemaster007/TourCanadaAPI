// import "./amazon-cognito-identity.min";
// import "./aws-cognito-sdk.min";

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function deleteCookie() {
  var cookies = document.cookie.split(";");

  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i];
    var eqPos = cookie.indexOf("=");
    var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    console.log(name);
    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;";
  }
  console.log(document.cookie);
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function checkCookie() {
  var user = getCookie("username");
  if (user != "") {
    // alert("Welcome again " + user);
  } else {
    alert("User not logged in! \n Please login again");
    window.location.href = 'index.html';
    // user = prompt("Please enter your name:", "");
    // if (user != "" && user != null) {
    //   setCookie("username", user, 365);
    // }
  }
}

function makeRequest(url, data = {}, method = "GET") {
  var resp = $.ajax({
    url: url,
    data: data,
    dataType: 'json',
    type: method,
    async: false,
    beforeSend: function (x) {
      if (x && x.overrideMimeType) {
        x.overrideMimeType("application/j-son;charset=UTF-8");
      }
    },
    success: function (resp) {
      console.log('i', resp);
    }
  }).responseJSON;
  return resp;
}

function getUserDetails(username) {
  var data = {
    'username': username
  };
  var method = 'GET';
  var url = 'http://cloudproj2-env.us-east-1.elasticbeanstalk.com/getUserDetails';
  var resp = makeRequest(url, data);
  if (resp['status']) {
    resp = resp['result'];
    $('#user_name').text(resp['name']);
    setCookie('name', resp['name']);
    setCookie('email', resp['email']);
  } else {
    alert('User not found!\nPlease sign in again!');
    window.location.href = 'index.html';
  }
}

function getDestinations(location) {
  if (location === null) {
    location = $("[name='location']").val();
  }
  console.log(location);
  setCookie('location', location, 1);
  window.location.href = 'destinations.html';
}

function getTrendingLocations(username) {
  var url = 'http://cloudproj2-env.us-east-1.elasticbeanstalk.com/getTrendingLocations';
  var data = {};
  var method = 'GET';
  var resp = makeRequest(url, data, method);
  console.log(resp);
  var fluid = $(".container-fluid");
  if (resp['status']) {
    resp = resp['result'];
    if (resp.length == 0) {
      fluid.append('<p class="alert-danger">No results found</p>')
    }
    for (i = 0; i < resp.length; i++) {
      var row = resp[i];
      var elem = '<div class="row">';
      for (j = 0; j < row.length; j++) {
        var col = resp[i][j];
        elem += '<div class="col-xl-4 col-md-4 mb-4">';
        elem += '<div id="' + col['location'] + '" class="card border-left-primary shadow p-1" style="height: 25rem;">';
        elem += '<img src="' + col['photoURL'] + '" class="card-img-top" style="height: 17rem;">';
        elem += '<div class="card-body">';
        elem += '<h5 class="card-title">' + col['location'] + '</h5>';
        elem += '</div>';
        elem += '<a href="#' + col['location'] + '" onclick="getDestinations(\'' + col['location'] + '\')" class="btn btn-primary stretched-link mr-2 ml-2 ">Get Info</a>';
        elem += '</div>';
        elem += '</div>';
      }
      elem += '</div>';
      fluid.append(elem);
    }
  } else {
    alert('Something went wrong! \nPlease try again later!');
  }
}

function redirectPayment() {
  var place = $('#placeName').text();
  var date = $('#date').val();
  if (date.length === 0) {
    alert("Please select date for your journey!");
    return false;
  }
  console.log(place);
  console.log(getCookie('location'));
  console.log(date);
  setCookie('place', place, 1);
  setCookie('date', date, 1)
  // console.log()
  window.location.href = 'payment_new.html';
}

function getSearchResults() {
  var location = getCookie('location');
  var url = 'http://cloudproj2-env.us-east-1.elasticbeanstalk.com/destinations';
  var data = {
    'location': location
  };
  var method = 'GET';
  $("#header").text('Results for ' + location);
  $("[name='location']").val(location);
  var fluid = $(".container-fluid");
  var resp = makeRequest(url, data, method);
  console.log(resp);
  if (resp['status']) {
    resp = resp['result'];
    if (resp.length == 0) {
      fluid.append('<p class="text-center text-capitalize alert-danger rounded">No results found</p>')
    }
    for (i = 0; i < resp.length; i++) {
      var row = resp[i];
      var elem = '<div class="row">';
      for (j = 0; j < row.length; j++) {
        var col = resp[i][j];
        elem += '<div class="col-xl-4 col-md-4 mb-4">';
        elem += '<div id="' + col['name'] + '" class="card border-left-primary shadow p-1" style="height: 25rem;">';
        elem += '<img src="' + col['photoURL'] + '" class="card-img-top" style="height: 17rem;">';
        elem += '<div class="card-body">';
        elem += '<h5 class="card-title">' + col['name'] + '</h5>';
        elem += '</div>';
        elem += '<form>';
        elem += '<button onclick="showModal(\'' + col['name'] + '\')" class="btn btn-primary stretched-link mr-2 ml-2 " type="button">Make Payment</button>';
        elem += '</form>';
        elem += '</div>';
        elem += '</div>';
      }
      elem += '</div>';
      fluid.append(elem);
    }
  } else {
    alert('Something went wrong! Please try again later!');
  }

}

function showModal(location) {
  var modalHeader = $('#placeName');
  modalHeader.text(location);
  $('#selectDateModal').modal('show');
}

function changeBadge(val) {
  var bdg;
  var bdgSpan = $('#ticketBadge');
  var totalCount = $('#totalCount');
  var totalAmount = $('#totalAmount');
  // var totalInt=parseInt(totalCount.text());
  // console.log(totalInt);
  // totalCount.text(val);
  var totalText = val.toString();
  totalCount.text(totalText);
  var amount = val * 12;
  amount = '$' + amount.toString();
  totalAmount.text(amount);
  if (val > 1) {
    bdg = val.toString() + " tickets";
    bdgSpan.text(bdg);
  } else {
    bdg = val.toString() + " ticket";
    bdgSpan.text(bdg);
  }
}

function increaseTicketCounter() {
  var ipField = $('#ticketCount');
  var currVal = ipField.val();
  if (currVal >= 6) {
    alert('You can only buy at most 6 tickets in a single transaction!');
  } else {
    var newVal = parseInt(currVal) + 1;
    console.log(newVal);
    ipField.val(newVal);
    changeBadge(newVal);
  }
}

function decreaseTicketCounter() {
  var ipField = $('#ticketCount');
  var currVal = ipField.val();
  if (currVal <= 1) {
    alert('You need atleast 1 ticket to proceed!');
  } else {
    var newVal = parseInt(currVal) - 1;
    console.log(newVal);
    ipField.val(newVal);
    // console.log($(currVal, newVal).val());
    changeBadge(newVal);
  }
}

// var img_url=null;
function makePayment() {
  var cardNumber = $('#cardNumber').val();
  var expiry_month = $('#cc-mm').val();
  var expiry_year = $('#cc-yy').val();
  var cvv = $('#cc-cvv').val();
  var flag = true;
  var message = "";
  // console.log(cardNumber, expiry_month, expiry_year);
  if (cardNumber !== '1111 1111 1111 1111') {
    flag = false;
    message = "Please enter valid card number!";
    // alert('Please enter a valid card number');
  } else if (!parseInt(expiry_month)) {
    flag = false;
    message = "Please enter valid expiry month!";
  } else if (parseInt(expiry_month) > 12) {
    flag = false;
    message = "Please enter valid expiry month!";
  } else if (!parseInt(expiry_year)) {
    flag = false;
    message = "Please enter valid expiry month!";
  } else if (parseInt(expiry_year) < 20) {
    flag = false;
    message = "Please enter valid expiry year!";
  } else if (!parseInt(cvv)) {
    flag = false;
    message = "Please enter valid CVV!";
  }
  if (!flag) {
    alert(message);
    return false;
  } else {
    var user_id = getCookie('user_id');
    var username = getCookie('username');
    var location = getCookie('location');
    var place = getCookie('place');
    var date = getCookie('date');
    var numTickets = $('#ticketCount').val();
    setCookie('ticketCount', numTickets, 1);
    var amount = $('#totalAmount').text();
    setCookie('amount', amount, 1);
    numTickets = parseInt(numTickets);
    // amount = parseInt(amount);
    var data = {
      'user_id': user_id,
      'username': username,
      'location': location,
      'place': place,
      'numTickets': numTickets,
      'amount': amount,
      'date': date
    };
    var method = 'POST';
    var url = 'http://cloudproj2-env.us-east-1.elasticbeanstalk.com/make_payment';
    var resp = makeRequest(url, data, method);
    console.log(resp);
    if (resp['status']) {
      var uid = resp['result']['uid'];
      // img_url = resp['result']['img_url'];
      setCookie('uid', uid, 1);
      // setCookie('img_url', img_url, 1);
      window.location.href = 'ticket_new.html'
    } else {
      alert('Something went wrong! \n Please try again!')
    }
  }
}


function logout() {
  deleteCookie();
  window.location.href = 'index.html';
}

function load2FAcontent() {
  var email = getCookie('email');
  var username = getCookie('username');
  console.log('load2FA', email);
  var msg = 'Hi,\n' + username +
    '            , Your email is successfully verified. <a href="index.html">Click here</a> to login';
  $('#wlcmMsg').html(msg);
}

function print() {
  var username = getCookie('username');
  var uid = getCookie('uid');
  const filename = `${username}_${uid}.pdf`;

  console.log('inside print');
  html2canvas(document.querySelector('#ticketDownload')).then(canvas => {
    let pdf = new jsPDF('p', 'mm', 'a4');
    pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, 211, 298);
    pdf.save(filename);
  });
}

function loadDate() {
  var date = getCookie('date');
  console.log(date);
  $('#journeyDate').text(date);
}


function loadTicketContent() {
  var date = getCookie('date');
  var place = getCookie('place');
  var location = getCookie('location');
  var name = getCookie('name');
  var uid = getCookie('uid');
  var email = getCookie('email');
  var ticketCount = getCookie('ticketCount');
  var user_id = getCookie('user_id');
  var data = {
    'user_id': user_id
  };
  var method = 'GET';
  var url = 'http://cloudproj2-env.us-east-1.elasticbeanstalk.com/get_image_url';
  var resp = makeRequest(url, data, method);
  var img_url = resp['result']['img_url'];

  // var img_url = getCookie('img_url');
  console.log(img_url);
  if (parseInt(ticketCount) <= 1) {
    $('#ticket_count').text("Ticket: " + ticketCount);
  } else {
    $('#ticket_count').text("Tickets: " + ticketCount);
  }
  console.log(img_url);
  $('#qrcode').attr('src', img_url);
  $('#ticket_ticket_id').text(uid);
  $('#ticket_user_name').text(name);
  $('#ticket_place_name').text(place);
  $('#ticket_location_name').text(location);
  $('#ticket_inside_user_name').text(name);
  $('#ticket_trip_date').text(date);
  $('#ticket_email').text(email);
  console.log()

}

function loadMyBookings() {
  var user_id = getCookie('user_id')
  var data = {
    'user_id': user_id
  };
  var method = 'GET';
  var url = 'http://cloudproj2-env.us-east-1.elasticbeanstalk.com/get_my_bookings';
  var resp = makeRequest(url, data, method);
  console.log(resp);
  // var result=resp['result'];
  var name = getCookie('name');
  var email = getCookie('email');
  var fluid = $(".container-fluid");
  if (resp['status']) {
    resp = resp['result'];
    if (resp.length == 0) {
      fluid.append('<p class="text-center text-capitalize alert-danger rounded">No results found</p>')
    }
    for (i = 0; i < resp.length; i++) {
      var row = resp[i];
      var elem = '<div class="row">';
      for (j = 0; j < row.length; j++) {
        var col = resp[i][j];
        var uid = col['id'];
        var date = col['date_ticket'];
        var place = col['ticket_location'];
        var city = col['ticket_city'];
        var img_url = col['img_url'];
        var ticketCount = parseInt(col['numTickets']);
        elem += '<div class="col-xl-4 col-md-4 mb-4">';
        elem += '<div class="card-body text-dark rounded">';
        elem += '<div class="card border-left-primary">';
        elem += '<div class="card-header" style="font-size:1.12vw;">';
        elem += '<span>Ticket ID:';
        elem += `<span>${col['id']}</span>`;
        elem += '</span><br>';
        if (ticketCount <= 1) {
          elem += `<small id="ticket_count">Ticket: ${ticketCount}</small>`;
        } else {
          elem += `<small id="ticket_count">Tickets: ${ticketCount}</small>`;
        }
        elem += '</div>';
        elem += '<div class="card-body text-dark">';
        elem += `<center><img class="card-img-top h-50 w-50" src="${img_url}" alt="url"/></center>`;
        elem += '<table class="table table-responsive text-dark w-auto" style="font-size:1vw;">';
        elem += '<tr>';
        elem += '<td>';
        elem += '<span>Date <img src="img/calendar.svg"/> :</span>';
        elem += '</td>';
        elem += '<td>';
        elem += `<span id="ticket_trip_date">${date}</span>`;
        elem += '</td>';
        elem += '</tr>';
        elem += `<tr>
                      <td>
                        <span>PLACE <img src="img/map-marker-alt.svg"/> :</span>
                      </td>
                      <td>
                        <span id="ticket_place_name">${place}</span>
                      </td>
                    </tr>`;
        elem += `<tr>
                      <td>
                        <span>CITY <img src="img/city.svg"/> :</span>
                      </td>
                      <td>
                        <span id="ticket_location_name">${city}</span>
                      </td>
                    </tr>`;
        elem += `<tr>
                      <td>
                        <span>Name <img src="img/user.svg"/> :</span>
                      </td>
                      <td>
                        <span id="ticket_inside_user_name">${name}</span>
                      </td>
                    </tr>`;
        elem += `<tr>
                      <td>
                        <span>Email <img src="img/envelope.svg"/> :</span>
                      </td>
                      <td>
                        <span id="ticket_email">${email}</span>
                      </td>
                    </tr>
                  </table>
                </div>`;
        elem += '<div class="card-footer mt-2">Have a nice trip!</div>';
        elem += '</div>';
        elem += '</div>';
        elem += '</div>';
      }
      elem += '</div>';
      fluid.append(elem);
    }
  } else {
    alert('Something went wrong! Please try again later!');
  }
}

function checkToken() {
  var url_string = window.location.href;
  var url = new URL(url_string);
  var auth_token = url.searchParams.get("auth_token");
  var username = url.searchParams.get("username");
  console.log(auth_token);
  console.log(username);
  if (auth_token && username) {

    var data = {
      'username': username,
      'auth_token': auth_token
    };
    var resp = makeRequest('http://18.207.227.150:5000/verify_account', data, 'POST');
    if (resp['code'] === 200) {
      alert('Successfully verified!');
    } else {
      alert('Something went wrong!\n Please try again..');
      window.location.href = "index.html";
    }
  } else {
    alert('Something went wrong!\n Please try again..');
    window.location.href = "index.html";
  }
}

function register() {
  var fname = $('#registration_fname').val();
  var lname = $('#registration_lname').val();
  var email = $('#registration_email').val();
  var username = $('#registration_username').val();
  var password = $('#registration_password').val();
  var cpassword = $('#registration_cpassword').val();
  if (password.localeCompare(cpassword) != 0) {
    alert('Confirm Password and password did not matched');
    return;
  }
  var data = {
    'fname': fname,
    'lname': lname,
    'name': fname + ' ' + lname,
    'email': email,
    'username': username,
    'password': password
  };
  var resp = makeRequest('http://18.207.227.150:5000/register', data, 'POST');
  if (resp['code'] === 200) {
    alert(resp['message']);
    var resp = $.ajax({
      url: 'http://cloudproj2-env.us-east-1.elasticbeanstalk.com/register',
      data: data,
      dataType: 'json',
      type: 'POST',
      async: false,
      beforeSend: function (x) {
        if (x && x.overrideMimeType) {
          x.overrideMimeType("application/j-son;charset=UTF-8");
        }
      },
      success: function (response) {
        console.log(response);
      },
      error: function (error) {
      }
    });

    var final = resp.responseJSON;
    console.log(final);
    if (final['status']) {
      console.log(final['message']);
      setCookie('username', username, 1);
      setCookie('email', email, 1)
    }
    window.location.href = "index.html";
  } else if (res['code'] === 400) {
    alert(resp['message']);
    window.location.href = "index.html";
  } else {
    alert('Something went wrong! Please try again');
  }

}

function signIn() {
  var username = $('#sign_in_username').val();
  var password = $('#sign_in_password').val();
  var data = {
    'username': username,
    'password': password
  };
  var resp = makeRequest('http://18.207.227.150:5000/verify_password', data, 'POST');
  if (resp['code'] === 200) {
    // alert(resp['message']);
    var sub = resp['result']['username'];
    setCookie('username', data['username'], 1);
    setCookie('user_id', sub, 1);
    // alert(sub);
    window.location.href = "home.html";
  } else if (res['code'] === 400) {
    alert(resp['message']);
    window.location.href = "index.html";
  } else if (resp['code']===401){
    var resp = makeRequest('http://18.207.227.150:5000/resend_verification', data, 'POST');
    alert('Email not verified!\nPlease verify you email with the link received.');
  }
  else {
    alert('Something went wrong! Please try again');
  }
}