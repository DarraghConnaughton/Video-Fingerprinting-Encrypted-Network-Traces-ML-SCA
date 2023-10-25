fpm -f -t rpm -n package-name -C \
	-s dir \ 
	-p victim_viewer.rpm \
	--inputs fpm_input.txt
