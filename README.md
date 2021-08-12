# Meraki-Disconnect-VLAN-from-VPN

With this code you can monitor the status of the main link (WAN 1) in a Meraki MX, and in case of failure of this link, "automagically" stop announcing a certain VLAN over the SD-WAN, for example a VLAN that consumes a lot of bandwidth, like the one used for CCTV, Voice, etc.

Great to use when your secondary link is Satellite or Cellular, and you want to avoid large charges for passing not critical traffic for the business over Meraki SD-WAN.
