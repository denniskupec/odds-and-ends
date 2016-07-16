<?php

trait Singleton {

	private static $instance;

	final public static function getInstance()
	{
		if(!isset(static::$instance)) {
			static::$instance = new static;
		}
		return static::$instance;
	}

	final private function __construct()
	{
		throw new ErrorException("You cannot instantiate a Singleton class.")
	}

	final private function __wakeup() {}
	final private function __clone() {}   

}
