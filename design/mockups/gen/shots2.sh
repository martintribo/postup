# strictly <=2 browsers
cd /workspace/postup-pm/mockups
while read n q s; do bash gen/shot1.sh $n "$q" $s & bash -c 'read n q s; [ -n "$n" ] && bash gen/shot1.sh $n "$q" $s' <<< "" ; wait; done < "$1"
