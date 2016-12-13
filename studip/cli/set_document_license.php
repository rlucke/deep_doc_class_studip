#!/usr/bin/env php
<?php
/*
 * set_document_license.php - use deep_doc_class results to set document license
 *
 * Copyright (C) 2016 - Ron Lucke <rlucke@uos.de>
 * 
 * usage: 
 * -f flag csv file with prediction and document id
 * -p flag as prediction limit
 * output can be piped to a csv file
 */
require_once 'studip_cli_env.inc.php';
if (isset($_SERVER["argv"])) {
    // check for command line options
    $options = getopt("p:f:");
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
    //read file
    if (($handle = fopen($file, "r")) !== FALSE) {
        $documents = array();
        $header = null;
        while ($row = fgetcsv($handle)) {
            if ($header === null) {
                $header = $row;
                continue;
            }
            $documents[] = array_combine($header, $row);
        }
        fclose($handle);
    }
    
    //write in db
    
    $db = DBManager::get();
    echo '"document_id", "records affected"'." \n";
    foreach ($documents as $document) {
        if ($prediction <= $document["prediction"]) {
            //TODO set right license id
             $stmt = $db->prepare("
                UPDATE
                    dokumente
                SET 
                    protected = '42'
                WHERE
                    protected = '0'
                AND 
                    dokument_id = :id
                ");
            $stmt->bindParam(":id", $document['id']);
            $stmt->execute();
            echo '"'.$document["id"].'", "'.$stmt->rowCount().'"'." \n";
        }
    }

   
   
}
?>
