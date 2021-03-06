/*
 * Copyright 2011 Facebook, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

Config = null;

// I think we need to run this only if we are called in the context of facebook
function facebookInit(config) {
  Config = config;

  FB.init({
    appId: Config.appId,
    cookie: true,
    xfbml: true,
    channelUrl:
      window.location.protocol + '//' + window.location.host + Config.channelUrl 
  });
  FB.Event.subscribe('auth.sessionChange', handleSessionChange);
  FB.Canvas.setAutoResize();

  // ensure we're always running on apps.facebook.com
  // NOTE: this function check if we are in a frame
  // which we want to disable since we want to support both regular & facebook app
  // if (window == top) { goHome(); }
}

 function facebookConnect(form){
      function handleResponse(response){
          form.submit();
      }
      FB.login(handleResponse/*,{perms:'publish_stream,sms,offline_access,email,read_stream,status_update,etc'}*/);
  }

function handleSessionChange(response) {
  // NOTE: kusno - this function is called when session changed
  // Not sure why we need this function in the original run with friends
  // maybe by going home, it will relogin with the new uid ?
  if ((Config.userIdOnServer && !response.session) ||
      Config.userIdOnServer != response.session.uid) {
    // this happen if the session change, and user id is different from the one 
    // in the application. Maybe somebody logged in with different credential
    // before.
    // goHome();
  }
}

function goHome() {
  top.location = 'http://apps.facebook.com/' + Config.canvasName + '/';
}

function setDateFields(date) {
  document.getElementById('date_year').value = date.getFullYear();
  document.getElementById('date_month').value = date.getMonth() + 1;
  document.getElementById('date_day').value = date.getDate();
}
function dateToday() {
  setDateFields(new Date());
}
function dateYesterday() {
  var date = new Date();
  date.setDate(date.getDate() - 1);
  setDateFields(date);
}

function publishRun(title) {
  FB.ui({
    method: 'stream.publish',
    attachment: {
      name: title,
      caption: "I'm running!",
      media: [{
        type: 'image',
        href: 'http://runwithfriends.appspot.com/',
        src: 'http://runwithfriends.appspot.com/splash.jpg'
      }]
    },
    action_links: [{
      text: 'Join the Run',
      href: 'http://runwithfriends.appspot.com/'
    }],
    user_message_prompt: 'Tell your friends about the run:'
  });
}
