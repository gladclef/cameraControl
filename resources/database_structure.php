<?php
$a_basic_tables_structure = array(
	"cameras" => array(
		"id" =>                    array("type" => "INT",          "indexed" => TRUE,  "isPrimaryKey" => TRUE,  "special" => "AUTO_INCREMENT"),
		"name" =>                  array("type" => "VARCHAR(255)", "indexed" => TRUE,  "isPrimaryKey" => FALSE, "special" => ""),
		"pan" =>                   array("type" => "INT",          "indexed" => FALSE, "isPrimaryKey" => FALSE, "special" => ""),
		"tilt" =>                  array("type" => "INT",          "indexed" => FALSE, "isPrimaryKey" => FALSE, "special" => ""),
		"pan_range" =>             array("type" => "INT",          "indexed" => FALSE, "isPrimaryKey" => FALSE, "special" => ""),
		"tilt_range" =>            array("type" => "INT",          "indexed" => FALSE, "isPrimaryKey" => FALSE, "special" => ""),
		"remote_pan" =>            array("type" => "INT",          "indexed" => FALSE, "isPrimaryKey" => FALSE, "special" => ""),
		"remote_tilt" =>           array("type" => "INT",          "indexed" => FALSE, "isPrimaryKey" => FALSE, "special" => "")
	)
);
$a_database_insert_values = array();
?>