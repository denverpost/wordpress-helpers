<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Redirect Helper</title>
        <meta name="description" content="" />
        <meta name="viewport" content="width=device-width" />
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta http-equiv="Content-Type" content="text/html;" />
        <link rel='stylesheet' id='knowlton-styles-css'  href='https://assets.digitalfirstmedia.com/prod/static/css/denverpost.css?ver=1.0' type='text/css' media='all' />
        <link rel='stylesheet' id='mason-fonts-css'  href='https://fonts.googleapis.com/css?family=Open%20Sans|Source+Serif+Pro%3A400%2C400italic%2C600%2C600italic%2C700%2C700italic%7CSource+Sans+Pro%3A400%2C400italic%2C600%2C600italic%2C700%2C400italic&#038;ver=4.5.3' type='text/css' media='all' />
        <style type="text/css">
input, textarea { clear: both; }
body { margin: .5em 1em; }
input[type=url],
input[type=email]
{
    border: 1px solid #999;
    border-radius: 0;
    color: #1a1a1a;
    height: 30px;
    padding: .5em .625em;
    transition: border-color .25s linear;
}
p
{
    margin-bottom: 1em;
}
        </style>
    </head>
    <body class="body-copy">
        <h1>Redirect Helper</h1>
        <p>Emails a ticket to DFM from you requesting a redirect.</p>
<?php
if ( isset($_POST['email']) ):
    $to = 'websupport@medianewsgroup.com';
    $from = trim(htmlspecialchars($_POST['email']));
    $url_from = trim(htmlspecialchars($_POST['url_from']));
    $url_to = trim(htmlspecialchars($_POST['url_to']));
    $subject = 'Redirect request for ' . $url_from;
    $message = 'Hi, could you please redirect ' . $url_from . ' to ' . $url_to . ' . Thanks!';
    $headers = 'From: ' . $from . "\r\n" .
    'Reply-To: ' . $from . "\r\n" .
    'Bcc: jmurphy@denverpost.com ' . "\r\n" .
    'X-Mailer: PHP/' . phpversion();
    mail($to, $subject, $message, $headers);
?>
        <p><strong>Thanks!</strong> The following email was sent to websupport@medianewsgroup.com:</p>
        <p><?php echo $message; ?></p>
<?php
else:
?>
        <form method="POST">
            <p>
                <label for="email">
                    Hi, my email address is <input type="email" name="email">
                </label>
                <label for="url_from">
                    and I want to redirect from <input type="url" name="url_from" placeholder="http://...">
                </label>
                <label for="url_to">
                    to <input type="url" name="url_to" placeholder="http://..."> and when I click that red button this script will request this redirect from DFM.
                </label>
            </p>
            <input type="submit" value="Request the redirect">
        </form>
<?php
endif;

