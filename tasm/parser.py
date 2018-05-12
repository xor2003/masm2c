# ScummVM - Graphic Adventure Engine
#
# ScummVM is the legal property of its developers, whose names
# are too numerous to list here. Please refer to the COPYRIGHT
# file distributed with this source distribution.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import os, re
from proc import proc
import lex
import op

import traceback
import sys

class parser:
	def __init__(self, skip_binary_data = []):
		self.skip_binary_data = skip_binary_data
		self.strip_path = 0
		self.__globals = {}
		self.__offsets = {}
		self.__stack = []
		self.proc = None
		self.proc_list = []
		self.binary_data = []
		self.c_data = []

		self.symbols = []
		self.link_later = []
		self.data_started = False
		self.prev_data_type = 0
		self.prev_data_ctype = 0

	def visible(self):
		for i in self.__stack:
			if not i or i == 0:
				return False
		return True

	def push_if(self, text):
		value = self.eval(text)
		#print "if %s -> %s" %(text, value)
		self.__stack.append(value)

	def push_else(self):
		#print "else"
		self.__stack[-1] = not self.__stack[-1]

	def pop_if(self):
		#print "endif"
		return self.__stack.pop()

	def set_global(self, name, value):
		if len(name) == 0:
			raise Exception("empty name is not allowed")
		name = name.lower()
		#print "adding global %s -> %s" %(name, value)
		if self.__globals.has_key(name):
			raise Exception("global %s was already defined", name)
		self.__globals[name] = value

	def get_global(self, name):
		name = name.lower()
		try:
			g = self.__globals[name]
		except KeyError:
			print "get_global KeyError %s" %(name)
			raise Exception("KeyError")
		g.used = True
		return g

	def get_globals(self):
		return self.__globals

	def has_global(self, name):
		name = name.lower()
		return self.__globals.has_key(name)

	def set_offset(self, name, value):
		if len(name) == 0:
			raise Exception("empty name is not allowed")
		name = name.lower()
		print "adding offset %s -> %s" %(name, value)
		if self.__offsets.has_key(name):
			raise Exception("offset %s was already defined", name)
		self.__offsets[name] = value

	def get_offset(self, name):
		name = name.lower()
		return self.__offsets[name]
	
	def include(self, basedir, fname):
		path = fname.split('\\')[self.strip_path:]
		path = os.path.join(basedir, os.path.pathsep.join(path))
		#print "including %s" %(path)
		
		self.parse(path)

	def eval(self, stmt):
		try: 
			return self.parse_int(stmt)
		except:
			pass
		value = self.__globals[stmt.lower()].value
		return int(value)
	
	def expr_callback(self, match):
		name = match.group(1).lower()
		g = self.get_global(name)
		if isinstance(g, op.const):
			return g.value
		else:
			return "0x%04x" %g.offset
	
	def eval_expr(self, expr):
		n = 1
		while n > 0:
			expr, n = re.subn(r'\b([a-zA-Z_]+[a-zA-Z0-9_]*)', self.expr_callback, expr)
		#print "~%s~" %(expr)
		expr = expr.strip()
		exprr = expr.lower()
		if exprr[-1] == 'h':
			print "eval_expr: %s" %(expr)
			expr = '0x'.expr[0:len(expr)-1]
			print "eval_expr: %s" %(expr)

		if expr == '?':
			return 0
		try:
			return eval(expr)
		except SyntaxError:
			print "eval_expr SyntaxError ~%s~" %(expr)
			return 0
			
	
	def expand_globals(self, text):
		return text
	
	def fix_dollar(self, v):
		print("$ = %d" %len(self.binary_data))
		return re.sub(r'\$', "%d" %len(self.binary_data), v)

	def parse_int(self, v):
		#print "~1~ %s" %v
		v = v.strip()
		#print "~2~ %s" %v
		if re.match(r'[01]+b$', v):
			v = int(v[:-1], 2)
			#print "~2~ %i" %v
		if re.match(r'[\+-]?[0-9a-fA-F]+[Hh]$', v):
			v = int(v[:-1], 16)
