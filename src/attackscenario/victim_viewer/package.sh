fpm -f -t rpm -n package-name -C \
	-prefix=/opt/victim_viewer \
	-p victim_viewer.rpm \
	--input-file fpm_input.txt
