<?php
include_once './db.php';
include_once './utils.php';
$user = getUserOrRedirect();

$db = new Database();

$photo = $db->getPhoto($_GET['id'], $user);
include_once './template-start.php';
?>
<div class="card">
    <img class="card-img-top" src="<?= e($photo->getUrl()) ?>"/>
    <div class="card-body">
        <div class="card-title">
            <?= e($photo->getTitle()) ?>
        </div>
    </div>
</div>

<?php
include_once './template-end.php';
?>
