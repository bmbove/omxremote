<?php


$run_setup = 0;
// Check for configuration file
if(!file_exists("config.php")){
		$run_setup = 1;
	}
else{
	require_once("config.php");
}

?>

<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
	<head>
		<title>OMXRemote</title>
	</head>

	<body>
<?php

if($run_setup == 1){

?>

		<h1>OMXRemote Initial Configuration</h1>
<?php
}
else{
?>

		<h1>OMXRemote</h1>
	</body>
</html>	
<?php

}
?>
