# By James Aceret 6/5/2015
# New version of qcasTSLGenerator utilising awk and shell scripting only. 
# 
BEGIN {
	# Field Separator
	FS=",";
	# Output Field Separator
	OFS=",";
	# Output Record Separator
	ORS="\n";
	
	# Field Constants
	game_name_field=1;
	manufacturer_field=2;
	ssan_field=6;
	vid_type_field=7;
	binimage_field=8;
	binimage_type_field=9;
}

{ 
	split($0, TSLEntry, ",");
	ssan = TSLEntry[ssan_field];
	new_game_entry[FNR] = ssan;
	manufacturer[ssan] = TSLEntry[manufacturer_field];
	game_ssan[ssan] = TSLEntry[ssan_field];
	binimage[ssan] = TSLEntry[8];
	
	# Other form of String Comparison with tolower() function to ignore case
	if ( tolower(TSLEntry[vid_type_field]) ~ /video/)  {
		game_name[ssan] = TSLEntry[game_name_field] "-V";
	} else 	game_name[ssan] = TSLEntry[game_name_field] "-S";
	
	# Identify file type. 
	# Need to add other File Types here if needed 
	if ( match(TSLEntry[binimage_type_field], /BIN LINK FILE/))  {
		filetype[ssan] = "BLNK"
	} else if (match(TSLEntry[binimage_type_field], /PSA 32/)) {
			filetype[ssan] = "PS32"
	}
	else if (match(TSLEntry[binimage_type_field], /HMAC SHA1/)) { 
			filetype[ssan] = "SHA1"
	}
}

# Sample TSL Record
# 00,0000093250,2CAN-V                                                      ,10160853            ,BLNK
END {
	for (i in new_game_entry) {	
		printf("%02d,%010d,%-60s,%-20s,%-4s\n", manufacturer[new_game_entry[i]], game_ssan[new_game_entry[i]], game_name[new_game_entry[i]], binimage[new_game_entry[i]], filetype[new_game_entry[i]]);
	}
}