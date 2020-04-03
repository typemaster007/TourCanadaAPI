var poolData = {
    UserPoolId: 'us-east-1_XN8aPr8lM', // Your user pool id here
    ClientId: '1ii0qtop55e71mbd5eups6njcc' // Your client id here
};
console.log('here');

function hello() {
    console.log('inside Hello');
}

function signIn() {
    var username = $('#sign_in_username').val();
    var password = $('#sign_in_password').val();
    // console.log('asas');
    console.log(username);
    console.log(password);
    var authenticationData = {
        Username: username,
        Password: password,
    };

    var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(authenticationData);
    var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(poolData);

    var userData = {
        Username: username,
        Pool: userPool
    };

    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function (result) {
            twoFA();
        },

        onFailure: function (err) {
            alert(err);
        }

    });
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
    // var phone =$('#registration_phone').val();
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

    var attributeList = [];

    var dataEmail = {
        Name: 'email',
        Value: email
    };

//     var dataPhoneNumber = {
// 	Name: 'phone_number',
// 	Value: '+15555555555',
// };

    var attributeEmail = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserAttribute(dataEmail);
//     var attributePhoneNumber = new AmazonCognitoIdentity.CognitoUserAttribute(
// 	dataPhoneNumber
// );

    attributeList.push(attributeEmail);
    // attributeList.push(attributePhoneNumber);


    userPool.signUp(username, password, attributeList, null, function (err, result) {
        if (err) {
            alert(err);
            return;
        }
        cognitoUser = result.user;
        console.log('user name is ' + cognitoUser.getUsername());
    });
    var data = {
        "username": username,
        "password": password,
        'name': fname+' '+lname,
        'email': email
    };
    var resp = $.ajax({
        url: '/register',
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
        },
        error: function (error) {
        }
    });

    var final = resp.responseJSON;
    console.log(final);
    if (final['success']) {
        window.location.href = '/register/authenticate?username=' + username + '&email=' + email;
    }
}

function validate() {
    var username=$('#code_username').val();
    var code = $('#code_code').val();
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

    var userData = {
        Username: username,
        Pool: userPool
    };

    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
    cognitoUser.confirmRegistration(code, true, function (err, result) {
        if (err) {
            alert(err);
            return;
        }
        console.log('call result: ' + result);
        window.location.href='/login'
    });
}

function signOut() {
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var cognitoUser = userPool.getCurrentUser();

    if (cognitoUser !== null) {
        cognitoUser.signOut();
    }
    window.location.href = "/";
}

function twoFA() {
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var cognitoUser = userPool.getCurrentUser();

    if (cognitoUser != null) {
        cognitoUser.getSession(function (err, session) {
            if (err) {
                alert(err);
                return;
            }
            console.log(cognitoUser.signInUserSession.accessToken.jwtToken);
            $('#username').html(cognitoUser.username);
        });
    }

    var url = "/api/protected_api";


    cognitoUser.getAttributeVerificationCode('email', {
        onSuccess: function (result) {
            var data = {
                "username": cognitoUser.username
            };
            var resp = $.ajax({
                url: '/login',
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
                },
                error: function (error) {
                }
            });

            var final = resp.responseJSON;
            console.log(final);
            if (final['success']) {
                window.location.href = '/home';
            }
        },
        onFailure: function (err) {
            alert(err.message || JSON.stringify(err));
        },
        inputVerificationCode: function () {
            var verificationCode = prompt('Please input verification code: ', '');
            cognitoUser.verifyAttribute('email', verificationCode, this);
        },
    });
}