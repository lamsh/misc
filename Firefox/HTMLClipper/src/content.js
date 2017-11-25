////////////////////////////////////////////////////////////////////////////////
/// \file      content.js
/// \author    SENOO, Ken
/// \copyright CC0
////////////////////////////////////////////////////////////////////////////////

"use strict";

browser.runtime.onMessage.addListener(copyAsHTML);

function copyAsHTML(tab){
  // Create URL DOM
  var field = document.createElement("a");
  field.setAttribute("href", tab.url);
  field.innerText = tab.title;
  document.body.appendChild(field);

  var range = document.createRange();
  range.selectNode(field);
  var selection = getSelection();
  selection.removeAllRanges();
  selection.addRange(range);

  document.execCommand("copy");
  field.parentNode.removeChild(field);
}
