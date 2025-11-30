<?php
class Database {
    private $host = "localhost";
    private $db_name = "your_database_name"; // Replace with your actual database name
    private $username = "your_username";     // Replace with your MySQL username
    private $password = "your_password";     // Replace with your MySQL password
    public $conn;

    public function getConnection() {
        $this->conn = null;
        try {
            $this->conn = new PDO("mysql:host=" . $this->host . ";dbname=" . $this->db_name, $this->username, $this->password);
            $this->conn->exec("set names utf8");
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch(PDOException $exception) {
            error_log("Connection error: " . $exception->getMessage());
            throw $exception; // Re-throw to see the actual error
        }
        return $this->conn;
    }
}
?>