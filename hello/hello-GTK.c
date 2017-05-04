// (File name: hi.c)
// Author: SENOO, Ken
// Lincense: CC0
// (Last update:  2015-06-28T14:16+09:00)


#include <gtk/gtk.h>

int main (int argc, char *argv[])
{
    GtkWidget *window;
    gtk_init (&argc, &argv);
    window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
    gtk_widget_show (window);
    gtk_main ();
    return 0;
}
