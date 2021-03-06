# This file was automatically generated by pywxrc.
# -*- coding: UTF-8 -*-

import wx
import wx.xrc as xrc

__res = None

def get_resources():
    """ This function provides access to the XML resources in this module."""
    global __res
    if __res == None:
        __init_resources()
    return __res




class xrcPoleDiag(wx.Dialog):
#!XRCED:begin-block:xrcPoleDiag.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcPoleDiag.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreDialog()
        self.PreCreate(pre)
        get_resources().LoadOnDialog(pre, parent, "PoleDiag")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.DEEP_DENT = xrc.XRCCTRL(self, "DEEP_DENT")
        self.CRIT_LENGTH = xrc.XRCCTRL(self, "CRIT_LENGTH")
        self.NEEDFILL = xrc.XRCCTRL(self, "NEEDFILL")
        self.NEEDWRAP = xrc.XRCCTRL(self, "NEEDWRAP")
        self.WRAPLEFT = xrc.XRCCTRL(self, "WRAPLEFT")
        self.WRAPRIGHT = xrc.XRCCTRL(self, "WRAPRIGHT")
        self.RIGHTEND_XCOORD = xrc.XRCCTRL(self, "RIGHTEND_XCOORD")
        self.RIGHTEND_RAD = xrc.XRCCTRL(self, "RIGHTEND_RAD")
        self.LEFTEND_XCOORD = xrc.XRCCTRL(self, "LEFTEND_XCOORD")
        self.LEFTEND_RAD = xrc.XRCCTRL(self, "LEFTEND_RAD")
        self.LENGTH_INCR = xrc.XRCCTRL(self, "LENGTH_INCR")
        self.LENGTH_RAd = xrc.XRCCTRL(self, "LENGTH_RAd")
        self.PARA_leftplatecenterx = xrc.XRCCTRL(self, "PARA_leftplatecenterx")
        self.PARA_rightplatecenterx = xrc.XRCCTRL(self, "PARA_rightplatecenterx")
        self.PARA_plateheighty = xrc.XRCCTRL(self, "PARA_plateheighty")
        self.PARA_lengthx = xrc.XRCCTRL(self, "PARA_lengthx")
        self.PARA_heighty = xrc.XRCCTRL(self, "PARA_heighty")
        self.PARA_stiffness = xrc.XRCCTRL(self, "PARA_stiffness")
        self.PoleProcess = xrc.XRCCTRL(self, "PoleProcess")





# ------------------------ Resource data ----------------------

