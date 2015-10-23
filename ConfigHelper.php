<?php

/*
* Instantiate the class once somewhere in your project and provide the constructor an array of values.
* Only works in PHP 7 and above since thats where they added static arrays.
* To use the class just create a new instance or invoke the variable (like a lambda) and the object will
* return your initial array of values.
* Proof of concept.
*/

class Config
{

	protected static $storage = [];
	
	// why can't you type hint AND provide a default value? who knows, maybe im just dumb
	public function __construct($config=[])
	{
		if(!empty($config) && is_array($config))
			self::$storage = array_merge(self::$storage, $config);

		// using self instead of static or even Config to be sure im resolving to this class
		return self::$storage;
	}

	/*
	* $b = new Config(["key" => "value"]);
	* $a = new ConfigConsumer($b());
	*
	* Shorter than making a new Config object and its probably faster too
	*/
	public function __invoke(string $key=null)
	{
		if(!is_null($key))
			return self::$storage[$key];

		return self::$storage;
	}

	public function __get(string $key)
	{
		return self::$storage[$key];
	}

	public function __set(string $key, $value)
	{
		self::$storage[$key] = $value;
	}

	public function __isset(string $key)
	{
		return isset(self::$storage[$key]);
	}

	public function __unset(string $key)
	{
		unset(self::$storage[$key]);
	}

}
