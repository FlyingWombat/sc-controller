#!/usr/bin/env python2
"""
SC-Controller - AREA_TO_ACTION

Maps areas on SVG images into actions.
Used by ActionEditor.
"""

from scc.actions import AxisAction, MouseAction, ButtonAction
from scc.actions import HatLeftAction, HatRightAction
from scc.actions import HatUpAction, HatDownAction
from scc.uinput import Keys, Axes, Rels

AREA_TO_ACTION = {
	# Values in tuples: ActionClass, param1, param2...
	
	# Buttons
	'TL'				: (ButtonAction, Keys.BTN_TL),
	'TR'				: (ButtonAction, Keys.BTN_TR),
	'THUMBL'			: (ButtonAction, Keys.BTN_THUMBL),
	'THUMBR'			: (ButtonAction, Keys.BTN_THUMBR),
	'SELECT'			: (ButtonAction, Keys.BTN_SELECT),
	'START'				: (ButtonAction, Keys.BTN_START),
	'A'					: (ButtonAction, Keys.BTN_A),
	'B'					: (ButtonAction, Keys.BTN_B),
	'X'					: (ButtonAction, Keys.BTN_X),
	'Y'					: (ButtonAction, Keys.BTN_Y),
	
	# Dpad
	'DPAD_LEFT'			: (HatLeftAction, Axes.ABS_HAT0X),
	'DPAD_RIGHT'		: (HatRightAction, Axes.ABS_HAT0X),
	'DPAD_UP'			: (HatUpAction, Axes.ABS_HAT0Y),
	'DPAD_DOWN'			: (HatDownAction, Axes.ABS_HAT0Y),
	'ABS_HAT0X'			: (AxisAction, Axes.ABS_HAT0X),
	'ABS_HAT0Y'			: (AxisAction, Axes.ABS_HAT0Y),

	# Left stick
	'LSTICK_LEFT'		: (AxisAction, Axes.ABS_X, 0, -32767),
	'LSTICK_RIGHT'		: (AxisAction, Axes.ABS_X, 0, 32767),
	'LSTICK_UP'			: (AxisAction, Axes.ABS_Y, 0, -32767),
	'LSTICK_DOWN'		: (AxisAction, Axes.ABS_Y, 0, 32767),
	'ABS_X'				: (AxisAction, Axes.ABS_X),
	'ABS_Y'				: (AxisAction, Axes.ABS_Y),

	# Right stick
	'RSTICK_LEFT'		: (AxisAction, Axes.ABS_RX, 0, -32767),
	'RSTICK_RIGHT'		: (AxisAction, Axes.ABS_RX, 0, 32767),
	'RSTICK_UP'			: (AxisAction, Axes.ABS_RY, 0, 32767),
	'RSTICK_DOWN'		: (AxisAction, Axes.ABS_RY, 0, -32767),
	'ABS_RX'			: (AxisAction, Axes.ABS_RX),
	'ABS_RY'			: (AxisAction, Axes.ABS_RY),
	
	# Triggers
	'ABS_Z'				: (AxisAction, Axes.ABS_Z),
	'ABS_RZ'			: (AxisAction, Axes.ABS_RZ),
	
	# Mouse
	'MOUSE_LEFT'		: (MouseAction, Rels.REL_X, -1),
	'MOUSE_RIGHT'		: (MouseAction, Rels.REL_X, 1),
	'MOUSE_UP'			: (MouseAction, Rels.REL_Y, -1),
	'MOUSE_DOWN'		: (MouseAction, Rels.REL_Y, 1,),
	'MOUSE_X'			: (MouseAction, Rels.REL_X, 1),
	'MOUSE_Y'			: (MouseAction, Rels.REL_Y, 1),
	'MOUSE_WHEEL'		: (MouseAction, Rels.REL_WHEEL, 1),
	
	# Mouse buttons
	'MOUSE1'			: (ButtonAction, Keys.BTN_LEFT),
	'MOUSE2'			: (ButtonAction, Keys.BTN_MIDDLE),
	'MOUSE3'			: (ButtonAction, Keys.BTN_RIGHT),
	'MOUSE4'			: (ButtonAction, Rels.REL_WHEEL, 1),
	'MOUSE5'			: (ButtonAction, Rels.REL_WHEEL, -1),
	'MOUSE8'			: (ButtonAction, Keys.BTN_SIDE),
	'MOUSE9'			: (ButtonAction, Keys.BTN_EXTRA),
}

_CLS_TO_AREA = {}
for x in AREA_TO_ACTION:
	cls, params = AREA_TO_ACTION[x][0], AREA_TO_ACTION[x][1:]
	if not cls in _CLS_TO_AREA:
		_CLS_TO_AREA[cls] = []
	_CLS_TO_AREA[cls].append((x, params))


def action_to_area(action):
	"""
	Returns area that matches provided action (both class and parameters)
	or None if there is no such area.
	"""
	cls = action.__class__
	if not cls in _CLS_TO_AREA:
		return None
	for area, pars in _CLS_TO_AREA[cls]:
		if not len(pars) == len(action.parameters):
			continue
		differs = False
		for i in xrange(0, len(pars)):
			if pars[i] != action.parameters[i]:
				differs = True
				break
		if differs : continue
		return area
	return None