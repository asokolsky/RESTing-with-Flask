/**
 * Common JS functions
 */

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(
        /[?&]+([^=&]+)=([^&]*)/gi, 
        function (m, key, value) {
            vars[key]=value;
        });
    return vars;
}
function getUrlParam(param, defaultValue) {
    if(window.location.href.indexOf(param) > -1)
        return getUrlVars()[param];
    return defaultValue;
}
/**
 * Execute HTTP GET on url, and then call foo on the result.
 */
function RESTget(url, foo) {
    var req = new XMLHttpRequest();
    req.open('GET', url, true);
    req.onload = function() {
        if(req.status < 200 || req.status >= 400)
            return;
        var data = JSON.parse( this.response );
        foo(data);
    }
    req.send();
}
