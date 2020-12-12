@echo on


rem Устанавливаем значения переменных

@REM Params from args
set Server=%1
set BaseName=%2

set ServerName=%Server%:3541
set SererRac=%Server%:3545
set uccode=КодРазрешения
set RacPath="c:\Program Files (x86)\1cv8\8.3.3.721\bin\rac.exe"
set UserName=Администратор
set UserPass=канарейка
set ConStr=/S%serverName%\%BaseName%

set CF_DIR=C:\kit\1.0.0.82\

SET LOG_DIR=C:\kit\log
SET LOG_FILE=%LOG_DIR%\%BASE_NAME%_%date:~6,4%-%date:~3,2%-%date:~0,2%.log

rem Завершаем работу пользователей
call deployka session kill -ras %SererRac% -rac %RacPath% -db %BaseName% -db-user %UserName% -db-pwd %UserPass%  -lockuccode %uccode% 

rem Обновляем конфигурацию из файла cf
call deployka loadcfg %ConStr% /mode -cf %CF_DIR% -db-user %UserName% -db-pwd %UserPass% -uccode %uccode% 

rem Обновляем конфигурацию базы данных
call deployka dbupdate %ConStr% -db-user %UserName% -db-pwd %UserPass% -uccode %uccode% 

rem Снимаем блокировку сеансов
call deployka session unlock -ras %SererRac% -rac %RacPath% -db %BaseName% -db-user %UserName% -db-pwd %UserPass% -lockuccode %uccode% 
cd "c:\Program Files (x86)\1cv8\8.3.3.721\bin\"
1cv8.exe ENTERPRISE /Ssd-kit4:3541\testpatiokitminsk /N Администратор /P канарейка /CВыполнитьОбновлениеИЗавершитьРаботу 

PAUSE
