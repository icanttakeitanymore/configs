<html>
  <head>
    <title>"Тестирование php webserver"</title>
    <meta charset="utf-8">
    <META HTTP-EQUIV="refresh" CONTENT="20">
    <link rel="stylesheet" href="/stylesheet.css" type="text/css" >
  </head>
  <body>
 <header>
 <nav>
<ul id="topmenu">
  <li><a href="/index.php"><i class="icon icon-main"></i><br>Персо</a></li>
  <li><a href="/soc.php"><i class="icon icon-main"></i><br>Соцзащита</a></li>

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
<div class=post>
    <form action="calc.php" method="post" enctype="multipart/form-data">
Прикрепление файлов для сверки, первый файл список персо, в котором должно быть три столбца,<br>
второй список файл с соглашениями.<br>
<input name="userfile1" type="file"><br>
<input name="userfile2" type="file"><br>
       <label>Пароль к базе данных<input type="password" name="password" value="########">
     <p><input type="submit" href=index.php></p>
</form>
<?php
$pid = shell_exec('cat /var/www/webserver/uploads/pid');
echo "Процесс запущен с pid : $pid";
?>
<br>
<form action=/stop.php method="post">
<input type="submit" value="Завершить принудительно">
</form>
<?php
$output = shell_exec('tree ./uploads/');
echo "<pre>$output</pre>";
$date = date("Ynd");
?>
<div class=tables>

</div>
</div>
  </div>
  </body>
</html>
