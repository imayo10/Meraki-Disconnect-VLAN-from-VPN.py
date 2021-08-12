import time
import meraki
import credentials

dashboard = meraki.DashboardAPI(credentials.api_key)

i = True
# Ask for the status of all the links in the organization
while i == True:
    links = dashboard.organizations.getOrganizationUplinksStatuses(organizationId="XXXXXXXXXXXX")
    for network in links:
        try:
#Choose a specific network that you want to monitor
            if network['networkId']=='XXXXXXXXXXXXXXXXXX':
                for uplinks in network['uplinks']:
                    print(network['uplinks'])
                    if uplinks['interface']=='wan1' and uplinks['status']=='active':
                        #print(network)
                        print("Enlace Primario activo")
                        vpn = dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(networkId=network['networkId'])
                        for subnet in vpn['subnets']:
                        # --Change all the 192.168.241.0/24 showed in the script to the subnet that you want to disconnect from vpn in case of failure --
                            if subnet['localSubnet'] == '192.168.241.0/24' and subnet['useVpn'] == False:
                                subnet['useVpn'] = True
                                del vpn['mode']
                                #print(vpn)
                                print("CHANGE - Reconnecting voice subnet, main uplink goes up ")
                                update = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
                                    networkId=network['networkId'], mode='spoke', **vpn)
                            elif subnet['localSubnet'] == '192.168.241.0/24' and subnet['useVpn'] == True:
                                print("Main link is active, voice vlan is on VPN")
                    #In case of failure of the WAN1 link, the subnet will be disconnected from the VPN.
                    elif uplinks['interface']=='wan1' and uplinks['status']=='not connected' or uplinks['status']=='failed':
                        #print(network)
                        print("Enlace principal esta caido")
                        vpn = dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(networkId=network['networkId'])
                        #print(vpn)
                        for subnet in vpn['subnets']:
                            if subnet['localSubnet']=='192.168.241.0/24' and subnet['useVpn']==True:
                                subnet['useVpn']=False
                                del vpn['mode']
                                #print(vpn)
                                print("CHANGE - Disconnecting voice vlan from VPN, main link is down")
                                update = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(networkId=network['networkId'], mode='spoke', **vpn)
                            elif subnet['localSubnet'] == '192.168.241.0/24' and subnet['useVpn'] == False:
                                print("Main link is down, voice vlan is disconnected of the VPN.")
        except TypeError as e:
            print(e)
        except meraki.APIError as e:
            print(e)
    time.sleep(5)
