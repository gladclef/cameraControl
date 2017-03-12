<?php

require_once(dirname(__FILE__) . "/resources/globals.php");
require_once(dirname(__FILE__) . "/derekdnd.php");

?><!DOCTYPE html>
<html>
	<head>
		<script type="text/javascript" src="<?php echo $global_path_to_jquery; ?>"></script>
		<script type="text/javascript" src="<?php echo $global_path_to_d3; ?>"></script>
		<script type="text/javascript" src="control.js"></script>
		<script>
			// holds the values pan, tilt, pan_range, and tilt_range
			var serverStats = JSON.parse('<?php printAsJSON(); ?>');
			$.each(serverStats, function(k,v) {
				serverStats[k] = parseInt(v);
			});
			var remotePan = serverStats["remote_pan"];
			var remoteTilt = serverStats["remote_tilt"];
		</script>
	</head>
	<body>
		<svg id="canvas_container"></svg>
	</body>
</html>