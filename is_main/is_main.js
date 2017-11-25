/****************************************************************************
 \file      is_main.js
 \author    SENOO, Ken
 \copyright CC0
 \date      first created date: 2016-08-20T00:15+09:00
 \date      last  updated date: 2016-08-20T00:59+09:00
*****************************************************************************/

function is_main(this_file_name){
  return (typeof(module ) !== "undefined" && !module.parent     ) ||
    (typeof(WScript) !== "undefined" && WScript.ScriptName === this_file_name)
}

if (typeof(print) === "undefined"){  // for SpiderMonkey
  function print(text){
    if      (typeof(console) !== "undefined") console.log(text );
    else if (typeof(WScript) !== "undefined") WScript.Echo(text);
  }
}

if (is_main("is_main.js")){
  print("Hello");
}
