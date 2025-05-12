#!/usr/bin/env python3
import datetime
import argparse
import requests
from sys import exit
import urllib3
import json
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

date_time = datetime.datetime.now()
file_name = date_time.strftime("capcheck_" + "%m-%d-%y-%X.txt")
file_name = file_name.replace(":", "-")

scope_list = []
successful_results = []

endpoint_table = [
    [1, "MS Graph", "https://graph.microsoft.com"],
    [2, "aad_graph_api", "https://graph.windows.net"],
    [3, "Azure Management", "https://management.azure.com"],
    [4, "windows_net_mgmt_api", "https://management.core.windows.net"],
    [5, "cloudwebappproxy", "https://proxy.cloudwebappproxy.net/registerapp"],
    [6, "Office Apps", "https://officeapps.live.com"],
    [7, "outlook", "https://outlook.office365.com"],
    [8, "webshellsuite", "https://webshell.suite.office.com"],
    [9, "sara", "https://api.diagnostics.office.com"],
    [10, "office_mgmt", "https://manage.office.com"],
    [11, "spacesapi", "https://api.spaces.skype.com"],
    [12, "datacatalog", "https://datacatalog.azure.com"],
    [13, "database", "https://database.windows.net"],
    [14, "AzureKeyVault", "https://vault.azure.net"],
    [15, "onenote", "https://onenote.com"],
    [16, "o365_yammer", "https://api.yammer.com"],
    [17, "skype4business", "https://api.skypeforbusiness.com"],
    [18, "o365_exchange", "https://outlook-sdf.office.com"],
    [19, "aad_account", "https://account.activedirectory.windowsazure.com"],
    [20, "Substrate", "https://substrate.office.com"],
    [21, "Intune", "https://msmamservice.api.application"]
    ]

