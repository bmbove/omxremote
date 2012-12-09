<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>

    <meta http-equiv="content-type" content="text/html; charset=utf-8" />

    <meta name="viewport" content="width=device-width; height=device-height; initial-scale=1.0; maximum-scale=1.0; user-scalable=no;" />

    <meta name="MobileOptimized" content="width" />

    <meta name="HandheldFriendly" content="true" />

    <title>OMXRemote</title>

    <link rel="stylesheet" href="style" type="text/css" media="screen, projection" />

</head>

<body>

<div id="wrapper">

    <div id="header">
        <div id='current_header'>
           <a href='index'><img src='/images/remote.png' width=50 height=50 /></a> Currently Playing: {{playing}}
            <form action='index' method='post'>
                <button type='submit' value='1' name='pause'> Pause </button>&nbsp;<button type='submit' value='1' name='stop'> Stop </button>
            </form>
        </div>

    </div><!-- #header-->

