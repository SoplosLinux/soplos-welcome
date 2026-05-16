#!/bin/bash
# ==============================================================================
# DaVinci Resolve 18/19+ - Patch for integrated AMD and Intel GPUs on Linux
# Fixes: "GPU not supported", "DeviceNotFound", sudden crashes (Signal 11)
# Supports: AMD Radeon iGPU/APU (Rusticl/radeonsi), Intel UHD/Iris/N-series (NEO)
# Tested on: Debian Testing (Forky), kernel 6.19, Intel N150 (ADL-N), AMD iGPU
# ==============================================================================

set -e

# Resolve real user when running via pkexec
if [ -n "$PKEXEC_UID" ]; then
    REAL_USER=$(getent passwd "$PKEXEC_UID" | cut -d: -f1)
    REAL_HOME=$(getent passwd "$PKEXEC_UID" | cut -d: -f6)
else
    REAL_USER="$USER"
    REAL_HOME="$HOME"
fi

detect_gpu() {
    if lspci 2>/dev/null | grep -qi "VGA.*Intel\|Display.*Intel\|3D.*Intel"; then
        echo "intel"
    elif lspci 2>/dev/null | grep -qi "VGA.*AMD\|Display.*AMD\|3D.*AMD\|VGA.*ATI"; then
        echo "amd"
    else
        echo "unknown"
    fi
}

GPU_VENDOR="${1:-$(detect_gpu)}"

echo "=================================================="
echo "  DaVinci Resolve - Integrated GPU Patcher"
echo "  Detected vendor: $GPU_VENDOR"
echo "=================================================="
echo ""

if [ "$GPU_VENDOR" = "unknown" ]; then
    echo "[!] Could not detect GPU automatically."
    echo "    Usage: $0 [amd|intel]"
    exit 1
fi

# ==============================================================================
# STEP 1: Dependencies
# ==============================================================================
echo "Step 1: Installing dependencies for $GPU_VENDOR..."

if command -v apt-get &> /dev/null; then
    apt-get update

    if [ "$GPU_VENDOR" = "amd" ]; then
        apt-get install -y mesa-opencl-icd gcc ocl-icd-opencl-dev
        echo "[OK] AMD dependencies installed (Mesa Rusticl)."

    elif [ "$GPU_VENDOR" = "intel" ]; then
        apt-get install -y \
            mesa-opencl-icd \
            intel-opencl-icd \
            intel-media-va-driver-non-free \
            libva-drm2 \
            gcc \
            ocl-icd-opencl-dev
        echo "[OK] Intel dependencies installed (NEO + Mesa)."
    fi
else
    echo "[!] apt not found. Install manually:"
    [ "$GPU_VENDOR" = "amd" ] && echo "    -> mesa-opencl-icd gcc" || echo "    -> mesa-opencl-icd intel-opencl-icd intel-media-va-driver-non-free libva-drm2 gcc"
fi

# ==============================================================================
# STEP 2: Intel i915 firmware
# ==============================================================================
if [ "$GPU_VENDOR" = "intel" ]; then
    echo ""
    echo "Step 2: Checking i915 firmware..."

    FIRMWARE_BASE="https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/i915"
    FIRMWARE_DIR="/lib/firmware/i915"
    NEED_INITRAMFS=0

    mkdir -p "$FIRMWARE_DIR"

    for FW in adlp_dmc.bin tgl_guc_70.bin tgl_huc.bin; do
        if [ ! -f "$FIRMWARE_DIR/$FW" ]; then
            echo "    Downloading $FW..."
            curl -L "$FIRMWARE_BASE/$FW" -o "$FIRMWARE_DIR/$FW"
            echo "[OK] $FW downloaded."
            NEED_INITRAMFS=1
        else
            echo "[OK] $FW already present."
        fi
    done

    if [ "$NEED_INITRAMFS" = "1" ]; then
        echo "    Rebuilding initramfs (this may take a moment)..."
        update-initramfs -u -k all
        echo "[OK] initramfs rebuilt. A reboot is required for firmware to take effect."
        REBOOT_NEEDED=1
    fi
fi

