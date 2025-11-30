#!/bin/bash

#
# DaVinci Resolve Multi Debian package creator
# Release 2025-08-11
# By Daniel Tufvesson
#
MAKERESOLVEDEB_VERSION=1.8.3

check_command() {
    echo -n "Checking for ${1}..."
    if [[ ! -x $(command -v "${1}") ]]; then
	echo "Missing! Sorry, need '$1' to continue."
	exit 1
    fi
    echo "found!"
}

copy_object() {
    if [[ -e "${1}" ]]; then
	if ! cp -rp "$1" "$2"; then
	    ERRORS=$((ERRORS+1))
	fi
    else
	echo "[ERROR: MISSING] $1"
	ERRORS=$((ERRORS+1))
    fi
}

assert_object() {
    if [[ ! -e "${1}" ]]; then
	echo "[ERROR: MISSING] $1"
	ERRORS=$((ERRORS+1))
    fi
}

link_object() {
    if [[ -e "${2}" ]]; then
	echo "[ERROR: LINK ALREADY EXISTS] $2"
	ERRORS=$((ERRORS+1))
    else
	if ! ln -s "${1}" "${2}"; then
	    echo "[ERROR: UNABLE TO CREATE LINK] $2 -> $1"
	    ERRORS=$((ERRORS+1))
	fi
    fi
}

create_directory() {
    if [[ -e "${1}" ]]; then
	echo "[ERROR: DIRECTORY ALREADY EXISTS] $1"
	ERRORS=$((ERRORS+1))
    else
	mkdir -p "${1}"
	chmod 755 "${1}"
    fi
    if [[ ! -w "${1}" ]]; then
	echo "[ERROR: DIRECTORY NOT WRITABLE] $1"
	ERRORS=$((ERRORS+1))
    fi
}

createf_directory() {
    if [[ -e "${1}" ]]; then
	chmod a+w -R "${1}"
	rm -rf "${1}"
    fi
    if [[ -e "${1}" ]]; then
	echo "[ERROR: UNABLE TO REPLACE DIRECTORY] $1"
	ERRORS=$((ERRORS+1))	
    fi
    create_directory "${1}"
}

creates_directory() {
    if [[ ! -e "${1}" ]]; then
	create_directory "${1}"
    fi
}

remove_directory() {
    if [[ -e "${1}" ]]; then
	chmod a+w -R "${1}"
	rm -rf "${1}"
    else
	echo "[ERROR: MISSING] $1"
	ERRORS=$((ERRORS+1))
    fi
}

extract_tgz() {
    if [[ -f "${1}" ]]; then
	tar -zxf "${1}" -C "${2}" "${3}"
    else
	echo "[ERROR: MISSING] $1"
	ERRORS=$((ERRORS+1))
    fi
}

init_deb() {
    if [[ -z "$MAINTAINER" ]]; then
	MAINTAINER=$(whoami)@$(hostname)
    fi
    create_directory "${DEB_DIR}"/DEBIAN
    cat > "${DEB_DIR}"/DEBIAN/control <<EOF
Package: ${DEB_NAME}
Version: ${DEB_VERSION}
Section: video
Priority: optional
Architecture: amd64
Maintainer: ${MAINTAINER}
Description: ${RESOLVE_NAME} made from ${INSTALLER_ARCHIVE} using MakeResolveDeb ${MAKERESOLVEDEB_VERSION}
Conflicts: ${DEB_CONFLICTS}
EOF
    echo "#!/bin/sh" > "${DEB_DIR}"/DEBIAN/postinst
    echo "#!/bin/sh" > "${DEB_DIR}"/DEBIAN/postrm
    create_directory "${DEB_DIR}"/usr/share/applications
    create_directory "${DEB_DIR}"/usr/share/mime/packages
}

close_deb() {
    chmod 644 "${DEB_DIR}"/DEBIAN/control
    echo "exit 0" >> "${DEB_DIR}"/DEBIAN/postinst
    chmod 755 "${DEB_DIR}"/DEBIAN/postinst
    echo "exit 0" >> "${DEB_DIR}"/DEBIAN/postrm
    chmod 755 "${DEB_DIR}"/DEBIAN/postrm
}

