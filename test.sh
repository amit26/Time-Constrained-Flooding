#!/bin/bash 

if [ $# -lt 7 ]; then
    echo "Usage: ./test.sh <Source> <Destination> <graph_file> <budget> \
    <output_file> <position_file> <edge_labels (0 or 1)>"
    exit
fi

EX_G="./example_graphs/"
OUT="./output/"
SOURCE=$1
DEST=$2
BUDGET=$4
LOGFILE=$OUT$5".txt"
LOOPLESSFILE=$OUT$5"_loopless.txt"
IMAGE=$OUT$5".png"
GRAPH=$EX_G$3
POSITIONFILE=$EX_G$6
EDGE_LABELS=$7

echo "Run Algorithm!\n"

python tcf.py -i $LOGFILE -o $LOOPLESSFILE -s $SOURCE -d $DEST -g $GRAPH -b $BUDGET

echo "Algorithm Run Complete. Output Written to"$LOGFILE"..Now removing the loops"

echo "Draw graph\n!"

python draw_graph.py -g $GRAPH -i $LOGFILE -o $IMAGE -s $SOURCE -d $DEST -p $POSITIONFILE -w $LOOPLESSFILE -e $EDGE_LABELS

echo "Finished Drawing the Network Graph..Exiting"
