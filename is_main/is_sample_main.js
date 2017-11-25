/// \file is_sample_main.js

if (WScript.ScriptName){
  WScript.Echo('Failure');
}

if (WScript.ScriptName === "is_sample_main.js"){
  WScript.Echo("Not shown");
}
