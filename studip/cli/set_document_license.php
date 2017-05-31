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
 * -m flag for monochrome output, use this if you want to pipe
 */
require_once 'studip_cli_env.inc.php';
if (isset($_SERVER["argv"])) {
    // check for command line options
    $options = getopt("p:f:l:hm");
    if (isset($options["m"])) { 
        $red     = "";
        $green   = "";
        $blue    = "";
        $black   = "";
        $redbg   = "";
        $greenbg = "";
        $bluebg  = "";
        
    } else {
        $red      = "\033[1;31m";
        $green    = "\033[1;32m";
        $blue     = "\033[1;34m";
        $black    = "\033[0m";
        $redbg    = "\033[1;41m";
        $greenbg  = "\033[1;42m";
        $bluebg   = "\033[44m";
    }
    if (isset($options["h"])) {
        echo "\n";
        echo $blue."Set document license with predictions from deep doc class  \n".$black;
        echo $blue."___________________________________________________________\n".$black;
        echo "\n";
        echo $blue."usage:\n".$black;
        echo "\n";
        echo $blue."-f".$black." flag csv file with prediction and document id \n";
        echo $blue."-l".$black." flag license id default is 42\n";
        echo $blue."-p".$black." flag as prediction limit \n";
        echo $blue."-m".$black." flag for monochrome output, use this if you want to pipe\n";
        echo $blue."___________________________________________________________\n".$black;
        echo "\n";
        exit(1);
    }
    if (isset($options["f"])) {
        $opt_file = $options["f"];
    } else {
        exit(1);
    }
    if (isset($options["p"])) {
        $opt_prediction = $options["p"];
    } else {
        $opt_prediction = 50;
    }
    if (isset($options["l"])) {
        $opt_license = $options["l"];
    } else {
        // TODO set correct default
        $opt_license = 1;
    }
    //read file

    echo "\n";
    echo $blue."Set document license with predictions from deep doc class  \n".$black;
    echo $blue."_______________________________________________________________\n".$black;
    echo "\n";
    if (($handle = fopen($opt_file, "r")) !== FALSE) {
        echo $blue."reading file ".$file." ... ".$black;
        $documents = [];
        $csv = array_map('str_getcsv', file($opt_file));
        $document_id = array_search("document_id" , $csv[0]);
        $prediction = array_search("prediction" , $csv[0]);
        if (is_int($document_id) && is_int($prediction)) {
            foreach ($csv as $num => $row) {
                if ($num == 0) { continue; }
                array_push($documents, array("id"=>$row[$document_id], "prediction"=> $row[$prediction]));
            }
        echo $green."done!\n".$black;
        echo "\n";
        echo $blue."prediction has to be greater than ".$opt_prediction.$black."\n";
        } else {
            echo $red."fail!\n\n";
            if (!is_int($document_id)) echo "could not found document_id \n";
            if (!is_int($prediction)) echo "could not found prediction \n";
            echo $black."\n";
            exit(1);
        }
    }
    else {
        echo $red."\nError: file not found! \n";
        echo "please select a csv file with document ids and predictions \n";
        echo $black."\n";
        exit(1);
    }



    //write in db
    echo $blue."\nwrite in DB...\n\n".$black;
    $db = DBManager::get();
    echo $bluebg."          document_id              prediction   record updated ".$black."\n";
    $docs = 0;
    foreach ($documents as $document) {
        if ($opt_prediction <= $document["prediction"]) {
            $docs++;
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
            $stmt->bindParam(":license", $opt_license);
            $exec = $stmt->execute();
            if($exec) {
                echo $blue.$document["id"]."       ".$document["prediction"]."      ".$black;
                if ($stmt->rowCount() == 0) {
                    echo $redbg."       no       ".$black."\n";
                } else {
                    echo $greenbg."       yes      ".$black."\n";
                }
            } else {
                echo $red."Error can not update licence for document:". $document["id"] .$black."\n";
            }
        }
    }
    if ($docs == 0) {
        echo $redbg."         no document has a prediction greater than ".$opt_prediction."          ".$black."\n";
        echo $redbg."            no values were updated in the database             ".$black."\n";
    }
    echo "\n";
    echo $green."done!\n\n".$black;

}
?>
