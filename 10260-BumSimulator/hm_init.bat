cd /d %~dp0
set /a gstype= %4%%100

echo 清理配置
start /wait /min .\hm_init\hm_clean.bat
md "C:\Users\Administrator\Documents\"
md "C:\Users\Public\Documents\"

echo 调整DPI
python .\hm_init\dpi_utils.py

echo 覆盖配置
if %gstype% == 0 (
	xcopy ".\hm_init\all\config_1\*" "C:\Users\Administrator\AppData\Local\BumSim\Saved\Config\WindowsNoEditor" /e /i /y /c
) else (
	..\haima_init_program\ghostcopy.exe ".\hm_init\all\config_1\*" "C:\Users\Administrator\AppData\Local\BumSim\Saved\Config\WindowsNoEditor"
)

echo 关闭修复模糊弹窗
REG ADD "HKEY_CURRENT_USER\Control Panel\Desktop"  /v EnablePerProcessSystemDPI /t REG_DWORD /d 1 /f

exit 0