process_15() {
    # Create directories
    create_directory "${RESOLVE_BASE_DIR}"/configs
    create_directory "${RESOLVE_BASE_DIR}"/easyDCP
    create_directory "${RESOLVE_BASE_DIR}"/logs
    create_directory "${RESOLVE_BASE_DIR}"/scripts
    create_directory "${RESOLVE_BASE_DIR}"/.LUT
    create_directory "${RESOLVE_BASE_DIR}"/.license
    create_directory "${RESOLVE_BASE_DIR}"/.crashreport
    create_directory "${RESOLVE_BASE_DIR}"/DolbyVision
    create_directory "${RESOLVE_BASE_DIR}"/Fairlight
    create_directory "${RESOLVE_BASE_DIR}"/Media
    create_directory "${RESOLVE_BASE_DIR}"/"Resolve Disk Database"

    # Copy objects
    copy_object "${UNPACK_DIR}"/bin "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Control "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/DaVinci\ Resolve\ Panels\ Setup "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Developer "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/docs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Fusion "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/graphics "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/libs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/LUT "${RESOLVE_BASE_DIR}"
    if [[ -z "$SKIP_ONBOARDING" ]]; then
	copy_object "${UNPACK_DIR}"/Onboarding "${RESOLVE_BASE_DIR}"
    fi
    copy_object "${UNPACK_DIR}"/plugins "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/UI_Resource "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/scripts/script.checkfirmware "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.getlogs.v4 "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.start "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/share/default-config-linux.dat "${RESOLVE_BASE_DIR}"/configs/config.dat-pkg-default
    copy_object "${UNPACK_DIR}"/share/log-conf.xml "${RESOLVE_BASE_DIR}"/configs/log-conf.xml-pkg-default
    copy_object "${UNPACK_DIR}"/share/default_cm_config.bin "${RESOLVE_BASE_DIR}"/DolbyVision/config.bin-pkg-default
    copy_object "${UNPACK_DIR}"/libs/libBlackmagicRawAPI.so "${RESOLVE_BASE_DIR}"/bin/

    # Install panel API library
    create_directory "${DEB_DIR}"/usr/lib/
    extract_tgz "${UNPACK_DIR}"/share/panels/dvpanel-framework-linux-x86_64.tgz "${DEB_DIR}"/usr/lib/ libDaVinciPanelAPI.so

    # Add postinst commands
    cat >> "${DEB_DIR}"/DEBIAN/postinst <<EOF
test -e /opt/resolve/configs/config.dat || cp /opt/resolve/configs/config.dat-pkg-default /opt/resolve/configs/config.dat
test -e /opt/resolve/configs/log-conf.xml || cp /opt/resolve/configs/log-conf.xml-pkg-default /opt/resolve/configs/log-conf.xml
test -e /opt/resolve/DolbyVision/config.bin || cp /opt/resolve/DolbyVision/config.bin-pkg-default /opt/resolve/DolbyVision/config.bin
chmod -R a+rw /opt/resolve/configs
chmod -R a+rw /opt/resolve/easyDCP
chmod -R a+rw /opt/resolve/logs
chmod -R a+rw /opt/resolve/Developer
chmod -R a+rw /opt/resolve/DolbyVision
chmod -R a+rw /opt/resolve/LUT
chmod -R a+rw /opt/resolve/.LUT
chmod -R a+rw /opt/resolve/.license
chmod -R a+rw /opt/resolve/.crashreport
chmod -R a+rw /opt/resolve/"Resolve Disk Database"
chmod -R a+rw /opt/resolve/Fairlight
chmod -R a+rw /opt/resolve/Media
EOF
}

process_16() {
    # Create directories
    create_directory "${RESOLVE_BASE_DIR}"/easyDCP
    create_directory "${RESOLVE_BASE_DIR}"/scripts
    create_directory "${RESOLVE_BASE_DIR}"/.license
    create_directory "${RESOLVE_BASE_DIR}"/share
    create_directory "${RESOLVE_BASE_DIR}"/Fairlight

    # Copy objects
    copy_object "${UNPACK_DIR}"/bin "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Control "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/DaVinci\ Resolve\ Panels\ Setup "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Developer "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/docs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Fusion "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/graphics "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/libs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/LUT "${RESOLVE_BASE_DIR}"
    if [[ -z "$SKIP_ONBOARDING" ]]; then
	copy_object "${UNPACK_DIR}"/Onboarding "${RESOLVE_BASE_DIR}"
    fi
    copy_object "${UNPACK_DIR}"/plugins "${RESOLVE_BASE_DIR}"
    if [[ ! "$RESOLVE_VERSION" == 16.0b* ]]; then
	copy_object "${UNPACK_DIR}"/Technical\ Documentation "${RESOLVE_BASE_DIR}"
    fi
    copy_object "${UNPACK_DIR}"/UI_Resource "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/scripts/script.checkfirmware "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.getlogs.v4 "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.start "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/share/default-config.dat "${RESOLVE_BASE_DIR}"/share/
    copy_object "${UNPACK_DIR}"/share/log-conf.xml "${RESOLVE_BASE_DIR}"/share/
    copy_object "${UNPACK_DIR}"/share/default_cm_config.bin "${RESOLVE_BASE_DIR}"/share/

    # Extract panel API library
    create_directory "${DEB_DIR}"/usr/lib
    extract_tgz "${UNPACK_DIR}"/share/panels/dvpanel-framework-linux-x86_64.tgz "${DEB_DIR}"/usr/lib libDaVinciPanelAPI.so

    # BlackmagicRawAPI fixes
    create_directory "${RESOLVE_BASE_DIR}"/bin/BlackmagicRawAPI/
    link_object ../libs/libBlackmagicRawAPI.so "${RESOLVE_BASE_DIR}"/bin/libBlackmagicRawAPI.so
    link_object ../../libs/libBlackmagicRawAPI.so "${RESOLVE_BASE_DIR}"/bin/BlackmagicRawAPI/libBlackmagicRawAPI.so

    # Create common data dir
    create_directory "${DEB_DIR}"/var/BlackmagicDesign/DaVinci\ Resolve

    # Add postinst commands
    cat >> "${DEB_DIR}"/DEBIAN/postinst <<EOF
chmod -R a+rw /opt/resolve/easyDCP
chmod -R a+rw /opt/resolve/LUT
chmod -R a+rw /opt/resolve/.license
chmod -R a+rw /opt/resolve/Fairlight
chmod -R a+rw /var/BlackmagicDesign/"DaVinci Resolve"
EOF
    
    # libcudafix for Resolve 16.0 & 16.1
    if [[ "$RESOLVE_VERSION" == 16.0* ]] || [[ "$RESOLVE_VERSION" == 16.1* ]];
    then
	echo "Implementing libcudafix"
	echo "test ! -e /usr/lib64 && mkdir /usr/lib64 && touch /usr/lib64.by.makeresolvedeb" >> "${DEB_DIR}"/DEBIAN/postinst
	echo "test ! -h /usr/lib64/libcuda.so && ln -s /usr/lib/x86_64-linux-gnu/libcuda.so /usr/lib64/libcuda.so && touch /usr/lib64/libcuda.so.by.makeresolvedeb" >> "${DEB_DIR}"/DEBIAN/postinst
	echo "test -e /usr/lib64/libcuda.so.by.makeresolvedeb && rm /usr/lib64/libcuda.so && rm /usr/lib64/libcuda.so.by.makeresolvedeb" >> "${DEB_DIR}"/DEBIAN/postrm
	echo "test -e /usr/lib64.by.makeresolvedeb && rmdir /usr/lib64 && rm /usr/lib64.by.makeresolvedeb" >> "${DEB_DIR}"/DEBIAN/postrm
    fi
}

