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
	return db_query("SELECT `pan`,`tilt`,`pan_range`,`tilt_range` FROM `${maindb}`.`cameras` WHERE " . array_to_where_clause($where), $where);
}

function printAll()
{
	$panTiltAndRange = getVals()[0];
	foreach ($panTiltAndRange as $k=>$v)
	{
		echo "${k}:${v}<br/>";
	}
}

function setPanAndTilt($pan, $tilt)
{
	global $maindb;
	global $cameraName;

	$updates = ["pan"=>$pan, "tilt"=>$tilt];
	$where = ["name"=>"${cameraName}"];
	$combined = array_merge($where, $updates);
	return db_query("UPDATE `${maindb}`.`cameras` SET " . array_to_update_clause($updates) . " WHERE " . array_to_where_clause($where), $combined, TRUE);
}

?>