#pylint: skip-file
errorinfo='''
 * opkg_install_cmd: Cannot install package adblock.
 * opkg_install_cmd: Cannot install package ath10k-firmware-qca6174.
 * opkg_install_cmd: Cannot install package ath10k-firmware-qca988x.
 * opkg_install_cmd: Cannot install package ath10k-firmware-qca99x0.
 * opkg_install_cmd: Cannot install package ath9k-htc-firmware.
 * opkg_install_cmd: Cannot install package b43legacy-firmware.
 * opkg_install_cmd: Cannot install package brcmfmac-firmware-pcie.
 * opkg_install_cmd: Cannot install package brcmfmac-firmware-sdio.
 * opkg_install_cmd: Cannot install package brcmfmac-firmware-usb.
 * opkg_install_cmd: Cannot install package carl9170-firmware.
 * opkg_install_cmd: Cannot install package iwl3945-firmware.
 * opkg_install_cmd: Cannot install package iwl4965-firmware.
 * opkg_install_cmd: Cannot install package iwlwifi-firmware.
 * opkg_install_cmd: Cannot install package kmod-hermes.
 * opkg_install_cmd: Cannot install package kmod-hermes-pci.
 * opkg_install_cmd: Cannot install package kmod-hermes-plx.
 * opkg_install_cmd: Cannot install package kmod-ipt-debug.
 * opkg_install_cmd: Cannot install package kmod-ipw2100.
 * opkg_install_cmd: Cannot install package kmod-ipw2200.
 * opkg_install_cmd: Cannot install package kmod-iwlwifi.
 * opkg_install_cmd: Cannot install package kmod-libertas-spi.
 * opkg_install_cmd: Cannot install package kmod-libipw.
 * opkg_install_cmd: Cannot install package kmod-mt7601u.
 * opkg_install_cmd: Cannot install package kmod-rtl8xxxu.
 * opkg_install_cmd: Cannot install package libertas-sdio-firmware.
 * opkg_install_cmd: Cannot install package libertas-spi-firmware.
 * opkg_install_cmd: Cannot install package libertas-usb-firmware.
 * opkg_install_cmd: Cannot install package logd.
 * opkg_install_cmd: Cannot install package luci-app-adblock.
 * opkg_install_cmd: Cannot install package luci-app-aria2.
 * opkg_install_cmd: Cannot install package luci-app-syncdial.
 * opkg_install_cmd: Cannot install package luci-theme-amazeui.
 * opkg_install_cmd: Cannot install package luci-theme-atmaterial.
 * opkg_install_cmd: Cannot install package luci-theme-openwrtcn.
 * opkg_install_cmd: Cannot install package luci-theme-oxygen.
 * opkg_install_cmd: Cannot install package luci-theme-xeye.
 * opkg_install_cmd: Cannot install package mt7601u-firmware.
 * opkg_install_cmd: Cannot install package mwifiex-pcie-firmware.
 * opkg_install_cmd: Cannot install package mwl8k-firmware.
 * opkg_install_cmd: Cannot install package rt2800-pci-firmware.
 * opkg_install_cmd: Cannot install package rt2800-usb-firmware.
 * opkg_install_cmd: Cannot install package rt61-pci-firmware.
 * opkg_install_cmd: Cannot install package rt73-usb-firmware.
 * opkg_install_cmd: Cannot install package rtl8192ce-firmware.
 * opkg_install_cmd: Cannot install package rtl8192cu-firmware.
 * opkg_install_cmd: Cannot install package rtl8192de-firmware.
 * opkg_install_cmd: Cannot install package yaaw.
'''
packages='''adblock ahcpd ar aria2 ath10k-firmware-qca6174 ath10k-firmware-qca988x ath10k-firmware-qca99x0 ath9k-htc-firmware b43legacy-firmware base-files block-mount brcmfmac-firmware-pcie brcmfmac-firmware-sdio brcmfmac-firmware-usb bridge busybox bzip2 ca-certificates carl9170-firmware certtool coreutils coreutils-chroot coreutils-sha1sum ddns-scripts debootstrap dnsmasq dropbear ead firewall freifunk-common freifunk-firewall freifunk-gwcheck freifunk-mapupdate freifunk-watchdog fstools gnutls-utils horst hostapd hostapd-common hostapd-common-old hostapd-utils htop iftop ip ip6tables ip6tables-extra ip6tables-mod-nat iperf iperf3 ipset iptables iptables-mod-conntrack-extra iptables-mod-ipopt iptables-mod-nat-extra iw iwl3945-firmware iwl4965-firmware iwlwifi-firmware jshn jsonfilter kernel kmod-3c59x kmod-8139too kmod-adm8211 kmod-arptables kmod-ath kmod-ath10k kmod-ath5k kmod-ath9k kmod-ath9k-common kmod-ath9k-htc kmod-b43 kmod-b43legacy kmod-bcma kmod-brcmfmac kmod-brcmsmac kmod-brcmutil kmod-bridge kmod-carl9170 kmod-cfg80211 kmod-crypto-arc4 kmod-crypto-core kmod-crypto-hash kmod-crypto-michael-mic kmod-e100 kmod-e1000 kmod-ebtables kmod-ebtables-ipv4 kmod-ebtables-ipv6 kmod-ebtables-watchers kmod-eeprom-93cx6 kmod-hermes kmod-hermes-pci kmod-hermes-plx kmod-hid kmod-hid-generic kmod-hostap kmod-hostap-pci kmod-hostap-plx kmod-hwmon-core kmod-ifb kmod-input-core kmod-input-evdev kmod-ip6tables kmod-ip6tables-extra kmod-ipt-account kmod-ipt-chaos kmod-ipt-cluster kmod-ipt-clusterip kmod-ipt-compat-xtables kmod-ipt-condition kmod-ipt-conntrack kmod-ipt-conntrack-extra kmod-ipt-core kmod-ipt-debug kmod-ipt-delude kmod-ipt-dhcpmac kmod-ipt-dnetmap kmod-ipt-extra kmod-ipt-filter kmod-ipt-fuzzy kmod-ipt-geoip kmod-ipt-hashlimit kmod-ipt-iface kmod-ipt-ipmark kmod-ipt-ipopt kmod-ipt-ipp2p kmod-ipt-iprange kmod-ipt-ipsec kmod-ipt-ipset kmod-ipt-ipv4options kmod-ipt-led kmod-ipt-length2 kmod-ipt-logmark kmod-ipt-lscan kmod-ipt-lua kmod-ipt-nat kmod-ipt-nat-extra kmod-ipt-nat6 kmod-ipt-nathelper-rtsp kmod-ipt-nflog kmod-ipt-nfqueue kmod-ipt-psd kmod-ipt-quota2 kmod-ipt-sysrq kmod-ipt-tarpit kmod-ipt-tee kmod-ipt-tproxy kmod-ipt-u32 kmod-ipt-ulog kmod-ipv6 kmod-ipw2100 kmod-ipw2200 kmod-iwl-legacy kmod-iwl3945 kmod-iwl4965 kmod-iwlwifi kmod-lib-cordic kmod-lib-crc-ccitt kmod-lib-crc-itu-t kmod-lib-crc8 kmod-lib-textsearch kmod-lib80211 kmod-libertas-sdio kmod-libertas-spi kmod-libertas-usb kmod-libipw kmod-libphy kmod-llc kmod-mac80211 kmod-mac80211-hwsim kmod-macvlan kmod-mii kmod-mmc kmod-mppe kmod-mt76 kmod-mt7601u kmod-mwifiex-pcie kmod-mwl8k kmod-natsemi kmod-ne2k-pci kmod-net-airo kmod-net-prism54 kmod-net-rtl8188eu kmod-net-rtl8192su kmod-nf-conntrack kmod-nf-conntrack-netlink kmod-nf-conntrack6 kmod-nf-ipt kmod-nf-ipt6 kmod-nf-nat kmod-nf-nat6 kmod-nf-nathelper kmod-nf-nathelper-extra kmod-nfnetlink kmod-nfnetlink-log kmod-nfnetlink-queue kmod-nft-core kmod-nft-nat kmod-nft-nat6 kmod-nls-base kmod-nls-utf8 kmod-p54-common kmod-p54-pci kmod-p54-usb kmod-pcnet32 kmod-ppp kmod-pppoe kmod-pppox kmod-pps kmod-ptp kmod-r8169 kmod-rt2400-pci kmod-rt2500-pci kmod-rt2500-usb kmod-rt2800-lib kmod-rt2800-mmio kmod-rt2800-pci kmod-rt2800-usb kmod-rt2x00-lib kmod-rt2x00-mmio kmod-rt2x00-pci kmod-rt2x00-usb kmod-rt61-pci kmod-rt73-usb kmod-rtl8180 kmod-rtl8187 kmod-rtl8192c-common kmod-rtl8192ce kmod-rtl8192cu kmod-rtl8192de kmod-rtl8192se kmod-rtl8xxxu kmod-rtlwifi kmod-rtlwifi-pci kmod-rtlwifi-usb kmod-sched kmod-sched-connmark kmod-sched-core kmod-scsi-core kmod-scsi-generic kmod-sis900 kmod-slhc kmod-ssb kmod-stp kmod-tg3 kmod-tun kmod-usb-acm kmod-usb-core kmod-usb-hid kmod-usb-ohci kmod-usb-ohci-pci kmod-usb-storage kmod-usb-storage-extras kmod-usb-uhci kmod-usb2 kmod-usb2-pci kmod-usb3 kmod-via-rhine kmod-via-velocity kmod-zd1211rw libbfd libblobmsg-json libbz2 libc libcurl libertas-sdio-firmware libertas-spi-firmware libertas-usb-firmware libevent2 libgcc libgmp libgnutls libip4tc libip6tc libiwinfo libiwinfo-lua libjson-c libjson-script liblua liblzo libmnl libncurses libnettle libnl-tiny libopenssl libpcap libpcre libpolarssl libpthread librt libsensors libstdcpp libsysfs libubox libubus libubus-lua libuci libuci-lua libustream-polarssl libxml2 libxtables lm-sensors lm-sensors-detect logd lua luci luci-app-adblock luci-app-ahcp luci-app-aria2 luci-app-ddns luci-app-firewall luci-app-mwan3 luci-app-olsr luci-app-olsr-services luci-app-openvpn luci-app-qos luci-app-samba luci-app-splash luci-app-syncdial luci-app-tinyproxy luci-app-transmission luci-base luci-lib-ip luci-lib-json luci-lib-luaneightbl luci-lib-nixio luci-mod-admin-full luci-mod-rpc luci-proto-ipv6 luci-proto-openconnect luci-proto-ppp luci-ssl luci-theme-amazeui luci-theme-atmaterial luci-theme-bootstrap luci-theme-freifunk-bno luci-theme-freifunk-generic luci-theme-openwrt luci-theme-openwrtcn luci-theme-oxygen luci-theme-xeye mt7601u-firmware mtd mwan3 mwifiex-pcie-firmware mwl8k-firmware nano netifd odhcp6c odhcpd olsrd olsrd-mod-dyn-gw-plain olsrd-mod-jsoninfo olsrd-mod-nameservice olsrd-mod-watchdog openconnect openvpn-openssl opkg perl perlbase-base perlbase-bytes perlbase-class perlbase-config perlbase-cwd perlbase-errno perlbase-essential perlbase-fcntl perlbase-file perlbase-filehandle perlbase-i18n perlbase-integer perlbase-io perlbase-list perlbase-locale perlbase-params perlbase-posix perlbase-re perlbase-scalar perlbase-selectsaver perlbase-socket perlbase-symbol perlbase-tie perlbase-utf8 perlbase-xsloader ppp ppp-mod-pppoe pptpd procd px5g qos-scripts r8169-firmware r8188eu-firmware resolveip rpcd rt2800-pci-firmware rt2800-usb-firmware rt61-pci-firmware rt73-usb-firmware rtl8192ce-firmware rtl8192cu-firmware rtl8192de-firmware samba36-server sudo sysfsutils tc terminfo tinyproxy transmission-daemon ubox ubus ubusd uci uclibcxx udev uhttpd uhttpd-mod-ubus usign vpnc-scripts vsftpd vsftpd-tls wavemon wget wireless-tools yaaw zlib'''
makeprefix = "make image PROFILE=Generic PACKAGES="
packages_array=[]
packages_array_out=list(packages.split(' '))
packages_out=""
for l in errorinfo.split('\n'):
    packages_array.append(l.split(' ')[-1][:-1])

for elem in packages.split(' '):
    if elem in packages_array:
        packages_array_out.remove(elem)
for elem in packages_array_out:
    packages_out +=  " "+elem        
print(makeprefix+' " '+packages_out+'"',file=open("a.txt","wt"))