### Adding Custom Error Handlers

So far you might have realized that whenever the API is throwing `404` error code, we can getting following message in the `response body`
```html
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try
    again.</p>
```
This is a default `HTML` message that is added by `flask`
Naturally, we dont want to deal with HTML in APIs.
So our goal is to return some message in `json` format for error codes of `404` or `500`