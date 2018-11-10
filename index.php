<?php

require_once(dirname(__FILE__) . "/derekdnd.php");

if(isset($_GET["printAsJSON"]))
{
	printAsJSON();
}
else
{
	printAll();
	
	print("<br />");
	print("Also see <tt>update.php</tt>, or <tt>index.php?printAsJSON</tt>");
}

?>