# ==============================================================================
# STEP 3: libProResRAW.so stub
# ==============================================================================
if [ -f "/opt/resolve/libs/libProResRAW.so" ]; then
    echo ""
    echo "Step 3: Building and injecting dummy ProResRAW library..."

    cat << 'EOF' > /tmp/dummy_prores.c
void* PRRawCreateBooleanSettingPropertyValue()      { return 0; }
void* PRRawCreateClipSettingsContext()              { return 0; }
void* PRRawCreateClipSettingsRawConversionParams()  { return 0; }
void* PRRawCreateCUDAProcessor()                    { return 0; }
void* PRRawCreateDecoder()                          { return 0; }
void* PRRawCreateFloat32SettingPropertyValue()      { return 0; }
void* PRRawCreateInt32SettingPropertyValue()        { return 0; }
void* PRRawCreateOpenCLProcessorForQueue()          { return 0; }
void* PRRawCreateRawImageMetadata()                 { return 0; }
void* PRRawCreateUInt32SettingPropertyValue()       { return 0; }
void* PRRawCreateUTF8StringSettingPropertyValue()   { return 0; }
void* PRRawCUDAProcessFrame_Texture()               { return 0; }
void* PRRawDecodeFrame()                            { return 0; }
void* PRRawDestroyClipSettingsContext()             { return 0; }
void* PRRawDestroyClipSettingsRawConversionParams() { return 0; }
void* PRRawDestroyCUDAProcessor()                   { return 0; }
void* PRRawDestroyDecoder()                         { return 0; }
void* PRRawDestroyOpenCLProcessor()                 { return 0; }
void* PRRawDestroyRawImageMetadata()                { return 0; }
void* PRRawDestroySettingPropertyValue()            { return 0; }
void* PRRawGetArraySettingPropertyValue()           { return 0; }
void* PRRawGetArraySettingPropertyValueSize()       { return 0; }
void* PRRawGetBooleanSettingPropertyValue()         { return 0; }
void* PRRawGetFloat32SettingPropertyValue()         { return 0; }
void* PRRawGetFrameHeaderMetadata()                 { return 0; }
void* PRRawGetHeight()                              { return 0; }
void* PRRawGetInt32SettingPropertyValue()           { return 0; }
void* PRRawGetOutputColorSpecifier()                { return 0; }
void* PRRawGetRawConversionPlugInIdentifier()       { return 0; }
void* PRRawGetRawConversionPlugInLoadingErrorInfo() { return 0; }
void* PRRawGetRawConversionPlugInName()             { return 0; }
void* PRRawGetRawConversionPlugIns()                { return 0; }
void* PRRawGetRawConversionPlugInVersionMajor()     { return 0; }
void* PRRawGetRawConversionPlugInVersionMinor()     { return 0; }
void* PRRawGetSettingPropertyValue()                { return 0; }
void* PRRawGetSettingPropertyValueType()            { return 0; }
void* PRRawGetSupportedSettings()                   { return 0; }
void* PRRawGetUInt32SettingPropertyValue()          { return 0; }
void* PRRawGetUTF8StringSettingPropertyValue()      { return 0; }
void* PRRawGetUTF8StringSettingPropertyValueLength(){ return 0; }
void* PRRawGetWidth()                               { return 0; }
void* PRRawImageBytesPerRowNeeded()                 { return 0; }
void* PRRawImageMetadataGetBytesPerRow()            { return 0; }
void* PRRawImageMetadataGetHeight()                 { return 0; }
void* PRRawImageMetadataGetWidth()                  { return 0; }
void* PRRawIsRawConversionPlugInCompatibleWithClip(){ return 0; }
void* PRRawMetadataDictionaryAddBinaryDataItem()    { return 0; }
void* PRRawMetadataDictionaryAddFloat32Item()       { return 0; }
void* PRRawMetadataDictionaryAddUInt32Item()        { return 0; }
void* PRRawMetadataDictionaryAddUTF8StringItem()    { return 0; }
void* PRRawMetadataDictionaryCreate()               { return 0; }
void* PRRawMetadataDictionaryDestroy()              { return 0; }
void* PRRawOpenCLProcessFrame_Texture()             { return 0; }
void* PRRawSetSettingCurrentValue()                 { return 0; }
EOF

    gcc -shared -fPIC /tmp/dummy_prores.c -o /tmp/libProResRAW.so

    if [ ! -f "/opt/resolve/libs/libProResRAW.so.bak" ]; then
        mv /opt/resolve/libs/libProResRAW.so /opt/resolve/libs/libProResRAW.so.bak
        echo "[OK] Backup saved as libProResRAW.so.bak"
    else
        echo "[!] Backup already exists, skipping."
    fi

    cp /tmp/libProResRAW.so /opt/resolve/libs/libProResRAW.so
    rm /tmp/dummy_prores.c /tmp/libProResRAW.so
    echo "[OK] libProResRAW stub injected."