#			v = hex(int(v[:-1], 16))
			#print "~3~ %i" %v
		#print "~4~ %s" %v
		return int(v)
#		return v
	
	def compact_data(self, width, data):
		#print "COMPACTING %d %s" %(width, data)
		r = []
		base = 0x100 if width == 1 else 0x10000
		for v in data:
			v = v.strip()
			if v[0] == "'":
				if v[-1] != "'":
					raise Exception("invalid string %s" %v)
				if width == 2:
					raise Exception("string with data width more than 1") #we could allow it :)
				for i in xrange(1, len(v) - 1):
					r.append(ord(v[i]))
				continue
			
			m = re.match(r'(\w+)\s+dup\s+\((\s*\S+\s*)\)', v)
			if m is not None:
				#we should parse that
				n = self.parse_int(m.group(1))
				if m.group(2) != '?':
					value = self.parse_int(m.group(2))
				else:
					value = 0
				for i in xrange(0, n):
					v = value
					for b in xrange(0, width):
						r.append(v & 0xff);
						v >>= 8
				continue
			
			try:
				v = self.parse_int(v)
				if v < 0:
					v += base
			except:
				#global name
				print "global/expr: %s" %v
				try:
					g = self.get_global(v)
					v = g.offset
				except:
					print "unknown address %s" %(v)
					self.link_later.append((len(self.binary_data) + len(r), v))
					v = 0
		
			for b in xrange(0, width):
				r.append(v & 0xff);
				v >>= 8
		#print r
		return r

	def compact_cdata(self, label, width, data):
		print "COMPACTING %s %d %s" %(label, width, data)
		first = True
		string = False
		elements = 0
		data_ctype = {1: 'uint8_t', 2: 'uint16_t', 4: 'uint32_t'}[width]
		r = []
		base = 0x100 if width == 1 else 0x10000
		for v in data:
			v = v.strip()
			#if width == 1 and (v[0] == '"' or v[0] == "'"):
			if width == 1 and (v[0] == "'"):
				#if v[-1] != '"' and v[-1] != "'":
				if v[-1] != "'":
					raise Exception("invalid string %s" %v)
				if width > 1:
					raise Exception("string with data width more than 1") #we could allow it :)
				#for i in xrange(1, len(v) - 1):
					#r.append(ord(v[i]))
				for i in xrange(1, len(v) - 1):
					r.append(v[i])

				string = True
				continue

				'''
				print "~1~: v = %s" %v
				v = v.replace("'", r'"')
				vv = ""
				vvv = ""

				if len(label) and first:
					vv = "\nconst char * const " + label + " = { "
					if self.strings_started == True:
						vv = "}" + vv
				for i in xrange(1, len(v) - 1):
					vvv += "'" + v[i] + "'"
					if i != len(v) - 1:
						vvv += ","

				r.append(vv + vvv)
				first = False
				'''
			
			m = re.match(r'(\w+)\s+dup\s+\(\s*(\S+)\s*\)', v)
			if m is not None:
				#we should parse that
				n = self.parse_int(m.group(1))
				if m.group(2) != '?':
					value = self.parse_int(m.group(2))
				else:
					value = 0

				for i in xrange(0, n):
					v = value
					r.append(v);
				elements += n
				first = False
				continue
			
			try:	
				elements += 1
				#print "1: ~%s~" %v
				v = v.strip()
				#print "2: ~%s~" %v
				if v == '?':
					v = '0'
				v = self.parse_int(v)
				#print "3: ~%s~" %v
				#print "4: ~%s~" %v
				if v < 0:
					v += base
				#print "5: ~%s~" %v

			except:
				#global name
				#traceback.print_stack(file=sys.stdout)
				print "global/expr: ~%s~" %v
				vv = v.split()
				#print vv
				if vv[0] == "offset":
					v = vv[1]

					data_ctype += r"*"
					v = "&" + vv[1]
					r.append(v);

				#print "global/expr: ~%s~" %v
				try:
					g = self.get_global(v)
					v = g.offset
				except:
					print "unknown address %s" %(v)
					self.link_later.append((len(self.binary_data) + len(r), v))
					v = 0
		
			r.append(v);

			first = False

		cur_data_type = 0
		if string:
			if len(r) >= 1 and r[-1] == 0:
				cur_data_type = 1 # 0 terminated
			else:
				cur_data_type = 2 # array string
				#string = False
				#cur_data_type = 4 # array

		else:
			cur_data_type = 3 # numbers
			if elements > 1:
				cur_data_type = 4 # array

		if self.prev_data_type == 4 and cur_data_type == 3 and len(label)==0 and data_ctype == self.prev_data_ctype: # if no label and it was same size and number or array
				cur_data_type = 4 # array

		#print "current data type = %d current data c type = %s" %(cur_data_type, data_ctype)
		print "current data type = %d current data c type = %s" %(cur_data_type, data_ctype)
  	        vv = ""
		if (self.prev_data_type != 0 and (cur_data_type != self.prev_data_type or data_ctype != self.prev_data_ctype)) or len(label) or self.prev_data_type == 1 or self.prev_data_type == 3:
			if self.prev_data_type == 4 or self.prev_data_type == 2:
				vv += "}"
			vv += ";\n"
		else: 
			if self.prev_data_type != 0 and (cur_data_type == 2 or cur_data_type == 3 or cur_data_type == 4):
				vv += ","

		if len(label):
		    if cur_data_type == 1: # 0 terminated string
				vv += "const char * const " + label + " = "

		    elif cur_data_type == 2: # array string
				vv += "const char " + label + "[] = { "

		    elif cur_data_type == 3: # numbers
				vv += data_ctype + " " + label
				vv += " = "

		    elif cur_data_type == 4: # array
				vv += data_ctype + " " + label
				vv += "[] = {"

		if cur_data_type == 1:
				vv += "\""
				for i in xrange(0, len(r)-1):
					if isinstance(r[i], int):
						if r[i] == 13:
							vv += r"\r"
						elif r[i] == 10:
							vv += r"\n"
						else:
							vv += chr(r[i])
					else:
						vv += r[i]
				vv += "\""
				r = []
				r.append(vv)

		elif cur_data_type == 2:
				for i in xrange(0, len(r)):
					    if isinstance(r[i], int):
						if r[i] == 13:
							vv += r"'\r'"
						elif r[i] == 10:
							vv += r"'\n'"
						else:
							vv += r"'" + str(r[i]) + r"'"
					    else:
						vv += "'" + r[i] + "'"
					    if i != len(r)-1:
						vv += ","
				r = []
				r.append(vv)

		elif cur_data_type == 4:
				for i in xrange(0, len(r)):
					vv += str(r[i])
					if i != len(r)-1:
						vv += ","
				r = []
				r.append(vv)

		elif cur_data_type == 3:
				vv += str(r[0])
				r = []
				r.append(vv)
		'''
		elif cur_data_type == 4:
			for i in xrange(0, len(r)):
				vv += str(r[i])
				if i != len(r)-1:
					vv += ","
			r = []
			r.append(vv)
		'''

		print r
		print "retturinging" 
		self.prev_data_type = cur_data_type
		self.prev_data_ctype = data_ctype
		self.data_started = True
		return r

	def parse(self, fname):
