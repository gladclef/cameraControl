<?php

require_once(dirname(__FILE__) . "/resources/globals.php");
require_once(dirname(__FILE__) . "/derekdnd.php");

?><!DOCTYPE html>
<html>
	<head>
		<script type="text/javascript" src="<?php echo $global_path_to_jquery; ?>"></script>
		<script type="text/javascript" src="<?php echo $global_path_to_d3; ?>"></script>
		<script type="text/javascript" src="control.js"></script>
		<script type="text/javascript" src="toExec.js"></script>
		<script type="text/javascript" src="communication/longPoll/pushPull.js"></script>
		<script>
			if (window.a_toExec === undefined) window.a_toExec = [];

			a_toExec[a_toExec.length] = {
				"name": "control.php",
				"dependencies": ["jQuery"],
				"function": function() {
					// holds the values pan, tilt, pan_range, and tilt_range
					window.serverStats = JSON.parse('<?php printAsJSON(); ?>');
					$.each(serverStats, function(k,v) {
						serverStats[k] = parseInt(v);
					});
				}
			};
		</script>
	</head>
	<body>
		<svg id="canvas_container"></svg>
	</body>
</html>