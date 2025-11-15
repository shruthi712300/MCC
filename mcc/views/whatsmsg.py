# from flask import Flask, request, jsonify
# from pywhatsapp import WhatsApp
# import threading

# app = Flask(__name__)

# # Initialize WhatsApp instance
# whatsapp = WhatsApp()

# # A flag to check if the session is authenticated
# is_authenticated = False

# # Function to run the WhatsApp login in a separate thread (for QR code scanning)
# def login_whatsapp():
#     global is_authenticated
#     whatsapp.login()  # This opens the QR code for scanning
#     is_authenticated = True
#     print("WhatsApp login successful!")

# # API to send WhatsApp messages
# @app.route('/send-message', methods=['POST'])
# def send_message():
#     if not is_authenticated:
#         return jsonify({"error": "QR code not scanned or session expired."}), 403

#     # Get data from POST request
#     data = request.get_json()
#     phone_number = data.get('phone_number')
#     message = data.get('message')

#     if not phone_number or not message:
#         return jsonify({"error": "Phone number and message are required."}), 400

#     try:
#         # Send the message via WhatsApp
#         whatsapp.send_message(phone_number, message)
#         return jsonify({"success": True, "message": "Message sent successfully!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Function to start the Flask app and WhatsApp login
# def run_app():
#     global is_authenticated
#     # Start the login process for WhatsApp (in a separate thread to allow Flask to run concurrently)
#     threading.Thread(target=login_whatsapp, daemon=True).start()
    
#     # Start the Flask app
#     app.run(debug=True, use_reloader=False)

# if __name__ == '__main__':
#     run_app()
