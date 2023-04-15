echo "1.cal\n 2.date\n 3.current directory\n 4.list all files"
read ch
 
case "$ch" in
	1) cal
;;
	2) date
;;
	3) pwd
;;
	4) ls -l
;;
	*) exit
;;
esac
