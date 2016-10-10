/****************************************************************************
 \file      print.js
 \author    SENOO, Ken
 \copyright CC0
 \date      first created date: 2016-08-14T15:43+09:00
 \date      last  updated date: 2016-08-20T00:18+09:00
*****************************************************************************/

/**
  \brief Wrapper function for display text on JavaScript, JScript, SpiderMonkey.
  \param[in] text Target displaying text.
*/
if (typeof(print) === "undefined"){  // for SpiderMonkey
  function print(text){
    if      (typeof(console) !== "undefined") console.log(text );
    else if (typeof(WScript) !== "undefined") WScript.Echo(text);
  }
}
