@echo off
rem Despliega AuryApp desde Windows: ejecuta deploy.sh dentro de WSL (Arch),
rem en la carpeta donde esta este .bat. No duplica logica: todo esta en deploy.sh.
wsl -d Arch --cd "%~dp0" -- bash ./deploy.sh
pause
