<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    include_once './utils.php';
    logout();
} else {
include_once './template-start.php';
?>
<form action="/logout.php" method="POST">
    <input class="btn btn-primary" type="submit" value="Logout" />
</form>
<?php
include_once './template-end.php';
}
?>