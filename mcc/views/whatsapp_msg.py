import requests
import base64

url = 'http://localhost:3000/send-message'  



#file_path = "C:/Users\KARTHIK/Downloads/36  Mahadhana Street  Opp VRS Thirumana Mahal Mayiladuthurai  609001 (2).pdf"

# with open(file_path, "rb") as file:
    # encoded_file = base64.b64encode(file.read()).decode('utf-8')

def send_whatsapp_msg(onsite_data):

    creation_date = onsite_data['creation_date']
    cname = onsite_data['cname']
    cphoneno = onsite_data['cphoneno']
    urgency = onsite_data['urgency']
    service_type = onsite_data['service_type']
    problem = onsite_data['problem']
    status = onsite_data['status']
    engineer_assign = onsite_data['engineer_assign']
    on_service_date = onsite_data['on_service_date']
    service_charge = onsite_data['service_charge']
    received_charge = onsite_data['received_charge']
    phonenos = ['919487529436','919443229436','919385357001']
    receiver_data = {
        '919487529436': 'Bhuvaneswari',
        '919385357001': 'Karthik',
        '919443229436': 'Balamurugan'
    }
    for phone in phonenos:
        if status == 'Open':
            message = f"*Hello {receiver_data[phone]},*\n\n New service has been added on {creation_date}. \n\n Customer Name: {cname} \n Customer Phoneno: {cphoneno}.\n Urgency: {urgency}. \n Service Type: {service_type}. \n Problem: {problem}.\n After completing the service update in the website. \nThis is an auto generated message."
        elif status == 'Assigned':
            message = f"*Hello {receiver_data[phone]},*\n\n Service has been assigned to {engineer_assign}. \n\n Customer Name: {cname} \n Customer Phoneno: {cphoneno}.\n Urgency: {urgency}. \n Service Type: {service_type}. \n Problem: {problem}.\n This is an auto generated message."
        elif status == 'Completed':
            message = f"*Hello {receiver_data[phone]},*\n\n Service has been completed. \n\n Customer Name: {cname} \n Customer Phoneno: {cphoneno}. \n Engineer: {engineer_assign}\n Service Type: {service_type}. \n Problem: {problem}. \n Service Charge: {service_charge} \n Received Charge: {received_charge}.\n This is an auto generated message."
           
        data = {
            'phoneNumber': phone,  
            'message': message
        }
        response = requests.post(url, json=data)  
        if response.status_code == 200:
            print(f"Message sent successfully: {response.json()['message']}")
        else:
            print(f"Failed to send message: {response.text}")
   
    # data['attachment'] = {
    #     'filename': '36  Mahadhana Street  Opp VRS Thirumana Mahal Mayiladuthurai  609001 (2).pdf',
    #     'data': encoded_file
    # }

    #response = requests.post(url, json=data)  
    if response.status_code == 200:
        print(f"Message sent successfully: {response.json()['message']}")
    else:
        print(f"Failed to send message: {response.text}")  
