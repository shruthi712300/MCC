# import requests
# import json

# def send_whatsapp_message(data):
#     print(data)
#     print(data.cphoneno)
#     phoneno1 = "91"+str(data.cphoneno)
#     print(phoneno1)
#     url = f'https://graph.facebook.com/v18.0/106885295759687/messages'

#     headers = {
#         'Authorization': f'Bearer EAAK3LGk3JkABO7l9CQBRqLq5lNvU753Yt2EYroPuZBMtMjZCNWSQGHSfPdkoUvcvm4g4DFDwfqbLD3vDx16yWCb1Y8ZAGb4ZAAYgWxdOiF7YOQPZBZBHrRI2kPbmL7hM18QulIu0YSIbmKd6ZCeMCFXLdHarYoZA2gHynjcJca7ZCMFpvHZCndZBZAOQ7WLGlzvwjWF7',
#         'Content-Type': 'application/json'
#     }

#     name = "kishore"
#     ss="ss"
#     # product = product
#     # model = model
#     # date = date
#     # bag = bag
#     # charger = charger
#     # power_cable = power_cable
#     # problem = problem

#     payload = {
#         "messaging_product": "whatsapp",
#         "to": phoneno1,
#         "type": "template",
#         "template": {
#             "name": "service_msg",
#             "language": {
#                 "code": "en_us"
#                 },
#             "components": [
#                 {
#                 "type": "BODY",
#                 "parameters": [
#                     {
#                         "type": "text",
#                         "text": data.product_model
#                         },
#                     {
#                         "type": "text",
#                         "text": data.product_type
#                         },
#                         {
#                         "type": "text",
#                         "text": data.service_date
#                         },{
#                         "type": "text",
#                         "text": data.bag
#                         },{
#                         "type": "text",
#                         "text": data.charger
#                         },
#                     {
#                         "type": "text",
#                         "text": data.power_cable
#                         },
#                         {
#                         "type": "text",
#                         "text": data.problem
#                         },
#                     ]
#                 }
#                 ]
#             }
#         }
            
     
        

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code == 200:
#         print("Message sent successfully.")
#     else:
#         print(response)
#         print("Failed to send message.")
#         try:
#             error_response = response.json()
#             print(json.dumps(error_response, indent=4))
#         except json.JSONDecodeError:
#             print('Response content is not in JSON format')
#             print(response.text)







# def send_delivered_message(model,product,date,bag,charger,power_cable,problem,phoneno,service_charge):
#     phoneno1 = "91"+str(phoneno)
#     print(phoneno1)
#     url = f'https://graph.facebook.com/v18.0/106885295759687/messages'

#     headers = {
#         'Authorization': f'Bearer EAAK3LGk3JkABO7l9CQBRqLq5lNvU753Yt2EYroPuZBMtMjZCNWSQGHSfPdkoUvcvm4g4DFDwfqbLD3vDx16yWCb1Y8ZAGb4ZAAYgWxdOiF7YOQPZBZBHrRI2kPbmL7hM18QulIu0YSIbmKd6ZCeMCFXLdHarYoZA2gHynjcJca7ZCMFpvHZCndZBZAOQ7WLGlzvwjWF7',
#         'Content-Type': 'application/json'
#     }

#     name = "kishore"
#     ss="ss"
#     product = product
#     model = model
#     date = date
#     bag = bag
#     charger = charger
#     power_cable = power_cable
#     problem = problem
#     service_charge = service_charge
#     payload = {
#         "messaging_product": "whatsapp",
#         "to": phoneno1,
#         "type": "template",
#         "template": {
#             "name": "delivery_msg",
#             "language": {
#                 "code": "en_us"
#                 },
#             "components": [
#                 {
#                 "type": "BODY",
#                 "parameters": [
#                     {
#                         "type": "text",
#                         "text": model
#                         },
#                     {
#                         "type": "text",
#                         "text": product
#                         },
#                         {
#                         "type": "text",
#                         "text": bag
#                         },{
#                         "type": "text",
#                         "text": charger
#                         },
#                     {
#                         "type": "text",
#                         "text": power_cable
#                         },
#                         {
#                         "type": "text",
#                         "text": service_charge
#                         },
                        
#                     ]
#                 }
#                 ]
#             }
#         }
            
     
        

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code == 200:
#         print("Message sent successfully.")
#     else:
#         print(response)
#         print("Failed to send message.")

