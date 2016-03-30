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
  <label>Query <input type="search" name="query" subject="form-query"
   maxlength="50">
  <p><input type="submit" value="Send"> <input type="reset" value="Reset"></p>
  </label>
  </form>
  </div>
 </header>
  <div class=main>
  <div class=text>
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
// запрос
$subject=trim ( $_POST['subject'] );
$text=trim ($_POST['text'] );
if (!$subject)
    die ("Не все данные введены.<br>Пожалуйста, вернитесь назад и закончите ввод");
$query = addslashes ($subject);
if (!$text)
    die ("Не все данные введены.<br>Пожалуйста, вернитесь назад и закончите ввод");
$query = addslashes ($text);
$result = mysql_query ("INSERT INTO posts (subject,text) VALUES ('".$subject."', '".$text."')");
$result = mysql_query ( "SELECT * FROM posts WHERE text like '%".$text."%'" );
$i=1;
while($row = mysql_fetch_array($result))
{
   echo "<p><b>".($i++) . $row['title']."</b><br>";
   echo "subject: ".$row['subject']."<br>";
   echo "text: ".$row['text']."<br>";
}
if ( $i == 1 ) echo "Ничего не можем предложить. Извините";
mysql_close( );
?>
<label>
<a href=/index.php>
 <input type="submit" value="Accept">
</label>
</div>
</div>
</body>
</html>