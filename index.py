from utils import generate_clf_schema;
import re
from resources import clf_base_URL,sam_base_URL,sam_api_url, sam_api_http_url, sam_func_url, sam_graph_api_url, sam_layer_url, sam_table_url, sam_state_machine_url, sam_app_url, sam_connecter_url, sam_api_url
# print(generate_clf_schema([clf_base_URL+resourceURL]))
sam_resources=[
        sam_func_url,
        sam_api_url,
        sam_api_http_url,  
        sam_table_url, 
        sam_state_machine_url, 
        sam_graph_api_url, 
        sam_layer_url, 
        sam_app_url, 
        sam_connecter_url, 
        ]
input_data=input("Select the resource to get the schema:\n1. SAM Lambda\n2. SAM API Gateway\n3. SAM Http API\n4. SAM Table\n5. SAM State Machine\n6. SAM GraphQL API\n7. SAM Layer\n9. SAM App\n10.SAM Connecter\n:")
if re.match(r'^[a-zA-Z]*$', input_data ):
    print("Invalid Entry!")
    exit()
if int(input_data) not in range(1,11):
    print("Invalid Option!")    
print(generate_clf_schema([sam_base_URL+sam_api_url],""))
# print("url",response_url)