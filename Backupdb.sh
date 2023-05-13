#This is a script backup
while getopts d:t: flag
do
    case "${flag}" in
        d) database=${OPTARG};;
        t) table=${OPTARG};;
    esac
done
mongodump --db=$database  --collection=$table --out=BACKUP/

