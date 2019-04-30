import maya.cmds as mc
import math as mt


def AADepthOfField():
	# Seleciona o shapeNode
	#Fazer verificacao se o objeto selecionado e uma camera
	myCam = mc.ls(sl=True, long=True)
	myCam = mc.listRelatives(myCam[0])
	print myCam
	
	# Cria um novo Attr Focus Plane caso não exista no cameraShape
	if not ( mc.attributeQuery( "AAfocusPlane", node= myCam[0] ,exists=True)):
		mc.addAttr( myCam[0], ln= "AAfocusPlane", nn= "Focus Plane", at= "bool", k=True)
		mc.setAttr( myCam[0]+".AAfocusPlane", 1)
		mc.setAttr( "cameraShape1.displayCameraNearClip", 1)
		mc.setAttr( "cameraShape1.displayCameraFarClip", 1)
		mc.setAttr( "cameraShape1.displayCameraFrustum", 1)
		
		for i in range(4):
			mc.spaceLocator(p= (0, 0, 0), name="AALocatorFPlane_01")
		
		createFocusPlane()
	
	update(myCam)


def createFocusPlane():
	mc.polyPlane( name= "AAfocusPlane", w= 10, h= 10, sx= 1, sy= 1, ax= (0, 1, 0), cuv= 2, ch= 0)
	
	mySurfaceShader = mc.shadingNode("surfaceShader", asShader=True, name= "AAfocusPlaneShader")
	mc.setAttr( "AAfocusPlaneShader.outColor", 1, 0, 0, type= "double3" )
	mc.setAttr( "AAfocusPlaneShader.outTransparency", 0.6, 0.6, 0.6, type= "double3" )
	
	mc.select( 'AAfocusPlane' )
	mc.hyperShade( assign= mySurfaceShader )
	mc.select( cl=True )
	mc.hyperShade( objects=mySurfaceShader )
	
	#set a visibilidade do plano para o render
	mc.setAttr( "AAfocusPlaneShape.castsShadows", 0)
	mc.setAttr( "AAfocusPlaneShape.receiveShadows", 0)
	mc.setAttr( "AAfocusPlaneShape.holdOut", 0)
	mc.setAttr( "AAfocusPlaneShape.motionBlur", 0)
	mc.setAttr( "AAfocusPlaneShape.primaryVisibility", 0)
	mc.setAttr( "AAfocusPlaneShape.smoothShading", 0)
	mc.setAttr( "AAfocusPlaneShape.visibleInReflections", 0)
	mc.setAttr( "AAfocusPlaneShape.visibleInRefractions", 0)
	mc.setAttr( "AAfocusPlaneShape.doubleSided", 1)
	
	
	
def update( myCam ):
	hFov = mc.camera( myCam[0], q=True, hfv=True)
	vFov = mc.camera( myCam[0], q=True, vfv=True)
	focusDist = mc.camera( myCam[0], q=True, fd=True)
	
	# Faz a matematica para achar a posicao dos vertices no frustum
	right = mt.tan( mt.radians( hFov / 2 )) * focusDist
	left = -right
	top = mt.tan( mt.radians( vFov / 2 )) * focusDist
	bottom = -top
	
	p0 = [left, bottom, -focusDist]
	p1 = [right, bottom, -focusDist]
	p2 = [left, top, -focusDist]
	p3 = [right, top, -focusDist]

	mc.setAttr("AALocatorFPlane_01.translate", p0[0], p0[1], p0[2])
	
	# Set Locators position
	#mc.setAttr("AALocatorFPlane_01.translateX", left)
	#mc.setAttr("AALocatorFPlane_01.translateY", bottom)
	#mc.setAttr("AALocatorFPlane_01.translateZ", -focusDist)
	
	mc.setAttr("AALocatorFPlane_02.translateX", right)
	mc.setAttr("AALocatorFPlane_02.translateY", bottom)
	mc.setAttr("AALocatorFPlane_02.translateZ", -focusDist)
	
	mc.setAttr("AALocatorFPlane_03.translateX", left)
	mc.setAttr("AALocatorFPlane_03.translateY", top)
	mc.setAttr("AALocatorFPlane_03.translateZ", -focusDist)
	
	mc.setAttr("AALocatorFPlane_04.translateX", right)
	mc.setAttr("AALocatorFPlane_04.translateY", top)
	mc.setAttr("AALocatorFPlane_04.translateZ", -focusDist)
	
	L0 = mc.pointPosition( 'AALocatorFPlane_01' )
	L1 = mc.pointPosition( 'AALocatorFPlane_02' )
	L2 = mc.pointPosition( 'AALocatorFPlane_03' )
	L3 = mc.pointPosition( 'AALocatorFPlane_04' )
	
	mc.move( L0[0], L0[1], L0[2], "AAfocusPlane.vtx[0]", a=True)
	mc.move( L1[0], L1[1], L1[2], "AAfocusPlane.vtx[1]", a=True)
	mc.move( L2[0], L2[1], L2[2], "AAfocusPlane.vtx[2]", a=True)
	mc.move( L3[0], L3[1], L3[2], "AAfocusPlane.vtx[3]", a=True)
