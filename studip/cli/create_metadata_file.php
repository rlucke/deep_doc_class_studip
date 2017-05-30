#!/usr/bin/env php
<?php
/*
 * create_metadata_file.php - Create metadata file for classification 
 *
 * Copyright (C) 2016 - Ron Lucke <rlucke@uos.de>
 * 
 * usage: 
 * -s flag is for semester selection, has to be the name from semester_data table
 * -f flag is for seminar selection with a csv file. Use a path to a csv file with seminar ids labeled as id
 * to create a metadata file just pipe the output of this script to a file of your choice
 *
 */
require_once 'studip_cli_env.inc.php';
if (isset($_SERVER["argv"])) {
    $db = DBManager::get();
    // check for command line options
    $options = getopt("s:f:h");
    if (isset($options["h"])) {
        echo "\n";
        echo "\033[1;34mCreate metadata file for deep doc class \033[0m \n";
        echo "\033[1;34m__________________________________________________________\033[0m \n";
        echo "\n";
        echo "\033[1;34musage: \033[0m \n";
        echo "\n";
        echo "\033[1;34m-s\033[0m flag is for semester selection, has to be the \n";
        echo "   name from semester_data table \n";
        echo "\n";
        echo "\033[1;34m-f\033[0m flag is for seminar selection with a csv file. \n";
        echo "   Use a path to a csv file with seminar ids labeled as id \n";
        echo "\n";
        echo "to create a metadata file just pipe the output of this  \n";
        echo "script to a file of your choice \n";
        echo "\033[1;34m__________________________________________________________ \033[0m \n";
        echo "\n";
        exit(1);
    }
    
    if (isset($options["s"])) {
        $semester_name = $options["s"];
    } else {
        $semester_name = "";
    }
    if (isset($options["f"])) {
        $file_path = $options["f"];
    } else {
        $file_path = "";
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
            echo "Error: \n";
            echo "semester not found! \n";
            echo "please select another semester \n";
            exit(1);
        }

        $beginn = $semester[0]["beginn"];
        $ende = $semester[0]["ende"];

        $sem_seminar ="
                    start_time >= $beginn
                    AND
                    start_time <= $ende
                ";
        
    } 

    if (!empty($file_path)) {
        if (($handle = fopen($file_path, "r")) !== FALSE) {
            $seminars = [];
            $csv = array_map('str_getcsv', file($file_path));
            $key = array_search("id" , $csv[0]);
            if ($key) {
                foreach ($csv as $num => $row) {
                    if ($num == 0) { continue; }
                    array_push($seminars, $row[$key]);
                }
                $file_seminar = "Seminar_id IN ("."'".implode("','", $seminars)."'".")";
            } else {
                echo "Error: \n";
                echo "row 'id' not found! \n";
                echo "please select a csv file with seminar ids labeled as 'id' \n";
                exit(1);
            }
        }
        else {
            echo "Error: \n";
            echo "file not found! \n";
            echo "please select a csv file with seminar ids labeled as 'id' \n";
            echo "\n";
            exit(1);
        }

    }

    $select_seminar = "SELECT Seminar_id FROM seminare";

    if (!empty($file_seminar) && !empty($sem_seminar)) {
            $select_seminar .= " WHERE ".$file_seminar . " OR " . $sem_seminar;
    }

    if (empty($file_seminar) && !empty($sem_seminar)) {
            $select_seminar .= " WHERE ".$sem_seminar;
    }

    if (!empty($file_seminar) && empty($sem_seminar)) {
            $select_seminar .= " WHERE ".$file_seminar;
    }

    $stmt = $db->prepare("
            SELECT
                dokumente.dokument_id as document_id , dokumente.filename as filename, folder.name as folder_name, folder.description as folder_description, dokumente.description as description, dokumente.seminar_id
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

    $csv = '"document_id", "filename", "folder_name", "folder_description", "description", "id"'." \n";
    foreach($dokumente as $dokument) {
        $csv .= '"'.join('","', $dokument).'"'." \n";
    }
    fwrite(STDOUT, $csv);
}
?>
