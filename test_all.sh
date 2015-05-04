#    echo "Usage: ./test.sh <Source> <Destination> <graph_file> <budget> \
#    <output_file> <position_file> <edge_labels (0 or 1)>"

#!/bin/bash 
SOURCE=4
DEST=12
BUDGET=660
LOGFILE=''
DIRECTORY=''
#while [ "$SOURCE" -lt 13 ]
#  do
#  DEST=1
    #while [ "$DEST" -lt 13 ]
#    do
while [ "$BUDGET" -lt 675 ]
do
 DIRECTORY="./results/""s""$SOURCE""d""$DEST/"
 if [ ! -d "$DIRECTORY" ]; then
   mkdir $DIRECTORY
 fi

#sh test.sh 1 3 real_graph.txt 720 output.txt positions.txt 1
#echo "i  ./test.sh $SOURCE $DEST \"real_graph.txt\" $BUDGET $BUDGET \"positions.txt\" 0"
 ./test.sh $SOURCE $DEST "real_graph.txt" $BUDGET $BUDGET "positions.txt" 0
 BUDGET=$((BUDGET+1))
done
#       done
#       DEST=$((DEST+1))
#    done
#  SOURCE=$((SOURCE+1))
#done
