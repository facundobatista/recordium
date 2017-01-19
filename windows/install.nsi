; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Recordium"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_PUBLISHER "publisher-team"
!define PRODUCT_WEB_SITE "https://github.com/facundobatista/recordium"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\recordium.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "..\media\recordium.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\recordium.exe"
!define MUI_FINISHPAGE_SHOWREADME "C:\Users\LOMAR\PycharmProjects\recordium\README.rst"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "SpanishInternational"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "Setup.exe"
InstallDir "$PROGRAMFILES\Recordium"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite try
  File "..\dist\recordium\api-ms-win-core-console-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-datetime-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-debug-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-errorhandling-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-file-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-file-l1-2-0.dll"
  File "..\dist\recordium\api-ms-win-core-file-l2-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-handle-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-heap-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-interlocked-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-libraryloader-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-localization-l1-2-0.dll"
  File "..\dist\recordium\api-ms-win-core-memory-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-namedpipe-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-processenvironment-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-processthreads-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-processthreads-l1-1-1.dll"
  File "..\dist\recordium\api-ms-win-core-profile-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-rtlsupport-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-string-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-synch-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-synch-l1-2-0.dll"
  File "..\dist\recordium\api-ms-win-core-sysinfo-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-timezone-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-core-util-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-conio-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-convert-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-environment-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-filesystem-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-heap-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-locale-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-math-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-multibyte-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-process-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-runtime-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-stdio-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-string-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-time-l1-1-0.dll"
  File "..\dist\recordium\api-ms-win-crt-utility-l1-1-0.dll"
  File "..\dist\recordium\base_library.zip"
  File "..\dist\recordium\icudt55.dll"
  File "..\dist\recordium\icuin55.dll"
  File "..\dist\recordium\icuuc55.dll"
  File "..\dist\recordium\LIBEAY32.dll"
  SetOutPath "$INSTDIR\media"
  File "..\dist\recordium\media\icon-192.png"
  File "..\dist\recordium\media\icon-active-192.png"
  File "..\dist\recordium\media\icon-problem-192.png"
  File "..\dist\recordium\media\logo.svg"
  File "..\dist\recordium\media\recordium.ico"
  SetOutPath "$INSTDIR"
  File "..\dist\recordium\mfc100u.dll"
  File "..\dist\recordium\MSVCP140.dll"
  File "..\dist\recordium\MSVCR100.dll"
  File "..\dist\recordium\pyexpat.pyd"
  File "..\dist\recordium\PyQt5.Qt.pyd"
  File "..\dist\recordium\PyQt5.QtCore.pyd"
  File "..\dist\recordium\PyQt5.QtGui.pyd"
  File "..\dist\recordium\PyQt5.QtNetwork.pyd"
  File "..\dist\recordium\PyQt5.QtPrintSupport.pyd"
  File "..\dist\recordium\PyQt5.QtWidgets.pyd"
  File "..\dist\recordium\python35.dll"
  File "..\dist\recordium\pythoncom35.dll"
  File "..\dist\recordium\pywintypes35.dll"
  File "..\dist\recordium\Qt5Core.dll"
  File "..\dist\recordium\Qt5Gui.dll"
  File "..\dist\recordium\Qt5Network.dll"
  File "..\dist\recordium\Qt5PrintSupport.dll"
  File "..\dist\recordium\Qt5Widgets.dll"
  File "..\dist\recordium\qwindows.dll"
  File "..\dist\recordium\recordium.exe"
  CreateDirectory "$SMPROGRAMS\Recordium"
  CreateShortCut "$SMPROGRAMS\Recordium\Recordium.lnk" "$INSTDIR\recordium.exe"
  CreateShortCut "$DESKTOP\Recordium.lnk" "$INSTDIR\recordium.exe"
  File "..\dist\recordium\recordium.exe.manifest"
  File "..\dist\recordium\select.pyd"
  File "..\dist\recordium\sip.pyd"
  File "..\dist\recordium\SSLEAY32.dll"
  File "..\dist\recordium\ucrtbase.dll"
  File "..\dist\recordium\unicodedata.pyd"
  File "..\dist\recordium\VCRUNTIME140.dll"
  File "..\dist\recordium\win32api.pyd"
  File "..\dist\recordium\win32com.shell.shell.pyd"
  File "..\dist\recordium\win32evtlog.pyd"
  File "..\dist\recordium\win32trace.pyd"
  File "..\dist\recordium\win32ui.pyd"
  File "..\dist\recordium\win32wnet.pyd"
  File "..\dist\recordium\_bz2.pyd"
  File "..\dist\recordium\_ctypes.pyd"
  File "..\dist\recordium\_hashlib.pyd"
  File "..\dist\recordium\_lzma.pyd"
  File "..\dist\recordium\_socket.pyd"
  File "..\dist\recordium\_ssl.pyd"
  File "..\dist\recordium\_win32sysloader.pyd"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\Recordium\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\Recordium\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\recordium.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\recordium.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
