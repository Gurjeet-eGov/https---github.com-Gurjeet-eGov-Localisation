from logic import Core
import utils

SW_obj = Core("sw-services")

# Main workflow
def NewSW():
    
    csr_login_RequestInfo = SW_obj.login("CSR")

    # CSR Create
    csr_create_response = SW_obj.call_api(csr_login_RequestInfo, "SW/csr_create_data.json", SW_obj.get_endpoint("create"))["SewerageConnections"]
    
    # CSR Update
    csr_update_data = utils.prepare_update_payload(RequestInfo=csr_login_RequestInfo, 
                        sample_payload_path="SW/update_payload.json", 
                        obj_keyword="SewerageConnection",
                        prev_response=csr_create_response, 
                        mod_data_path="SW/csr_update_data.json")
    csr_update_response = SW_obj.call_api(csr_login_RequestInfo, csr_update_data, SW_obj.get_endpoint("update"))["SewerageConnections"]


    # use CSR credentials for FieldEmp actions
    login_RequestInfo = csr_login_RequestInfo

    # DV Update
    dv_update_data = utils.prepare_update_payload(RequestInfo=login_RequestInfo, 
                        sample_payload_path="SW/update_payload.json", 
                        obj_keyword="SewerageConnection",
                        prev_response=csr_update_response, 
                        mod_data_path="SW/dv_update_data.json")
    dv_update_response = SW_obj.call_api(login_RequestInfo, dv_update_data, SW_obj.get_endpoint("update"))["SewerageConnections"]

    # FI Update (still using CSR credentials)
    fi_update_data = utils.prepare_update_payload(RequestInfo=login_RequestInfo, 
                        sample_payload_path="SW/update_payload.json", 
                        obj_keyword="SewerageConnection",
                        prev_response=dv_update_response, 
                        mod_data_path="SW/fi_update_data.json")
    fi_update_response = SW_obj.call_api(login_RequestInfo, fi_update_data, SW_obj.get_endpoint("update"))["SewerageConnections"]
    
    # use CSR credentials for OfficeEmp actions as well
    login_RequestInfo = csr_login_RequestInfo

    # AP Update payload
    ap_update_data = utils.prepare_update_payload(RequestInfo=login_RequestInfo, 
                        sample_payload_path="SW/update_payload.json", 
                        obj_keyword="SewerageConnection",
                        prev_response=fi_update_response, 
                        mod_data_path="SW/ap_update_data.json")
    ap_update_response = SW_obj.call_api(login_RequestInfo, ap_update_data, 
                                         SW_obj.get_endpoint("update"))["SewerageConnections"]

    fetch_bill_response = SW_obj.fetch_bill(csr_login_RequestInfo, ap_update_response[0]["applicationNumber"], "SW.ONE_TIME_FEE")
    collection_response = SW_obj.collect_fee(csr_login_RequestInfo, fetch_bill_response)
    # After collection, search to get connection details for activation
    search_param = {"tenantId": SW_obj.CITY, "applicationNumber": ap_update_response[0]["applicationNumber"]}
    sw_search_response = SW_obj.call_api(csr_login_RequestInfo, payload={}, api=SW_obj.get_endpoint("search"), params=search_param)["SewerageConnections"]
    Connection_ID = sw_search_response[0]["connectionNo"]

    # Prepare activation payload using the latest connection response
    act_update_data = utils.prepare_update_payload(RequestInfo=csr_login_RequestInfo,
                                                  sample_payload_path="SW/update_payload.json",
                                                  obj_keyword="SewerageConnection",
                                                  prev_response=sw_search_response,
                                                  mod_data_path="SW/act_update_data copy.json")
    act_update_response = SW_obj.call_api(csr_login_RequestInfo, act_update_data, SW_obj.get_endpoint("update"))["SewerageConnections"]

    # logout CSR
    SW_obj.logout(csr_login_RequestInfo)
    return Connection_ID

