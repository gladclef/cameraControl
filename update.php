<?php

require_once(dirname(__FILE__) . "/resources/common_functions.php");
require_once(dirname(__FILE__) . "/derekdnd.php");

if (sizeof($_GET) == 0)
{
	$url = curPageURL();
	echo "Pass in the arguments 'pan' and 'tilt'. Example: \"${url}?pan=0&tilt=0\"";
}

$pan = $_GET["pan"];
$tilt = $_GET["tilt"];
setPanAndTilt($pan, $tilt);
printAll();

?>