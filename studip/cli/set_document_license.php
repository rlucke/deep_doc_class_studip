#!/usr/bin/env php
<?php
/*
 * set_document_license.php - use deep_doc_class results to set document license
 *
 * Copyright (C) 2016 - Ron Lucke <rlucke@uos.de>
 * 
 * usage: 
 *
 */
require_once 'studip_cli_env.inc.php';
if (isset($_SERVER["argv"])) {
    // check for command line options
    $options = getopt("p:");
    if (isset($options["p"])) {
        $percentage = $options["p"];
    } else {
        $percentage = 50;
    }
    $db = DBManager::get();
   
}
?>