process_17() {
    # Create directories
    create_directory "${RESOLVE_BASE_DIR}"/easyDCP
    create_directory "${RESOLVE_BASE_DIR}"/scripts
    create_directory "${RESOLVE_BASE_DIR}"/.license
    create_directory "${RESOLVE_BASE_DIR}"/share
    create_directory "${RESOLVE_BASE_DIR}"/Fairlight

    # Copy objects
    copy_object "${UNPACK_DIR}"/bin "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Control "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/DaVinci\ Control\ Panels\ Setup "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Developer "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/docs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Fusion "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/graphics "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/libs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/LUT "${RESOLVE_BASE_DIR}"
    if [[ -z "$SKIP_ONBOARDING" ]]; then
	copy_object "${UNPACK_DIR}"/Onboarding "${RESOLVE_BASE_DIR}"
    fi
    copy_object "${UNPACK_DIR}"/plugins "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Technical\ Documentation "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/UI_Resource "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/scripts/script.checkfirmware "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.getlogs.v4 "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.start "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/share/default-config.dat "${RESOLVE_BASE_DIR}"/share/
    copy_object "${UNPACK_DIR}"/share/log-conf.xml "${RESOLVE_BASE_DIR}"/share/
    copy_object "${UNPACK_DIR}"/share/default_cm_config.bin "${RESOLVE_BASE_DIR}"/share/

    # Extract panel API library
    create_directory "${DEB_DIR}"/usr/lib
    extract_tgz "${UNPACK_DIR}"/share/panels/dvpanel-framework-linux-x86_64.tgz "${DEB_DIR}"/usr/lib libDaVinciPanelAPI.so
    extract_tgz "${UNPACK_DIR}"/share/panels/dvpanel-framework-linux-x86_64.tgz "${DEB_DIR}"/usr/lib libFairlightPanelAPI.so

    # BlackmagicRawAPI fixes for 17.0 & 17.1
    if [[ "$RESOLVE_VERSION" == 17.0* ]] || [[ "$RESOLVE_VERSION" == 17.1* ]];
    then
	create_directory "${RESOLVE_BASE_DIR}"/bin/BlackmagicRawAPI/
	link_object ../libs/libBlackmagicRawAPI.so "${RESOLVE_BASE_DIR}"/bin/libBlackmagicRawAPI.so
	link_object ../../libs/libBlackmagicRawAPI.so "${RESOLVE_BASE_DIR}"/bin/BlackmagicRawAPI/libBlackmagicRawAPI.so
    fi

    # Create common data dir
    create_directory "${DEB_DIR}"/var/BlackmagicDesign/DaVinci\ Resolve

    # Add postinst commands
    cat >> "${DEB_DIR}"/DEBIAN/postinst <<EOF
chmod -R a+rw /opt/resolve/easyDCP
chmod -R a+rw /opt/resolve/LUT
chmod -R a+rw /opt/resolve/.license
chmod -R a+rw /opt/resolve/Fairlight
chmod -R a+rw /var/BlackmagicDesign/"DaVinci Resolve"
EOF
}

process_18() {
    # Create directories
    create_directory "${RESOLVE_BASE_DIR}"/easyDCP
    create_directory "${RESOLVE_BASE_DIR}"/scripts
    create_directory "${RESOLVE_BASE_DIR}"/.license
    create_directory "${RESOLVE_BASE_DIR}"/share
    create_directory "${RESOLVE_BASE_DIR}"/Fairlight

    # Copy objects
    copy_object "${UNPACK_DIR}"/bin "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Control "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Certificates "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/DaVinci\ Control\ Panels\ Setup "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Developer "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/docs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Fairlight\ Studio\ Utility "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Fusion "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/graphics "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/libs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/LUT "${RESOLVE_BASE_DIR}"
    if [[ -z "$SKIP_ONBOARDING" ]]; then
	copy_object "${UNPACK_DIR}"/Onboarding "${RESOLVE_BASE_DIR}"
    fi
    copy_object "${UNPACK_DIR}"/plugins "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Technical\ Documentation "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/UI_Resource "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/scripts/script.checkfirmware "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.getlogs.v4 "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.start "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/share/default-config.dat "${RESOLVE_BASE_DIR}"/share/
    copy_object "${UNPACK_DIR}"/share/default_cm_config.bin "${RESOLVE_BASE_DIR}"/share/
    copy_object "${UNPACK_DIR}"/share/log-conf.xml "${RESOLVE_BASE_DIR}"/share/
    if [[ -e "${UNPACK_DIR}"/share/remote-monitoring-log-conf.xml ]]; then
	copy_object "${UNPACK_DIR}"/share/remote-monitoring-log-conf.xml "${RESOLVE_BASE_DIR}"/share/
    fi
    
    # Extract panel API library
    create_directory "${DEB_DIR}"/usr/lib
    extract_tgz "${UNPACK_DIR}"/share/panels/dvpanel-framework-linux-x86_64.tgz "${DEB_DIR}"/usr/lib libDaVinciPanelAPI.so
    extract_tgz "${UNPACK_DIR}"/share/panels/dvpanel-framework-linux-x86_64.tgz "${DEB_DIR}"/usr/lib libFairlightPanelAPI.so

    # Create common data dir
    create_directory "${DEB_DIR}"/var/BlackmagicDesign/DaVinci\ Resolve

    # Add postinst commands
    cat >> "${DEB_DIR}"/DEBIAN/postinst <<EOF
chmod -R a+rw /opt/resolve/easyDCP
chmod -R a+rw /opt/resolve/LUT
chmod -R a+rw /opt/resolve/.license
chmod -R a+rw /opt/resolve/Fairlight
chmod -R a+rw /var/BlackmagicDesign/"DaVinci Resolve"
EOF
}

