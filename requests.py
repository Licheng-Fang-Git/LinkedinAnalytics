# import requests
# import json
#
# # Assuming you have an access_token
# access_token = "AQUUTXDRCI6qpWMlZNxxLR0Gdo__YKehuxAwSi6si2dSjwKTlAUo4i1DT7yHEVbxfFJ15-TsjvoFcOMCAxyPMrPaI0Vl9XH6uZFiboLGP1UltcGZfRXLw_TaM7CXEQcyso0B4TzqEWSbd-f_DTURSDS4vV-LcxNfvA4Y8aU3_y_UCPEmMx_6w7E9ZipjjMR1hKwUR6cMCnE-IMcxVrYSYmXzYstyTHg7UP8ywLSlKsSsZNbBkoMss6MGEOFqWwUy2dXUPC4T7lhcaXf8QNpW66UZOsMQzrBUwSjkKM6hVnECT1EHv8rtYAWix2truqy2btgTGzMUv7NRpUytQMAC5dHLx2v0cQ"
# # Example: Get the authenticated user's profile
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Linkedin-Version": '202411',
#     "Content-Type": "application/json"
#
# }
#
# response = requests.get("https://api.linkedin.com/rest/dmaFieldsOfStudy", headers=headers)
#
# if response.status_code == 200:
#     profile_data = response.json()
#     print(json.dumps(profile_data, indent=4))
# else:
#     print(f"Error: {response.status_code} - {response.text}")


