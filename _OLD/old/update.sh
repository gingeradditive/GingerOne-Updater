#!/bin/sh
LAST_RELEASE_LOCATION=$(curl -s https://api.github.com/repos/GiacomoGuaresi/pieDeployChainExploration/releases/latest | grep tarball_url | awk '{ print $2 }' | sed 's/,$//' | sed 's/"//g' );
LAST_RELEASE_VERSION=$(curl -s https://api.github.com/repos/GiacomoGuaresi/pieDeployChainExploration/releases/latest | grep tag_name | awk '{ print $2 }');
TEMP_DIR=/tmp/GingerUpdateSourceFolder
RELEASE_FOLDER_REGEX=GiacomoGuaresi*
CURRENT_RELEASE_VERSION_FILE=/etc/GingerAddiction.version

#pulisci aggiornamenti passati
rm -rf $TEMP_DIR
mkdir $TEMP_DIR

#controlla esistenza del file contenente la versione corrente
if [ ! -f $CURRENT_RELEASE_VERSION_FILE ]; then
    echo "Current release version file NOT found!"
	echo "v?.?.?" | sudo tee $CURRENT_RELEASE_VERSION_FILE > /dev/null
fi

#controlla versione corrente con quella dell'ultima release
CURRENT_VERSION=$(cat $CURRENT_RELEASE_VERSION_FILE)
if [ ! "$LAST_RELEASE_VERSION" = "$CURRENT_VERSION" ]; then
    echo "Version not match, try update"
	
    #scarica ultima release
	wget -qO- $LAST_RELEASE_LOCATION | tar xvz -C $TEMP_DIR/

	#installa ultima release
	cd $RELEASE_FOLDER_REGEX
	sh deploy.sh
	
	#aggiorna versione locale
	echo "$LAST_RELEASE_VERSION" | sudo tee $CURRENT_RELEASE_VERSION_FILE > /dev/null
else
	echo "No need to update"
	echo $LAST_RELEASE_VERSION
fi

