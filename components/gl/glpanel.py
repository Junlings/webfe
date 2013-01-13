#!/usr/bin/python2.7

import sys
from wx import glcanvas
import numpy as np
import wx
try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print ''' Fehler: PyOpenGL nicht intalliert !!'''
    sys.exit(  )

class wxGLWindow(glcanvas.GLCanvas):
    """Implements a simple wxPython OpenGL window.
    This class provides a simple window,
    into which GL commands can be issued.
    This is done by overriding the built in functions InitGL(), DrawGL(), and FinishGL().
    The main difference between it and the plain wxGLCanvas is that it copes with refreshing and resizing the window
    """

    def __init__(self, parent,*args,**kw):
        self.GL_uninitialised = 1
        
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)
        
        self.init = False
        self.size = None
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        
        # scaling factor
        self.scalingFactorRotation = 0.4
        self.scalingFactorTranslation = 0.4
        self.scalingFactorScaling = 0.1
        
        # moving factor
        self.tx, self.ty, self.tz = 0,0,0
        self.angx,self.rxx, self.rxy, self.rxz = 0,0,0,0
        self.angy,self.ryx, self.ryy, self.ryz = 0,0,0,0
        self.sx, self.sy, self.sz = 1,1,1
        
        # rotationg factor =
        self.Do_rotation = None
        self.Do_scaling = None
        self.Do_translate = None
        
        #
        self.w, self.h = self.GetClientSizeTuple()
        
        #
        self.Bind(wx.EVT_SIZE, self.wxSize)
        self.Bind(wx.EVT_PAINT, self.wxPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.wxEraseBackground)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

    def OnMouseUp(self, evt):
        self.ReleaseMouse()


    def OnLeftMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()


    def OnMouseWheel(self,evt):
        wheelRotation = -evt.GetWheelRotation()
        self.sx = 1-wheelRotation/abs(wheelRotation)*self.scalingFactorScaling
        self.sy = self.sx
        self.sz = self.sx
        self.Do_scaling = True
        #print self.sx
        self.wxRedrawGL()

    def OnMouseMotion(self, evt):

        self.lastx, self.lasty = self.x, self.y
        self.x, self.y = evt.GetPosition()

        deltaX = self.x - self.lastx
        deltaY = self.y - self.lasty


        if evt.Dragging() and evt.RightIsDown():
            self.Do_translate = True
            self.tx = deltaX * self.scalingFactorTranslation
            self.ty = -deltaY * self.scalingFactorTranslation
            self.wxRedrawGL()
    
        elif evt.Dragging() and evt.LeftIsDown():
            self.Do_rotation = True
            self.angx = deltaY * self.scalingFactorRotation
            self.rxx,self.rxy,self.rxz = 1,0,0
            self.angy = deltaX * self.scalingFactorRotation
            self.ryx,self.ryy,self.ryz = 0,1,0
            self.wxRedrawGL()



    def __del__(self):
        #      self.SetCurrent()
        self.FinishGL()

    def InitGL(self):
        """OpenGL initialisation routine (to be overridden).
    
        This routine, containing purely OpenGL commands,
        should be overridden by the user to set up the GL scene.
        If it is not overridden, it defaults to setting an ambient light, setting the background colour to gray, and enabling GL_DEPTH_TEST and GL_COLOR_MATERIAL."""
        return 1

    def FinishGL(self):
        """OpenGL closing routine (to be overridden).

        This routine should be overridden if necessary by any OpenGL commands need to be specified when deleting the GLWindow (e.g. deleting Display Lists)."""
        pass

    def DrawGL(self):
        """OpenGL drawing routine (to be overridden).
    
        This routine, containing purely OpenGL commands, should be overridden by the user to draw the GL scene. If it is not overridden, it defaults to drawing a colour cube."""
        pass

    def wxSize(self, event = None):
        """Called when the window is resized"""
        """Called when the window is resized"""
        pass
    
        self.w,self.h = self.GetClientSizeTuple()
        if self.GetContext():
            self.SetCurrent()
            glViewport(0, 0, self.w, self.h)
            event.Skip()


    def wxEraseBackground(self, evt):
        """Routine does nothing, but prevents flashing"""
        pass        

    def wxPaint(self, event=None):
        #  """Called on a paint event.
        self.SetCurrent(self.context)
        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
          self.InitGL()
          self.init = True
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity( )
    
        self.generate_vertices()
        
        #glutInit()
        #xSize, ySize = glutGet( GLUT_WINDOW_WIDTH ), glutGet( GLUT_WINDOW_HEIGHT )
        #gluPerspective(90, float(xSize) / float(ySize), 0.1, 500)
        glOrtho(-max(self.modelbond)*2,max(self.modelbond)*2,-max(self.modelbond)*2,max(self.modelbond)*2,-10000,100000)
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity( )
        #glTranslatef( -4, 0, -4 )
        glTranslatef((self.modelbond[1]+self.modelbond[0]), (self.modelbond[2]+self.modelbond[3]), (self.modelbond[4]+self.modelbond[5])/2)
    
        self.DrawGL(event)
        self.SwapBuffers()  # Swap buffers

    def wxRedraw(self, event=None):
        """Called on a redraw request
    
        This sets the drawing context, then calls the base routine wxRedrawGL(). It can be called by the user when a refresh is needed"""
        dc = wxClientDC(self)
        self.wxRedrawGL(event)


    def wxRedrawGL(self, event=None):
        """This is the routine called when drawing actually takes place.
    
        It needs to be separate so that it can be called by both paint events and by other events. It should not be called directly"""
        self.SetCurrent(self.context)
        if self.GL_uninitialised:
          glViewport(0, 0, self.w, self.h)
          self.InitGL()
          self.GL_uninitialised=0
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.DrawGL()
        glFlush()                   # Flush
        self.SwapBuffers()  # Swap buffers

    def transformation(self):
        if self.Do_translate != None:
          glTranslatef(self.tx, self.ty, self.tz)
          self.Do_translate = None
    
        elif self.Do_rotation != None:
          glRotatef(self.angx, self.rxx, self.rxy, self.rxz)
          glRotatef(self.angy, self.ryx, self.ryy, self.ryz)
          self.Do_rotation = None
    
        elif self.Do_scaling != None:
          glScalef (self.sx, self.sy, self.sz)
          self.Do_scaling = None

