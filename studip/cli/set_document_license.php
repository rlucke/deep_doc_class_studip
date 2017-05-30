#!/usr/bin/env php
<?php
/*
 * set_document_license.php - use deep_doc_class results to set document license
 *
 * Copyright (C) 2016 - Ron Lucke <rlucke@uos.de>
 * 
 * usage: 
 * -f flag csv file with prediction and document id
 * -l flag license id default is 42
 * -p flag as prediction limit
 */
require_once 'studip_cli_env.inc.php';
if (isset($_SERVER["argv"])) {
    // check for command line options
    $options = getopt("p:f:l:h");
    if (isset($options["h"])) {
        echo "\n";
        echo "\033[1;34mSet document license with predictions from deep doc class \033[0m \n";
        echo "\033[1;34m__________________________________________________________ \033[0m \n";
        echo "\n";
        echo "\033[1;34m usage: \033[0m \n";
        echo "\n";
        echo "\033[1;34m -f\033[0m flag csv file with prediction and document id \n";
        echo "\033[1;34m -l\033[0m flag license id default is 42\n";
        echo "\033[1;34m -p\033[0m flag as prediction limit \n";
        echo "\033[1;34m__________________________________________________________ \033[0m \n";
        echo "\n";
        exit(1);
    }
    if (isset($options["f"])) {
        $file = $options["f"];
    } else {
        exit(1);
    }
    if (isset($options["p"])) {
        $prediction = $options["p"];
    } else {
        $prediction = 50;
    }
    if (isset($options["l"])) {
        $license = $options["l"];
    } else {
        // TODO set correct default
        $license = 42;
    }
    //read file

    if (!empty($file)) {
        echo "\n";
        echo "\033[1;34mSet document license with predictions from deep doc class \033[0m \n";
        echo "\033[1;34m__________________________________________________________ \033[0m \n";
        echo "\n";
        if (($handle = fopen($file, "r")) !== FALSE) {
            echo "\033[1;34mreading file... \033[0m";
            $documents = [];
            $csv = array_map('str_getcsv', file($file));
            $document_id = array_search("document_id" , $csv[0]);
            $prediction = array_search("prediction" , $csv[0]);
            if (is_int($document_id) && is_int($prediction)) {
                foreach ($csv as $num => $row) {
                    if ($num == 0) { continue; }
                    array_push($documents, array("id"=>$row[$document_id], "prediction"=> $row[$prediction]));
                }
            echo "\033[1;32mdone! \033[0m \n";
            } else {
                echo "\033[1;31mfail!\n\n";
                if (!is_int($document_id)) echo "could not found document_id \n";
                if (!is_int($prediction)) echo "could not found prediction \n";
                echo "\033[0m \n";
                exit(1);
            }
        }
        else {
            echo "\033[1;31m\nError: file not found! \n";
            echo "please select a csv file with document ids and predictions \n";
            echo "\033[0m \n";
            exit(1);
        }

    }
    
    //write in db
    echo "\033[1;34m\nwrite in DB... \033[0m \n \n";
    $db = DBManager::get();
    echo "\033[44m          document_id             record updated \033[0m\n";
    foreach ($documents as $document) {
        if ($prediction <= $document["prediction"]) {
             $stmt = $db->prepare("
                UPDATE
                    dokumente
                SET 
                    protected = :license
                WHERE
                    protected = '0'
                AND 
                    dokument_id = :id
                ");
            $stmt->bindParam(":id", $document['id']);
            $stmt->bindParam(":license", $license);
            $exec = $stmt->execute();
            if($exec) {
                echo "\033[1;34m".$document["id"]." \033[0m";
                if ($stmt->rowCount() == 0) {
                    echo "\033[1;41m       no       \033[0m\n";
                } else {
                    echo "\033[1;42m       yes      \033[0m\n";
                }
            } else {
                echo "\033[1;31m Error can not update licence for document:". $document["id"] ."\033[0m \n";
            }
        }
    }
    echo "\n";
    echo "\033[1;32mdone! \033[0m \n \n";

   
   
}
?>
