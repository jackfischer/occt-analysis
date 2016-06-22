list=$(ls -1 *.png |sort -g)
a=1
for i in $list; do
  new=$(printf "%04d.png" "$a") #04 pad to length of 4
  mv -- "$i" "$new"
  let a=a+1
done
