#!/usr/bin/perl

$dir = "/home/tomcat/share/MEDIA/XML_PICTURE";
$old = 30;

opendir(dh, $dir) ||
    die "Unable to open directory $dir";

while (defined($filename = readdir(dh))) {
    if ((-f "$dir/$filename") && (-M "$dir/$filename" > $old)) {
        print "Deleting $dir/$filename\n";
        unlink("$dir/$filename") ||
            die "Unable to unlink file $dir/$filename";
    }
}

closedir(dh);