process_19() {
    # Create directories
    create_directory "${RESOLVE_BASE_DIR}"/easyDCP
    create_directory "${RESOLVE_BASE_DIR}"/scripts
    create_directory "${RESOLVE_BASE_DIR}"/.license
    create_directory "${RESOLVE_BASE_DIR}"/share
    create_directory "${RESOLVE_BASE_DIR}"/Fairlight

    # Copy objects
    copy_object "${UNPACK_DIR}"/bin "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Control "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Certificates "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/DaVinci\ Control\ Panels\ Setup "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Developer "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/docs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Fairlight\ Studio\ Utility "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Fusion "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/graphics "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/libs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/LUT "${RESOLVE_BASE_DIR}"
    if [[ -z "$SKIP_ONBOARDING" ]]; then
	copy_object "${UNPACK_DIR}"/Onboarding "${RESOLVE_BASE_DIR}"
    fi
    copy_object "${UNPACK_DIR}"/plugins "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Technical\ Documentation "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/UI_Resource "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/scripts/script.checkfirmware "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.getlogs.v4 "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.start "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/share/default-config.dat "${RESOLVE_BASE_DIR}"/share/
    copy_object "${UNPACK_DIR}"/share/default_cm_config.bin "${RESOLVE_BASE_DIR}"/share/
    copy_object "${UNPACK_DIR}"/share/log-conf.xml "${RESOLVE_BASE_DIR}"/share/
    if [[ -e "${UNPACK_DIR}"/share/remote-monitor-log-conf.xml ]]; then
	copy_object "${UNPACK_DIR}"/share/remote-monitor-log-conf.xml "${RESOLVE_BASE_DIR}"/share/
    fi

    # Disable libs
    for lib in "libgio-2.0" "libglib-2.0" "libgobject-2.0" "libgmodule-2.0"; do
	mkdir -p "${RESOLVE_BASE_DIR}"/libs/disabled
	mv "${RESOLVE_BASE_DIR}"/libs/"${lib}"* "${RESOLVE_BASE_DIR}"/libs/disabled/
    done

    # Extract panel API library
    create_directory "${DEB_DIR}"/usr/lib
    extract_tgz "${UNPACK_DIR}"/share/panels/dvpanel-framework-linux-x86_64.tgz "${DEB_DIR}"/usr/lib libDaVinciPanelAPI.so
    extract_tgz "${UNPACK_DIR}"/share/panels/dvpanel-framework-linux-x86_64.tgz "${DEB_DIR}"/usr/lib libFairlightPanelAPI.so

    # Create common data dir
    create_directory "${DEB_DIR}"/var/BlackmagicDesign/DaVinci\ Resolve

    # Add postinst commands
    cat >> "${DEB_DIR}"/DEBIAN/postinst <<EOF
chmod -R a+rw /opt/resolve/easyDCP
chmod -R a+rw /opt/resolve/LUT
chmod -R a+rw /opt/resolve/.license
chmod -R a+rw /opt/resolve/Fairlight
chmod -R a+rw /var/BlackmagicDesign/"DaVinci Resolve"
EOF
}

process_20() {
    # Create directories
    create_directory "${RESOLVE_BASE_DIR}"/easyDCP
    create_directory "${RESOLVE_BASE_DIR}"/scripts
    create_directory "${RESOLVE_BASE_DIR}"/.license
    create_directory "${RESOLVE_BASE_DIR}"/share
    create_directory "${RESOLVE_BASE_DIR}"/Fairlight
    create_directory "${RESOLVE_BASE_DIR}"/Extras
    create_directory "${RESOLVE_BASE_DIR}"/Apple\ Immersive

    # Copy objects
    copy_object "${UNPACK_DIR}"/bin "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Control "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Certificates "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/DaVinci\ Control\ Panels\ Setup "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Developer "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/docs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Fairlight\ Studio\ Utility "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Fusion "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/graphics "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/libs "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/LUT "${RESOLVE_BASE_DIR}"
    if [[ -z "$SKIP_ONBOARDING" ]]; then
	copy_object "${UNPACK_DIR}"/Onboarding "${RESOLVE_BASE_DIR}"
    fi
    copy_object "${UNPACK_DIR}"/plugins "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/Technical\ Documentation "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/UI_Resource "${RESOLVE_BASE_DIR}"
    copy_object "${UNPACK_DIR}"/scripts/script.checkfirmware "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.getlogs.v4 "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/scripts/script.start "${RESOLVE_BASE_DIR}"/scripts/
    copy_object "${UNPACK_DIR}"/share/default-config.dat "${RESOLVE_BASE_DIR}"/share/
    copy_object "${UNPACK_DIR}"/share/default_cm_config.bin "${RESOLVE_BASE_DIR}"/share/
    copy_object "${UNPACK_DIR}"/share/log-conf.xml "${RESOLVE_BASE_DIR}"/share/
    if [[ -e "${UNPACK_DIR}"/share/remote-monitor-log-conf.xml ]]; then
	copy_object "${UNPACK_DIR}"/share/remote-monitor-log-conf.xml "${RESOLVE_BASE_DIR}"/share/
    fi

    # Disable libs
    for lib in "libgio-2.0" "libglib-2.0" "libgobject-2.0" "libgmodule-2.0"; do
	mkdir -p "${RESOLVE_BASE_DIR}"/libs/disabled
	mv "${RESOLVE_BASE_DIR}"/libs/"${lib}"* "${RESOLVE_BASE_DIR}"/libs/disabled/
    done

    # Extract panel API library
    create_directory "${DEB_DIR}"/usr/lib
    extract_tgz "${UNPACK_DIR}"/share/panels/dvpanel-framework-linux-x86_64.tgz "${DEB_DIR}"/usr/lib libDaVinciPanelAPI.so
    extract_tgz "${UNPACK_DIR}"/share/panels/dvpanel-framework-linux-x86_64.tgz "${DEB_DIR}"/usr/lib libFairlightPanelAPI.so

    # Create common data dir
    create_directory "${DEB_DIR}"/var/BlackmagicDesign/DaVinci\ Resolve

    # Add postinst commands
    cat >> "${DEB_DIR}"/DEBIAN/postinst <<EOF
chmod -R a+rw /opt/resolve/easyDCP
chmod -R a+rw /opt/resolve/LUT
chmod -R a+rw /opt/resolve/.license
chmod -R a+rw /opt/resolve/Fairlight
chmod -R a+rw /var/BlackmagicDesign/"DaVinci Resolve"
chmod -R a+rw /opt/resolve/Extras
chmod -R a+rw /opt/resolve/Apple\ Immersive
EOF
}

