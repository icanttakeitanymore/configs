<html>
  <head>
    <title>"webserver"</title>
    <meta charset="utf-8">
    <META HTTP-EQUIV="refresh" CONTENT="20">
    <link rel="stylesheet" href="/stylesheet.css" type="text/css" >
  </head>
  <body>
 <header>
 <nav>
<ul id="topmenu">
  <li><a href="#main"><i class="icon icon-main"></i><br>Main</a></li>
</ul>
</nav>
<div class=query>
  <form action="/query.php" method="post">
  <label>Query <input type="search" name="query" id="form-query"
   maxlength="50">
  <p><input type="submit" value="Send"> <input type="reset" value="Reset"></p>
  </label>
  </form>
  </div>
 </header>

<div class=main>
<?php
// ------------------------------------------------------------ 

header('Content-Type: text/html; charset=UTF-8');

mb_internal_encoding('UTF-8'); 
mb_http_output('UTF-8'); 
mb_http_input('UTF-8'); 
mb_regex_encoding('UTF-8'); 

// ------------------------------------------------------------ 

$date = date("Ymd");
$uploaddir = ("/var/www/webserver/uploads/pers$date/");
$uploadfile1 = $uploaddir . basename($_FILES['userfile1']['name']);
$uploadfile2 = $uploaddir . basename($_FILES['userfile2']['name']);
$val3=trim ($_POST['password'] );
$val2=trim ($_FILES['userfile2']['name'] );
$val1=trim ($_FILES['userfile1']['name'] );
shell_exec("mkdir -m 777 /var/www/webserver/uploads/pers$date");

echo '<pre>';
if (move_uploaded_file($_FILES['userfile1']['tmp_name'], $uploadfile1)) {
    echo "Файл корректен и был успешно загружен.\n";
} else {
    echo "Возможная атака с помощью файловой загрузки!\n";
}

print "</pre>";

echo '<pre>';
if (move_uploaded_file($_FILES['userfile2']['tmp_name'], $uploadfile2)) {
    echo "Файл корректен и был успешно загружен.\n";
} else {
    echo "Возможная атака с помощью файловой загрузки!\n";
}

print "</pre>";
shell_exec("/var/www/webserver/cgi/conv.sh $val1 $val2 $val3");

?>

</div>
</div>
  </div>
  </body>
</html>
