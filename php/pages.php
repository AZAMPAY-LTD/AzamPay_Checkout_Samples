<?php

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Scripting/EmptyPHP.php to edit this template
 */

class azampay_checkout_pages {

    // url to call to get the checkout page url generated
    public $url = "";
    // data which have all the information to be sent to azampay checkout page
    public $data = "";

    public function __construct($data, $testMode) {
        if ($testMode == "yes" || $testMode) {
            $this->url = 'https://sandbox.azampay.co.tz/api/v1/Partner/PostCheckout';
        } else {
            $this->url = 'https://checkout.azampay.co.tz/api/v1/Partner/PostCheckout';
        }
        $this->data = $data;
    }

    public function call_gw() {
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $this->url);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($this->data));
        $headers = array(
            'Content-Type: application/json-patch+json',
        );
        curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
        $result = curl_exec($curl);

        // echo $result;

        header('Location: ' . $result);
    }

}

$postfields = array();
// ClientID after registering your application on azampay checkout platform
$postfields['clientId'] = "7f2cd55d-47d3-43b4-90c4-9a98a49bb11a";
// Name of the application as registered on the azampay checkout platform
$postfields['appName'] = "DemoApp";
// Name of the application will be displayed on the checkout page, if empty then appName will be displayed
$postfields['vendorName'] = "DemoApp";
// Amount to be charged
$postfields['amount'] = "100";
// Currency which was registered while registering the application
$postfields['currency'] = "TZS";
// language
$postfields['language'] = "English";
// The ID which is the primary key for the transaction
$postfields['externalId'] = "123";
// The url from client if the transaction is successful charged
$postfields['redirectSuccessURL'] = "http://192.168.116.79/php/checkout/pages_callback.php";
// The url from client if the transaction is failed to be charged
$postfields['redirectFailURL'] = "http://192.168.116.79/php/checkout/pages_callback.php";
// The items which you want to process payment for
$postfields['cart']['items'][0]['name'] = "Invoide 2";
// if "yes" or true then its test environment, if "no" then its production environment
$testMode = "yes";

$acp = new azampay_checkout_pages($postfields, $testMode);

$acp->call_gw();
?>