else
    echo "[!] libProResRAW.so not found — may already be patched or at a different path."
fi

# ==============================================================================
# STEP 4: Patch .desktop launcher
# ==============================================================================
echo ""
echo "Step 4: Patching .desktop launcher..."

DESKTOP_SYS="/usr/share/applications/com.blackmagicdesign.resolve.desktop"
DESKTOP_LOCAL="$REAL_HOME/.local/share/applications/com.blackmagicdesign.resolve.desktop"

LIBSTDC=$(find /usr/lib -name "libstdc++.so.6" -print -quit 2>/dev/null)
if [ -z "$LIBSTDC" ]; then
    LIBSTDC=$(ldconfig -p 2>/dev/null | grep "libstdc++.so.6" | awk '{print $NF}' | head -1)
fi

if [ -z "$LIBSTDC" ]; then
    echo "[ERROR] libstdc++.so.6 not found. Install libstdc++6."
    exit 1
fi
echo "[OK] libstdc++ found at: $LIBSTDC"

if [ "$GPU_VENDOR" = "amd" ]; then
    ENV_VARS="RUSTICL_ENABLE=radeonsi OCL_ICD_VENDORS=rusticl.icd"
elif [ "$GPU_VENDOR" = "intel" ]; then
    ENV_VARS="OCL_ICD_VENDORS=intel.icd"
    echo "[INFO] Using Intel NEO stack (OCL_ICD_VENDORS=intel.icd)."
fi

mkdir -p "$REAL_HOME/.local/share/applications/"

if [ -f "$DESKTOP_SYS" ]; then
    cp "$DESKTOP_SYS" "$DESKTOP_LOCAL"
    chown "$REAL_USER":"$REAL_USER" "$DESKTOP_LOCAL"
    sed -i "s|^Exec=.*|Exec=env $ENV_VARS LD_PRELOAD=$LIBSTDC /opt/resolve/bin/resolve|g" "$DESKTOP_LOCAL"
    update-desktop-database "$REAL_HOME/.local/share/applications/" 2>/dev/null || true
    echo "[OK] Launcher patched:"
    echo "     -> $ENV_VARS LD_PRELOAD=$LIBSTDC"
else
    echo "[ERROR] Launcher not found at $DESKTOP_SYS"
    echo "        Launch Resolve manually with:"
    echo "        env $ENV_VARS LD_PRELOAD=$LIBSTDC /opt/resolve/bin/resolve"
fi

# ==============================================================================
# STEP 5: /dev/dri group membership
# ==============================================================================
echo ""
echo "Step 5: Checking /dev/dri permissions..."
if id -nG "$REAL_USER" | grep -qw "render"; then
    echo "[OK] User already in 'render' group."
else
    usermod -aG render,video "$REAL_USER"
    echo "[OK] Added $REAL_USER to render and video groups. Log out to apply."
    REBOOT_NEEDED=1
fi

# ==============================================================================
# Summary
# ==============================================================================
echo ""
echo "======================================================"
echo "   PATCH APPLIED ($GPU_VENDOR)"
echo "   Launch DaVinci Resolve from the menu or with:"
echo "   env $ENV_VARS LD_PRELOAD=$LIBSTDC /opt/resolve/bin/resolve"
if [ "${REBOOT_NEEDED:-0}" = "1" ]; then
    echo ""
    echo "   *** REBOOT REQUIRED for firmware/group changes ***"
fi
echo "======================================================"
