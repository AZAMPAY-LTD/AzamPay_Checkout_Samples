<?php

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Scripting/EmptyPHP.php to edit this template
 */

$http_rs = file_get_contents("php://input");
$response = json_decode($http_rs);

print_r($response);
echo "[" . $http_rs . "]<br/><br/>";

if (is_array($response)) {
    if ($response->transactionstatus == "success") {
        // $response->transid
        // $response->amount
        // $response->utilityref
        // your code goes here to process if response is success
    }

    print_r($response);

    $file = fopen("./log_pages.log", "a") or die("Unable to open file!");
    fwrite($file, Date("Y-m-d H:i:s") . ": " . json_encode($response) . "\n");
    fclose($file);
} else {
    $response = "Contact AzamPay Support Team for callback issue";
    $file = fopen("./log_pages.log", "a") or die("Unable to open file!");
    fwrite($file, Date("Y-m-d H:i:s") . ": " . $response . "\n");
    fclose($file);
    echo $response;
}
?>