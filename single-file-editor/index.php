<?php
    include('/var/www/lib/class.ftp.php');
    function ftp_it($filename)
    {
        /*
        */
        $path_cache = '';
        $ftp = new ftp;
        $ftp->ftp_directory = '/DenverPost/app/elections/2016';
        //$file_name, $file_directory_local = '', $file_format = 'js', $error_display = FALSE, $file_mode = FTP_ASCII, $file_directory_remote = ''
        $ftp->file_put($filename, $path_cache, '', FALSE, FTP_ASCII, '/DenverPost/app/elections/2016/');
        $ftp->ftp_connection_close();
        return "\n FTP'd: $filename to <a href='http://extras.denverpost.com/app/elections/2016/headline.html'>http://extras.denverpost.com/app/elections/2016/headline.html</a>";
    }
?>
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
            .alert { color: red; }
        </style>
    </head>
    <body class="body-copy">
        <h1>Single-file editor</h1>
        <p></p>
        <form method="POST">
            <input type="submit" name="submit" value="Submit">
            <input type="submit" name="submit" value="Restore Backup">
            <input type="submit" name="submit" value="Impact Hed">
            <hr noshade>
            <p></p>
            <textarea name="content" id="content" cols="100" rows="60" style="clear: both; width:100%; height:80%;">
<?php
if ( isset($_POST['content']) ):
    if ( $_POST['submit'] == 'Submit' ):
        // Strip the custom markup on the paragraphs
        $content = str_replace("\n\n", "\n", $_POST['content']);
        
        file_put_contents('headline.html', $content);
        echo file_get_contents('headline.html');
        $response = ftp_it('headline.html');
    elseif ( $_POST['submit'] == 'Restore Backup' ):
        echo file_get_contents('headline-back.html');
    elseif ( $_POST['submit'] == 'Impact Hed' ):
        echo file_get_contents('impact-back.html');
    endif;
else:
    echo file_get_contents('headline.html');
endif; 
?>
</textarea>
            <input type="submit" value="Submit">
        </form>
<?php if ( isset($response) ) echo '<h3 class="alert">' . $response . '</h3>'; ?>
</body>
</html>