!insertmacro MUI_UNGETLANGUAGE
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\_win32sysloader.pyd"
  Delete "$INSTDIR\_ssl.pyd"
  Delete "$INSTDIR\_socket.pyd"
  Delete "$INSTDIR\_lzma.pyd"
  Delete "$INSTDIR\_hashlib.pyd"
  Delete "$INSTDIR\_ctypes.pyd"
  Delete "$INSTDIR\_bz2.pyd"
  Delete "$INSTDIR\win32wnet.pyd"
  Delete "$INSTDIR\win32ui.pyd"
  Delete "$INSTDIR\win32trace.pyd"
  Delete "$INSTDIR\win32evtlog.pyd"
  Delete "$INSTDIR\win32com.shell.shell.pyd"
  Delete "$INSTDIR\win32api.pyd"
  Delete "$INSTDIR\VCRUNTIME140.dll"
  Delete "$INSTDIR\unicodedata.pyd"
  Delete "$INSTDIR\ucrtbase.dll"
  Delete "$INSTDIR\SSLEAY32.dll"
  Delete "$INSTDIR\sip.pyd"
  Delete "$INSTDIR\select.pyd"
  Delete "$INSTDIR\recordium.exe.manifest"
  Delete "$INSTDIR\recordium.exe"
  Delete "$INSTDIR\qwindows.dll"
  Delete "$INSTDIR\Qt5Widgets.dll"
  Delete "$INSTDIR\Qt5PrintSupport.dll"
  Delete "$INSTDIR\Qt5Network.dll"
  Delete "$INSTDIR\Qt5Gui.dll"
  Delete "$INSTDIR\Qt5Core.dll"
  Delete "$INSTDIR\pywintypes35.dll"
  Delete "$INSTDIR\pythoncom35.dll"
  Delete "$INSTDIR\python35.dll"
  Delete "$INSTDIR\PyQt5.QtWidgets.pyd"
  Delete "$INSTDIR\PyQt5.QtPrintSupport.pyd"
  Delete "$INSTDIR\PyQt5.QtNetwork.pyd"
  Delete "$INSTDIR\PyQt5.QtGui.pyd"
  Delete "$INSTDIR\PyQt5.QtCore.pyd"
  Delete "$INSTDIR\PyQt5.Qt.pyd"
  Delete "$INSTDIR\pyexpat.pyd"
  Delete "$INSTDIR\MSVCR100.dll"
  Delete "$INSTDIR\MSVCP140.dll"
  Delete "$INSTDIR\mfc100u.dll"
  Delete "$INSTDIR\media\recordium.ico"
  Delete "$INSTDIR\media\logo.svg"
  Delete "$INSTDIR\media\icon-problem-192.png"
  Delete "$INSTDIR\media\icon-active-192.png"
  Delete "$INSTDIR\media\icon-192.png"
  Delete "$INSTDIR\LIBEAY32.dll"
  Delete "$INSTDIR\icuuc55.dll"
  Delete "$INSTDIR\icuin55.dll"
  Delete "$INSTDIR\icudt55.dll"
  Delete "$INSTDIR\base_library.zip"
  Delete "$INSTDIR\api-ms-win-crt-utility-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-time-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-string-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-stdio-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-runtime-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-process-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-multibyte-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-math-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-locale-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-heap-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-filesystem-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-environment-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-convert-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-conio-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-util-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-timezone-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-sysinfo-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-synch-l1-2-0.dll"
  Delete "$INSTDIR\api-ms-win-core-synch-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-string-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-rtlsupport-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-profile-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-processthreads-l1-1-1.dll"
  Delete "$INSTDIR\api-ms-win-core-processthreads-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-processenvironment-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-namedpipe-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-memory-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-localization-l1-2-0.dll"
  Delete "$INSTDIR\api-ms-win-core-libraryloader-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-interlocked-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-heap-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-handle-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-file-l2-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-file-l1-2-0.dll"
  Delete "$INSTDIR\api-ms-win-core-file-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-errorhandling-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-debug-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-datetime-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-core-console-l1-1-0.dll"

  Delete "$SMPROGRAMS\Recordium\Uninstall.lnk"
  Delete "$SMPROGRAMS\Recordium\Website.lnk"
  Delete "$DESKTOP\Recordium.lnk"
  Delete "$SMPROGRAMS\Recordium\Recordium.lnk"

  RMDir "$SMPROGRAMS\Recordium"
  RMDir "$INSTDIR\media"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd