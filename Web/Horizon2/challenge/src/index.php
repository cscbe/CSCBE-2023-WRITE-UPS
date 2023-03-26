<?php
include_once './db.php';
include_once './utils.php';
$user = getUserOrRedirect(); 

include_once './template-start.php';

?>
<h1>Find photos</h1>
<form action="/index.php" method="GET">
    <label class="form-label" for="title">Title</label>
    <input class="form-control" id="title" name="title" type="text" />
    <input class="btn btn-primary" type="submit" value="Search"/>
</form>

<a href="/add_photo.php">Add photo</a>

<h1>Photos</h1>
<?php
$db = new Database();

$title = isset($_GET['title'])? $_GET['title'] : '';
$photos = $db->searchPhotos($title , $user);
if (empty($photos)) {
    echo "<p>No photos found!</p>";
} else {
    echo '<div class="list-group">';
    foreach ($photos as $photo) {
        echo '<a class="list-group-item list-group-item-action" href="/photo.php?id=' . e($photo->getId()) . '">';
        echo e($photo->getTitle()) . ' (' .  e($photo->getUser()->getUsername()) . ')';
        echo '</a>';
    }
    echo '</div>';
}


include_once './template-end.php';

?>