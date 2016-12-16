#!/usr/bin/env php
<?php
/*
 * create_metadata_file.php - Create metadata file for classification 
 *
 * Copyright (C) 2016 - Ron Lucke <rlucke@uos.de>
 * 
 * usage: 
 * -s flag is for semester selection, has to be the name from semester_data table
 * to create a metadata file just pipe the output of this script to a file of your choice
 *
 */
require_once 'studip_cli_env.inc.php';
if (isset($_SERVER["argv"])) {
    $db = DBManager::get();
    // check for command line options
    $options = getopt("s:");
    if (isset($options["s"])) {
        $semester_name = $options["s"];
    } else {
        $semester_name = "";
    }

    if (!empty($semester_name)) {
        $stmt = $db->prepare("
                SELECT
                    *
                FROM 
                    semester_data
                WHERE
                    name = :name
                ");
        $stmt->bindParam(":name", $semester_name);
        $stmt->execute();
        $semester = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if(empty($semester)) {
            echo "semester not found";
            exit(1);
        }

        $beginn = $semester[0]["beginn"];
        $ende = $semester[0]["ende"];

        $select_seminar ="
                SELECT
                    Seminar_id
                FROM 
                    seminare
                WHERE
                    start_time >= $beginn
                    AND
                    start_time <= $ende
                ";
        
    } else {
        $select_seminar ="
                SELECT
                    Seminar_id
                FROM 
                    seminare
                ";
       
    }

    $stmt = $db->prepare("
            SELECT
                dokumente.dokument_id as document_id , dokumente.filename as filename, folder.name as folder_name, folder.description as folder_description, dokumente.description as description
            FROM 
                dokumente
            JOIN
                folder
            WHERE
                dokumente.seminar_id
                IN
                ($select_seminar)
            AND
                dokumente.range_id = folder.folder_id
            ");
    $stmt->execute();
    $dokumente = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $csv = '"document_id", "filename", "folder_name", "folder_description", "description"'." \n";
    foreach($dokumente as $dokument) {
        $csv .= '"'.join('","', $dokument).'"'." \n";
    }
    fwrite(STDOUT, $csv);
}
?>
