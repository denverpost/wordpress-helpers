<!DOCTYPE html>
<html lang="en">
    <head>
        <title></title>
        <meta name="description" content="" />
        <meta name="viewport" content="width=device-width" />
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta http-equiv="Content-Type" content="text/html;" />
        <link rel='stylesheet' id='knowlton-styles-css'  href='https://assets.digitalfirstmedia.com/prod/static/css/denverpost.css?ver=1.0' type='text/css' media='all' />
        <link rel='stylesheet' id='mason-fonts-css'  href='https://fonts.googleapis.com/css?family=Open%20Sans|Source+Serif+Pro%3A400%2C400italic%2C600%2C600italic%2C700%2C700italic%7CSource+Sans+Pro%3A400%2C400italic%2C600%2C600italic%2C700%2C400italic&#038;ver=4.5.3' type='text/css' media='all' />
        <style type="text/css">
            input, textarea { clear: both; }
        </style>
    </head>
    <body class="body-copy">
        <h1></h1>
        <p></p>
        <form method="POST">
            <input type="submit" value="Submit">
            <hr noshade>
            <p></p>
            <textarea name="content" id="content" cols="100" rows="40" style="clear: both; width:100%; height:80%;">
<?php
if ( isset($_POST['content']) ):
?>
<?php
    // Strip the custom markup on the paragraphs
    $content = str_replace("\n\n", "\n", '<li>' . $_POST['content']);

    $content = htmlspecialchars($content); 
    
    echo $content;
?>
<?php endif; ?>
</textarea>
            <input type="submit" value="Submit">
        </form>

</body>
</html>