process_braw() {
    if [[ -n "$SKIP_BRAW" ]]; then
	return;
    fi
    if [[ -e "${UNPACK_DIR}"/BlackmagicRAWPlayer ]]; then
	echo "Adding BlackmagicRAWPlayer"
	
	copy_object "${UNPACK_DIR}"/BlackmagicRAWPlayer "${RESOLVE_BASE_DIR}"
	
	assert_object "${DEB_DIR}"/opt/resolve/graphics/blackmagicraw-player_256x256_apps.png
	assert_object "${DEB_DIR}"/opt/resolve/BlackmagicRAWPlayer/BlackmagicRAWPlayer
	cat > "${DEB_DIR}"/usr/share/applications/com.blackmagicdesign.rawplayer.desktop <<EOF
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Type=Application
Name=Blackmagic RAW Player
Exec=/opt/resolve/BlackmagicRAWPlayer/BlackmagicRAWPlayer
Icon=/opt/resolve/graphics/blackmagicraw-player_256x256_apps.png
Terminal=false
MimeType=application/x-braw-clip;application/x-braw-sidecar
StartupNotify=true
Categories=AudioVideo
EOF
    fi
    if [[ -e "${UNPACK_DIR}"/BlackmagicRAWSpeedTest ]]; then
	echo "Adding BlackmagicRAWSpeedTest"
	
	copy_object "${UNPACK_DIR}"/BlackmagicRAWSpeedTest "${RESOLVE_BASE_DIR}"
	
	assert_object "${DEB_DIR}"/opt/resolve/graphics/blackmagicraw-speedtest_256x256_apps.png
	assert_object "${DEB_DIR}"/opt/resolve/BlackmagicRAWSpeedTest/BlackmagicRAWSpeedTest
	cat > "${DEB_DIR}"/usr/share/applications/com.blackmagicdesign.rawspeedtest.desktop <<EOF
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Type=Application
Name=Blackmagic RAW Speed Test
Exec=/opt/resolve/BlackmagicRAWSpeedTest/BlackmagicRAWSpeedTest
Icon=/opt/resolve/graphics/blackmagicraw-speedtest_256x256_apps.png
Terminal=false
StartupNotify=true
Categories=AudioVideo
EOF
    fi
    cat > "${DEB_DIR}"/usr/share/mime/packages/blackmagicraw.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="application/x-braw-clip">
         <comment xml:lang="en">Blackmagic RAW Clip</comment>
         <glob pattern="*.braw"/>
  </mime-type>
  <mime-type type="application/x-braw-sidecar">
         <comment xml:lang="en">Blackmagic RAW Sidecar</comment>
         <glob pattern="*.sidecar"/>
  </mime-type>
</mime-info>
EOF
    if [[ -e "${DEB_DIR}"/opt/resolve/graphics/application-x-braw-clip_256x256_mimetypes.png ]]; then
	creates_directory "${DEB_DIR}"/usr/share/icons/hicolor/256x256/mimetypes/
	copy_object "${DEB_DIR}"/opt/resolve/graphics/application-x-braw-clip_256x256_mimetypes.png "${DEB_DIR}"/usr/share/icons/hicolor/256x256/mimetypes/application-x-braw-clip.png
    fi
    if [[ -e "${DEB_DIR}"/opt/resolve/graphics/application-x-braw-sidecar_256x256_mimetypes.png ]]; then
	creates_directory "${DEB_DIR}"/usr/share/icons/hicolor/256x256/mimetypes/
	copy_object "${DEB_DIR}"/opt/resolve/graphics/application-x-braw-sidecar_256x256_mimetypes.png "${DEB_DIR}"/usr/share/icons/hicolor/256x256/mimetypes/application-x-braw-sidecar.png
    fi
    if [[ -e "${DEB_DIR}"/opt/resolve/graphics/application-x-braw-clip_48x48_mimetypes.png ]]; then
	creates_directory "${DEB_DIR}"/usr/share/icons/hicolor/48x48/mimetypes/
	copy_object "${DEB_DIR}"/opt/resolve/graphics/application-x-braw-clip_48x48_mimetypes.png "${DEB_DIR}"/usr/share/icons/hicolor/48x48/mimetypes/application-x-braw-clip.png
    fi
    if [[ -e "${DEB_DIR}"/opt/resolve/graphics/application-x-braw-sidecar_48x48_mimetypes.png ]]; then
	creates_directory "${DEB_DIR}"/usr/share/icons/hicolor/48x48/mimetypes/
	copy_object "${DEB_DIR}"/opt/resolve/graphics/application-x-braw-sidecar_48x48_mimetypes.png "${DEB_DIR}"/usr/share/icons/hicolor/48x48/mimetypes/application-x-braw-sidecar.png
    fi
}

