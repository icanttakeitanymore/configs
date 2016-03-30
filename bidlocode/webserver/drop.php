<html>
  <head>
    <title>"Тестирование php stderr.ru"</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="stylesheet.css" type="text/css" >
  </head>
  <body>
 <header>

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
require_once 'secret/passwords.php'; // подключаем скрипт
 
// подключаемся к серверу
$link = mysql_connect( $host, $user, $password);
if (!$link) {
    die('Ошибка соединения: ' . mysql_error());
}
if (!mysql_select_db($database)) {
    die('Ошибка выбора базы данных: ' . mysql_error());
}
$drop_post=trim ( $_POST['drop_post'] );
if (!$drop_post)
    die ("Не все данные введены.<br>Пожалуйста, вернитесь назад и закончите ввод");
$query = addslashes ($drop_post);
// $result = mysql_query ("select * from posts where id like '%".$drop_post."%'");
// if ($result = 0) {
//     die ("такого id нет");
$result = mysql_query ( "delete from posts WHERE id like '%".$drop_post."%'") or die('Запрос не удался: ' . mysql_error());
mysql_close( );
?>
<label>
<a href=/index.php>
<input <input type="submit" value="Accept">
</label>
</div>
</body>
</html>