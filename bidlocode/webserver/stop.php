<html>
<head>
<meta refresh="5;http://10.60.46.7/index.php/">
</head>
<body>
<?php
shell_exec("/var/www/webserver/cgi/convstop.sh");
echo "процесс остановлен.";
?>
</body>
</html>
