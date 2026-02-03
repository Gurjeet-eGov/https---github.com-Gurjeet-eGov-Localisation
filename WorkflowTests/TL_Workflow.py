from logic import Core
import utils

TL_obj = Core("TL")

def NewTL_mod_tenant(epoch_key, epoch_value, tenant):
    
    su_login_RequestInfo = TL_obj.login("Super")

    file = tenant.split(".")[1]
    create_file_path = "TL/"+file+".json"
    
    csr_create_response = TL_obj.call_api(su_login_RequestInfo, create_file_path,
                                          TL_obj.get_endpoint("create"))["Licenses"]

    # CSR Update
    csr_update_data = utils.prepare_update_payload(RequestInfo=su_login_RequestInfo, 
                        sample_payload_path="TL/update_payload.json", 
                        obj_keyword="Licenses",
                        prev_response=csr_create_response, 
                        mod_data_path="TL/csr_update_data.json")

    
    csr_update_response = TL_obj.call_api(su_login_RequestInfo, csr_update_data, 
                                          TL_obj.get_endpoint("update"))["Licenses"]

    # DV Update
    dv_update_data = utils.prepare_update_payload(RequestInfo=su_login_RequestInfo, 
                        sample_payload_path="TL/update_payload.json", 
                        obj_keyword="Licenses",
                        prev_response=csr_update_response, 
                        mod_data_path="TL/dv_update_data.json")

    dv_update_response = TL_obj.call_api(su_login_RequestInfo, dv_update_data, 
                                         TL_obj.get_endpoint("update"))["Licenses"]
    
    
    # FI Update
    fi_update_data = utils.prepare_update_payload(RequestInfo=su_login_RequestInfo, 
                        sample_payload_path="TL/update_payload.json", 
                        obj_keyword="Licenses",
                        prev_response=dv_update_response, 
                        mod_data_path="TL/fi_update_data.json")
    
    fi_update_response = TL_obj.call_api(su_login_RequestInfo, fi_update_data, 
                                         TL_obj.get_endpoint("update"))["Licenses"]
    

    # AP Update payload
    ap_update_data = utils.prepare_update_payload(RequestInfo=su_login_RequestInfo, 
                        sample_payload_path="TL/update_payload.json", 
                        obj_keyword="Licenses",
                        prev_response=fi_update_response, 
                        mod_data_path="TL/ap_update_data.json")
    
    # updating epoch here
    ap_update_data = utils.mod_json(ap_update_data, epoch_key, epoch_value)

    ap_update_response = TL_obj.call_api(su_login_RequestInfo, ap_update_data, 
                                         TL_obj.get_endpoint("update"))["Licenses"]

    Application_ID = ap_update_response[0]["applicationNumber"]

    fetch_bill_response = TL_obj.fetch_bill(su_login_RequestInfo, Application_ID, "TL", tenant)
    collection_response = TL_obj.collect_fee(su_login_RequestInfo, fetch_bill_response, tenant)


    search_param = {"tenantId": tenant, "applicationNumber": Application_ID}
    tl_search_response = TL_obj.call_api(su_login_RequestInfo, payload={}, 
                                         api=TL_obj.get_endpoint("search"), params = search_param)["Licenses"]
    License_ID = tl_search_response[0]["licenseNumber"]

    # logout CSR
    TL_obj.logout(su_login_RequestInfo)

    return License_ID
