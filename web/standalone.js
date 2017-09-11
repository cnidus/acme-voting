// App specific
var identityPoolId = 'us-east-1:b0453bc5-1210-48c0-a375-24fc84114a9c';
var userPoolId = 'us-east-1_OMWTZDS27';//'us-east-1_fgCWraBkF';
var appClientId = '6l8gpqtsa1e8pt1qstj4mauele';//'57lq262n28o7ddt8i36jcjj7qd';
var region = 'us-east-1';

// constructed
var loginId = 'cognito-idp.' + region + '.amazonaws.com/' + userPoolId;
var poolData = {
   UserPoolId: userPoolId,
   ClientId: appClientId
};

function registerUser(user)
{
   // Need to provide placeholder keys unless unauthorised user access is enabled for user pool
   AWSCognito.config.update({accessKeyId: 'anything', secretAccessKey: 'anything'});

   var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(poolData);

   var attributeList = [];

   var dataEmail = {
      Name: 'email',
      Value: user.email
   };

   var dataName = {
      Name: 'name',
      Value: user.name
   };

   attributeList.push(new AWSCognito.CognitoIdentityServiceProvider.CognitoUserAttribute(dataEmail));
   attributeList.push(new AWSCognito.CognitoIdentityServiceProvider.CognitoUserAttribute(dataName));

   userPool.signUp(user.username, user.password, attributeList, null, function (err, result) {
      if (err) {
         console.log(err);
         return;
      }
      alert('User ' + user.username + ' Created')
   });
}

function confirmUser(username, code)
{
   // Need to provide placeholder keys unless unauthorised user access is enabled for user pool
   AWSCognito.config.update({accessKeyId: 'anything', secretAccessKey: 'anything'});

   var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(poolData);

   var userData = {
      Username: username,
      Pool: userPool
   };

   var cognitoUser = new AWSCognito.CognitoIdentityServiceProvider.CognitoUser(userData);

   cognitoUser.confirmRegistration(code, true, function (err, result){
      if (err) {
         console.log(err);
         return;
      }
      alert('User ' + username + '  Confirmed');
   });
}

function loginUser(username, password)
{
   // Need to provide placeholder keys unless unauthorised user access is enabled for user pool
   AWSCognito.config.update({accessKeyId: 'anything', secretAccessKey: 'anything'});

   var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(poolData);

   var authenticationData = {
      Username: username,
      Password: password
   };

   var authenticationDetails = new AWSCognito.CognitoIdentityServiceProvider.AuthenticationDetails(authenticationData);

   var userData = {
      Username: username,
      Pool: userPool
   };

   var cognitoUser = new AWSCognito.CognitoIdentityServiceProvider.CognitoUser(userData);

   cognitoUser.authenticateUser(authenticationDetails, {
      onSuccess: (result) => {
         alert(username + ' Logged In');
         setCredentials(result.getIdToken().getJwtToken());
      },
      onFailure: (err) => {
         console.log(err);
      }
   });
}

function getSession()
{
   var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(poolData);

   var cognitoUser = userPool.getCurrentUser();

   if (cognitoUser != null) {
      cognitoUser.getSession(function(err, session){
         if (err) {
            logoutUser();
            return;
         }
         $('.session').text(session.getIdToken().getJwtToken());
         setCredentials(session.getIdToken().getJwtToken());
      });
   }
   else logoutUser();
}

function logoutUser()
{
   var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(poolData);
   var cognitoUser = userPool.getCurrentUser();
   alert('Logged Out');
   if (cognitoUser != null) cognitoUser.signOut();
}

/* Helper Functions */

function setCredentials(token)
{
   AWS.config.credentials = new AWS.CognitoIdentityCredentials({
      IdentityPoolId: identityPoolId,
      Logins: {}
   });
   AWS.config.credentials.params.Logins[loginId] = token;
}
