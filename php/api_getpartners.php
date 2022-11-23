<?php

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Scripting/EmptyPHP.php to edit this template
 */

class azampay_checkout_api {

    public $token = "";
    public $app_name = "";
    // url to call to get the checkout page url generated
    public $url = "";
    // data which have all the information to be sent to azampay checkout page
    public $data = "";
    // Base URLs
    public $base_url = "";
    public $auth_url = "";
    // Endpoints
    public $partners_endpoint = 'api/v1/Partner/GetPaymentPartners';
    public $token_endpoint = 'AppRegistration/GenerateToken';

    public function __construct($data, $testMode) {
        if ($testMode == "yes" || $testMode == "on" || $testMode) {
            $this->base_url = 'https://sandbox.azampay.co.tz/';
            $this->auth_url = 'https://authenticator-sandbox.azampay.co.tz/';
        } else {
            $this->base_url = 'https://checkout.azampay.co.tz/';
            $this->auth_url = 'https://authenticator.azampay.co.tz/';
        }
        $this->data = $data;
    }

    public function get_partners() {
        $result = [
            'success' => false,
            'message' => '',
            'partners' => '',
        ];

        $this->token = $this->generate_token();
        if (is_null($this->token)) {
            $result["message"] = "Failed to get token";
        } else if (!$this->token["success"]) {
            $result["message"] = $this->token["message"];
        } else {

            $curl = curl_init();
            curl_setopt($curl, CURLOPT_URL, $this->base_url . $this->partners_endpoint);
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
            $headers = array(
                'Authorization: Bearer ' . $this->token["token"],
            );
            curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
            $rs = curl_exec($curl);

            $partners_response = json_decode($rs);

            if (is_null($partners_response)) {
                $result['message'] = 'Could not get payment partners.';
            } elseif (!is_array($partners_response) && property_exists($partners_response, 'status') && $partners_response->status === 'Error') {
                $result['message'] = property_exists($partners_response, 'message') ? 'Could not get payment partners. ' . $partners_response->message : 'Could not get payment partners.';
            } else {
                $result['success'] = true;
                $result['message'] = "Successful getting payment partners.";
                $result['partners'] = $partners_response;
            }
        }
        return $result;
    }

    private function generate_token() {

        $result = [
            'success' => false,
            'message' => '',
            'token' => '',
            'code' => '',
        ];

        $data_to_retrieve_token = array(
            'appName' => $this->data["app_name"],
            'clientId' => $this->data["client_id"],
            'clientSecret' => $this->data["client_secret"],
        );

        // Generate token for App
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $this->auth_url . $this->token_endpoint);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($data_to_retrieve_token));
        $headers = array(
            'Content-Type: application/json',
            'Accept: application/json',
            'X-API-KEY: ' . $this->data["client_token"],
        );
        curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
        $rs = curl_exec($curl);

        $data_rs = json_decode($rs);

        // Error generating token
        if ($rs == "" || !isset($data_rs) || !isset($data_rs->statusCode) || $data_rs->statusCode !== 200) {
            $result['code'] = '400';

            if ($rs == "") {
                $result['message'] = 'Something went wrong. Contact support team for more details.';
            } else if (!isset($data_rs->statusCode)) {
                if (isset($data_rs->errors->ClientSecret[0])) {
                    $result['message'] = $data_rs->errors->ClientSecret[0];
                } else if (isset($data_rs->errors->ClientId[0])) {
                    $result['message'] = $data_rs->errors->ClientId[0];
                } else if (isset($data_rs->errors->AppName[0])) {
                    $result['message'] = $data_rs->errors->AppName[0];
                } else {
                    $result['message'] = "Something went wrong. Contact support team for more details.";
                }
            } else if ($data_rs->statusCode === 423) {
                $result['message'] = 'Provided detail is not valid for this app or secret key has expired.';
            } elseif ($data_rs->statusCode === 500) {
                $result['message'] = 'Internal Server Error.';
            } else {
                $result['message'] = 'Something went wrong. Contact support team for more details.';
            }
        } else if (isset($data_rs->statusCode) && $data_rs->statusCode === 200) {
            // token was generated successfully
            $result['code'] = '200';

            $result['token'] = $data_rs->data->accessToken;

            $result['success'] = true;
        }

        return $result;
    }

}

$obj_data = null;
$obj_data["app_name"] = "DemoApp";
$obj_data["client_id"] = "7f2cd55d-47d3-43b4-90c4-9a98a49bb11a";
$obj_data["client_secret"] = "RfNxSk3mjV5T79GgQIVyPHFnDXWapi3TDKN7v5QOCCTIqnRhfXET6XPmUvTcRNKd1bYpjI9T3j+ydgDq2X/rGyDzojbvUDc6OhgWGrnfArw1+WtD3MyAYyvFI1mwb7xtUa3B6ntMlXL+FIvJziPPhwTdEeujQsHWeAQEKneHOZfZ2j9ROvQJGio+v5sQV5rSpRKOfdxFaOaZfzow/4G5n4eqh4S6WUfO3+Fj6fPKTfW8rU4iW8u4euffwi7XKYMVS68Vxf+94oG0KJ/jfzAe0DSxfbtVXIRlcu6Lnov0xHcL2qTI2dHLxqi3yvs8kevbWtW0zNFiZQnzIQSEFYKodM9HzeIk0KUuyXXV5eJ8EOPPuVVXDUZO3+0ovfjBUhZe3NtAGb9JOjZmpsC4ypfjPT4usa/DE1gYpc5gdX3RtzatpIfkG02Q1SMwFSZ3GAIUlcRxLtjNM7srLlZdni4Z+jFpLqG3z+dbiebCbNFgDculTMruE/YhRetOHG0c91tJrkGqJCYf34yDTHVdUGOFVCQsol+/vH3jZ60LDTnW8pIsLldD8a5lA+znIkJtB88LEpgYuHlO8q7vgjbsSC7KP7yDbuYQKcwu8w+RaRP0Nt4WWhAZzQsl0u2m1r9sRyfIUvteYf+R8ZlU3VZ5D8XP9kDNkSeIXunP3QdlqSjE4kM=";
$obj_data["client_token"] = "cbba010a-175b-4c57-b6dc-c5d636b5d20f";
// The above information will be provided from AzamPay Sandbox Platform for test and will be given after finalizing the eKYC process for Production

$obj = new azampay_checkout_api($obj_data, "yes");

$rs = $obj->get_partners();
// print_r(json_encode($rs));
?>