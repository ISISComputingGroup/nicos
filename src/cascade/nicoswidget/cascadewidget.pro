CONFIG += qt staticlib
TEMPLATE = lib

HEADERS += ../tofloader.h   ../tofdata.h   ../cascadewidget.h   ../cascadedialogs.h   ../bins.h   ../histogram_item.h
SOURCES += ../tofloader.cpp ../tofdata.cpp ../cascadewidget.cpp ../cascadedialogs.cpp ../bins.cpp ../histogram_item.cpp
LIBS += -lMinuit2 -lgomp -lQtNetwork -lqwt
