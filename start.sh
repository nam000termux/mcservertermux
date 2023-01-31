cd /sdcard/mcsv
jvm=`cat jvm.txt 2>/dev/null`
java -jar $jvm server.jar
echo off > $PREFIX/tmp/mcsv.status