process_udev() {
    # Create udev rules
    create_directory "${DEB_DIR}"/lib/udev/rules.d
    cat > "${DEB_DIR}"/lib/udev/rules.d/75-davincipanel.rules <<EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="1edb", MODE="0666"
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0777", GROUP="resolve"
EOF
    cat > "${DEB_DIR}"/lib/udev/rules.d/75-davincikb.rules <<EOF
SUBSYSTEMS=="usb", ENV{.LOCAL_ifNum}="\$attr{bInterfaceNumber}"
# Editor Keyboard
SUBSYSTEM=="hidraw", KERNEL=="hidraw*", ATTRS{idVendor}=="1edb", ATTRS{idProduct}=="da0b", ENV{.LOCAL_ifNum}=="04", MODE="0666"
# Speed Editor Keyboard
SUBSYSTEM=="hidraw", KERNEL=="hidraw*", ATTRS{idVendor}=="1edb", ATTRS{idProduct}=="da0e", ENV{.LOCAL_ifNum}=="02", MODE="0666"
# Micro Color Panel
SUBSYSTEM=="hidraw", KERNEL=="hidraw*", ATTRS{idVendor}=="1edb", ATTRS{idProduct}=="da0f", ENV{.LOCAL_ifNum}=="00", MODE="0666"
SUBSYSTEM=="hidraw", KERNEL=="hidraw*", ATTRS{idVendor}=="1edb", ATTRS{idProduct}=="da0f", ENV{.LOCAL_ifNum}=="01", MODE="0666"
SUBSYSTEM=="hidraw", KERNEL=="hidraw*", ATTRS{idVendor}=="1edb", ATTRS{idProduct}=="da0f", ENV{.LOCAL_ifNum}=="02", MODE="0666"
SUBSYSTEM=="hidraw", KERNEL=="hidraw*", ATTRS{idVendor}=="1edb", ATTRS{idProduct}=="da0f", ENV{.LOCAL_ifNum}=="03", MODE="0666"
EOF
    cat > "${DEB_DIR}"/lib/udev/rules.d/75-sdx.rules <<EOF
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTRS{idVendor}=="096e", MODE="0666"
EOF
    # Add postinst commands
    cat >> "${DEB_DIR}"/DEBIAN/postinst <<EOF
udevadm control --reload-rules
udevadm trigger
EOF
}