#		print "opening file %s..." %(fname, basedir)
		self.line_number = 0
		skipping_binary_data = False
		fd = open(fname, 'rb')
		for line in fd:
			self.line_number += 1
			line = line.strip()
			if len(line) == 0 or line[0] == ';' or line[0] == chr(0x1a):
				continue

			#print line
			m = re.match('(\w+)\s*?::?', line)
			if m is not None:
				line = line[len(m.group(0)):].strip()
				if self.visible():
					name = m.group(1)
					if not (name.lower() in self.skip_binary_data):
						print "offset %s -> %d" %(name, len(self.binary_data))
						if self.proc is not None:
							self.proc.add_label(name)
							self.set_offset(name, (len(self.binary_data), self.proc, len(self.proc.stmts) if self.proc is not None else 0))
						else:
							print "Label %s is outside the procedure" %name
						skipping_binary_data = False
					else:
						print "skipping binary data for %s" % (name,)
						skipping_binary_data = True
			print "%d:      %s" %(self.line_number, line)

			cmd = line.split()
			if len(cmd) == 0:
				continue
			
			cmd0 = str(cmd[0])
			if cmd0 == 'if':
				self.push_if(cmd[1])
				continue
			elif cmd0 == 'else':
				self.push_else()
				continue
			elif cmd0 == 'endif':
				self.pop_if()
				continue
			
			if not self.visible():
				continue

			if cmd0 == 'db' or cmd0 == 'dw' or cmd0 == 'dd':
				arg = line[len(cmd0):].strip()
				if not skipping_binary_data:
					print "%d:1: %s" %(len(self.binary_data), arg) #fixme: COPYPASTE
					binary_width = {'b': 1, 'w': 2, 'd': 4}[cmd0[1]]
					self.binary_data += self.compact_data(binary_width, lex.parse_args(arg))
					self.c_data += self.compact_cdata("", binary_width, lex.parse_args(arg))
				continue
			elif cmd0 == 'include':
				self.include(os.path.dirname(fname), cmd[1])
				continue
			elif cmd0 == 'endp' or (len(cmd) >= 2 and str(cmd[1]) == 'endp'):
				self.proc = None
				continue
			elif cmd0 == 'assume':
				print "skipping: %s" %line
				continue
			elif cmd0 == 'rep':
				self.proc.add(cmd0)
				self.proc.add(" ".join(cmd[1:]))
				continue
			
			if len(cmd) >= 3:
				cmd1 = cmd[1]
				if cmd1 == 'equ':
					if not (cmd0.lower() in self.skip_binary_data):
						v = cmd[2]
						self.set_global(cmd0, op.const(self.fix_dollar(v)))
					else:
						print "skipping binary data for %s" % (cmd0.lower(),)
						skipping_binary_data = True
				elif cmd1 == 'db' or cmd1 == 'dw' or cmd1 == 'dd':
					if not (cmd0.lower() in self.skip_binary_data):
						binary_width = {'b': 1, 'w': 2, 'd': 4}[cmd1[1]]
						offset = len(self.binary_data)
						arg = line[len(cmd0):].strip()
						arg = arg[len(cmd1):].strip()
						print "%d: %s" %(offset, arg)
						self.binary_data += self.compact_data(binary_width, lex.parse_args(arg))
						self.c_data += self.compact_cdata(cmd0, binary_width, lex.parse_args(arg))
						self.set_global(cmd0.lower(), op.var(binary_width, offset))
						skipping_binary_data = False
					else:
						print "skipping binary data for %s" % (cmd0.lower(),)
						skipping_binary_data = True
					continue
				elif cmd1 == 'proc':
					name = cmd0.lower()
					self.proc = proc(name)
					print "procedure %s, #%d" %(name, len(self.proc_list))
					self.proc_list.append(name)
					self.set_global(name, self.proc)
					continue
			if (self.proc):
				self.proc.add(line)
			else:
				#print line
				pass
			
		fd.close()
		return self

	def link(self):
		for addr, expr in self.link_later:
			try:
				v = self.eval_expr(expr)
				print "link: patching %04x -> %04x" %(addr, v)
			except:
				print "link: Exception %s" %expr
				continue
			while v != 0:
				self.binary_data[addr] = v & 0xff
				addr += 1
				v >>= 8
