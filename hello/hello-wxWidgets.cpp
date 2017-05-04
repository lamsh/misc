// (File name: hello-wxWidgets.cpp)
// Author: SENOO, Ken
// Lincense: CC0

#include <wx/wxprec.h>
#include <wx/wx.h>

class helloApp: public wxApp{
  public:
    virtual bool OnInit();
}

IMPLEMENT_APP(helloApp)

bool helloApp::OnInit(){
  wxMessageBox(wxT("Hello wxWidgets"), wxT("Message Box"), wxOK);
  return false;
}
