from __future__ import absolute_import
from __future__ import print_function

from masm2c.cpp import Cpp
from masm2c.parser import Parser
import traceback
import unittest

from random import randint


# Random order for tests runs. (Original is: -1 if x<y, 0 if x==y, 1 if x>y).
#unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: randint(-1, 1)

class ParserDataTest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.cpp = Cpp(self.parser)

    def test_data_10012(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="Dw seg default_seg")), ('seg_offset(default_seg), // dummy0_0\n', 'dw dummy0_0;\n', 2))

    def test_data_10011(self):
        self.parser.action_label(far=False, name='@df@@@@8', isproc=False)
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw @df@@@@8")), ('m2c::karbdfarbarbarbarb8, // dummy0_0\n', 'dw dummy0_0;\n', 2))

    def test_data_10010(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="ASCII DB '00000000',0Dh,0Ah,'$' ; buffer for ASCII string")), ("{'0','0','0','0','0','0','0','0','\\r','\\n','$'}, // ascii\n", 'char ascii[11];\n', 11))

    def test_data_10020(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_a070295122642\tdb '07/02/95 12:26:42',0 ; DATA XREF: seg003:off_2462E\x19o")), ('"07/02/95 12:26:42", // _a070295122642\n', 'char _a070295122642[18];\n', 18))

    def test_data_10030(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_a100Assembler\tdb '100% assembler!'")), ("{'1','0','0','%',' ','a','s','s','e','m','b','l','e','r','!'}, // _a100assembler\n", 'char _a100assembler[15];\n', 15))

    def test_data_10240(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aChannels	db 'Channels      :'")), ("{'C','h','a','n','n','e','l','s',' ',' ',' ',' ',' ',' ',':'}, // _achannels\n", 'char _achannels[15];\n', 15))

    def test_data_10260(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aConfigFileNotF	db 'Config file not found. Run ISETUP first',0Dh,0Ah,'$'")), ("{'C','o','n','f','i','g',' ','f','i','l','e',' ','n','o','t',' ','f','o','u','n','d','.',' ','R','u','n',' ','I','S','E','T','U','P',' ','f','i','r','s','t','\\r','\\n','$'}, // _aconfigfilenotf\n", 'char _aconfigfilenotf[42];\n', 42))

    def test_data_10270(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aCopyrightC1994	db 'Copyright (c) 1994,1995 by Stefan Danes and Ramon van Gorkom',0")), ('"Copyright (c) 1994,1995 by Stefan Danes and Ramon van Gorkom", // _acopyrightc1994\n', 'char _acopyrightc1994[61];\n', 61))

    def test_data_10290(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aCouldNotFindThe db 'Could not find the ULTRASND environment string',0Dh,0Ah,0")), ('"Could not find the ULTRASND environment string\\r\\n", // _acouldnotfindthe\n', 'char _acouldnotfindthe[49];\n', 49))

    def test_data_10320(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aCriticalErrorT	db 0Dh,0Ah		; DATA XREF: _start+31o")), ('{13,10}, // _acriticalerrort\n', 'db _acriticalerrort[2];\n', 2))

    def test_data_10340(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aCurrentSoundcard db 0Dh,'Current Soundcard settings:',0Dh,0Ah ; DATA XREF: _start:loc_19057o")), ("{'\\r','C','u','r','r','e','n','t',' ','S','o','u','n','d','c','a','r','d',' ','s','e','t','t','i','n','g','s',':','\\r','\\n'}, // _acurrentsoundcard\n", 'char _acurrentsoundcard[30];\n', 30))

    def test_data_10360(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aCursor		db 7Fh")), ('127, // _acursor\n', 'db _acursor;\n', 1))

    def test_data_10370(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aCursor_0	db 'Cursor ',1Bh,' '")), ("{'C','u','r','s','o','r',' ',27,' '}, // _acursor_0\n", 'char _acursor_0[9];\n', 9))

    def test_data_10390(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aDecIncAmplify	db 7Eh")), ('126, // _adecincamplify\n', 'db _adecincamplify;\n', 1))

    def test_data_10460(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aDeletingFile	db 'Deleting file: '    ; DATA XREF: _start+69Fo")), ("{'D','e','l','e','t','i','n','g',' ','f','i','l','e',':',' '}, // _adeletingfile\n", 'char _adeletingfile[15];\n', 15))

    def test_data_10490(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aDisableBpmOnOff db ' Disable BPM on/off'")), ("{' ','D','i','s','a','b','l','e',' ','B','P','M',' ','o','n','/','o','f','f'}, // _adisablebpmonoff\n", 'char _adisablebpmonoff[19];\n', 19))

    def test_data_10520(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aDosShellTypeExitT_0 db	'DOS Shell (Type EXIT to return)'")), ("{'D','O','S',' ','S','h','e','l','l',' ','(','T','y','p','e',' ','E','X','I','T',' ','t','o',' ','r','e','t','u','r','n',')'}, // _adosshelltypeexitt_0\n", 'char _adosshelltypeexitt_0[31];\n', 31))

    def test_data_10530(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aDosShellTypeExitToR db	'  DOS Shell (Type EXIT to return)'")), ("{' ',' ','D','O','S',' ','S','h','e','l','l',' ','(','T','y','p','e',' ','E','X','I','T',' ','t','o',' ','r','e','t','u','r','n',')'}, // _adosshelltypeexittor\n", 'char _adosshelltypeexittor[33];\n', 33))

    def test_data_10540(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aDramDma	db ', DRAM-DMA '")), ("{',',' ','D','R','A','M','-','D','M','A',' '}, // _adramdma\n", 'char _adramdma[11];\n', 11))

    def test_data_10550(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aE_command	db 'E_Command      ',0")), ('"E_Command      ", // _ae_command\n', 'char _ae_command[16];\n', 16))

    def test_data_10560(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aE_g_		db 'E.G.'")), ("{'E','.','G','.'}, // _ae_g_\n", 'char _ae_g_[4];\n', 4))

    def test_data_10640(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aErrorSoundcardN db 'Error: Soundcard not found!',0Dh,0Ah,'$',0")), ('"Error: Soundcard not found!\\r\\n$", // _aerrorsoundcardn\n', 'char _aerrorsoundcardn[31];\n', 31))

    def test_data_10670(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF1		db 'F-1'")), ("{'F','-','1'}, // _af1\n", 'char _af1[3];\n', 3))

    def test_data_10690(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF10_0		db 'F-10'")), ("{'F','-','1','0'}, // _af10_0\n", 'char _af10_0[4];\n', 4))

    def test_data_10700(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF10_1		db 'F-10'")), ("{'F','-','1','0'}, // _af10_1\n", 'char _af10_1[4];\n', 4))

    def test_data_10720(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF11_0		db 'F-11'")), ("{'F','-','1','1'}, // _af11_0\n", 'char _af11_0[4];\n', 4))

    def test_data_10730(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF11_1		db 'F-11'")), ("{'F','-','1','1'}, // _af11_1\n", 'char _af11_1[4];\n', 4))

    def test_data_10740(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF12		db 7Fh")), ('127, // _af12\n', 'db _af12;\n', 1))

    def test_data_10750(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF12_0		db 'F-12'")), ("{'F','-','1','2'}, // _af12_0\n", 'char _af12_0[4];\n', 4))

    def test_data_10760(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF12_1		db 'F-12'")), ("{'F','-','1','2'}, // _af12_1\n", 'char _af12_1[4];\n', 4))

    def test_data_10770(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF2_0		db 'F-2'")), ("{'F','-','2'}, // _af2_0\n", 'char _af2_0[3];\n', 3))

    def test_data_10780(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF3_0		db 'F-3'")), ("{'F','-','3'}, // _af3_0\n", 'char _af3_0[3];\n', 3))

    def test_data_10790(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF4_0		db 'F-4'")), ("{'F','-','4'}, // _af4_0\n", 'char _af4_0[3];\n', 3))

    def test_data_10800(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF5_0		db 'F-5'")), ("{'F','-','5'}, // _af5_0\n", 'char _af5_0[3];\n', 3))

    def test_data_10810(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF8_0		db 'F-8'")), ("{'F','-','8'}, // _af8_0\n", 'char _af8_0[3];\n', 3))

    def test_data_10820(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF8_1		db 'F-8'")), ("{'F','-','8'}, // _af8_1\n", 'char _af8_1[3];\n', 3))

    def test_data_10830(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF9		db ' [F-9]              ',0")), ('" [F-9]              ", // _af9\n', 'char _af9[21];\n', 21))

    def test_data_10840(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF9_0		db ' [F-9]',0")), ('" [F-9]", // _af9_0\n', 'char _af9_0[7];\n', 7))

    def test_data_10860(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF9_2		db 'F-9'")), ("{'F','-','9'}, // _af9_2\n", 'char _af9_2[3];\n', 3))

    def test_data_10870(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF9_3		db 'F-9'")), ("{'F','-','9'}, // _af9_3\n", 'char _af9_3[3];\n', 3))

    def test_data_10880(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aF9_4		db 'F-9'")), ("{'F','-','9'}, // _af9_4\n", 'char _af9_4[3];\n', 3))

    def test_data_10890(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aFar		db 'FAR■'")), ("{'F','A','R','\\xfe'}, // _afar\n", 'char _afar[4];\n', 4))

    def test_data_10920(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aFastErForward	db '  Fast(er) forward'")), ("{' ',' ','F','a','s','t','(','e','r',')',' ','f','o','r','w','a','r','d'}, // _afasterforward\n", 'char _afasterforward[18];\n', 18))

    def test_data_10930(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aFastErRewind	db '  Fast(er) rewind'")), ("{' ',' ','F','a','s','t','(','e','r',')',' ','r','e','w','i','n','d'}, // _afasterrewind\n", 'char _afasterrewind[17];\n', 17))

    def test_data_10950(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aFidonet	db 'FidoNet  : '")), ("{'F','i','d','o','N','e','t',' ',' ',':',' '}, // _afidonet\n", 'char _afidonet[11];\n', 11))

    def test_data_10960(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aFile		db 'File'               ; DATA XREF: _start+689w _start+6A8o")), ("{'F','i','l','e'}, // _afile\n", 'char _afile[4];\n', 4))

    def test_data_10980(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aFilename_0	db 'Filename      : '")), ("{'F','i','l','e','n','a','m','e',' ',' ',' ',' ',' ',' ',':',' '}, // _afilename_0\n", 'char _afilename_0[16];\n', 16))

    def test_data_10990(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aFilename_ext	db 'FileName.Ext'       ; DATA XREF: _read_module:loc_19E41o")), ("{'F','i','l','e','N','a','m','e','.','E','x','t'}, // _afilename_ext\n", 'char _afilename_ext[12];\n', 12))

    def test_data_11010(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aFinePortVolsl	db 'Fine Port+VolSl',0")), ('"Fine Port+VolSl", // _afineportvolsl\n', 'char _afineportvolsl[16];\n', 16))

    def test_data_11050(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aFineVibrVolsl	db 'Fine Vibr+VolSl',0")), ('"Fine Vibr+VolSl", // _afinevibrvolsl\n', 'char _afinevibrvolsl[16];\n', 16))

    def test_data_11140(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aGeneralMidi	db 'General MIDI',0     ; DATA XREF: dseg:02BEo")), ('"General MIDI", // _ageneralmidi\n', 'char _ageneralmidi[13];\n', 13))

    def test_data_11150(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aGeneralMidi_0	db 'General MIDI',0     ; DATA XREF: seg003:0D6Eo")), ('"General MIDI", // _ageneralmidi_0\n', 'char _ageneralmidi_0[13];\n', 13))

    def test_data_11190(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aGravisUltrasou	db 'Gravis UltraSound',0 ; DATA XREF: dseg:_table_sndcrdnameo")), ('"Gravis UltraSound", // _agravisultrasou\n', 'char _agravisultrasou[18];\n', 18))

    def test_data_11200(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aGravisUltrasoun db 'Gravis UltraSound',0 ; DATA XREF: seg003:_snd_cards_offso")), ('"Gravis UltraSound", // _agravisultrasoun\n', 'char _agravisultrasoun[18];\n', 18))

    def test_data_11220(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aGray_0		db 'Gray - +'")), ("{'G','r','a','y',' ','-',' ','+'}, // _agray_0\n", 'char _agray_0[8];\n', 8))

    def test_data_11240(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aGuess___	db '  Guess...'")), ("{' ',' ','G','u','e','s','s','.','.','.'}, // _aguess___\n", 'char _aguess___[10];\n', 10))

    def test_data_11250(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aHGf1Irq	db 'h, GF1-IRQ '")), ("{'h',',',' ','G','F','1','-','I','R','Q',' '}, // _ahgf1irq\n", 'char _ahgf1irq[11];\n', 11))

    def test_data_11270(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aHitBackspaceToRe db 'Hit backspace to return to playmode, F-1 for help, QuickRead='")), ("{'H','i','t',' ','b','a','c','k','s','p','a','c','e',' ','t','o',' ','r','e','t','u','r','n',' ','t','o',' ','p','l','a','y','m','o','d','e',',',' ','F','-','1',' ','f','o','r',' ','h','e','l','p',',',' ','Q','u','i','c','k','R','e','a','d','='}, // _ahitbackspacetore\n", 'char _ahitbackspacetore[61];\n', 61))

    def test_data_11310(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aIfYouHaveBugReports db	'If you have bug-reports, suggestions or comments send a message t'")), ("{'I','f',' ','y','o','u',' ','h','a','v','e',' ','b','u','g','-','r','e','p','o','r','t','s',',',' ','s','u','g','g','e','s','t','i','o','n','s',' ','o','r',' ','c','o','m','m','e','n','t','s',' ','s','e','n','d',' ','a',' ','m','e','s','s','a','g','e',' ','t'}, // _aifyouhavebugreports\n", 'char _aifyouhavebugreports[65];\n', 65))

    def test_data_11340(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aInertiaModule	db 'Inertia Module: ',0 ; DATA XREF: _useless_writeinr+29o")), ('"Inertia Module: ", // _ainertiamodule\n', 'char _ainertiamodule[17];\n', 17))

    def test_data_11350(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aInertiaModule_0 db 'Inertia Module: ',0 ; DATA XREF: _useless_writeinr+23o")), ('"Inertia Module: ", // _ainertiamodule_0\n', 'char _ainertiamodule_0[17];\n', 17))

    def test_data_11360(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aInertiaModule_1 db 'Inertia Module: '")), ("{'I','n','e','r','t','i','a',' ','M','o','d','u','l','e',':',' '}, // _ainertiamodule_1\n", 'char _ainertiamodule_1[16];\n', 16))

    def test_data_11380(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aInertiaPlayerV1_ db 'Inertia Player V1.22 written by Stefan Danes and Ramon van Gorkom'")), ("{'I','n','e','r','t','i','a',' ','P','l','a','y','e','r',' ','V','1','.','2','2',' ','w','r','i','t','t','e','n',' ','b','y',' ','S','t','e','f','a','n',' ','D','a','n','e','s',' ','a','n','d',' ','R','a','m','o','n',' ','v','a','n',' ','G','o','r','k','o','m'}, // _ainertiaplayerv1_\n", 'char _ainertiaplayerv1_[65];\n', 65))

    def test_data_11390(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aInertiaPlayerV1_22A db	'Inertia Player V1.22 Assembly ',27h,'94 CD Edition by Sound Solution'")), ("{'I','n','e','r','t','i','a',' ','P','l','a','y','e','r',' ','V','1','.','2','2',' ','A','s','s','e','m','b','l','y',' ',39,'9','4',' ','C','D',' ','E','d','i','t','i','o','n',' ','b','y',' ','S','o','u','n','d',' ','S','o','l','u','t','i','o','n'}, // _ainertiaplayerv1_22a\n", 'char _ainertiaplayerv1_22a[62];\n', 62))

    def test_data_11410(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aInertiaSample	db 'Inertia Sample: '   ; DATA XREF: _useless_writeinr_118+11o")), ("{'I','n','e','r','t','i','a',' ','S','a','m','p','l','e',':',' '}, // _ainertiasample\n", 'char _ainertiasample[16];\n', 16))

    def test_data_11420(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aInternet	db 'Internet : '")), ("{'I','n','t','e','r','n','e','t',' ',':',' '}, // _ainternet\n", 'char _ainternet[11];\n', 11))

    def test_data_11440(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aJanfebmaraprmayj db '   JanFebMarAprMayJunJulAugSepOctNovDec'")), ("{' ',' ',' ','J','a','n','F','e','b','M','a','r','A','p','r','M','a','y','J','u','n','J','u','l','A','u','g','S','e','p','O','c','t','N','o','v','D','e','c'}, // _ajanfebmaraprmayj\n", 'char _ajanfebmaraprmayj[39];\n', 39))

    def test_data_11470(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aKb		db 'KB',0               ; DATA XREF: _text_init2+1D7o")), ('"KB", // _akb\n', 'char _akb[3];\n', 3))

    def test_data_11480(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aKhz		db 'kHz',0              ; DATA XREF: seg003:117Bo seg003:11ADo ...")), ('"kHz", // _akhz\n', 'char _akhz[4];\n', 4))

    def test_data_11490(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aListFileNotFou	db 'List file not found.',0Dh,0Ah,'$' ; DATA XREF: _start+D07o")), ("{'L','i','s','t',' ','f','i','l','e',' ','n','o','t',' ','f','o','u','n','d','.','\\r','\\n','$'}, // _alistfilenotfou\n", 'char _alistfilenotfou[23];\n', 23))

    def test_data_11500(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aListserver@oliver_s db	'listserver@oliver.sun.ac.za'")), ("{'l','i','s','t','s','e','r','v','e','r','@','o','l','i','v','e','r','.','s','u','n','.','a','c','.','z','a'}, // _alistserverarboliver_s\n", 'char _alistserverarboliver_s[27];\n', 27))

    def test_data_11510(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aLoadingModule	db 'Loading module',0   ; DATA XREF: _start+41Ao")), ('"Loading module", // _aloadingmodule\n', 'char _aloadingmodule[15];\n', 15))

    def test_data_11560(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aMK		db 'M&K!'")), ("{'M','&','K','!'}, // _amk\n", 'char _amk[4];\n', 4))

    def test_data_11570(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aMK_0		db 'M!K!'")), ("{'M','!','K','!'}, // _amk_0\n", 'char _amk_0[4];\n', 4))

    def test_data_11580(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aM_k_		db 'M.K.'")), ("{'M','.','K','.'}, // _am_k_\n", 'char _am_k_[4];\n', 4))

    def test_data_11590(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aMainVolume	db 'Main Volume   :'")), ("{'M','a','i','n',' ','V','o','l','u','m','e',' ',' ',' ',':'}, // _amainvolume\n", 'char _amainvolume[15];\n', 15))

    def test_data_11610(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aMarkedToDelete	db '<Marked to Delete>    ',0 ; DATA XREF: _filelist_198B8+10Do")), ('"<Marked to Delete>    ", // _amarkedtodelete\n', 'char _amarkedtodelete[23];\n', 23))

    def test_data_11630(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aMixedAt	db ', mixed at ',0      ; DATA XREF: seg003:1173o seg003:11A5o ...")), ('", mixed at ", // _amixedat\n', 'char _amixedat[12];\n', 12))

    def test_data_11640(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aModuleIsCorrupt db 'Module is corrupt!',0 ; DATA XREF: _start+439o")), ('"Module is corrupt!", // _amoduleiscorrupt\n', 'char _amoduleiscorrupt[19];\n', 19))

    def test_data_11650(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aModuleLoadErro	db 'Module load error.',0Dh,0Ah,'$' ; DATA XREF: _readallmoules+1Bo")), ("{'M','o','d','u','l','e',' ','l','o','a','d',' ','e','r','r','o','r','.','\\r','\\n','$'}, // _amoduleloaderro\n", 'char _amoduleloaderro[21];\n', 21))

    def test_data_11660(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aModuleNotFound	db 'Module not found.',0Dh,0Ah,'$' ; DATA XREF: _find_mods+88o")), ("{'M','o','d','u','l','e',' ','n','o','t',' ','f','o','u','n','d','.','\\r','\\n','$'}, // _amodulenotfound\n", 'char _amodulenotfound[20];\n', 20))

    def test_data_11670(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aModuleType_0	db 'Module Type   : '")), ("{'M','o','d','u','l','e',' ','T','y','p','e',' ',' ',' ',':',' '}, // _amoduletype_0\n", 'char _amoduletype_0[16];\n', 16))

    def test_data_11690(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aMute		db '<Mute>                ',0 ; DATA XREF: seg001:1949o")), ('"<Mute>                ", // _amute\n', 'char _amute[23];\n', 23))

    def test_data_11710(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aName		db 'name'               ; DATA XREF: _start+692w")), ("{'n','a','m','e'}, // _aname\n", 'char _aname[4];\n', 4))

    def test_data_11730(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aNotEnoughDram_0 db 'Not enough DRAM on your UltraSound to load all samples!',0")), ('"Not enough DRAM on your UltraSound to load all samples!", // _anotenoughdram_0\n', 'char _anotenoughdram_0[56];\n', 56))

    def test_data_11740(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aNotEnoughMemo_0 db 'Not enough memory available to load all samples!',0")), ('"Not enough memory available to load all samples!", // _anotenoughmemo_0\n', 'char _anotenoughmemo_0[49];\n', 49))

    def test_data_11750(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aNotEnoughMemor	db 'Not enough memory.',0Dh,0Ah,'$' ; DATA XREF: _start+23Do")), ("{'N','o','t',' ','e','n','o','u','g','h',' ','m','e','m','o','r','y','.','\\r','\\n','$'}, // _anotenoughmemor\n", 'char _anotenoughmemor[21];\n', 21))

    def test_data_11790(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aNtsc		db '(NTSC)',0           ; DATA XREF: _txt_draw_bottom+53o")), ('"(NTSC)", // _antsc\n', 'char _antsc[7];\n', 7))

    def test_data_11810(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aPal		db '(PAL) ',0           ; DATA XREF: _txt_draw_bottom+49o")), ('"(PAL) ", // _apal\n', 'char _apal[7];\n', 7))

    def test_data_11850(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aPcHonker	db 'PC Honker',0        ; DATA XREF: dseg:02BCo")), ('"PC Honker", // _apchonker\n', 'char _apchonker[10];\n', 10))

    def test_data_11860(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aPcHonker_0	db 'PC Honker',0        ; DATA XREF: seg003:0D6Co")), ('"PC Honker", // _apchonker_0\n', 'char _apchonker_0[10];\n', 10))

    def test_data_11890(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aPlayer13029521	db 'Player: '")), ("{'P','l','a','y','e','r',':',' '}, // _aplayer13029521\n", 'char _aplayer13029521[8];\n', 8))

    def test_data_11900(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aPlayingInStereoFree db	' Playing in Stereo, Free:'")), ("{' ','P','l','a','y','i','n','g',' ','i','n',' ','S','t','e','r','e','o',',',' ','F','r','e','e',':'}, // _aplayinginstereofree\n", 'char _aplayinginstereofree[25];\n', 25))

    def test_data_11910(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aPlaypausloop	db 'PlayPausLoop'       ; DATA XREF: _txt_draw_bottom+164o")), ("{'P','l','a','y','P','a','u','s','L','o','o','p'}, // _aplaypausloop\n", 'char _aplaypausloop[12];\n', 12))

    def test_data_11920(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aPortVolslide	db 'Port + VolSlide',0")), ('"Port + VolSlide", // _aportvolslide\n', 'char _aportvolslide[16];\n', 16))

    def test_data_11980(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aPressF1ForHelpQu db '                 Press F-1 for help, QuickRead='")), ("{' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','P','r','e','s','s',' ','F','-','1',' ','f','o','r',' ','h','e','l','p',',',' ','Q','u','i','c','k','R','e','a','d','='}, // _apressf1forhelpqu\n", 'char _apressf1forhelpqu[47];\n', 47))

    def test_data_11990(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aProAudioSpectr	db 'Pro Audio Spectrum 16',0 ; DATA XREF: dseg:02ACo")), ('"Pro Audio Spectrum 16", // _aproaudiospectr\n', 'char _aproaudiospectr[22];\n', 22))

    def test_data_12000(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aProAudioSpectrum db 'Pro Audio Spectrum 16',0 ; DATA XREF: seg003:0D5Co")), ('"Pro Audio Spectrum 16", // _aproaudiospectrum\n', 'char _aproaudiospectrum[22];\n', 22))

    def test_data_12020(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aProtracker1_0Compat db	'  ProTracker 1.0 compatibility on/off'")), ("{' ',' ','P','r','o','T','r','a','c','k','e','r',' ','1','.','0',' ','c','o','m','p','a','t','i','b','i','l','i','t','y',' ','o','n','/','o','f','f'}, // _aprotracker1_0compat\n", 'char _aprotracker1_0compat[37];\n', 37))

    def test_data_12030(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aProtracker1_0_0 db ' ProTracker 1.0'")), ("{' ','P','r','o','T','r','a','c','k','e','r',' ','1','.','0'}, // _aprotracker1_0_0\n", 'char _aprotracker1_0_0[15];\n', 15))

    def test_data_12040(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aPsm		db 'PSM■'")), ("{'P','S','M','\\xfe'}, // _apsm\n", 'char _apsm[4];\n', 4))

    def test_data_12070(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aRetrigVolume	db 'Retrig+Volume  ',0")), ('"Retrig+Volume  ", // _aretrigvolume\n', 'char _aretrigvolume[16];\n', 16))

    def test_data_12090(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aReturnToPlaymodeOnl db	'Return to playmode [Only if the music is playing]'")), ("{'R','e','t','u','r','n',' ','t','o',' ','p','l','a','y','m','o','d','e',' ','[','O','n','l','y',' ','i','f',' ','t','h','e',' ','m','u','s','i','c',' ','i','s',' ','p','l','a','y','i','n','g',']'}, // _areturntoplaymodeonl\n", 'char _areturntoplaymodeonl[49];\n', 49))

    def test_data_12100(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSamplename	db '# SampleName   '    ; DATA XREF: seg001:1B7Co")), ("{'#',' ','S','a','m','p','l','e','N','a','m','e',' ',' ',' '}, // _asamplename\n", 'char _asamplename[15];\n', 15))

    def test_data_12110(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSamplesUsed	db 'Samples Used  :'")), ("{'S','a','m','p','l','e','s',' ','U','s','e','d',' ',' ',':'}, // _asamplesused\n", 'char _asamplesused[15];\n', 15))

    def test_data_12120(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aScream		db '!Scream!'")), ("{'!','S','c','r','e','a','m','!'}, // _ascream\n", 'char _ascream[8];\n', 8))

    def test_data_12150(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSdanes@marvels_hack db	'sdanes@marvels.hacktic.nl'")), ("{'s','d','a','n','e','s','@','m','a','r','v','e','l','s','.','h','a','c','k','t','i','c','.','n','l'}, // _asdanesarbmarvels_hack\n", 'char _asdanesarbmarvels_hack[25];\n', 25))

    def test_data_12180(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSetFilter	db 'Set Filter     ',0  ; DATA XREF: seg001:1A9Ao")), ('"Set Filter     ", // _asetfilter\n', 'char _asetfilter[16];\n', 16))

    def test_data_12200(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSetLoopPoint	db 'Set Loop Point ',0  ; DATA XREF: seg001:1A8Fo")), ('"Set Loop Point ", // _asetlooppoint\n', 'char _asetlooppoint[16];\n', 16))

    def test_data_12260(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aShell130295211	db 'Shell: 13/02/95 21:15:58'")), ("{'S','h','e','l','l',':',' ','1','3','/','0','2','/','9','5',' ','2','1',':','1','5',':','5','8'}, // _ashell130295211\n", 'char _ashell130295211[24];\n', 24))

    def test_data_12270(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aShellingToOperating db	'Shelling to Operating System...'")), ("{'S','h','e','l','l','i','n','g',' ','t','o',' ','O','p','e','r','a','t','i','n','g',' ','S','y','s','t','e','m','.','.','.'}, // _ashellingtooperating\n", 'char _ashellingtooperating[31];\n', 31))

    def test_data_12280(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSizeVolModeC2T	db '~   Size Vol Mode  C-2 Tune LoopPos LoopEnd',0")), ('"~   Size Vol Mode  C-2 Tune LoopPos LoopEnd", // _asizevolmodec2t\n', 'char _asizevolmodec2t[44];\n', 44))

    def test_data_12290(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSoYouWantedSomeHelp db	'So you wanted some help?'")), ("{'S','o',' ','y','o','u',' ','w','a','n','t','e','d',' ','s','o','m','e',' ','h','e','l','p','?'}, // _asoyouwantedsomehelp\n", 'char _asoyouwantedsomehelp[24];\n', 24))

    def test_data_12300(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSomeFunctionsOf db 'Some functions of the UltraSound do not work!',0Dh,0Ah")), ("{'S','o','m','e',' ','f','u','n','c','t','i','o','n','s',' ','o','f',' ','t','h','e',' ','U','l','t','r','a','S','o','u','n','d',' ','d','o',' ','n','o','t',' ','w','o','r','k','!','\\r','\\n'}, // _asomefunctionsof\n", 'char _asomefunctionsof[47];\n', 47))

    def test_data_12310(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSoundBlaster	db 'Sound Blaster',0    ; DATA XREF: dseg:02B4o")), ('"Sound Blaster", // _asoundblaster\n', 'char _asoundblaster[14];\n', 14))

    def test_data_12320(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSoundBlaster16	db 'Sound Blaster 16/16ASP',0 ; DATA XREF: dseg:02B0o")), ('"Sound Blaster 16/16ASP", // _asoundblaster16\n', 'char _asoundblaster16[23];\n', 23))

    def test_data_12330(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSoundBlaster1616 db 'Sound Blaster 16/16ASP',0 ; DATA XREF: seg003:0D60o")), ('"Sound Blaster 16/16ASP", // _asoundblaster1616\n', 'char _asoundblaster1616[23];\n', 23))

    def test_data_12340(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSoundBlasterPr	db 'Sound Blaster Pro',0 ; DATA XREF: dseg:02B2o")), ('"Sound Blaster Pro", // _asoundblasterpr\n', 'char _asoundblasterpr[18];\n', 18))

    def test_data_12350(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSoundBlasterPro db 'Sound Blaster Pro',0 ; DATA XREF: seg003:0D62o")), ('"Sound Blaster Pro", // _asoundblasterpro\n', 'char _asoundblasterpro[18];\n', 18))

    def test_data_12360(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSoundBlaster_0	db 'Sound Blaster',0    ; DATA XREF: seg003:0D64o")), ('"Sound Blaster", // _asoundblaster_0\n', 'char _asoundblaster_0[14];\n', 14))

    def test_data_12380(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aStereoOn1	db 'Stereo-On-1',0      ; DATA XREF: dseg:02B8o")), ('"Stereo-On-1", // _astereoon1\n', 'char _astereoon1[12];\n', 12))

    def test_data_12390(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aStereoOn1_0	db 'Stereo-On-1',0      ; DATA XREF: seg003:0D68o")), ('"Stereo-On-1", // _astereoon1_0\n', 'char _astereoon1_0[12];\n', 12))

    def test_data_12400(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSubscribeInertiaLis db	'subscribe inertia-list YourRealName'")), ("{'s','u','b','s','c','r','i','b','e',' ','i','n','e','r','t','i','a','-','l','i','s','t',' ','Y','o','u','r','R','e','a','l','N','a','m','e'}, // _asubscribeinertialis\n", 'char _asubscribeinertialis[35];\n', 35))

    def test_data_12410(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aSubscribeInertiaTal db	'subscribe inertia-talk YourRealName',0")), ('"subscribe inertia-talk YourRealName", // _asubscribeinertiatal\n', 'char _asubscribeinertiatal[36];\n', 36))

    def test_data_12460(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aThisHelpScreenButIG db	'This help screen, but I guess you already found it...'")), ("{'T','h','i','s',' ','h','e','l','p',' ','s','c','r','e','e','n',',',' ','b','u','t',' ','I',' ','g','u','e','s','s',' ','y','o','u',' ','a','l','r','e','a','d','y',' ','f','o','u','n','d',' ','i','t','.','.','.'}, // _athishelpscreenbutig\n", 'char _athishelpscreenbutig[53];\n', 53))

    def test_data_12470(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aThisProgramRequ db 'This program requires the soundcards device driver.',0Dh,0Ah,0")), ('"This program requires the soundcards device driver.\\r\\n", // _athisprogramrequ\n', 'char _athisprogramrequ[54];\n', 54))

    def test_data_12480(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aToConnectToBinaryIn db	'To connect to Binary Inertia releases: '")), ("{'T','o',' ','c','o','n','n','e','c','t',' ','t','o',' ','B','i','n','a','r','y',' ','I','n','e','r','t','i','a',' ','r','e','l','e','a','s','e','s',':',' '}, // _atoconnecttobinaryin\n", 'char _atoconnecttobinaryin[39];\n', 39))

    def test_data_12490(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aToConnectToDiscussi db	'To connect to Discussion Mailing list: '")), ("{'T','o',' ','c','o','n','n','e','c','t',' ','t','o',' ','D','i','s','c','u','s','s','i','o','n',' ','M','a','i','l','i','n','g',' ','l','i','s','t',':',' '}, // _atoconnecttodiscussi\n", 'char _atoconnecttodiscussi[39];\n', 39))

    def test_data_12540(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aToggle24bitInt	db 7Eh")), ('126, // _atoggle24bitint\n', 'db _atoggle24bitint;\n', 1))

    def test_data_12590(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aTrackPosition	db 'Track Position:'")), ("{'T','r','a','c','k',' ','P','o','s','i','t','i','o','n',':'}, // _atrackposition\n", 'char _atrackposition[15];\n', 15))

    def test_data_12650(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aUnused256	db ' Unused'")), ("{'\x7f',' ','U','n','u','s','e','d'}, // _aunused256\n", 'char _aunused256[8];\n', 8))

    def test_data_12670(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aVibrVolslide	db 'Vibr + VolSlide',0")), ('"Vibr + VolSlide", // _avibrvolslide\n', 'char _avibrvolslide[16];\n', 16))

    def test_data_12700(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aViewSampleNamesTwic db	'  View sample names (twice for more)'")), ("{' ',' ','V','i','e','w',' ','s','a','m','p','l','e',' ','n','a','m','e','s',' ','(','t','w','i','c','e',' ','f','o','r',' ','m','o','r','e',')'}, // _aviewsamplenamestwic\n", 'char _aviewsamplenamestwic[36];\n', 36))

    def test_data_12710(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aVolumeAmplify	db 'Volume Amplify:'")), ("{'V','o','l','u','m','e',' ','A','m','p','l','i','f','y',':'}, // _avolumeamplify\n", 'char _avolumeamplify[15];\n', 15))

    def test_data_12750(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aWindowsSoundSy	db 'Windows Sound System',0 ; DATA XREF: dseg:02AEo")), ('"Windows Sound System", // _awindowssoundsy\n', 'char _awindowssoundsy[21];\n', 21))

    def test_data_12760(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aWindowsSoundSyst db 'Windows Sound System',0 ; DATA XREF: seg003:0D5Eo")), ('"Windows Sound System", // _awindowssoundsyst\n', 'char _awindowssoundsyst[21];\n', 21))

    def test_data_12770(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aXpressF4ForMor	db 'xPress F-4 for more'")), ("{'x','P','r','e','s','s',' ','F','-','4',' ','f','o','r',' ','m','o','r','e'}, // _axpressf4formor\n", 'char _axpressf4formor[19];\n', 19))

    def test_data_12780(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_a_ext		db '.Ext'               ; DATA XREF: _start+69Bw")), ("{'.','E','x','t'}, // _a_ext\n", 'char _a_ext[4];\n', 4))

    def test_data_12790(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_a_m_k		db '.M.K'")), ("{'.','M','.','K'}, // _a_m_k\n", 'char _a_m_k[4];\n', 4))

    def test_data_12800(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_a_mod_nst_669_s	db '.MOD.NST.669.STM.S3M.MTM.PSM.WOW.INR.FAR.ULT.OKT.OCT',0,0,0,0")), ('".MOD.NST.669.STM.S3M.MTM.PSM.WOW.INR.FAR.ULT.OKT.OCT\\0\\0\\0", // _a_mod_nst_669_s\n', 'char _a_mod_nst_669_s[56];\n', 56))

    def test_data_12810(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_amount_of_x	dw 0			; DATA XREF: _read_module+75w")), ('0, // _amount_of_x\n', 'dw _amount_of_x;\n', 2))

    def test_data_12820(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_amplification	dw 100			; DATA XREF: _clean_11C43+83w")), ('100, // _amplification\n', 'dw _amplification;\n', 2))

    def test_data_12830(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_asmprintf_tbl	dw offset _mysprintf_0_nop ; DATA XREF: _myasmsprintf+1Cr")), ('_mysprintf_0_nop, // _asmprintf_tbl\n', 'dw _asmprintf_tbl;\n', 2))

    def test_data_12840(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_atop_title	dw 152h			; DATA XREF: _txt_draw_top_title+12o")), ('338, // _atop_title\n', 'dw _atop_title;\n', 2))

    def test_data_12860(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_bit_mode	db 8			; DATA XREF: sub_12DA8+55w")), ('8, // _bit_mode\n', 'db _bit_mode;\n', 1))

    def test_data_12870(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_bottom_menu	dw 0Ah			; DATA XREF: _text_init2+21Fo")), ('10, // _bottom_menu\n', 'dw _bottom_menu;\n', 2))

    def test_data_12880(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_buffer_1DBEC	db 0			; DATA XREF: _find_mods+32o")), ('0, // _buffer_1dbec\n', 'db _buffer_1dbec;\n', 1))

    def test_data_12890(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_buffer_1DC6C	dd 0			; DATA XREF: _start+2C5w _start+2D3o ...")), ('0, // _buffer_1dc6c\n', 'dd _buffer_1dc6c;\n', 4))

    def test_data_12920(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_byte_11C29	db 0			; DATA XREF: sub_11C0C:loc_11C14r")), ('0, // _byte_11c29\n', 'db _byte_11c29;\n', 1))

    def test_data_12930(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_byte_13C54	db 0,9,12h,1Bh,24h,2Dh,36h,40h,40h,4Ah,53h,5Ch,65h,6Eh")), ('{0,9,18,27,36,45,54,64,64,74,83,92,101,110}, // _byte_13c54\n', 'db _byte_13c54[14];\n', 14))

    def test_data_12990(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_byte_1CCEB	db 78h			; DATA XREF: _text_init2:loc_1A6C2w")), ('120, // _byte_1cceb\n', 'db _byte_1cceb;\n', 1))

    def test_data_13000(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_byte_1D616	db 20h			; DATA XREF: _useless_197F2+Dw")), ('32, // _byte_1d616\n', 'db _byte_1d616;\n', 1))

    def test_data_13010(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_byte_1D66B	db 20h			; DATA XREF: _useless_197F2+18w")), ('32, // _byte_1d66b\n', 'db _byte_1d66b;\n', 1))

    def test_data_13020(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_byte_1DC0A	db 62h dup(0)		; DATA XREF: _find_mods+6Fo")), ('{0}, // _byte_1dc0a\n', 'db _byte_1dc0a[98];\n', 98))

    def test_data_13030(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_byte_1DCF7	db 0FFh			; DATA XREF: _callsubx+1Cr _callsubx+55w")), ('255, // _byte_1dcf7\n', 'db _byte_1dcf7;\n', 1))

    def test_data_13090(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_byte_280E7	db ?			; DATA XREF: _s3m_module+1F3w")), ('0, // _byte_280e7\n', 'db _byte_280e7;\n', 1))

    def test_data_13100(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_byte_282E8	db 20h dup( ?)		; DATA XREF: _clean_11C43+AEo")), ('{0}, // _byte_282e8\n', 'db _byte_282e8[32];\n', 32))

    def test_data_13140(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_byte_3150A	db ?			; DATA XREF: _psm_module+139r")), ('0, // _byte_3150a\n', 'db _byte_3150a;\n', 1))

    def test_data_13160(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_chrin		dd ?			; DATA XREF: _moduleread:loc_10033o")), ('0, // _chrin\n', 'dd _chrin;\n', 4))

    def test_data_13180(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_configword	dw 218Bh		; DATA XREF: _start+60w	_start+6Cw ...")), ('8587, // _configword\n', 'dw _configword;\n', 2))

    def test_data_13300(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_dword_1DCEC	dd 10524E49h		; DATA XREF: _loadcfg+1Ar")), ('273829449, // _dword_1dcec\n', 'dd _dword_1dcec;\n', 4))

    def test_data_13320(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_dword_3063D	dd ?			; DATA XREF: _ult_module+225r")), ('0, // _dword_3063d\n', 'dd _dword_3063d;\n', 4))

    def test_data_13330(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_eModuleNotFound	db 'Module not found',0Dh,0Ah,0 ; DATA XREF: _moduleread+1Co")), ('"Module not found\\r\\n", // _emodulenotfound\n', 'char _emodulenotfound[19];\n', 19))

    @unittest.skip("to check")
    def test_data_13340(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_effoff_18F60	dw offset _eff_nullsub	; DATA XREF: sub_137D5+16r")), ('k_eff_nullsub, // _effoff_18f60\n', 'dw _effoff_18f60;\n', 2))

    def test_data_13400(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_f1_help_text	dw 3F8h			; DATA XREF: seg001:1CD8o")), ('1016, // _f1_help_text\n', 'dw _f1_help_text;\n', 2))

    def test_data_13450(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_frameborder	db '      ██████╔╗╚╝═║┌┐└┘─│╓╖╙╜─║╒╕╘╛═│',0 ; DATA XREF: _draw_frame+3Do")), ('"      '
 '\\xdb\\xdb\\xdb\\xdb\\xdb\\xdb\\xc9\\xbb\\xc8\\xbc\\xcd\\xba\\xda\\xbf\\xc0\\xd9\\xc4\\xb3\\xd6\\xb7\\xd3\\xbd\\xc4\\xba\\xd5\\xb8\\xd4\\xbe\\xcd\\xb3", '
 '// _frameborder\n',
 'char _frameborder[37];\n',
                                                                                                                                                                                     37))

    def test_data_13530(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_hopeyoulike	dw 3C6h			; DATA XREF: _start+204o")), ('966, // _hopeyoulike\n', 'dw _hopeyoulike;\n', 2))

    def test_data_13690(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_module_type_text dd 20202020h		; DATA XREF: _mod_n_t_modulew")), ('538976288, // _module_type_text\n', 'dd _module_type_text;\n', 4))

    def test_data_13700(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_module_type_txt	db '    '               ; DATA XREF: _read_module+6Fw")), ("{' ',' ',' ',' '}, // _module_type_txt\n", 'char _module_type_txt[4];\n', 4))

    def test_data_13760(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_msg		db 'Searching directory for modules  ',0 ; DATA XREF: _start+2F7o")), ('"Searching directory for modules  ", // _msg\n', 'char _msg[34];\n', 34))

    def test_data_13790(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_my_in		db ?			; DATA XREF: __2stm_module+50o")), ('0, // _my_in\n', 'db _my_in;\n', 1))

    def test_data_13820(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_myendl		db 0Dh,0Ah,'$'          ; DATA XREF: _start-1Do")), ("{'\\r','\\n','$'}, // _myendl\n", 'char _myendl[3];\n', 3))

    def test_data_13840(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_myin_0		db ?			; DATA XREF: _ult_module+3Ao")), ('0, // _myin_0\n', 'db _myin_0;\n', 1))

    def test_data_13870(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_notes		db '  C-C#D-D#E-F-F#G-G#A-A#B-' ; DATA XREF: seg001:1930r")), ("{' ',' ','C','-','C','#','D','-','D','#','E','-','F','-','F','#','G','-','G','#','A','-','A','#','B','-'}, // _notes\n", 'char _notes[26];\n', 26))

    @unittest.skip("to check")
    def test_data_13880(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_offs_draw	dw offset loc_19050	; DATA XREF: _keyb_screen_loop+32r")), ('kloc_19050, // _offs_draw\n', 'dw _offs_draw;\n', 2))

    def test_data_13980(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_pc_timer_tbl	db 40h,40h,40h,40h,40h,40h,40h,40h,40h,40h,3Fh,3Fh,3Fh")), ('{64,64,64,64,64,64,64,64,64,64,63,63,63}, // _pc_timer_tbl\n', 'db _pc_timer_tbl[13];\n', 13))

    def test_data_14030(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_s3mtable_108D6	db 0FFh,10h,0Bh,0Dh,15h,12h,11h,13h,14h,1Bh,1Dh,17h,16h")), ('{255,16,11,13,21,18,17,19,20,27,29,23,22}, // _s3mtable_108d6\n', 'db _s3mtable_108d6[13];\n', 13))

    def test_data_14040(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_s3mtable_108F0	db 0,3,5,4,7,0FFh,0FFh,0FFh,8,0FFh,0FFh,6,0Ch,0Dh,0FFh")), ('{0,3,5,4,7,255,255,255,8,255,255,6,12,13,255}, // _s3mtable_108f0\n', 'db _s3mtable_108f0[15];\n', 15))

    def test_data_14050(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_sIplay_cfg	db 'IPLAY.CFG',0     ; DATA XREF: _loadcfgo")), ('"IPLAY.CFG", // _siplay_cfg\n', 'char _siplay_cfg[10];\n', 10))

    def test_data_14140(self):
        self.assertEqual(
            self.cpp.produce_c_data_single(self.parser.action_data(line=r"_slider		db '─\|/─\|/'")),
            (r"{'\xc4','\\','|','/','\xc4','\\','|','/'}, // _slider"+"\n",
             'char _slider[8];\n',
             8))

    def test_data_14160(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_snd_base_port_0	dw 0FFFFh		; DATA XREF: _callsubx+3r _callsubx+45w")), ('65535, // _snd_base_port_0\n', 'dw _snd_base_port_0;\n', 2))

    def test_data_14180(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_aGravisUltrasoun db 'Gravis UltraSound',0 ; DATA XREF: seg003:_snd_cards_offso")), ('"Gravis UltraSound", // _agravisultrasoun\n', 'char _agravisultrasoun[18];\n', 18))
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_snd_cards_offs	dw offset _aGravisUltrasoun ; DATA XREF:	seg003:114Eo")), ('offset(default_seg,_agravisultrasoun), // _snd_cards_offs\n', 'dw _snd_cards_offs;\n', 2))

    def test_data_14260(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_13EC3	db 140,50,25,15,10,7,6,4,3,3,2,2,2,2,1,1 ; DATA	XREF: sub_13E9B+Dr")), ('{140,50,25,15,10,7,6,4,3,3,2,2,2,2,1,1}, // _table_13ec3\n', 'db _table_13ec3[16];\n', 16))

    def test_data_14270(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_14057	db 0FFh,80h,40h,2Ah,20h,19h,15h,12h,10h,0Eh,0Ch,0Bh,0Ah")), ('{255,128,64,42,32,25,21,18,16,14,12,11,10}, // _table_14057\n', 'db _table_14057[13];\n', 13))

    def test_data_14290(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_24716	dw 8000h,9000h,0A000h,0A952h,0B000h,0B521h,0B952h,0BCDEh")), ('{32768,36864,40960,43346,45056,46369,47442,48350}, // _table_24716\n', 'dw _table_24716[8];\n', 16))

    def test_data_14300(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_24798	dw 8000h,9800h,0A000h,0A800h,0B000h,0B400h,0B800h,0BC00h")), ('{32768,38912,40960,43008,45056,46080,47104,48128}, // _table_24798\n', 'dw _table_24798[8];\n', 16))

    def test_data_14310(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_24818	dw 8000h,9800h,0A000h,0A800h,0B000h,0B400h,0B800h,0BC00h")), ('{32768,38912,40960,43008,45056,46080,47104,48128}, // _table_24818\n', 'dw _table_24818[8];\n', 16))

    def test_data_14320(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_24898	db 1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh")), ('{30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30}, // _table_24898\n', 'db _table_24898[16];\n', 16))

    def test_data_14330(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_25118	dw 1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906,856,808,762,720,678,640,604,570,538,508,480,453")), ('{1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906,856,808,762,720,678,640,604,570,538,508,480,453}, // _table_25118\n', 'dw _table_25118[24];\n', 48))

    def test_data_14340(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_251C0	db  0,18h,31h,4Ah,61h,78h,8Dh,0A1h,0B4h,0C5h,0D4h,0E0h")), ('{0,24,49,74,97,120,141,161,180,197,212,224}, // _table_251c0\n', 'db _table_251c0[12];\n', 12))

    def test_data_14350(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_251E0	db  0,15h,20h,29h,30h,37h,3Dh,44h,49h,4Fh,54h,59h,5Eh")), ('{0,21,32,41,48,55,61,68,73,79,84,89,94}, // _table_251e0\n', 'db _table_251e0[13];\n', 13))

    def test_data_14360(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_25221	db  0, 4, 8,0Ch,10h,14h,18h,1Ch,20h,24h,28h,2Ch,30h,34h")), ('{0,4,8,12,16,20,24,28,32,36,40,44,48,52}, // _table_25221\n', 'db _table_25221[14];\n', 14))

    def test_data_14370(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_25261	db  0, 4, 8,0Ch,10h,14h,18h,1Ch,20h,24h,28h,2Ch,30h,34h")), ('{0,4,8,12,16,20,24,28,32,36,40,44,48,52}, // _table_25261\n', 'db _table_25261[14];\n', 14))

    @unittest.skip("to check")
    def test_data_14380(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_table_sndcrdname dw offset _aGravisUltrasou ; DATA XREF:	_text_init2+19Dr")), ('0, // _table_sndcrdname\n', 'dw _table_sndcrdname;\n', 2))

    def test_data_14390(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_tabledword_24526 dd    0,65536,46340,25079,12785,6423,3215,1608, 804, 402")), ('{0,65536,46340,25079,12785,6423,3215,1608,804,402}, // _tabledword_24526\n', 'dd _tabledword_24526[10];\n', 40))

    def test_data_14400(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_tabledword_24562 dd -131072,-65536,-19196,-4989,-1260,-316, -79, -20,  -5")), ('{4294836224,4294901760,4294948100,4294962307,4294966036,4294966980,4294967217,4294967276,4294967291}, // _tabledword_24562\n', 'dd _tabledword_24562[9];\n', 36))

    def test_data_14420(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_vga_palette	db 0,0,0		; DATA XREF: _init_vga_waves+1Fo")), ('{0}, // _vga_palette\n', 'db _vga_palette[3];\n', 3))

    def test_data_14460(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_volume_245FC	dw 100h			; DATA XREF: sub_1265D+5r")), ('256, // _volume_245fc\n', 'dw _volume_245fc;\n', 2))

    def test_data_14470(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_14913	dw 536h			; DATA XREF: _wss_set+14w")), ('1334, // _word_14913\n', 'dw _word_14913;\n', 2))

    def test_data_14480(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_14BBB	dw 22Fh			; DATA XREF: _sb16_on+49w _sb16_on+57w")), ('559, // _word_14bbb\n', 'dw _word_14bbb;\n', 2))

    def test_data_14490(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_14CEB	dw 22Eh			; DATA XREF: _sb_set-108w")), ('558, // _word_14ceb\n', 'dw _word_14ceb;\n', 2))

    def test_data_14500(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_14FC0	dw 1000h		; DATA XREF: _covox_init+33w")), ('4096, // _word_14fc0\n', 'dw _word_14fc0;\n', 2))

    def test_data_14510(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_14FC8	dw 378h			; DATA XREF: _covox_init+24w")), ('888, // _word_14fc8\n', 'dw _word_14fc8;\n', 2))

    def test_data_14520(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_1504D	dw 37Ah			; DATA XREF: _stereo_init+27w")), ('890, // _word_1504d\n', 'dw _word_1504d;\n', 2))

    def test_data_14530(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_15056	dw 1234h		; DATA XREF: _stereo_init+3Aw")), ('4660, // _word_15056\n', 'dw _word_15056;\n', 2))

    def test_data_14540(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_1519B	dw 1000h		; DATA XREF: _pcspeaker_init+1Ew")), ('4096, // _word_1519b\n', 'dw _word_1519b;\n', 2))

    def test_data_14550(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_151A3	dw 1234h		; DATA XREF: _pcspeaker_init+22w")), ('4660, // _word_151a3\n', 'dw _word_151a3;\n', 2))

    def test_data_14560(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_1D26D	dw 3F2h			; DATA XREF: _dosexec+19o")), ('1010, // _word_1d26d\n', 'dw _word_1d26d;\n', 2))

    def test_data_14570(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_1D3B0	dw 49Eh			; DATA XREF: _start+723o")), ('1182, // _word_1d3b0\n', 'dw _word_1d3b0;\n', 2))

    def test_data_14580(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_1D614	dw 2020h		; DATA XREF: _useless_197F2+7w")), ('8224, // _word_1d614\n', 'dw _word_1d614;\n', 2))

    def test_data_14600(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_1DE46	dw 0			; DATA XREF: _keyb_screen_loop+316r")), ('0, // _word_1de46\n', 'dw _word_1de46;\n', 2))

    def test_data_14610(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_246DE	dw 6B00h,6500h,5F40h,5A00h,54C0h,5000h,4B80h,4740h,4340h")), ('{27392,25856,24384,23040,21696,20480,19328,18240,17216}, // _word_246de\n', 'dw _word_246de[9];\n', 18))

    def test_data_14620(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_24998	dw 6B00h,6500h,5F40h,5A00h,54C0h,5000h,4B80h,4740h,4340h")), ('{27392,25856,24384,23040,21696,20480,19328,18240,17216}, // _word_24998\n', 'dw _word_24998[9];\n', 18))

    def test_data_14660(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_word_31508	dw ?			; DATA XREF: _mod_read_10311+5o")), ('0, // _word_31508\n', 'dw _word_31508;\n', 2))

    def test_data_14680(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_wss_freq_table2	dw  1,19D7h,0Fh,1F40h, 0,2580h,0Eh,2B11h, 3,3E80h, 2,49D4h")), ('{1,6615,15,8000,0,9600,14,11025,3,16000,2,18900}, // _wss_freq_table2\n', 'dw _wss_freq_table2[12];\n', 24))

    def test_data_14690(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="_x_storage	dw  0, 0, 0, 0,	0, 0, 0, 0, 0, 0, 0, 0,	0, 0, 0, 0, 0")), ('{0}, // _x_storage\n', 'dw _x_storage[17];\n', 34))

    def test_data_14700(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="a db 0ffh,0dfh,0h")), ('{255,223,0}, // a\n', 'db a[3];\n', 3))

    def test_data_14710(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="asc_1058C	db 0,18h,0Bh,0Dh,0Ah	; DATA XREF: __2stm_module+171r")), ('{0,24,11,13,10}, // asc_1058c\n', 'db asc_1058c[5];\n', 5))

    def test_data_14720(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="asc_182C3	db 0,0,1,3,0,2,0,4,0,0,0,5,6,0,0,7 ; DATA XREF:	_gravis_18216+5r")), ('{0,0,1,3,0,2,0,4,0,0,0,5,6,0,0,7}, // asc_182c3\n', 'db asc_182c3[16];\n', 16))

    def test_data_14730(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="asc_182D3	db 0,1,0,2,0,3,4,5	; DATA XREF: _gravis_18216+19r")), ('{0,1,0,2,0,3,4,5}, // asc_182d3\n', 'db asc_182d3[8];\n', 8))

    def test_data_14740(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="asc_1CC2D	db '                              ' ; DATA XREF: _read_module+A3o")), ("{' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '}, // asc_1cc2d\n", 'char asc_1cc2d[30];\n', 30))

    def test_data_14750(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="asc_1D6E0	db '               ',0  ; DATA XREF: seg001:1A80o")), ('"               ", // asc_1d6e0\n', 'char asc_1d6e0[16];\n', 16))

    def test_data_14760(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="asc_1DA00	db '                      ',0 ; DATA XREF: _modules_search:loc_19BDDo")), ('"                      ", // asc_1da00\n', 'char asc_1da00[23];\n', 23))

    def test_data_14770(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="asc_246B0	db '                                ' ; DATA XREF: _mod_1021E+22o")), ("{' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '}, // asc_246b0\n", 'char asc_246b0[32];\n', 32))

    def test_data_14780(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="asc_25856	db '                                ',0Dh,0Ah,1Ah")), ("{' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','\\r','\\n',26}, // asc_25856\n", 'char asc_25856[35];\n', 35))

    def test_data_14800(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="b dw 2")), ('2, // b\n', 'dw b;\n', 2))

    def test_data_14810(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="beginningdata db 4")), ('4, // beginningdata\n', 'db beginningdata;\n', 1))

    def test_data_14820(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="cc db 3")), ('3, // cc\n', 'db cc;\n', 1))

    def test_data_14830(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="d db 4")), ('4, // d\n', 'db d;\n', 1))

    def test_data_14840(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db    0")), ('0, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_14850(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db    ?	;")), ('0, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_14860(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db  0Ah")), ('10, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_14870(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db  20h")), ('32, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_14880(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db  20h")), ('32, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_14890(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db  2Ch	; ,")), ('44, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_14900(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db  80h	; Ç")), ('128, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_14910(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db  8Ah	; è")), ('138, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_14920(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db ' '")), ("{' '}, // dummy0_0\n", 'char dummy0_0[1];\n', 1))

    def test_data_14930(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db ' /?  This help screen',0Dh,0Ah")), ("{' ','/','?',' ',' ','T','h','i','s',' ','h','e','l','p',' ','s','c','r','e','e','n','\\r','\\n'}, // dummy0_0\n", 'char dummy0_0[23];\n', 23))

    def test_data_14940(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db ','")), ("{','}, // dummy0_0\n", 'char dummy0_0[1];\n', 1))

    def test_data_14950(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db '- +'")), ("{'-',' ','+'}, // dummy0_0\n", 'char dummy0_0[3];\n', 3))

    def test_data_14960(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db ':'")), ("{':'}, // dummy0_0\n", 'char dummy0_0[1];\n', 1))

    def test_data_14970(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 'ABC',0")), ('"ABC", // dummy0_0\n', 'char dummy0_0[4];\n', 4))

    def test_data_14980(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 'Close this DOS session first with the \"EXIT\" command.',0Dh,0Ah")), ("{'C','l','o','s','e',' ','t','h','i','s',' ','D','O','S',' ','s','e','s','s','i','o','n',' ','f','i','r','s','t',' ','w','i','t','h',' ','t','h','e',' ','\\\"','E','X','I','T','\\\"',' ','c','o','m','m','a','n','d','.','\\r','\\n'}, // dummy0_0\n", 'char dummy0_0[55];\n', 55))

    def test_data_14990(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 'OKOKOKOK'")), ("{'O','K','O','K','O','K','O','K'}, // dummy0_0\n", 'char dummy0_0[8];\n', 8))

    def test_data_15000(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 'OKOKOKOK',10,13")), ("{'O','K','O','K','O','K','O','K','\\n','\\r'}, // dummy0_0\n", 'char dummy0_0[10];\n', 10))

    def test_data_15010(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 'Try changing the AT-BUS Clock in the CMOS Setup.',0Dh,0Ah,0")), ('"Try changing the AT-BUS Clock in the CMOS Setup.\\r\\n", // dummy0_0\n', 'char dummy0_0[51];\n', 51))

    def test_data_15020(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 'Usage: IPLAY [Switches] [FileName.Ext|@FileList.Ext]',0Dh,0Ah")), ("{'U','s','a','g','e',':',' ','I','P','L','A','Y',' ','[','S','w','i','t','c','h','e','s',']',' ','[','F','i','l','e','N','a','m','e','.','E','x','t','|','@','F','i','l','e','L','i','s','t','.','E','x','t',']','\\r','\\n'}, // dummy0_0\n", 'char dummy0_0[54];\n', 54))

    def test_data_15030(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db '[ ]'")), ("{'[',' ',']'}, // dummy0_0\n", 'char dummy0_0[3];\n', 3))

    def test_data_15040(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db '[ ]',0")), ('"[ ]", // dummy0_0\n', 'char dummy0_0[4];\n', 4))

    def test_data_15050(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 'ed again.',0Dh,0Ah")), ("{'e','d',' ','a','g','a','i','n','.','\\r','\\n'}, // dummy0_0\n", 'char dummy0_0[11];\n', 11))

    def test_data_15060(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 'h'")), ("{'h'}, // dummy0_0\n", 'char dummy0_0[1];\n', 1))

    def test_data_15070(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 'o:'")), ("{'o',':'}, // dummy0_0\n", 'char dummy0_0[2];\n', 2))

    def test_data_15080(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 's'")), ("{'s'}, // dummy0_0\n", 'char dummy0_0[1];\n', 1))

    def test_data_15090(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 's',0Dh,0Ah,0")), ('"s\\r\\n", // dummy0_0\n', 'char dummy0_0[4];\n', 4))

    def test_data_15100(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db '─asdkweorjwoerj3434',13,10,92")), ("{'\\xc4','a','s','d','k','w','e','o','r','j','w','o','e','r','j','3','4','3','4','\\r','\\n',92}, // dummy0_0\n", 'char dummy0_0[22];\n', 22))

    def test_data_15110(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0")), ('0, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15120(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0,2Ah,2Ah")), ('{0,42,42}, // dummy0_0\n', 'db dummy0_0[3];\n', 3))

    def test_data_15130(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0A0h	; á		; self modifying")), ('160, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15140(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0A0h	; á")), ('160, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15150(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0A0h,0A4h,0A8h,0ACh,0B0h,0B4h,0B8h,0BCh,0C0h,0C4h,0C8h")), ('{160,164,168,172,176,180,184,188,192,196,200}, // dummy0_0\n', 'db dummy0_0[11];\n', 11))

    def test_data_15160(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0A1h")), ('161, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15170(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0A1h,0A5h,0AAh,0AEh,0B2h,0B6h,0BAh,0BEh,0C2h,0C6h,0CAh")), ('{161,165,170,174,178,182,186,190,194,198,202}, // dummy0_0\n', 'db dummy0_0[11];\n', 11))

    def test_data_15180(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0AAh	; ¬")), ('170, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15190(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0Ah")), ('10, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15200(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0Ah,'$'")), ("{'\\n','$'}, // dummy0_0\n", 'char dummy0_0[2];\n', 2))

    def test_data_15210(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0Ah,0Bh,1Bh")), ('{10,11,27}, // dummy0_0\n', 'db dummy0_0[3];\n', 3))

    def test_data_15220(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0B8h,0BBh,0BEh,0C1h,0C3h,0C6h,0C9h,0CCh,0CFh,0D1h,0D4h")), ('{184,187,190,193,195,198,201,204,207,209,212}, // dummy0_0\n', 'db dummy0_0[11];\n', 11))

    def test_data_15230(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0C5h,0B4h,0A1h,8Dh,78h,61h,4Ah,31h,18h")), ('{197,180,161,141,120,97,74,49,24}, // dummy0_0\n', 'db dummy0_0[9];\n', 9))

    def test_data_15240(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0Dh,0Ah")), ('{13,10}, // dummy0_0\n', 'db dummy0_0[2];\n', 2))

    def test_data_15250(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 0Dh,0Ah,'$'")), ("{'\\r','\\n','$'}, // dummy0_0\n", 'char dummy0_0[3];\n', 3))

    def test_data_15260(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 1")), ('1, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15270(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 1,1,1,1,1")), ('{1,1,1,1,1}, // dummy0_0\n', 'db dummy0_0[5];\n', 5))

    def test_data_15280(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 1,2,3,4")), ('{1,2,3,4}, // dummy0_0\n', 'db dummy0_0[4];\n', 4))

    def test_data_15290(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 10h,11h,2Ah")), ('{16,17,42}, // dummy0_0\n', 'db dummy0_0[3];\n', 3))

    def test_data_15300(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 12")), ('12, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15310(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 141")), ('141, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15320(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 7Fh")), ('127, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15330(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 8,8,8,7,7,7,7,6,6,6,6,6,6,5,5,5")), ('{8,8,8,7,7,7,7,6,6,6,6,6,6,5,5,5}, // dummy0_0\n', 'db dummy0_0[16];\n', 16))

    def test_data_15340(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 80h")), ('128, // dummy0_0\n', 'db dummy0_0;\n', 1))

    def test_data_15350(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 9,9,8")), ('{9,9,8}, // dummy0_0\n', 'db dummy0_0[3];\n', 3))

    def test_data_15360(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dd   -2,  -1,  -1,  -1,	 -1,   0")), ('{4294967294,4294967295,4294967295,4294967295,4294967295,0}, // dummy0_0\n', 'dd dummy0_0[6];\n', 24))

    def test_data_15370(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dd  201, 100,  50,  25,	 12")), ('{201,100,50,25,12}, // dummy0_0\n', 'dd dummy0_0[5];\n', 20))

    def test_data_15380(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dd 111,1")), ('{111,1}, // dummy0_0\n', 'dd dummy0_0[2];\n', 8))

    @unittest.skip("to check")
    def test_data_15390(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dd offset var5")), ('offset(_data,var5), // dummy0_0\n', 'dw dummy0_0;\n', 4))

    def test_data_15400(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dd unk_24453")), ('unk_24453, // dummy0_0\n', 'dd dummy0_0;\n', 4))

    def test_data_15410(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="doublequote db 'ab''cd',\"e\"")), ("{'a','b','\\'','c','d','e'}, // doublequote\n", 'char doublequote[6];\n', 6))

    def test_data_15420(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw  0, 0, 0, 0,	0, 0, 0, 0, 0, 0, 0, 0,	0, 0, 0, 0")), ('{0}, // dummy0_0\n', 'dw dummy0_0[16];\n', 32))

    def test_data_15430(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw  5,5622h, 7,6B25h, 4,7D00h, 6,8133h,0Dh,93A8h, 9,0AC44h")), ('{5,22050,7,27429,4,32000,6,33075,13,37800,9,44100}, // dummy0_0\n', 'dw dummy0_0[12];\n', 24))

    def test_data_15440(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw 0A06h")), ('2566, // dummy0_0\n', 'dw dummy0_0;\n', 2))

    def test_data_15450(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw 0BE0h,0B40h,0AA0h,0A00h,970h,8F0h,870h,7F0h,780h,710h")), ('{3040,2880,2720,2560,2416,2288,2160,2032,1920,1808}, // dummy0_0\n', 'dw dummy0_0[10];\n', 20))

    def test_data_15460(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw 0Bh,0BB80h,0Ch")), ('{11,48000,12}, // dummy0_0\n', 'dw dummy0_0[3];\n', 6))

    def test_data_15470(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw 32Ah")), ('810, // dummy0_0\n', 'dw dummy0_0;\n', 2))

    @unittest.skip("to check")
    def test_data_15480(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw @df@@@@8")), ('karbdfarbarbarbarb8, // dummy0_0\n', 'dw dummy0_0;\n', 2))

    @unittest.skip("to check")
    def test_data_15490(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw offset __2stm_module	; 2STM")), ('k__2stm_module, // dummy0_0\n', 'dw dummy0_0;\n', 2))

    @unittest.skip("to check")
    def test_data_15500(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw offset loc_17BEB")), ('kloc_17beb, // dummy0_0\n', 'dw dummy0_0;\n', 2))

    def test_data_15510(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="e db 5")), ('5, // e\n', 'db e;\n', 1))

    def test_data_15520(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="enddata db 4")), ('4, // enddata\n', 'db enddata;\n', 1))

    def test_data_15530(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="f db 6")), ('6, // f\n', 'db f;\n', 1))

    def test_data_15540(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="fileName db 'file1.txt',0")), ('"file1.txt", // filename\n', 'char filename[10];\n', 10))

    def test_data_15550(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="g dd 12345")), ('12345, // g\n', 'dd g;\n', 4))

    def test_data_15560(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="h db -1")), ('255, // h\n', 'db h;\n', 1))

    def test_data_15570(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="h2 db 1")), ('1, // h2\n', 'db h2;\n', 1))

    def test_data_15580(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="load_handle dd 0")), ('0, // load_handle\n', 'dd load_handle;\n', 4))

    def test_data_15590(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="myoffs		dw offset label2")), ('label2, // myoffs\n', 'dw myoffs;\n', 2))

    @unittest.skip("to check")
    def test_data_15600(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="off_18E00	dw offset loc_16A89	; DATA XREF: sub_1609F:loc_16963r")), ('kloc_16a89, // off_18e00\n', 'dw off_18e00;\n', 2))

    @unittest.skip("to check")
    def test_data_15610(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="off_25326	dw offset _inr_module	; DATA XREF: _moduleread:loc_10040o")), ('k_inr_module, // off_25326\n', 'dw off_25326;\n', 2))

    def test_data_15620(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="pal_jeu db 000,000,000,000,000,021,000,000,042,000,000,063,009,000,000,009")), ('{0,0,0,0,0,21,0,0,42,0,0,63,9,0,0,9}, // pal_jeu\n', 'db pal_jeu[16];\n', 16))

    def test_data_15630(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="pas_de_mem  db 'NOT enought memory for VGA display, controls work for network games',13,10,'$'")), ("{'N','O','T',' ','e','n','o','u','g','h','t',' ','m','e','m','o','r','y',' ','f','o','r',' ','V','G','A',' ','d','i','s','p','l','a','y',',',' ','c','o','n','t','r','o','l','s',' ','w','o','r','k',' ','f','o','r',' ','n','e','t','w','o','r','k',' ','g','a','m','e','s','\\r','\\n','$'}, // pas_de_mem\n", 'char pas_de_mem[70];\n', 70))

    def test_data_15640(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="pbs1        db 'probleme dans allocation de descriptor..',13,10,'$'")), ("{'p','r','o','b','l','e','m','e',' ','d','a','n','s',' ','a','l','l','o','c','a','t','i','o','n',' ','d','e',' ','d','e','s','c','r','i','p','t','o','r','.','.','\\r','\\n','$'}, // pbs1\n", 'char pbs1[43];\n', 43))

    def test_data_15650(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="pbs2        db 'probleme dans dans definition de la taille du segment',13,10,'$'")), ("{'p','r','o','b','l','e','m','e',' ','d','a','n','s',' ','d','a','n','s',' ','d','e','f','i','n','i','t','i','o','n',' ','d','e',' ','l','a',' ','t','a','i','l','l','e',' ','d','u',' ','s','e','g','m','e','n','t','\\r','\\n','$'}, // pbs2\n", 'char pbs2[56];\n', 56))

    def test_data_15690(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="str4 db 33,'cdeab',34")), ("{33,'c','d','e','a','b',34}, // str4\n", 'char str4[7];\n', 7))

    def test_data_15700(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="table   dw 0")), ('0, // table\n', 'dw table;\n', 2))

    def test_data_15710(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="testOVerlap db 1,2,3,4,5,6,7,8,9,10,11,12,13,14")), ('{1,2,3,4,5,6,7,8,9,10,11,12,13,14}, // testoverlap\n', 'db testoverlap[14];\n', 14))

    def test_data_15740(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="unk_1D516	db    2")), ('2, // unk_1d516\n', 'db unk_1d516;\n', 1))

    def test_data_15770(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="unk_24456	db  20h			; DATA XREF: dseg:7C5Bo dseg:7C5Fo")), ('32, // unk_24456\n', 'db unk_24456;\n', 1))

    def test_data_15790(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="unk_257D9	db    0")), ('0, // unk_257d9\n', 'db unk_257d9;\n', 1))

    def test_data_15800(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="unk_258A6	db  49h	; I		; DATA XREF: _useless_writeinr_118+Eo")), ('73, // unk_258a6\n', 'db unk_258a6;\n', 1))

    def test_data_15810(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="unk_30528	db    ?	;		; DATA XREF: _s3m_module+102r")), ('0, // unk_30528\n', 'db unk_30528;\n', 1))

    def test_data_15820(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="unk_3054A	db    ?	;		; DATA XREF: _mtm_module+7Bo")), ('0, // unk_3054a\n', 'db unk_3054a;\n', 1))

    def test_data_15830(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="unk_30941	db    ?	;		; DATA XREF: _mod_n_t_module+ACr")), ('0, // unk_30941\n', 'db unk_30941;\n', 1))

    def test_data_15840(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="var db 4 dup (5)")), ('{5,5,5,5}, // var\n', 'db var[4];\n', 4))

    def test_data_15850(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="var0 db 10 dup (?)")), ('{0}, // var0\n', 'db var0[10];\n', 10))

    def test_data_15860(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="var1 db 1,2,3")), ('{1,2,3}, // var1\n', 'db var1[3];\n', 3))

    def test_data_15880(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="var3 db 5*5 dup (0,testEqu*2,2*2*3,3)")),
                         (
                         '{0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3}, '
                         '// var3\n',
                         'db var3[100];\n',
                         100))

    def test_data_15890(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="var4 db 131")), ('131, // var4\n', 'db var4;\n', 1))

    def test_data_15920(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 000,009,000,000,009,021,000,009,042,000,009,063,009,009,000,009")), ('{0,9,0,0,9,21,0,9,42,0,9,63,9,9,0,9}, // dummy0_0\n', 'db dummy0_0[16];\n', 16))

    def test_data_15930(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="db 7,'¬¬êê',16,'éÇÇÇ',0")), ('"\\x07\\xaa\\xaa\\x88\\x88\\x10\\x82\\x80\\x80\\x80", // dummy0_0\n', 'char dummy0_0[11];\n', 11))

    def test_data_15940(self):
        self.parser.action_data(line="byte_10F8E db 131")
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="dw offset byte_10F8E+0F3h")), ('offset(default_seg,byte_10f8e)+243, // dummy0_0\n', 'dw dummy0_0;\n', 2))

    def test_data_15950(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line='db 0A0h,3 dup(0),88h,3 dup(0),82h')), ('{160,0,0,0,136,0,0,0,130}, // dummy0_0\n', 'db dummy0_0[9];\n', 9))

    def test_data_15960(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="var6 dd 9,8,7,1\ndw var6+4")), ('{9,8,7,1}, // var6\n', 'dd var6[4];\n', 16))

    def test_data_15970(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="aII db 8,'ê\"\"',8,'ê\"\"',0")), ('"\\x08\\x88\\"\\x08\\x88\\"", // aii\n', 'char aii[7];\n', 7))

    def test_data_15980(self):
        self.parser.itislst = True
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="aII db 8,'ê\"\"',8,'ê\"\"',0")), ('"\\x08\\x88\\"\\"\\x08\\x88\\"\\"", // aii\n', 'char aii[9];\n', 9))

    def test_data_15990(self):
        self.parser.itislst = True
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="aa db ',ªan:ª',0")), ('",\\xa6" "an:\\xa6", // aa\n', 'char aa[7];\n', 7))

    def test_data_16000(self):
        self.parser.action_data(line='aa db 0')
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="var4 dw aa")), ('offset(default_seg,aa), // var4\n', 'dw var4;\n', 2))
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="var5 dd aa")), ('far_offset(default_seg,aa), // var5\n', 'dd var5;\n', 4))

    def test_data_15910(self):
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="var6 dd 9,8,7,1")), ('{9,8,7,1}, // var6\n', 'dd var6[4];\n', 16))

    def test_data_16010(self):
        self.parser.action_data(line='loc_11990:')
        self.assertEqual(self.cpp.produce_c_data_single(self.parser.action_data(line="var4 dw offset loc_11990+2-offset loc_11990")), ('m2c::kloc_11990+2-m2c::kloc_11990, // var4\n', 'dw var4;\n', 2))

if __name__ == "__main__":
    unittest.main()