def NewSW_mod(epoch_key, epoch_value):
    
    csr_login_RequestInfo = SW_obj.login("CSR")

    # CSR Create
    csr_create_response = SW_obj.call_api(csr_login_RequestInfo, "SW/csr_create_data.json", SW_obj.get_endpoint("create"))["SewerageConnections"]

    # CSR Update
    csr_update_data = utils.prepare_update_payload(RequestInfo=csr_login_RequestInfo, 
                        sample_payload_path="SW/update_payload.json", 
                        obj_keyword="SewerageConnection",
                        prev_response=csr_create_response, 
                        mod_data_path="SW/csr_update_data.json")

    
    csr_update_response = SW_obj.call_api(csr_login_RequestInfo, csr_update_data, SW_obj.get_endpoint("update"))["SewerageConnections"]


    # use CSR credentials for FieldEmp actions
    login_RequestInfo = csr_login_RequestInfo
    # DV Update
    dv_update_data = utils.prepare_update_payload(RequestInfo=login_RequestInfo, 
                        sample_payload_path="SW/update_payload.json", 
                        obj_keyword="SewerageConnection",
                        prev_response=csr_update_response, 
                        mod_data_path="SW/dv_update_data.json")

    dv_update_response = SW_obj.call_api(login_RequestInfo, dv_update_data, SW_obj.get_endpoint("update"))["SewerageConnections"]
    
    
    # FI Update
    fi_update_data = utils.prepare_update_payload(RequestInfo=login_RequestInfo, 
                        sample_payload_path="SW/update_payload.json", 
                        obj_keyword="SewerageConnection",
                        prev_response=dv_update_response, 
                        mod_data_path="SW/fi_update_data.json")
    
    fi_update_response = SW_obj.call_api(login_RequestInfo, fi_update_data, SW_obj.get_endpoint("update"))["SewerageConnections"]

    # use CSR credentials for OfficeEmp actions as well
    login_RequestInfo = csr_login_RequestInfo
    # AP Update payload
    ap_update_data = utils.prepare_update_payload(RequestInfo=login_RequestInfo, 
                        sample_payload_path="SW/update_payload.json", 
                        obj_keyword="SewerageConnection",
                        prev_response=fi_update_response, 
                        mod_data_path="SW/ap_update_data.json")
    
    # updating epoch here
    ap_update_data = utils.mod_json(ap_update_data, epoch_key, epoch_value)

    ap_update_response = SW_obj.call_api(login_RequestInfo, ap_update_data, 
                                         SW_obj.get_endpoint("update"))["SewerageConnections"]

    Application_ID = ap_update_response[0]["applicationNumber"]

    # logout OfficeEmp
    SW_obj.logout(login_RequestInfo)


    fetch_bill_response = SW_obj.fetch_bill(csr_login_RequestInfo, Application_ID, "SW.ONE_TIME_FEE")
    collection_response = SW_obj.collect_fee(csr_login_RequestInfo, fetch_bill_response)

    search_param = {"tenantId": SW_obj.CITY, "applicationNumber": Application_ID}
    sw_search_response = SW_obj.call_api(csr_login_RequestInfo, payload={}, 
                                         api=SW_obj.get_endpoint("search"), params = search_param)["SewerageConnections"]
    Connection_ID = sw_search_response[0]["connectionNo"]

    # Prepare activation payload and call update
    act_update_data = utils.prepare_update_payload(RequestInfo=csr_login_RequestInfo,
                                                  sample_payload_path="SW/update_payload.json",
                                                  obj_keyword="SewerageConnection",
                                                  prev_response=sw_search_response,
                                                  mod_data_path="SW/act_update_data copy.json")
    act_update_response = SW_obj.call_api(csr_login_RequestInfo, act_update_data, SW_obj.get_endpoint("update"))["SewerageConnections"]

    # logout CSR
    SW_obj.logout(csr_login_RequestInfo)

    return Connection_ID