process_desktop_shortcuts() {
    assert_object "${DEB_DIR}"/opt/resolve/graphics/DV_Resolve.png
    cat > "${DEB_DIR}"/usr/share/applications/com.blackmagicdesign.resolve.desktop <<EOF
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Type=Application
Name=${RESOLVE_NAME}
Path=/opt/resolve
Exec=/opt/resolve/bin/resolve
Icon=/opt/resolve/graphics/DV_Resolve.png
Terminal=false
MimeType=application/x-resolveproj;application/x-resolvebin;application/x-resolvetimeline;application/x-resolvetemplatebundle;application/x-resolvedbkey
StartupNotify=true
Categories=AudioVideo
EOF
    if [[ -e "${DEB_DIR}"/"opt/resolve/DaVinci Resolve Panels Setup/DaVinci Resolve Panels Setup" ]]; then
	assert_object "${DEB_DIR}"/opt/resolve/graphics/DV_Panels.png
	cat > "${DEB_DIR}"/usr/share/applications/com.blackmagicdesign.resolve-Panels.desktop <<EOF
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Type=Application
Name=DaVinci Resolve Panels Setup
Path=/opt/resolve
Exec="/opt/resolve/DaVinci Resolve Panels Setup/DaVinci Resolve Panels Setup"
Icon=/opt/resolve/graphics/DV_Panels.png
Terminal=false
StartupNotify=true
Categories=AudioVideo
EOF
    fi
    if [[ -e "${DEB_DIR}"/"opt/resolve/DaVinci Control Panels Setup/DaVinci Control Panels Setup" ]]; then
	assert_object "${DEB_DIR}"/opt/resolve/graphics/DV_Panels.png
	cat > "${DEB_DIR}"/usr/share/applications/com.blackmagicdesign.resolve-Panels.desktop <<EOF
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Type=Application
Name=DaVinci Control Panels Setup
Path=/opt/resolve
Exec="/opt/resolve/DaVinci Control Panels Setup/DaVinci Control Panels Setup"
Icon=/opt/resolve/graphics/DV_Panels.png
Terminal=false
StartupNotify=true
Categories=AudioVideo
EOF
    fi
    if [[ -e "${DEB_DIR}"/"opt/resolve/bin/DaVinci Remote Monitoring" ]]; then
	assert_object "${DEB_DIR}"/opt/resolve/graphics/Remote_Monitoring.png
	cat > "${DEB_DIR}"/usr/share/applications/com.blackmagicdesign.resolve-DaVinciRemoteMonitoring.desktop <<EOF
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Type=Application
Name=DaVinci Remote Monitoring
Path=/opt/resolve
Exec="/opt/resolve/bin/DaVinci Remote Monitoring"
Icon=/opt/resolve/graphics/Remote_Monitoring.png
Terminal=false
StartupNotify=true
Categories=AudioVideo
EOF
    fi
    if [[ -e "${DEB_DIR}"/"opt/resolve/bin/DaVinci Remote Monitor" ]]; then
	assert_object "${DEB_DIR}"/opt/resolve/graphics/Remote_Monitoring.png
	cat > "${DEB_DIR}"/usr/share/applications/com.blackmagicdesign.resolve-DaVinciRemoteMonitoring.desktop <<EOF
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Type=Application
Name=DaVinci Remote Monitor
Path=/opt/resolve
Exec="/opt/resolve/bin/DaVinci Remote Monitor"
Icon=/opt/resolve/graphics/Remote_Monitoring.png
Terminal=false
StartupNotify=true
Categories=AudioVideo
EOF
    fi
    cat > "${DEB_DIR}"/usr/share/mime/packages/blackmagicresolve.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
   <mime-type type="application/x-resolveproj">
     <comment>DaVinci Resolve Project</comment>
     <glob pattern="*.drp"/>
   </mime-type>
   <mime-type type="application/x-resolvebin">
     <comment>DaVinci Resolve Bin</comment>
     <glob pattern="*.drb"/>
   </mime-type>
   <mime-type type="application/x-resolvetimeline">
     <comment>DaVinci Resolve Timeline</comment>
     <glob pattern="*.drt"/>
   </mime-type>
   <mime-type type="application/x-resolvetemplatebundle">
     <comment>DaVinci Resolve Template Bundle</comment>
     <glob pattern="*.drfx"/>
   </mime-type>
   <mime-type type="application/x-resolvedbkey">
     <comment>DaVinci Resolve Database Access Key</comment>
     <glob pattern="*.resolvedbkey"/>
   </mime-type>
</mime-info>
EOF
    if [[ -e "${DEB_DIR}"/opt/resolve/graphics/DV_ResolveBin.png ]]; then
	creates_directory "${DEB_DIR}"/usr/share/icons/hicolor/128x128/mimetypes/
	copy_object "${DEB_DIR}"/opt/resolve/graphics/DV_ResolveBin.png "${DEB_DIR}"/usr/share/icons/hicolor/128x128/mimetypes/application-x-resolvebin.png
    fi
    if [[ -e "${DEB_DIR}"/opt/resolve/graphics/DV_ResolveProj.png ]]; then
	creates_directory "${DEB_DIR}"/usr/share/icons/hicolor/128x128/mimetypes/
	copy_object "${DEB_DIR}"/opt/resolve/graphics/DV_ResolveProj.png "${DEB_DIR}"/usr/share/icons/hicolor/128x128/mimetypes/application-x-resolveproj.png
    fi
    if [[ -e "${DEB_DIR}"/opt/resolve/graphics/DV_ResolveTimeline.png ]]; then
	creates_directory "${DEB_DIR}"/usr/share/icons/hicolor/128x128/mimetypes/
	copy_object "${DEB_DIR}"/opt/resolve/graphics/DV_ResolveTimeline.png "${DEB_DIR}"/usr/share/icons/hicolor/128x128/mimetypes/application-x-resolvetimeline.png
    fi
    if [[ -e "${DEB_DIR}"/opt/resolve/graphics/DV_TemplateBundle.png ]]; then
	creates_directory "${DEB_DIR}"/usr/share/icons/hicolor/128x128/mimetypes/
	copy_object "${DEB_DIR}"/opt/resolve/graphics/DV_TemplateBundle.png "${DEB_DIR}"/usr/share/icons/hicolor/128x128/mimetypes/application-x-resolvetemplatebundle.png
    fi
    if [[ -e "${DEB_DIR}"/opt/resolve/graphics/DV_ServerAccess.png ]]; then
	creates_directory "${DEB_DIR}"/usr/share/icons/hicolor/128x128/mimetypes/
	copy_object "${DEB_DIR}"/opt/resolve/graphics/DV_ServerAccess.png "${DEB_DIR}"/usr/share/icons/hicolor/128x128/mimetypes/application-x-resolvedbkey.png
    fi
}

installer_extract_xorriso() {
    check_command xorriso
    echo "Extracting archive"
    createf_directory "${UNPACK_DIR}"
    xorriso -osirrox on -indev "${INSTALLER_ARCHIVE}" -extract / "${UNPACK_DIR}"
    if [[ -z $(ls -A "${UNPACK_DIR}") ]];
    then
	echo "[ERROR] Failed to extract DaVinci Resolve installer archive"
	remove_directory "${UNPACK_DIR}"
	exit 1
    fi
}

installer_extract_native() {
    echo "Extracting archive"
    createf_directory "${UNPACK_DIR}"
    chmod a+x "${INSTALLER_ARCHIVE}"
    if [[ ! -x "${INSTALLER_ARCHIVE}" ]];
    then
	echo "[ERROR] DaVinci Resolve installer archive is not executable"
	exit 1
    fi
    link_object "${UNPACK_DIR}" ./squashfs-root
    EXTRACT_OUT=$(./"${INSTALLER_ARCHIVE}" --appimage-extract 2>&1)
    rm -f ./squashfs-root
    find "${UNPACK_DIR}" -exec chmod a+r {} \;
    find "${UNPACK_DIR}" -type d -exec chmod a+x {} \;
    NUMEXTRACT=$(echo "${EXTRACT_OUT}" | grep "^squashfs-root/" -c)
    echo "Found ${NUMEXTRACT} objects"
    if [[ -z $(ls -A "${UNPACK_DIR}") ]];
    then
	echo "[ERROR] Failed to extract DaVinci Resolve installer archive"
	echo "${EXTRACT_OUT}" | tail
	remove_directory "${UNPACK_DIR}"
	exit 1
    fi
}

print_usage() {
    echo "Usage: $0 <DaVinci_Resolve_*_Linux.run>"
    echo "Advanced options:"
    echo "  -h | --help       Display this help"
    echo "  --skip-onboarding Exclude Onboarding feature"
    echo "  --skip-braw       Exclude BRAW Player and Speed Test"
}