useragent_table = [
    [1, "Mobile - iOS - Safari", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604"],
    [2, "Mobile - Android - Chrome", "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.3"],
    [3, "Desktop - MacOS - Safari", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.1"],
    [4, "Desktop - Linux - Firefox", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"],
    [5, "Desktop - Windows - Edge", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"],
    [6, "Python Requests", "python-requests/2.32.3"],
    [7, "Blank", ""]
]

clientid_table = [
    [1, "EnterpriseRoamingandBackup", "60c8bde5-3167-4f92-8fdb-059f6176dc0f"],
    [2, "MicrosoftApprovalManagement", "38049638-cc2c-4cde-abe4-4479d721ed44"],
    [3, "MicrosoftAuthenticationBroker", "29d9ed98-a469-4536-ade2-f981bc1d605e"],
    [4, "MicrosoftAzureCLI", "04b07795-8ddb-461a-bbee-02f9e1bf7b46"],
    [5, "MicrosoftAzurePowerShell", "1950a258-227b-4e31-a9cf-717495945fc2"],
    [6, "MicrosoftBingSearch", "cf36b471-5b44-428c-9ce7-313bf84528de"],
    [7, "MicrosoftBingSearchforMicrosoftEdge", "2d7f3606-b07d-41d1-b9d2-0d0c9296a6e8"],
    [8, "MicrosoftDocs", "18fbca16-2224-45f6-85b0-f7bf2b39b3f3"],
    [9, "MicrosoftExchangeRESTAPIBasedPowershell", "fb78d390-0c51-40cd-8e17-fdbfab77341b"],
    [10, "MicrosoftExchangeWebServices", "47629505-c2b6-4a80-adb1-9b3a3d233b7b"],
    [11, "MicrosoftIntuneWindowsAgent", "fc0f3af4-6835-4174-b806-f7db311fd2f3"],
    [12, "MicrosoftOffice", "d3590ed6-52b3-4102-aeff-aad2292ab01c"],
    [13, "MicrosoftPowerBI", "c0d2a505-13b8-4ae0-aa9e-cddd5eab0b12"],
    [14, "MicrosoftTeams", "1fec8e78-bce4-4aaf-ab1b-5451cc387264"],
    [15, "Office365Management", "00b41c95-dab0-4487-9791-b9d2c32c80f2"],
    [16, "Office365SharePointOnline", "00000003-0000-0ff1-ce00-000000000000"],
    [17, "OneDriveSyncEngine", "ab9b8c07-8f02-4f72-87fa-80105867a763"],
    [18, "OutlookMobile", "27922004-5251-4030-b22d-91ecd9a37ea4"],
    [19, "SkypeforBusinessOnline", "00000004-0000-0ff1-ce00-000000000000"],
    [20, "UniversalStoreNativeClient", "268761a2-03f3-40df-8a8b-c3db24145b6b"],
    [21, "WindowsDefenderATPPortal", "a3b79187-70b2-4139-83f9-6016c58cd27b"],
    [22, "WindowsSearch", "26a7ee05-5602-4d76-a7ba-eae8b7b67941"],
    [23, "WindowsSpotlight", "1b3c667f-cde3-4090-b60b-3d2abd0117f0"],
    [24, "MicrosoftGraphCommandLineTools", "14d82eec-204b-4c2f-b7e8-296a70dab67e"],
    [25, "OutlookUserSettingsConsumer", "7ae974c5-1af7-4923-af3a-fb1fd14dcb7e"],
    [26, "Vortex[wsfedenabled]", "5572c4c0-d078-44ce-b81c-6cbf8d3ed39e"],
    [27, "OfficeUWPPWA", "0ec893e0-5785-4de6-99da-4ed124e5296c"],
    [28, "WindowsShell", "145fc680-eb72-4bcf-b4d5-8277021a1ce8"],
    [29, "SSOExtensionIntune", "163b648b-025e-455b-9937-a7f39a65d171"],
    [30, "EditorBrowserExtension", "1a20851a-696e-4c7e-96f4-c282dfe48872"],
    [31, "AzureActiveDirectoryPowerShell", "1b730954-1685-4b74-9bfd-dac224a7b894"],
    [32, "MicrosoftTo-Doclient", "22098786-6e16-43cc-a27d-191a01a1e3b5"],
    [33, "ModernWorkplaceCustomerAPINative", "2e307cd5-5d2d-4499-b656-a97de9f52708"],
    [34, "PowerAutomateDesktopForWindows", "386ce8c0-7421-48c9-a1df-2a532400339f"],
    [35, "EnterpriseDashboardProject", "3a4d129e-7f50-4e0d-a7fd-033add0a29f4"],
    [36, "PowerApps-apps.powerapps.com", "3e62f81e-590b-425b-9531-cad6683656cf"],
    [37, "UniversalPrintEnabledPrinter", "417ae6eb-aac8-42c8-900c-0e50debba688"],
    [38, "MicrosoftAuthenticatorApp", "4813382a-8fa7-425e-ab75-3b753aab3abb"],
    [39, "FXIrisClient", "4b0964e4-58f1-47f4-a552-e2e1fc56dcd7"],
    [40, "PowerApps", "4e291c71-d680-4d0e-9640-0a3358e31177"],
    [41, "SurfaceDashboard", "507a7586-da5c-4e86-80f2-2bc2e55ae394"],
    [42, "GraphFilesManager", "52c2e0b5-c7b6-4d11-a89c-21e42bcec444"],
    [43, "MicrosoftWhiteboardClient", "57336123-6e14-4acc-8dcf-287b6088aa28"],
    [44, "SharePointOnlineClient", "57fb890c-0dab-4253-a5e0-7188c88b2bb4"],
    [45, "MicrosoftFlowMobilePROD-GCCH-CN", "57fcbcfa-7cee-4eb1-8b25-12d2030b4ee0"],
    [46, "MicrosoftOutlook", "5d661950-3475-41cd-a2c3-d671a3162bc1"],
    [47, "WindowsUpdateforBusinessDeploymentService", "61ae9cd9-7bca-458c-affc-861e2f24ba3b"],
    [48, "MicrosoftPlanner", "66375f6b-983f-4c2c-9701-d680650f588f"],
    [49, "HoloLensCameraRollUpload", "6b11041d-54a2-4c4f-96a2-6053efe46d8b"],
    [50, "WindowsUpdate-Service", "6f0478d5-61a3-4897-a2f2-de09a5a90c7f"],
    [51, "MicrosoftApplicationCommandService", "6f7e0f60-9401-4f5b-98e2-cf15bd5fd5e3"],
    [52, "ZTNADataAcquisition-PROD", "7dd7250c-c317-4bc6-8528-8d27b02707ef"],
    [53, "PowerBIDesktop", "7f67af8a-fedc-4b08-8b4e-37c4d127b6cf"],
    [54, "UniversalPrintConnector", "80331ee5-4436-4815-883e-93bc833a9a15"],
    [55, "MicrosoftStreamMobileNative", "844cca35-0656-46ce-b636-13f48b0eecbd"],
    [56, "OutlookWebAppWidgets", "87223343-80b1-4097-be13-2332ffa1d666"],
    [57, "VisualStudio-Legacy", "872cd9fa-d31f-45e0-9eab-6e460a02d1f1"],
    [58, "MicrosoftTeams-DeviceAdminAgent", "87749df4-7ccf-48f8-aa87-704bad0e0e16"],
    [59, "MicrosoftIntuneCompanyPortal", "9ba1a5c7-f17a-4de9-a1f1-6178c8d51223"],
    [60, "Microsoft.MileIQ", "a25dbca8-4e60-48e5-80a2-0664fdb5c9b6"],
    [61, "AccountsControlUI", "a40d7d7d-59aa-447e-a655-679a4107e548"],
    [62, "YammeriPhone", "a569458c-7f2b-45cb-bab9-b7dee514d112"],
    [63, "MicrosoftPowerQueryforExcel", "a672d62c-fc7b-4e81-a576-e60dc46e951d"],
    [64, "AzureHDInsightonAKSClient", "a6943a7f-5ba0-4a34-bf91-ab439efdda3f"],
    [65, "CommonJobProvider", "a99783bc-5466-4cef-82eb-ebf285d77131"],
    [66, "UniversalPrintPSModule", "aad98258-6bb0-44ed-a095-21506dfb68fe"],
    [67, "VisualStudioCode", "aebc6443-996d-45c2-90f0-388ff96faa56"],
    [68, "OneDriveiOSApp", "af124e86-4e96-495a-b70a-90f90ab96707"],
    [69, "OneDrive", "b26aadf8-566f-4478-926f-589f601d9c74"],
    [70, "OutlookOnlineAdd-inApp", "bc59ab01-8403-45c6-8796-ac3ef710b3e3"],
    [71, "M365ComplianceDriveClient", "be1918be-3fe3-4be9-b32b-b542fc27f02e"],
    [72, "SharePointOnlineClientExtensibility", "c58637bb-e2e1-4312-8a00-04b5ffcd3403"],
    [73, "MicrosoftDefenderPlatform", "cab96880-db5b-4e15-90a7-f3f1d62ffe39"],
    [74, "MicrosoftAzureActiveDirectoryConnect", "cb1056e2-e479-49de-ae31-7812af012ed8"],
    [75, "SharePoint", "d326c1ce-6cc6-4de2-bebc-4591e5e13ef0"],
    [76, "MicrosoftActivityFeedService", "d32c68ad-72d2-4acb-a0c7-46bb2cf93873"],
    [77, "WindowsUpdateforBusinessCloudExtensionsPowerShell", "d5097d05-956f-4ae2-b6a2-eff25f5689b3"],
    [78, "DynamicsRetailCloudPOS", "d5527362-3bc8-4e63-b5b3-606dc14747e9"],
    [79, "MicrosoftEdgeEnterpriseNewTabPage", "d7b530a4-7680-4c23-a8bf-c52c121d2e87"],
    [80, "UniversalPrintNativeClient", "dae89220-69ba-4957-a77a-47b78695e883"],
    [81, "MicrosoftDefenderforMobile", "dd47d17a-3194-4d86-bfd5-c6ae6f5651e3"],
    [82, "MicrosoftDeviceRegistrationClient", "dd762716-544d-4aeb-a526-687b73838a22"],
    [83, "DeviceManagementClient", "de50c81f-5f80-4771-b66b-cebd28ccdfc1"],
    [84, "ModernWorkplaceAppDiagnosticAuthenticator", "e036f41b-7edf-47ee-b373-b4b374a2e33c"],
    [85, "OfficeBrowserExtension", "e28ff72c-58a5-49ba-8125-42ec264d7cd0"],
    [86, "OutlookLite", "e9b154d0-7658-433b-bb25-6b8e0a8a7c59"],
    [87, "MicrosoftEdge", "f44b1140-bc5e-48c6-8dc0-5cf5a53c0e34"],
    [88, "MicrosoftTunnel", "eb539595-3fe1-474e-9c1d-feb3625d1be5"],
    [89, "SharePointAndroid", "f05ff7c9-f75a-4acd-a3b5-f4b6a870245d"],
    [90, "IDS-PROD", "f36c30df-d241-4c14-a0ee-752c71e4d3da"],
    [91, "MediaRecordingforDynamics365Sales", "f448d7e5-e313-4f90-a3eb-5dbb3277e4b3"],
    [92, "MicrosoftRemoteAssist", "fca5a20d-55aa-4395-9c2f-c6147f3c9ffa"],
    [93, "Teams Application Gateway", "8a753eec-59bc-4c6a-be91-6bf7bfe0bcdf"],
    [94, "LinkedIn", "f03e9017-17a2-4eea-b8d1-c27da31393d2"],
    [95, "Box", "89220c47-d3bd-4942-a242-bda247a5bc5b"],
    [96, "ISV Portal", "c6871074-3ded-4935-a5dc-b8f8d91d7d06"],
    [97, "BrowserStack", "33261ead-27d2-41e8-97e5-24319826c2af"],
    [98, "Groupies Web Service", "925eb0d0-da50-4604-a19f-bd8de9147958"],
    [99, "Azure ESTS Service", "00000001-0000-0000-c000-000000000000"],
    [100, "MOD Demo Platform UnifiedApiConsumer", "aff75787-e598-43f9-a0ea-7a0ca00ababc"],
    [101, "Kaizala Sync Service", "d82073ec-4d7c-4851-9c5d-5d97a911d71d"],
    [102, "MicrosoftTeamsCortanaSkills", "2bb78a2a-f8f1-4bc3-8ecf-c1e15a0726e6"],
    [103, "Salesforce", "481732f5-fe5b-48c0-8445-d238ab230658"],
    [104, "Microsoft Dynamics CRM Learning Path", "2db8cb1d-fb6c-450b-ab09-49b6ae35186b"],
    [105, "Azure Media Service", "803ee9ca-3f7f-4824-bd6e-0b99d720c35c"],
    [106, "Cortana at Work Bing Services", "22d7579f-06c2-4baa-89d2-e844486adb9d"],
    [107, "YammerOnOls", "c26550d6-bc82-4484-82ca-ac1c75308ca3"],
    [108, "Microsoft Kaizala", "dc3294af-4679-418f-a30c-76948e23fe1c"],
    [109, "Twitter", "1683fa2e-8c1a-41e7-92f9-940cc8852759"],
    [110, "Office UWP PWA", "0ec893e0-5785-4de6-99da-4ed124e5296c"],
    [111, "Microsoft Edge", "e9c51622-460d-4d3d-952d-966a5b1da34c"],
    [112, "Microsoft Edge", "ecd6b820-32c2-49b6-98a6-444530e5a77a"]
]


def get_clientid_name(client_id):
    for id_entry in clientid_table:
        if id_entry[2] == client_id:
            return id_entry[1]
    return "Unknown ClientID"



def main():
    # Take in user args
    parser = argparse.ArgumentParser(
        description="Audit Azure endpoints for MFA conditional access policy bypasses with a valid username and password. This tool will also print the scopes of the tokens obtained.",
        epilog=(
            "examples:\n"
            "# List build in parameters.\n"
            "python3 capcheck.py --list-all\n\n"

            "# Sign into intune using the MS intune company portal client id and windows desktop user agent. Use the built in numbers or specify the value directly.\n" 
            "python3 capcheck.py -u user@client.com -p password -c 59 -e 21 -a 5\n"
            "python3 capcheck.py -u user@client.com -p password -c '9ba1a5c7-f17a-4de9-a1f1-6178c8d51223' -e 'https://msmamservice.api.application' -a 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'\n\n"

            "# Brute force various built in parameters.\n"
            "python3 capcheck.py -u user@client.com -p password --useragent-brute\n"
            "python3 capcheck.py -u user@client.com -p password --clientid-brute\n"
            "python3 capcheck.py -u user@client.com -p password --endpoint-brute\n\n"
            
            "# Brute force everything, proxy the requests.\n"
            "python3 capcheck.py -u user@client.com -p password --brute-all --proxy http://127.0.0.1:8080\n"

        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
                                    
    parser.add_argument("-u", "--username", dest='username', default=None, help="The username for authentication.")
    parser.add_argument("-U", "--userlist", dest='username_list', default=None, help="A file containing a list of usernames. Useful when common passwords are used more than once across users in the organization.")
    parser.add_argument("-p", "--password", dest='password', default=None, help="The password for authentication.")
    parser.add_argument("-a", "--useragent", dest='useragent', default=None, help="Define a user agent to try. Default is iPhone.")
    #parser.add_argument("-A", "--useragentfile", dest='useragent_file', default=None, help="A file containing a list of user agents.")
    parser.add_argument("-c", "--clientid", dest='clientid', default=None, help="Define a client id to try. Default is aadps.")
    #parser.add_argument("-C", "--clientidfile", dest='clientid_file', default=None, help="A file containing a list of client ids.")
    parser.add_argument("-e", "--endpoint", dest='endpoint', default=None, help="The endpoint to spray. Deafult is MS Graph.")
    #parser.add_argument("-E", "--endpointfile", dest='endpoint_file', default=None, help="A file containing a list of azure endpoints.")
    parser.add_argument("-ab", "--useragent-brute", dest='useragent_brute', action='store_true', help="Perform user agent brute forcing with built in list.")
    parser.add_argument("-cb", "--clientid-brute", dest='clientid_brute', action='store_true', help="Perform client id brute forcing with built in list.")
    parser.add_argument("-eb", "--endpoint-brute", dest='endpoint_brute', action='store_true', help="Perform endpoint brute forcing with built in list.")
    parser.add_argument("--brute-all", dest='brute_all', action='store_true', help="Perform user agent, endpoint, and client ID brute forcing with built in lists. WARNING - lots of requests..")
    parser.add_argument("--list-useragents", dest='list_useragents', action='store_true', help="List the built in user agents.")
    parser.add_argument("--list-endpoints", dest='list_endpoints', action='store_true', help="List the built in endpoints.")
    parser.add_argument("--list-clientids", dest='list_clientids', action='store_true', help="List the built in client ids.")
    parser.add_argument("--list-all", dest='list_all', action='store_true', help="List all the built in user agents, endpoints, and client ids.")
    #parser.add_argument("-j", "--jitter", dest='jitter', action='store_true', help="Randomized jitter between requests.")
    #parser.add_argument("-d", "--delay", dest='delay', action='store_true', help="Delay between requests.")
    #parser.add_argument("-q", "--quiet", dest='quiet', action='store_true', help="Only display attempts when a token is obtained.")
    parser.add_argument("--proxy", dest='proxy', default=None, help="Proxy to use, ex: http://127.0.0.1:8080")

    args = parser.parse_args()

    username = args.username
    username_list = args.username_list
    password = args.password
    useragent_brute = args.useragent_brute
    clientid_brute = args.clientid_brute
    endpoint_brute = args.endpoint_brute
    proxy = args.proxy

    if args.list_all is True:
        args.list_useragents = True
        args.list_endpoints = True
        args.list_clientids = True

    if args.brute_all is True:
        useragent_brute = True
        clientid_brute = True
        endpoint_brute = True


    if args.list_useragents or args.list_endpoints or args.list_clientids:
        if args.list_useragents:
            desc_width = max(len(agent[1]) for agent in useragent_table) + 1

            print("User-Agents:")
            for agent in useragent_table:
                print(f"{str(agent[0]):<{3}} {agent[1]:<{desc_width}} {agent[2]}")
            print()

        if args.list_endpoints:
            desc_width = max(len(url[1]) for url in endpoint_table) + 1

            print("Endpoints:")
            for url in endpoint_table:
                print(f"{str(url[0]):<{3}} {url[1]:<{desc_width}} {url[2]}")
            print()

        if args.list_clientids:
            desc_width = max(len(id[1]) for id in clientid_table) + 1

            print("Client IDs:")
            for id in clientid_table:
                print(f"{str(id[0]):<{3}} {id[1]:<{desc_width}} {id[2]}")
            print()
        exit()
        
    if not args.username and not args.username_list:
        print("You provide a username to test.")
        exit()

    if not args.password:
        print("You must provide a password for the user.")
        exit()
              
    # set default user agent as first entry in table
    if args.useragent is None:
        user_agent = useragent_table[0][2]
        user_agent_name = useragent_table[0][1]

    else:
        try:
            user_agent_num = int(args.useragent)
            user_agent = useragent_table[(user_agent_num-1)][2]
            user_agent_name = useragent_table[(user_agent_num-1)][1]

        except:
            user_agent = args.useragent
            user_agent_name = args.useragent

    # set default client id as first entry in table
    if args.clientid is None:
        client_id = clientid_table[0][2]

    else:
        try:
            client_id_num = int(args.clientid)
            client_id = clientid_table[(client_id_num-1)][2]
        
        except: 
            client_id = args.clientid

    # set default endpoint as first entry in table
    if args.endpoint is None:
        endpoint = endpoint_table[0][2]

    else:
        try:
            endpoint_num = int(args.endpoint)
            endpoint = endpoint_table[(endpoint_num-1)][2]

        except: 
            endpoint = args.endpoint


    if useragent_brute:
        if clientid_brute:
            if endpoint_brute:
                # All 3
                answer = input("This will generate " + str(len(clientid_table)*len(endpoint_table)*len(useragent_table)) + " login attempts for each user specified. Logging results to ./capcheck_log/" + file_name + ". Continue? [Y/n] \n")
                if answer.lower() == 'y' or answer.lower() == '':

                    for agent in useragent_table:
                        user_agent = agent[2]
                        user_agent_name = agent[1]
                        
                        for id in clientid_table:
                            client_id = id[2]

                            for url in endpoint_table:
                                endpoint = url[2]

                                if username_list:
                                    with open(username_list, 'r') as file:
                                        for user in file:
                                            username = user.strip()

                                            login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
                                else:
                                    login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)

                else:
                    exit()

            else:
                # useragent and cliendid brute only
                answer = input("This will generate " + str(len(clientid_table)*len(useragent_table)) + " login attempts. Logging results to ./capcheck_log/" + file_name + ". Continue? [Y/n] \n")
                if answer.lower() == 'y' or answer.lower() == '':

                    for agent in useragent_table:
                        user_agent = agent[2]
                        user_agent_name = agent[1]

                        for id in clientid_table:
                            client_id = id[2]

                            if username_list:
                                with open(username_list, 'r') as file:
                                    for user in file:
                                        username = user.strip()
                                        
                                        login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)

                            else:
                                login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
                else:
                    exit()


        elif endpoint_brute:
            # useragent and endpoint brute only
            answer = input("This will generate " + str(len(useragent_table)*len(endpoint_table)) + " login attempts. Logging results to ./capcheck_log/" + file_name + ". Continue? [Y/n] \n")
            if answer.lower() == 'y' or answer.lower() == '':

                for agent in useragent_table:
                    user_agent = agent[2]
                    user_agent_name = agent[1]

                    for url in endpoint_table:
                        endpoint = url[2]

                        if username_list:
                            with open(username_list, 'r') as file:
                                for user in file:
                                    username = user.strip()

                                    login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
                        else:
                            login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
            else:
                exit()


        else: 
            # useragent brute only
            answer = input("This will generate " + str(len(useragent_table)) + " login attempts. Logging results to ./capcheck_log/" + file_name + ". Continue? [Y/n] \n")
            if answer.lower() == 'y' or answer.lower() == '':
                
                for agent in useragent_table:
                    user_agent = agent[2]
                    user_agent_name = agent[1]

                    if username_list:
                        with open(username_list, 'r') as file:
                            for user in file:
                                username = user.strip()

                                login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
                    else:
                        login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
                    
            else:
                exit()


    elif clientid_brute:
        if endpoint_brute:
            # clientid and endpoint brute only
            answer = input("This will generate " + str(len(clientid_table)*len(endpoint_table)) + " login attempts. Logging results to ./capcheck_log/" + file_name + ". Continue? [Y/n] \n")
            if answer.lower() == 'y' or answer.lower() == '':

                for id in clientid_table:
                    client_id = id[2]

                    for url in endpoint_table:
                        endpoint = url[2]

                        if username_list:
                            with open(username_list, 'r') as file:
                                for user in file:
                                    username = user.strip()

                                    login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)

                        else:
                            login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
            else:
                exit()
        
        else:
            # clientid brute only
            answer = input("This will generate " + str(len(clientid_table)) + " login attempts. Logging results to ./capcheck_log/" + file_name + ". Continue? [Y/n] \n")
            if answer.lower() == 'y' or answer.lower() == '':

                for id in clientid_table:
                    client_id = id[2]

                    if username_list:
                        with open(username_list, 'r') as file:
                            for user in file:
                                username = user.strip()

                                login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
                    else:
                        login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
            else:
                exit()


    elif endpoint_brute:
        #endpoint BF
        answer = input("This will generate " + str(len(endpoint_table)) + " login attempts. Logging results to ./capcheck_log/" + file_name + ". Continue? [Y/n] \n")
        if answer.lower() == 'y' or answer.lower() == '':
            
            for url in endpoint_table:
                endpoint = url[2]

                if username_list:
                    with open(username_list, 'r') as file:
                        for user in file:
                            username = user.strip()

                            login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
                else:
                    login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy) 
        else:
            exit()
            

    else:
        # No BF
        answer = input("This will generate 1 login attempt for each user specified. Logging results to ./capcheck_log/" + file_name + ". Continue? [Y/n]")
        if answer.lower() == 'y' or answer.lower() == '':
            
            if username_list:
                with open(username_list, 'r') as file:
                    for user in file:
                        username = user.strip()
                        
                        login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
            else:
                login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy)
        else:
            exit()

    print("Finished login attempts.")

    if successful_results:
        print("\nSummary of Successful Results")
        print("-" * 80)
        for entry in successful_results:
            print(f"Username:     {entry['username']}")
            print(f"Endpoint:     {entry['endpoint']}")
            print(f"ClientID:     {entry['clientid_name']} ({entry['clientid']})")
            print(f"User-Agent:   {entry['user_agent']}")
            if entry.get("scope"):
                print(f"Scope:        {entry['scope']}")
            print("-" * 80)
    else:
        print("\nNo successful logins were detected.")

    if scope_list:
        print("\nThe tokens we obtained have the following scopes.")
        print("-------------------------------------------------")
        for entry in scope_list:
            print(entry["clientid"] + " - " + entry["resource"] + " - " + entry["scope"])

def login(file_name, username, password, endpoint, client_id, user_agent, user_agent_name, proxy=None):
    Path("./capcheck_log").mkdir(parents=True, exist_ok=True)

    validation_log = open("./capcheck_log/" + file_name, "a")
    current_date_time = datetime.datetime.now()
    time = current_date_time.strftime("%m/%d/%y %X")

    proxies = {"http": proxy, "https": proxy}

    url = 'https://login.microsoftonline.com'

    body = {
        'resource': endpoint,
        'client_id': client_id,
        'client_info': '1',
        'grant_type': 'password',
        'username': username,
        'scope': 'openid',
    }

    encoded_password = password.replace("%", "%25")

    body_string = "&".join(f"{key}={requests.utils.quote(str(value))}" for key, value in body.items())
    body_string += f"&password={encoded_password}"

    headers = {
        'Accept': 'application/json',
        'User-Agent': user_agent,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    r = requests.post(f"{url}/common/oauth2/token", headers=headers, data=body_string, proxies=proxies, verify=False)
    json_response = json.loads(r.text)

    clientid_name = get_clientid_name(client_id)

    if r.status_code == 200:
        result = ('\033[32m' + f'Successful login | {username} | {endpoint} | {clientid_name} ({client_id}) | {user_agent_name}' + '\033[39m')
        print(result)

        successful_results.append({
            "username": username,
            "endpoint": endpoint,
            "clientid": client_id,
            "clientid_name": clientid_name,
            "user_agent": user_agent_name,
            "scope": json_response.get("scope", "")
        })

    elif r.status_code == 400:
        error_code = json_response.get('error_codes', [])

        if 50076 in error_code:
            result = ("Success: MFA Required" + f" | {username} | {endpoint} | {clientid_name} ({client_id}) | {user_agent_name}")

        elif 50079 in error_code:
            result = ('\033[32m' + "Success: MFA Setup Required" + f" | {username} | {endpoint} | {clientid_name} ({client_id}) | {user_agent_name}" + '\033[39m')
        elif 50158 in error_code:
            result = ("\033[33m" + "Probable Success: External security challenge" + f" | {username} | {endpoint} | {clientid_name} ({client_id}) | {user_agent_name}" + "\033[39m")
        elif 53003 in error_code:
            result = ("\033[33m" + "Probable Success: Blocked by conditional access policies." + f" | {username} | {endpoint} | {clientid_name} ({client_id}) | {user_agent_name}" + "\033[39m")
        elif 50053 in error_code:
            result = ("\033[31m" + "Success: Account Locked" + f" | {username} | {endpoint} | {clientid_name} ({client_id}) | {user_agent_name}" + "\033[39m")
        elif 50057 in error_code:
            result = ("\033[31m" + "Success: Account Disabled" + f" | {username} | {endpoint} | {clientid_name} ({client_id}) | {user_agent_name}" + "\033[39m")
        else:
            if error_code:
                result = ("\033[33m" + "Unsupported error code: " + str(error_code) + f" | {username} | {endpoint} | {clientid_name} ({client_id}) | {user_agent_name}" + "\033[39m")
            else:
                result = "Unknown error."

        print(result)

    elif r.status_code == 401:
        error_code = json_response.get('error_codes', [])
        result = ("\033[33m" + "Unauthorized: " + str(error_code) + f" | {username} | {endpoint} | {clientid_name} ({client_id}) | {user_agent_name}" + "\033[39m")
        print(result)

    else:
        result = ("\033[31m" + "Failed to connect." + f" | {username} | {endpoint} | {clientid_name} ({client_id}) | {user_agent_name}" + "\033[39m")
        print(result)

    validation_log.write("Time: " + time + "\n" + "Username: " + username + "\n" + "Endpoint: " + endpoint + "\n" + "Client ID: " + client_id + "\n" + "User-Agent: " + user_agent + "\n\n")
    validation_log.write(r.text + "\n\n\n")
    validation_log.close()

if __name__ == "__main__":
    main()
