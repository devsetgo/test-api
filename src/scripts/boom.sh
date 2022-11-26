#!/bin/bash
############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Add description of the script functions here."
   echo
   echo "Syntax: scriptTemplate [-g|h|v|V]"
   echo "options:"
   echo "g     Print the GPL license notification."
   echo "h     Print this Help."
   echo "v     Verbose mode."
   echo "V     Print software version and exit."
   echo "e     prd, dev, clean"
   echo
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################
############################################################
# Process the input options. Add options as needed.        #
############################################################
# Get the options
while getopts ":he:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      e) # Enter a name
         Set=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done


# if ["$Set" == "prd"];
# then
#     echo "deleting db"
# fi

str1="Hello Bash"
str2="Hello  "

if [ "$Set" == "prd" ]; then
    echo "deleting db"
else
    echo "Strings are not equal"
fi


echo "Run Env $Set!"