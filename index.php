<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// Replace with your actual Groq API key
$apiKey = "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";

// Get input text (either GET or POST)
$inputText = isset($_GET['text']) ? $_GET['text'] : ( $_POST['text'] ?? '' );

if (empty($inputText)) {
    echo json_encode(["error" => "No input text provided"]);
    exit;
}

// Prepare request to Groq API
$url = "https://api.groq.com/openai/v1/chat/completions";

$data = [
    "model" => "llama-3.1-8b-instant", // you can change to another Groq-supported model
    "messages" => [
        ["role" => "system", "content" => "You are a helpful AI assistant."],
        ["role" => "user", "content" => $inputText]
    ]
];

// cURL request
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json",
    "Authorization: Bearer " . $apiKey
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));

$response = curl_exec($ch);
if (curl_errno($ch)) {
    echo json_encode(["error" => curl_error($ch)]);
    curl_close($ch);
    exit;
}
curl_close($ch);

// Decode and return only the assistant's reply
$result = json_decode($response, true);

if (isset($result['choices'][0]['message']['content'])) {
    echo json_encode([
        "input" => $inputText,
        "reply" => $result['choices'][0]['message']['content']
    ]);
} else {
    echo $response; // Return full API response if something went wrong
}
