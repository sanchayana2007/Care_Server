#This is a script backup
		for user in "$@" 
			do
    			i=$((i + 1));
		        echo $user	
			 if [ -f $user ]; then
				
				cp $user  BACKUP/
		         else
				 echo "Not found: $user";

			 fi 

		done



