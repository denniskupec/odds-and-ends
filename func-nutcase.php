<?php

/*
* Input a word or string then out comes a nutcase version.
* Whitespace is preserved.
* Example:
* 	In  -> the quick brown fox jumps over the lazy dog
* 	Out -> THe qUIcK BRowN fOx jumps oveR ThE LaZY Dog
*/ 

function nutcase(string $string) {
	array_map(function($c) use (&$nut)
	{
		$nut .= rand(0, 1) ? strtolower($c) : strtoupper($c);
	}, str_split($string));
	
	return $nut;
}