class FEM_3D_window(wxGLWindow):

    def __init__(self,parent,model):#*args,**kargs):
        wxGLWindow.__init__(self,parent)#,args,kargs)
        self.model = model
        self.InitGL()

    def InitGL(self):
        self.generate_vertices()

    def generate_vertices(self,mode='element',factor=1):
        global vertices_line
        global vertices_quad
        global vertices_hex
        global vertices_grid
    

        # distill grids
        vertices_grid = self.model.gl_get_nodetable()#'nodeform',factor)
   
        self.modelbond = self.model.gl_get_modelbound()
        #[grid[:,0].min(),grid[:,0].max(),
        #                grid[:,1].min(),grid[:,1].max(),
        #                grid[:,2].min(),grid[:,2].max()]    
       
       


        vertices_elem = self.model.gl_get_elemtable('nodeform')
    
        grid = np.array(vertices_grid)
    

        #print self.modelbond
        if mode == 'element':
            vertices_line = np.array(vertices_elem['line'])
            vertices_quad = np.array(vertices_elem['quad'])
            vertices_hex =  np.array(vertices_elem['hex'])
            vertices_grid = grid

    def DrawGL(self, event=None):
        #print 'draw new'
    
        self.transformation()
        glEnableClientState(GL_VERTEX_ARRAY)
    
        # create line element
        if len(vertices_line) > 0 :
            glVertexPointerd(vertices_line)
            n_line=len(vertices_line)
            glDrawArrays(GL_LINES, 0, n_line)
    
        #create quad elements
        if len(vertices_quad ) >0:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
            glVertexPointerd(vertices_quad)
            n_quad=len(vertices_quad)
            glDrawArrays(GL_QUADS, 0, n_quad)
    
        
        #create nodes
        glVertexPointerd(vertices_grid)
        n_grid=len(vertices_grid)
        glDrawArrays(GL_POINTS, 0, n_grid)

    def OnRefresh(self,event):
        global vertices_line
        global vertices_quad
        global vertices_hex
        global vertices_grid
        vertices_grid = []
        # distill grids
        temp =coordlist.get_nodetable('nodeform',1)
        vertices_grid.extend(temp)
    
        vertices_elem = {}
        vertices_elem['line'] = []
        vertices_elem['quad'] = []
        vertices_elem['hex'] = []
    
    
        vertices_elem = connlist.get_elemtable(coordlist,vertices_elem,'nodeform')
    
        grid = np.array(vertices_grid)
    
        self.modelbond=[grid[:,0].min(),grid[:,0].max(),
                        grid[:,1].min(),grid[:,1].max(),
                        grid[:,2].min(),grid[:,2].max()]
        #print self.modelbond
    
        vertices_line = []#np.array(vertices_elem['line'])
        vertices_quad = [] #np.array(vertices_elem_input['quad'])
        vertices_hex =  [] #np.array(vertices_elem_input['hex'])
        vertices_grid = grid

'''
class Model3dPanel(wx.Panel):
    def __init__(self,parent = None,id=-1,model=None):
        wx.Panel.__init__(self,parent, id, style = wx.NO_FULL_REPAINT_ON_RESIZE)
        self.model = model
        ## add opengl windows to the frame
        box = wx.BoxSizer(wx.HORIZONTAL)
        glwindow = FEM_3D_window(self,self.model)
        box.Add(glwindow, 1,wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        
        self.Show(True)

    def OnRefresh(self,event):
        global vertices_line
        global vertices_quad
        global vertices_hex
        global vertices_grid
        vertices_grid = []
        # distill grids
        temp =coordlist.get_nodetable('nodeform',1)
        vertices_grid.extend(temp)
    
        vertices_elem = {}
        vertices_elem['line'] = []
        vertices_elem['quad'] = []
        vertices_elem['hex'] = []
    
    
        vertices_elem = connlist.get_elemtable(coordlist,vertices_elem,'nodeform')
    
        grid = np.array(vertices_grid)
    
        self.modelbond=[grid[:,0].min(),grid[:,0].max(),
                        grid[:,1].min(),grid[:,1].max(),
                        grid[:,2].min(),grid[:,2].max()]
        #print self.modelbond
    
        vertices_line = []#np.array(vertices_elem['line'])
        vertices_quad = [] #np.array(vertices_elem_input['quad'])
        vertices_hex =  [] #np.array(vertices_elem_input['hex'])
        vertices_grid = grid

'''


if __name__ == '__main__':

    import sys
    sys.path.append('../..')
    from core.model.registry import model
    from core import settings
    
    model1 = model(settings)
    
    # create node
    model1.node([[0,0,0],
                [1,0,0],
                [2,0,0],
                [3,0,0],
                [3,0,0],
                [5,0,0]])
    
    # create element
    model1.element([[1,2],
                    [2,3],
                    [3,4]])
    app = wx.App()
    f1 = wx.Frame(None)
    p1 = FEM_3D_window(f1,model=model1)
    f1.Show()

    app.MainLoop()
    
