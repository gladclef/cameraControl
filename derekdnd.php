<?php

require_once(dirname(__FILE__) . "/resources/db_query.php");

init();

function init()
{
	global $cameraName;
	global $maindb;

	$cameraName = "Derek DnD";

	create_row_if_not_existing(["database"=>"${maindb}", "table"=>"cameras", "name"=>"${cameraName}"]);
	$range = ["pan_range"=>200, "tilt_range"=>100];
	if (!db_query("UPDATE `${maindb}`.`cameras` SET " . array_to_update_clause($range) . "", $range))
	{
		echo "failed to set range on camera ${cameraName}";
	}
}

function getVals()
{
	global $cameraName;
	global $maindb;

	$where = ["name"=>"${cameraName}"];
	$retval = db_query("SELECT `pan`,`tilt`,`pan_range`,`tilt_range`,`remote_pan`,`remote_tilt` FROM `${maindb}`.`cameras` WHERE " . array_to_where_clause($where), $where);
	$retval = $retval[0];
	$retval["name"] = $cameraName;
	return $retval;
}

function printAll()
{
	$panTiltAndRange = getVals();
	foreach ($panTiltAndRange as $k=>$v)
	{
		echo "${k}:${v}<br/>";
	}
}

function printAsJSON()
{
	$panTiltAndRange = getVals();
	echo json_encode($panTiltAndRange);
}

function setPanAndTilt($pan, $tilt, $remote = FALSE)
{
	global $maindb;
	global $cameraName;

	// make sure the values don't exceed the limiting range values
	$panTiltAndRange = getVals();
	$pan = (int)$pan;
	$tilt = (int)$tilt;
	$pan_range = (int)$panTiltAndRange["pan_range"];
	$tilt_range = (int)$panTiltAndRange["tilt_range"];
	$pan = min(max($pan, -$pan_range), $pan_range);
	$tilt = min(max($tilt, -$tilt_range), $tilt_range);

	// get the variable names
	$originalUpdates = ["pan"=>$pan, "tilt"=>$tilt];
	$updates = array();
	foreach ($originalUpdates as $k=>$v)
	{
		if ($remote)
		{
			$k = "remote_${k}";
		}
		$updates[$k] = $v;
	}

	// update the variables
	$where = ["name"=>"${cameraName}"];
	$combined = array_merge($where, $updates);
	return db_query("UPDATE `${maindb}`.`cameras` SET " . array_to_update_clause($updates) . " WHERE " . array_to_where_clause($where), $combined);
}

?>