<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight request
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Get the raw POST data
$input = file_get_contents('php://input');
$data = json_decode($input, true);

// Validate required fields
$required_fields = [
    'full_name', 'mykad_no', 'home_address', 'hp_no', 
    'membership_type', 'proposer_name', 'proposer_mykad',
    'seconder_name', 'seconder_mykad', 'application_date'
];

foreach ($required_fields as $field) {
    if (empty($data[$field])) {
        echo json_encode([
            'success' => false,
            'message' => "Missing required field: $field"
        ]);
        exit;
    }
}

// Include database configuration
include_once 'database.php';

try {
    $database = new Database();
    $conn = $database->getConnection();

    // Prepare SQL statement - updated to match your database structure
    $sql = "INSERT INTO membership_applications (
        full_name, mykad_no, home_address, office_address, 
        phone_home, phone_office, hp_no, email, political_party,
        membership_type, years, amount_paid, proposer_name, 
        proposer_mykad, seconder_name, seconder_mykad, application_date,
        submitted_at, status
    ) VALUES (
        :full_name, :mykad_no, :home_address, :office_address,
        :phone_home, :phone_office, :hp_no, :email, :political_party,
        :membership_type, :years, :amount_paid, :proposer_name,
        :proposer_mykad, :seconder_name, :seconder_mykad, :application_date,
        NOW(), 'pending'
    )";

    $stmt = $conn->prepare($sql);
    
    // Bind parameters
    $stmt->bindParam(':full_name', $data['full_name']);
    $stmt->bindParam(':mykad_no', $data['mykad_no']);
    $stmt->bindParam(':home_address', $data['home_address']);
    $stmt->bindParam(':office_address', $data['office_address']);
    $stmt->bindParam(':phone_home', $data['phone_home']);
    $stmt->bindParam(':phone_office', $data['phone_office']);
    $stmt->bindParam(':hp_no', $data['hp_no']);
    $stmt->bindParam(':email', $data['email']);
    $stmt->bindParam(':political_party', $data['political_party']);
    $stmt->bindParam(':membership_type', $data['membership_type']);
    $stmt->bindParam(':years', $data['years']);
    $stmt->bindParam(':amount_paid', $data['amount_paid']);
    $stmt->bindParam(':proposer_name', $data['proposer_name']);
    $stmt->bindParam(':proposer_mykad', $data['proposer_mykad']);
    $stmt->bindParam(':seconder_name', $data['seconder_name']);
    $stmt->bindParam(':seconder_mykad', $data['seconder_mykad']);
    $stmt->bindParam(':application_date', $data['application_date']);

    // Execute the statement
    if ($stmt->execute()) {
        echo json_encode([
            'success' => true,
            'message' => 'Membership application submitted successfully!'
        ]);
    } else {
        echo json_encode([
            'success' => false,
            'message' => 'Failed to submit application'
        ]);
    }

} catch(PDOException $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}

$conn = null;
?>