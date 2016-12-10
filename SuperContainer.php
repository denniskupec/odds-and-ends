<?php

class SuperContainer
{
	
	protected $data;
	
	public function __construct()
	{
		$this->data = new SplObjectStorage;
	}
	
	public function __get($key)
	{
		return $this->data->$key;
	}
	
	public function __set($key, $value)
	{
		$this->data->$key = $value;
	}
	

	public function __call($name, $arguments)
	{
		$c = create_function('$arguments, $that', $name);
		return call_user_func($c, $arguments, $this);
	}

}

$c = new SuperContainer;

$c->poop = "dong";

echo $c->{'

	return "Hello, $arguments[0]" . PHP_EOL .
			 "Poop" . $that->poop;

'}("world!");

// this is supposed to be a joke
