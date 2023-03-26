<?php
include_once './db.php';
include_once './utils.php';

$user = getUserOrRedirect();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $db = new Database();
    $photo = $db->addPhoto($_POST['title'], $_POST['url'], isset($_POST['visible']) ? 1 : 0, $user);

    header("Location: /photo.php?id=" . urlencode($photo->getId()));
    exit();
} else {

include_once './template-start.php';
?>
<h1>Add photo</h1>
<form action="/add_photo.php" method="POST">
    <label class="form-label" for="title">Title</label>
    <input class="form-control" id="title" name="title" type="text" />
    <label class="form-label" for="url">Url</label>
    <input class="form-control" id="url" name="url" type="text" />
    <div class="form-check form-switch">
        <input class="form-check-input" type="checkbox" name="hidden" id="hidden">
        <label class="form-check-label" for="hidden">Hidden</label>
    </div>
    <input class="btn btn-primary" type="submit" name="Add" />
</form>

<?php
include_once './template-end.php';
}
?>

