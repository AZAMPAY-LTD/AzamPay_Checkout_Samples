<?php

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Scripting/EmptyPHP.php to edit this template
 */
$http_rs = file_get_contents("php://input");
$response = json_decode($http_rs);

if (is_array($response)) {

    if ($response->transactionstatus == "success") {
        // $response->msisdn
        // $response->amount
        // $response->message
        // $response->utilityref
        // $response->operator
        // $response->reference
        // $response->transactionstatus
        // $response->submerchantAcc
        //
        // All parameters which was passed on additionalProperties when sending a request will be available here
        // $response->additionalProperties->customerId
        // $response->additionalProperties->orderId
        // $response->additionalProperties->total
        // your code goes here to process if response is success
    }

    print_r($response);

    $file = fopen("./log_api.log", "a") or die("Unable to open file!");
    fwrite($file, Date("Y-m-d H:i:s") . ": " . json_encode($response) . "\n");
    fclose($file);
} else {
    $response = "Contact AzamPay Support Team for callback issue";
    $file = fopen("./log_api.log", "a") or die("Unable to open file!");
    fwrite($file, Date("Y-m-d H:i:s") . ": " . $response . "\n");
    fclose($file);
    echo $response;
}
?>