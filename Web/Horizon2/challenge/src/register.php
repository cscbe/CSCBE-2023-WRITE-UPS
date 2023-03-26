<?php
include_once './db.php';
include_once './utils.php';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $db = new Database();

    $user = $db->register($username, $password);
    login($user);
} else {
    include_once './template-start.php';
?>

<h1>Create account</h1>
<form action="/register.php" method="POST">
    <label class="form-label" for="username">Username</label>
    <input class="form-control" id="username" name="username" type="text" />
    <label class="form-label" for="password">Password</label>
    <input class="form-control" id="password" name="password" type="text" />
    <input class="btn btn-primary" type="submit" value="Register" />
</form>

<a href="/login.php">Login instead</a>
<?php
include_once './template-end.php';
}
?>
