// (File name: hello-Qt.cpp)
// Author: SENOO, Ken
// Lincense: CC0

#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>

int main(int argc, char *argv[])
{
  QApplication app(argc, argv);

  QLabel label("Hello World");
  label.show();

  return app.exec();
}
