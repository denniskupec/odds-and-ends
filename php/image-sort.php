<?php

/*
 * Take a folder of images with incorrect file extensions
 * and make them well again.
 */

function getExt(string $f): string
{
    $e = exif_imagetype($f);

    $types = ['.gif', '.jpg', '.png', '.swf', '.psd', '.bmp', 
                '.tiff', '.tiff', '.jpc', '.jp2', '.jpx', '.jb2', 
                '.swc', '.iff', '.bmp', '.xbm', '.ico'];

    return (!$e) ? '' : $types[--$e];
}

$dir = scandir('.');
$a = microtime(true);

foreach ($dir as $f)
{
    if ($f[0] !== '.') {
        rename($f, md5_file($f) . getExt($f));
        //rename($f, $f . getExt($f));
    }
}

echo round((microtime(true) - $a) * 1000, 3) . PHP_EOL;
