<?php

class User {
    private string $username;
    private int $id;

    function __construct(int $id, string $username) {
        $this->id = $id;
        $this->username = $username;
      }

    function getId(): int {
        return $this->id;
    }

    function getUsername(): string {
        return $this->username;
    }
}


class Photo {
    private int $id;
    private string $title;
    private string $url;
    private $visible;
    private User $user;

    function __construct(int $id, string $title, string $url, bool $visible, User $user) {
        $this->id = $id;
        $this->title = $title;
        $this->url = $url;
        $this->visible = $visible;
        $this->user = $user;
    }

    function getTitle(): string {
        return $this->title;
    }

    function getId(): int {
        return $this->id;
    }

    function getUrl(): string {
        return $this->url;
    }

    function getUser(): User {
        return $this->user;
    }

    function isVisible() {
        return $this->visible;
    }
}

class Database {
   private $conn;

    function __construct() {
        $this->conn = new mysqli(
            $_ENV['MYSQL_HOST'], 
            $_ENV['MYSQL_USER'], 
            $_ENV['MYSQL_PASSWORD'], 
            $_ENV['MYSQL_DATABASE'], 
        );
    }

    function register($username, $password) {
        $password = password_hash($password,  PASSWORD_BCRYPT);

        $result = $this->conn->query(
            sprintf(
                "INSERT INTO users (username, password) VALUES ('%s', '%s')",
                $this->conn->real_escape_string($username),
                $this->conn->real_escape_string($password)
            )
        );

        if (!$result) {
            die(mysqli_error($this->conn));
        }

        return new User($this->conn->insert_id, $username);
    }

    function login($username, $password) {
        $result = $this->conn->query(
            sprintf(
                "SELECT id, password FROM users WHERE username = '%s'",
                $this->conn->real_escape_string($username),
            )
        );

        if (!$result) {
            die(mysqli_error($this->conn));
        }

        if ($result->num_rows == 0) {
            die('User not found');
        }

        $user = $result->fetch_object();

        if (!password_verify($password, $user->password)) {
            die('Invalid password');
        }

        return new User($user->id, $username);
    }

    function addPhoto($title, $url, $visible, $user) {
        $lowerUrl = strtolower($url);
        if(!(str_starts_with($lowerUrl, "http://") || str_starts_with($lowerUrl, "https://"))) {
            die('Invalid url');
        }
        
        $result = $this->conn->query(
            sprintf(
                "INSERT INTO photos (title, url, visible, user_id) VALUES " .
                "('%s', '%s', '%s', %s)",
                $this->conn->real_escape_string($title),
                $this->conn->real_escape_string($url),
                $this->conn->real_escape_string($visible),
                $this->conn->real_escape_string($user->getId())
            )
        );

        if (!$result) {
            die(mysqli_error($this->conn));
        }

        return new Photo($this->conn->insert_id, $title, $url, $visible, $user);
    }

    function getPhoto($id, $user) {
        $result = $this->conn->query(
            sprintf(
                "SELECT photos.id, title, url, visible, user_id, username FROM photos " .
                "INNER JOIN users ON users.id = photos.user_id " . 
                "WHERE (user_id = %s OR visible = 1) AND photos.id = %s LIMIT 1",
                $this->conn->real_escape_string($user->getId()),
                $this->conn->real_escape_string($id)
            )
        );


        if (!$result) {
            die(mysqli_error($this->conn));
        }

        if ($result->num_rows == 0) {
            die('Photo not found');
        }

        $photo = $result->fetch_object();

        return new Photo(
            $photo->id, 
            $photo->title, 
            $photo->url, 
            $photo->visible,
            new User($photo->user_id, $photo->username)
    );
    }

    /**
     * @return Photo[]
     */
    function searchPhotos($title, $user) {
        $query = sprintf(
            "SELECT photos.id, title, url, visible, user_id, username FROM photos " . 
            "INNER JOIN users ON users.id = photos.user_id " . 
            "WHERE LOWER(title) LIKE LOWER('%%%s%%') AND (user_id = %s OR visible = 1) LIMIT 10",
            $this->conn->real_escape_string($title),
            $this->conn->real_escape_string($user->getId())
        );

        $result = $this->conn->query($query);

        if (!$result) {
            die(mysqli_error($this->conn));
        }

        $photos = [];
        while($photo = $result->fetch_object()) {
            $user = new User($photo->user_id, $photo->username);
            $photos[] = new Photo(
                $photo->id, 
                $photo->title, 
                $photo->url, 
                $photo->visible,
                $user
            );
        }

        return $photos;
    }

    function __destruct() {
        $this->conn->close();
    }    
}
