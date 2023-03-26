<?php
include_once 'db.php';

function getUserOrRedirect() {
    session_start();
    if (!isset($_SESSION['user_id'])) {
        header("Location: /login.php");
        exit();
    }
   return new User($_SESSION['user_id'], $_SESSION['username']);
}

function login($user) {
    session_start();
    $_SESSION['user_id'] = $user->getId();
    $_SESSION['username'] = $user->getUsername();
    header("Location: /index.php");
    exit();
}

function logout() {
    session_start();
    unset($_SESSION['user_id']);   
    unset($_SESSION['username']);
    header("Location: /login.php");
    exit();
}

function e($text) {
    return htmlspecialchars($text);
}