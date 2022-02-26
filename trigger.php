<?php

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'GET':
        $id= $_GET["id"];
        echo("Your Id:" . $id);
        shell_exec("python3 get.py $id");
        echo("Done \n");
        break;
    case 'POST':
        echo ("Hello Post");
        $command= "bash audio_encoding.sh";
        echo($command);
        shell_exec($command);

        echo("done");
        break;
    case 'PUT':
        echo ("Hello Put");
        $raw=file_get_contents('php://input');
        $params=json_decode($raw,true);
        $id=$_GET[id];
    default:
        $message = "Please pass a parameter";
        echo($message);
        break;
}



?>