def __init_resources():
    global __res
    __res = xrc.EmptyXmlResource()

    wx.FileSystem.AddHandler(wx.MemoryFSHandler())

    Pole_diag2_xrc = '''\
<?xml version="1.0" ?><resource>
  <object class="wxDialog" name="PoleDiag">
    <title>Pole Pre-Process </title>
    <style>wxDEFAULT_DIALOG_STYLE|wxCAPTION|wxSYSTEM_MENU</style>
    <object class="wxBoxSizer">
      <orient>wxVERTICAL</orient>
      <object class="sizeritem">
        <object class="wxBoxSizer">
          <orient>wxVERTICAL</orient>
          <object class="sizeritem">
            <object class="wxStaticBoxSizer">
              <label>Dent Material Option</label>
              <orient>wxVERTICAL</orient>
              <object class="sizeritem">
                <object class="wxGridSizer">
                  <cols>2</cols>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Deepest dent</label>
                    </object>
                    <flag>wxALL|wxEXPAND|wxALIGN_CENTRE_VERTICAL|wxALIGN_CENTRE_HORIZONTAL</flag>
                  </object>
                  <rows>6</rows>
                  <vgap>5</vgap>
                  <hgap>5</hgap>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="DEEP_DENT">
                      <value>50</value>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Critical Length</label>
                    </object>
                    <flag>wxALL|wxEXPAND|wxALIGN_CENTRE_VERTICAL|wxALIGN_CENTRE_HORIZONTAL</flag>
                  </object>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="CRIT_LENGTH">
                      <value>50</value>
                      <style/>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Need Fill?</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxCheckBox" name="NEEDFILL">
                      <label/>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Need Wrap</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxCheckBox" name="NEEDWRAP">
                      <label/>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Wrap left coord</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="WRAPLEFT"/>
                  </object>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Wrap right  coord</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="WRAPRIGHT"/>
                  </object>
                </object>
                <flag>wxALL|wxEXPAND|wxALIGN_CENTRE_VERTICAL</flag>
              </object>
            </object>
            <option>1</option>
            <flag>wxALL|wxEXPAND</flag>
          </object>
          <object class="spacer">
            <size>20,20</size>
          </object>
          <object class="sizeritem">
            <object class="wxStaticBoxSizer">
              <label>Dimensions</label>
              <orient>wxVERTICAL</orient>
              <object class="sizeritem">
                <object class="wxGridSizer">
                  <cols>2</cols>
                  <rows>7</rows>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Coord X_rightend (+)</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="RIGHTEND_XCOORD"/>
                  </object>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Raidus_rightend</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="RIGHTEND_RAD"/>
                  </object>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Coord X_leftend    (-)</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="LEFTEND_XCOORD"/>
                  </object>
                  <vgap>5</vgap>
                  <hgap>5</hgap>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Raidus_leftend</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="LEFTEND_RAD"/>
                  </object>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Segments of Length</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="LENGTH_INCR"/>
                  </object>
                  <object class="sizeritem">
                    <object class="wxStaticText">
                      <label>Segments of Circumstance</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxTextCtrl" name="LENGTH_RAd"/>
                  </object>
                </object>
                <flag>wxEXPAND</flag>
              </object>
            </object>
            <flag>wxEXPAND</flag>
          </object>
          <object class="spacer">
            <size>20,20</size>
          </object>
          <object class="sizeritem">
            <object class="wxBoxSizer">
              <orient>wxHORIZONTAL</orient>
              <object class="sizeritem">
                <object class="wxStaticBoxSizer">
                  <label>Loading Plate</label>
                  <orient>wxVERTICAL</orient>
                  <object class="sizeritem">
                    <object class="wxGridSizer">
                      <cols>2</cols>
                      <rows>6</rows>
                      <object class="sizeritem">
                        <object class="wxStaticText">
                          <label>left load  X</label>
                        </object>
                      </object>
                      <object class="sizeritem">
                        <object class="wxTextCtrl" name="PARA_leftplatecenterx"/>
                      </object>
                      <object class="sizeritem">
                        <object class="wxStaticText">
                          <label>right load X</label>
                        </object>
                      </object>
                      <object class="sizeritem">
                        <object class="wxTextCtrl" name="PARA_rightplatecenterx"/>
                      </object>
                      <object class="sizeritem">
                        <object class="wxStaticText">
                          <label>Load range Y</label>
                        </object>
                      </object>
                      <object class="sizeritem">
                        <object class="wxTextCtrl" name="PARA_plateheighty"/>
                      </object>
                      <object class="sizeritem">
                        <object class="wxStaticText">
                          <label>Plate length (x)</label>
                        </object>
                      </object>
                      <object class="sizeritem">
                        <object class="wxTextCtrl" name="PARA_lengthx"/>
                      </object>
                      <vgap>5</vgap>
                      <hgap>5</hgap>
                      <object class="sizeritem">
                        <object class="wxStaticText">
                          <label>Plate height y</label>
                        </object>
                      </object>
                      <object class="sizeritem">
                        <object class="wxTextCtrl" name="PARA_heighty"/>
                      </object>
                      <object class="sizeritem">
                        <object class="wxStaticText">
                          <label>spring stiffness</label>
                        </object>
                      </object>
                      <object class="sizeritem">
                        <object class="wxTextCtrl" name="PARA_stiffness"/>
                      </object>
                    </object>
                    <flag>wxEXPAND</flag>
                  </object>
                </object>
                <option>1</option>
              </object>
            </object>
            <flag>wxEXPAND</flag>
          </object>
          <object class="spacer">
            <size>20,20</size>
          </object>
          <object class="sizeritem">
            <object class="wxBoxSizer">
              <orient>wxHORIZONTAL</orient>
              <object class="sizeritem">
                <object class="wxGridSizer">
                  <cols>2</cols>
                  <rows>1</rows>
                  <hgap>5</hgap>
                  <object class="sizeritem">
                    <object class="wxButton">
                      <label>Help</label>
                    </object>
                  </object>
                  <object class="sizeritem">
                    <object class="wxButton" name="PoleProcess">
                      <label>Process</label>
                    </object>
                  </object>
                </object>
              </object>
            </object>
            <flag>wxALIGN_RIGHT</flag>
          </object>
        </object>
        <option>1</option>
        <flag>wxALL|wxEXPAND</flag>
        <border>10</border>
      </object>
    </object>
  </object>
</resource>'''

    wx.MemoryFSHandler.AddFile('XRC/Pole_diag2/Pole_diag2_xrc', Pole_diag2_xrc)
    __res.Load('memory:XRC/Pole_diag2/Pole_diag2_xrc')

