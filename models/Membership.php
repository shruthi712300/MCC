<?php
class Membership {
    private $conn;
    private $table_name = "memberships"; // Your table name

    public $id;
    public $full_name;
    public $mykad_no;
    public $home_address;
    public $office_address;
    public $phone_home;
    public $phone_office;
    public $hp_no;
    public $email;
    public $political_party;
    public $membership_type;
    public $years;
    public $amount_paid;
    public $proposer_name;
    public $proposer_mykad;
    public $seconder_name;
    public $seconder_mykad;
    public $application_date;
    public $submitted_at;
    public $status;
    public $branch_id;

    public function __construct($db) {
        $this->conn = $db;
    }

    public function create() {
        $query = "INSERT INTO " . $this->table_name . " 
                SET 
                    full_name=:full_name, 
                    mykad_no=:mykad_no, 
                    home_address=:home_address, 
                    office_address=:office_address, 
                    phone_home=:phone_home, 
                    phone_office=:phone_office,
                    hp_no=:hp_no, 
                    email=:email, 
                    political_party=:political_party, 
                    membership_type=:membership_type, 
                    years=:years, 
                    amount_paid=:amount_paid,
                    proposer_name=:proposer_name, 
                    proposer_mykad=:proposer_mykad,
                    seconder_name=:seconder_name, 
                    seconder_mykad=:seconder_mykad,
                    application_date=:application_date,
                    submitted_at=NOW(),
                    status='pending',
                    branch_id=:branch_id";

        $stmt = $this->conn->prepare($query);

        // Bind parameters
        $stmt->bindParam(":full_name", $this->full_name);
        $stmt->bindParam(":mykad_no", $this->mykad_no);
        $stmt->bindParam(":home_address", $this->home_address);
        $stmt->bindParam(":office_address", $this->office_address);
        $stmt->bindParam(":phone_home", $this->phone_home);
        $stmt->bindParam(":phone_office", $this->phone_office);
        $stmt->bindParam(":hp_no", $this->hp_no);
        $stmt->bindParam(":email", $this->email);
        $stmt->bindParam(":political_party", $this->political_party);
        $stmt->bindParam(":membership_type", $this->membership_type);
        $stmt->bindParam(":years", $this->years);
        $stmt->bindParam(":amount_paid", $this->amount_paid);
        $stmt->bindParam(":proposer_name", $this->proposer_name);
        $stmt->bindParam(":proposer_mykad", $this->proposer_mykad);
        $stmt->bindParam(":seconder_name", $this->seconder_name);
        $stmt->bindParam(":seconder_mykad", $this->seconder_mykad);
        $stmt->bindParam(":application_date", $this->application_date);
        $stmt->bindParam(":branch_id", $this->branch_id);

        if($stmt->execute()) {
            return true;
        }
        return false;
    }

    public function mykadExists() {
        $query = "SELECT id FROM " . $this->table_name . " WHERE mykad_no = ? LIMIT 0,1";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $this->mykad_no);
        $stmt->execute();
        
        if($stmt->rowCount() > 0) {
            return true;
        }
        return false;
    }
}
?>