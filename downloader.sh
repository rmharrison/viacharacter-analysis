################################################################################
# ViaCharacter analysis tool
# Ryan M Harrison
# ryan.m.harrison@gmail.com
# 
# @brief Downloads and parses records from ViaCharacter.org
# @detail Must be logged into the site to access records.
# Could manage the session via curl or wget, but it's easier
# to login through a browser and use the cookies.
# I use the FireFox plugin: 
# 'ExportCookies' (https://addons.mozilla.org/en-US/firefox/addon/export-cookies/)
################################################################################

cookiefile="cookies.txt"
recorddir="sample_data"
if [ -s $cookiefile ]
then
    echo "wget using cookie file: $cookiefile"
else
    echo "Please save a cookie file (default filename: $cookiefile)"
    echo "e.g. Firefox plugin ExportCookies (https://addons.mozilla.org/en-US/firefox/addon/export-cookies/)"
    exit -1
fi

for recordid in {2000001..2000100}
do
    filepath="$recorddir/$recordid.txt"
    wget --load-cookies="$cookiefile" www.viacharacter.org/survey/Surveys/NewResults/$recordid 1>/dev/null 2>/dev/null
    if [ -f $recordid ]
    then
        name=`grep '<h2>' $recordid | awk -F'[<>]' '{print $3}'`
        attribs=`grep '<h3>' $recordid | awk -F'[<>]' '{print $5}'`
        if [[ "$name" && "$attribs" ]]
        then
            echo "#$recordid : $name" > $filepath
            echo "$attribs" >> $filepath
        fi
        rm -f $recordid
    fi
done

# To redact id and name...
#for i in `ls *txt`; do mv $i Redacted_"$count".txt; count=$(($count + 1)); done
