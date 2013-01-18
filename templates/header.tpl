<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>

    <meta http-equiv="content-type" content="text/html; charset=utf-8" />

    <meta name="viewport" content="width=device-width; height=device-height; initial-scale=1.0; maximum-scale=1.0; user-scalable=no;" />

    <meta name="MobileOptimized" content="width" />

    <meta name="HandheldFriendly" content="true" />

    <title>OMXRemote</title>

    <link rel="stylesheet" href="style" type="text/css" media="screen, projection" />

<script>
function control(str, value)
{
var xmlhttp;    
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
value = typeof value !== 'undefined' ? value : 1;
xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
    document.getElementById("current_file").innerHTML=xmlhttp.responseText;
    }
  }
xmlhttp.open("GET","remcontrols?"+str+"="+value,true);
xmlhttp.send();
}


function ajaxreq(type, value){
    var xmlhttp;
    if (window.XMLHttpRequest){
        xmlhttp = new XMLHttpRequest();
    }
    value = typeof value !== 'undefined' ? value :1;
    xmlhttp.onreadstatechange=function(){
        if (xmlhttp.readState == 4 && xmlhttp.status == 200){
            document.getElementById("current_file").innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "ajaxhandler?req_type="+type+"&value="+value, true);
    xmlhttp.send();
}
</script>


</head>

<body>

<div id="wrapper">

    <div id="header">
        <div id='current_header'>
           <a href='index'><img src='/images/remote.png' width=50 height=50 /></a> Currently Playing: <div id='current_file'>{{playing}}</div><br/>
                <button onclick="control('pause')"> Pause </button>&nbsp;
                <button onclick="control('stop')"> Stop </button>
                <button onclick="control('vol_down')"> Vol - </button>&nbsp;
                <button onclick="control('vol_up')"> Vol + </button>&nbsp;
                <button onclick="control('rw')"> << </button>&nbsp;
                <button onclick="control('ff')"> >> </button>
        </div>

    </div><!-- #header-->

