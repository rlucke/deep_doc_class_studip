#!/usr/bin/env php
<?php
/*
 * create_metadata_file.php - Create metadata file for classification 
 *
 * Copyright (C) 2016 - Ron Lucke <rlucke@uos.de>
 *
 */
require_once 'studip_cli_env.inc.php';

if (isset($_SERVER["argv"])) {

    // check for command line options
    $options = getopt("s:");

    if (isset($options["s"])) {
        $semester_name = $options["s"];
    } else {
        $semester_name = "";
    }

    $db = DBManager::get();
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

        
        $beginn = $semester[0]["beginn"];
        $ende = $semester[0]["ende"];
        
        echo "collecting seminars...";
        $stmt = $db->prepare("
                SELECT
                    Seminar_id
                FROM 
                    seminare
                WHERE
                    start_time >= :beginn
                    AND
                    start_time <= :ende
                ");
        $stmt->bindParam(":beginn", $beginn);
        $stmt->bindParam(":ende", $ende);
        $stmt->execute();
        $seminare = $stmt->fetchAll(PDO::FETCH_ASSOC);
    } else {
        echo "collecting seminars...";
        $stmt = $db->prepare("
                SELECT
                    Seminar_id
                FROM 
                    seminare
                ");
        $stmt->execute();
        $seminare = $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    if(empty($seminare)) {
        echo " no seminars found. \n";
        exit(1);
    } else {
        echo " done. \n";
    }

    $seminar_ids = array();
    foreach ($seminare as $seminar) {
        array_push($seminar_ids, $seminar["Seminar_id"]);
    }

    echo "collecting documents... ";
    $seminar_ids_string = "('".join("','", $seminar_ids)."')";
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
                $seminar_ids_string
            AND
                dokumente.range_id = folder.folder_id
            ");
    $stmt->execute();
    $dokumente = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo " done. \n";
    echo "writing csv file...";
    $fp = fopen('meta.csv', 'w');
    fputs($fp, "document_id; filename; folder_name; folder_description; description \n");
    foreach($dokumente as $dokument) {
        fputs($fp, join(";", $dokument)."\n");
    }
    fclose($fp); 
    echo " done. \n";
}
?>
