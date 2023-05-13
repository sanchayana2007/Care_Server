		# to remove the matches of the grep procerss( grep -v "grep")
		
		#Initilaize
		dbname="DocBookingService"
		filensames=("./server_v2/web/booking/clinic_update_admin.py")
                tables=("SlotInfo")
        	serverfiles=("./server_v2/web/booking/clinic_update_admin.py")
		serverip="35.161.169.44"        



		# Create the backupcommands
	        cmd="./Backupscripts.sh"
        	for i in ${!serverfiles[@]};   
                	do
                        cmd="${cmd} ${serverfiles[$i]}"                                                
        
                done
 		echo $cmd
	        dbcmd="./Backupdb.sh -d $dbname -t ${tables[0]}"

		#Clean create Backups is Remote server
		ssh -i "~/.ssh/id_rsa.pub" ubuntu@$serverip << EOF 
		rm -rf NEWCODE;
		mkdir -m 777 NEWCODE ;
                rm -rf BACKUP;
		mkdir -m 777 BACKUP ;
		ls;
                "./test.sh";
                "${dbcmd}";

EOF

                for i in ${!filensames[@]};
                        do
                                echo "####################### ${filensames[$i]} ################################"
				pil=$(grep "PIL" "${filensames[$i]}")
				if [[ ! -z "$pil"  ]];
				then
				   echo "PIL is found in files"
			   	   exit 0 
				fi

                                scp  "${filensames[$i]}"  ubuntu@$serverip:/home/ubuntu/NEWCODE/
			done

		for i in ${!tables[@]};
                        do
                                echo "####################### ${tables[$i]} ################################"
				mongodump --db=DocBookingService  --collection="${tables[$i]}" --out=data/	
			done


		 echo "####################### Create db dumps  ################################"
		 if [ -d "data" ]; then
    			echo "data got created"
			cd data
			for i in ${!tables[@]};
                        do
                                echo "####################### ${tables[$i]} ################################"
                        	tar -zcvf "${!tables[$i]}.tar"   "${!tables[$i]}/"   
				scp "${!tables[$i]}.tar"  ubuntu@$serverip:/home/ubuntu/NEWCODE/	
			done



		 else
    			echo "DB Data dosent got cretaed."

		 fi 

