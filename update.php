<?php

require_once(dirname(__FILE__) . "/resources/common_functions.php");
require_once(dirname(__FILE__) . "/derekdnd.php");

if (sizeof($_GET) == 0)
{
	$url = curPageURL();
	$newUrl = "${url}?pan=0&tilt=0";
	echo "Pass in the arguments 'pan' and 'tilt'.<br />";
	echo "Include the getvar \"remote\" to update the remote pan and tilt values, instead.<br />";
	echo "Example: <a href=\"${newUrl}\">${newUrl}</a><br /><br />";
}

$pan = $_GET["pan"];
$tilt = $_GET["tilt"];
setPanAndTilt($pan, $tilt, isset($_GET["remote"]));
printAll();

?>