echo "MakeResolveDeb ${MAKERESOLVEDEB_VERSION}"

# Warn if running as root
if [[ $EUID -eq 0 ]];
then
    echo
    echo "[WARNING] This should not be run as root or using sudo"
    echo
fi

# Parse arguments
for arg in "$@"
do
    case $arg in
	-h|--help)
	    print_usage
	    exit 1
	    ;;
        --skip-onboarding)
            SKIP_ONBOARDING="yes"
            shift
            ;;
        --skip-braw)
            SKIP_BRAW="yes"
            shift
            ;;
        --*|-*)
            echo "[ERROR] Unknown argument '$1'"
	    exit 1
            ;;
        *)
	    if [[ -z "$INSTALLER_ARCHIVE" ]]; then
		INSTALLER_ARCHIVE="${1}"
		shift
	    else
		echo "[ERROR] Only one installer archive file may be specified"
		exit 1
	    fi
            ;;
    esac
done
if [[ -z "$INSTALLER_ARCHIVE" ]]; then
    echo "No installer archive file specified"
    print_usage
    exit 1
fi
if [[ ! -e "$INSTALLER_ARCHIVE" ]] || [[ "$INSTALLER_ARCHIVE" != $(basename "${INSTALLER_ARCHIVE}") ]];
then
    echo "[ERROR] ${INSTALLER_ARCHIVE} does not exist or is located outside the working directory"
    exit 1
fi

# Validate and parse archive name
FILENAMEP1=$(echo "${INSTALLER_ARCHIVE}" | cut -d'_' -f1 -)
FILENAMEP2=$(echo "${INSTALLER_ARCHIVE}" | cut -d'_' -f2 -)
FILENAMEP3=$(echo "${INSTALLER_ARCHIVE}" | cut -d'_' -f3 -)
FILENAMEP4=$(echo "${INSTALLER_ARCHIVE}" | cut -d'_' -f4 -)
FILENAMEP5=$(echo "${INSTALLER_ARCHIVE}" | cut -d'_' -f5 -)
if [[ "${FILENAMEP1}" != "DaVinci" ]] || [[ "${FILENAMEP2}" != "Resolve" ]];
then
    echo "[ERROR] File does not look like a valid DaVinci Resolve installer archive"
    exit 1
fi
if [[ "${FILENAMEP5}" == "Linux.run" ]] && [[ "${FILENAMEP3}" == "Studio" ]];
then
    RESOLVE_NAME="DaVinci Resolve Studio"
    RESOLVE_VERSION=$FILENAMEP4
    DEB_NAME=davinci-resolve-studio
    DEB_CONFLICTS=davinci-resolve
elif [[ "$FILENAMEP4" == "Linux.run" ]];
then
    RESOLVE_NAME="DaVinci Resolve"
    RESOLVE_VERSION=$FILENAMEP3
    DEB_NAME=davinci-resolve
    DEB_CONFLICTS=davinci-resolve-studio
else
    echo "[ERROR] File does not look like a valid DaVinci Resolve installer archive"
    exit 1
fi
UNPACK_DIR=./unpack-"${DEB_NAME}"-"${RESOLVE_VERSION}"
DEB_VERSION="${RESOLVE_VERSION}"-mrd"${MAKERESOLVEDEB_VERSION}"
DEB_DIR=./"${DEB_NAME}"_"${DEB_VERSION}"_amd64
RESOLVE_BASE_DIR="${DEB_DIR}"/opt/resolve
ERRORS=0

echo
echo "Detected ${RESOLVE_NAME} version ${RESOLVE_VERSION}"
echo

# Verify that we have the commands we need
check_command tar
check_command fakeroot
check_command dpkg-deb
echo

# Create destination directories
createf_directory "${DEB_DIR}"
createf_directory "${RESOLVE_BASE_DIR}"

# Initialize Debian package structure
init_deb

# Determine which conversion processs to use
case $RESOLVE_VERSION in
    15.*)
	echo "Using Resolve 15 conversion process"
	installer_extract_xorriso
	process_15
	process_udev
	process_desktop_shortcuts
	;;
    16.*)
	echo "Using Resolve 16 conversion process"
	installer_extract_xorriso
	process_16
	process_braw
	process_udev
	process_desktop_shortcuts
	;;
    17.*)
	echo "Using Resolve 17 conversion process"
	installer_extract_native
	process_17
	process_braw
	process_udev
	process_desktop_shortcuts
	;;
    18.*)
	echo "Using Resolve 18 conversion process"
	installer_extract_native
	process_18
	process_braw
	process_udev
	process_desktop_shortcuts
	;;
    19.*)
	echo "Using Resolve 19 conversion process"
	installer_extract_native
	process_19
	process_braw
	process_udev
	process_desktop_shortcuts
	;;
    20.*)
	echo "Using Resolve 20 conversion process"
	installer_extract_native
	process_20
	process_braw
	process_udev
	process_desktop_shortcuts
	;;
    *)
	echo "Unknown Resolve version"
	echo "Trying Resolve 20 conversion process"
	installer_extract_native
	process_20
	process_braw
	process_udev
	process_desktop_shortcuts
	;;
esac

# Finalize Debian package
close_deb

if [[ -z "$CI_TEST" ]]; then
    create_directory "./tmp"
    echo "Creating Debian package (This can take a while. Do not interrupt)"
    if ! TMPDIR=./tmp fakeroot dpkg-deb -b "${DEB_DIR}" "${DEB_DIR}".deb;
    then
	ERRORS=$((ERRORS+1))
    fi
    
    # Clean up
    remove_directory "./tmp"
    remove_directory "${UNPACK_DIR}"
    remove_directory "${DEB_DIR}"
fi

# Report
echo
echo "[DONE] errors reported ${ERRORS}"
echo

exit $ERRORS
