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

    def test_data_10011(self):
        self.parser.action_label(far=False, name='@df@@@@8', isproc=False)
        self.assertEqual(self.parser.action_data(line="dw @df@@@@8").produce_c_data_single(), ('karbdfarbarbarbarb8, // dummy1\n', 'dw dummy1;\n', 2))

    def test_data_10010(self):
        self.assertEqual(self.parser.action_data(line="ASCII DB '00000000',0Dh,0Ah,'$' ; buffer for ASCII string").produce_c_data_single(), ("{'0','0','0','0','0','0','0','0','\\r','\\n','$'}, // ascii\n", 'char ascii[11];\n', 11))

    def test_data_10020(self):
        self.assertEqual(self.parser.action_data(line="_a070295122642\tdb '07/02/95 12:26:42',0 ; DATA XREF: seg003:off_2462E\x19o").produce_c_data_single(), ('"07/02/95 12:26:42", // _a070295122642\n', 'char _a070295122642[18];\n', 18))

    def test_data_10030(self):
        self.assertEqual(self.parser.action_data(line="_a100Assembler\tdb '100% assembler!'").produce_c_data_single(), ("{'1','0','0','%',' ','a','s','s','e','m','b','l','e','r','!'}, // _a100assembler\n", 'char _a100assembler[15];\n', 15))

    def test_data_10040(self):
        self.assertEqual(self.parser.action_data(line="_a1024\t\tdb '1024',0").produce_c_data_single(), ('"1024", // _a1024\n', 'char _a1024[5];\n', 5))

    def test_data_10050(self):
        self.assertEqual(self.parser.action_data(line="_a130295211558\tdb '13/02/95 21:15:58',0 ; DATA XREF: _read_module+BE\x18w").produce_c_data_single(), ('"13/02/95 21:15:58", // _a130295211558\n', 'char _a130295211558[18];\n', 18))

    def test_data_10060(self):
        self.assertEqual(self.parser.action_data(line="_a1Thru0		db '1 Thru 0'").produce_c_data_single(), ("{'1',' ','T','h','r','u',' ','0'}, // _a1thru0\n", 'char _a1thru0[8];\n', 8))

    def test_data_10070(self):
        self.assertEqual(self.parser.action_data(line="_a2284116_8	db '2:284/116.8'").produce_c_data_single(), ("{'2',':','2','8','4','/','1','1','6','.','8'}, // _a2284116_8\n", 'char _a2284116_8[11];\n', 11))

    def test_data_10080(self):
        self.assertEqual(self.parser.action_data(line="_a24bitInterpolation db ' 24bit Interpolation'").produce_c_data_single(), ("{' ','2','4','b','i','t',' ','I','n','t','e','r','p','o','l','a','t','i','o','n'}, // _a24bitinterpolation\n", 'char _a24bitinterpolation[20];\n', 20))

    def test_data_10090(self):
        self.assertEqual(self.parser.action_data(line="_a256		db '256',0              ; DATA XREF: _text_init2+1CEo").produce_c_data_single(), ('"256", // _a256\n', 'char _a256[4];\n', 4))

    def test_data_10100(self):
        self.assertEqual(self.parser.action_data(line="_a512		db '512',0").produce_c_data_single(), ('"512", // _a512\n', 'char _a512[4];\n', 4))

    def test_data_10110(self):
        self.assertEqual(self.parser.action_data(line="_a768		db '768',0").produce_c_data_single(), ('"768", // _a768\n', 'char _a768[4];\n', 4))

    def test_data_10120(self):
        self.assertEqual(self.parser.action_data(line="_aAdlibSoundcard	db 'Adlib SoundCard',0  ; DATA XREF: dseg:02BAo").produce_c_data_single(), ('"Adlib SoundCard", // _aadlibsoundcard\n', 'char _aadlibsoundcard[16];\n', 16))

    def test_data_10130(self):
        self.assertEqual(self.parser.action_data(line="_aAdlibSoundcard_0 db 'Adlib SoundCard',0 ; DATA XREF: seg003:0D6Ao").produce_c_data_single(), ('"Adlib SoundCard", // _aadlibsoundcard_0\n', 'char _aadlibsoundcard_0[16];\n', 16))

    def test_data_10140(self):
        self.assertEqual(self.parser.action_data(line="_aAnd		db ' and '").produce_c_data_single(), ("{' ','a','n','d',' '}, // _aand\n", 'char _aand[5];\n', 5))

    def test_data_10150(self):
        self.assertEqual(self.parser.action_data(line="_aAndWriteFollowingTe db	' and write following text in your message:'").produce_c_data_single(), ("{' ','a','n','d',' ','w','r','i','t','e',' ','f','o','l','l','o','w','i','n','g',' ','t','e','x','t',' ','i','n',' ','y','o','u','r',' ','m','e','s','s','a','g','e',':'}, // _aandwritefollowingte\n", 'char _aandwritefollowingte[42];\n', 42))

    def test_data_10160(self):
        self.assertEqual(self.parser.action_data(line="_aArpeggio	db 'Arpeggio       ',0  ; DATA XREF: seg001:loc_1AB0Do").produce_c_data_single(), ('"Arpeggio       ", // _aarpeggio\n', 'char _aarpeggio[16];\n', 16))

    def test_data_10170(self):
        self.assertEqual(self.parser.action_data(line="_aAt		db ' at',0              ; DATA XREF: seg003:10BFo seg003:1152o ...").produce_c_data_single(), ('" at", // _aat\n', 'char _aat[4];\n', 4))

    def test_data_10180(self):
        self.assertEqual(self.parser.action_data(line="_aAutoToneporta	db 'Auto TonePorta ',0").produce_c_data_single(), ('"Auto TonePorta ", // _aautotoneporta\n', 'char _aautotoneporta[16];\n', 16))

    def test_data_10190(self):
        self.assertEqual(self.parser.action_data(line="_aBackspace	db 'BackSpace'").produce_c_data_single(), ("{'B','a','c','k','S','p','a','c','e'}, // _abackspace\n", 'char _abackspace[9];\n', 9))

    def test_data_10200(self):
        self.assertEqual(self.parser.action_data(line="_aBasePort	db ' base port ',0      ; DATA XREF: seg003:10C3o seg003:1156o ...").produce_c_data_single(), ('" base port ", // _abaseport\n', 'char _abaseport[12];\n', 12))

    def test_data_10210(self):
        self.assertEqual(self.parser.action_data(line="_aBmod2stm	db 'BMOD2STM'").produce_c_data_single(), ("{'B','M','O','D','2','S','T','M'}, // _abmod2stm\n", 'char _abmod2stm[8];\n', 8))

    def test_data_10220(self):
        self.assertEqual(self.parser.action_data(line="_aCd81		db 'CD81'").produce_c_data_single(), ("{'C','D','8','1'}, // _acd81\n", 'char _acd81[4];\n', 4))

    def test_data_10230(self):
        self.assertEqual(self.parser.action_data(line="_aCh		db 'CH'").produce_c_data_single(), ("{'C','H'}, // _ach\n", 'char _ach[2];\n', 2))

    def test_data_10240(self):
        self.assertEqual(self.parser.action_data(line="_aChannels	db 'Channels      :'").produce_c_data_single(), ("{'C','h','a','n','n','e','l','s',' ',' ',' ',' ',' ',' ',':'}, // _achannels\n", 'char _achannels[15];\n', 15))

    def test_data_10250(self):
        self.assertEqual(self.parser.action_data(line="_aChn		db 'CHN'").produce_c_data_single(), ("{'C','H','N'}, // _achn\n", 'char _achn[3];\n', 3))

    def test_data_10260(self):
        self.assertEqual(self.parser.action_data(line="_aConfigFileNotF	db 'Config file not found. Run ISETUP first',0Dh,0Ah,'$'").produce_c_data_single(), ("{'C','o','n','f','i','g',' ','f','i','l','e',' ','n','o','t',' ','f','o','u','n','d','.',' ','R','u','n',' ','I','S','E','T','U','P',' ','f','i','r','s','t','\\r','\\n','$'}, // _aconfigfilenotf\n", 'char _aconfigfilenotf[42];\n', 42))

    def test_data_10270(self):
        self.assertEqual(self.parser.action_data(line="_aCopyrightC1994	db 'Copyright (c) 1994,1995 by Stefan Danes and Ramon van Gorkom',0").produce_c_data_single(), ('"Copyright (c) 1994,1995 by Stefan Danes and Ramon van Gorkom", // _acopyrightc1994\n', 'char _acopyrightc1994[61];\n', 61))

    def test_data_10280(self):
        self.assertEqual(self.parser.action_data(line="_aCouldNotFindT_0 db 'Could not find the Gravis UltraSound at the specified port addres'").produce_c_data_single(), ("{'C','o','u','l','d',' ','n','o','t',' ','f','i','n','d',' ','t','h','e',' ','G','r','a','v','i','s',' ','U','l','t','r','a','S','o','u','n','d',' ','a','t',' ','t','h','e',' ','s','p','e','c','i','f','i','e','d',' ','p','o','r','t',' ','a','d','d','r','e','s'}, // _acouldnotfindt_0\n", 'char _acouldnotfindt_0[65];\n', 65))

    def test_data_10290(self):
        self.assertEqual(self.parser.action_data(line="_aCouldNotFindThe db 'Could not find the ULTRASND environment string',0Dh,0Ah,0").produce_c_data_single(), ('"Could not find the ULTRASND environment string\\r\\n", // _acouldnotfindthe\n', 'char _acouldnotfindthe[49];\n', 49))

    def test_data_10300(self):
        self.assertEqual(self.parser.action_data(line="_aCovox		db 'Covox',0            ; DATA XREF: dseg:02B6o").produce_c_data_single(), ('"Covox", // _acovox\n', 'char _acovox[6];\n', 6))

    def test_data_10310(self):
        self.assertEqual(self.parser.action_data(line="_aCovox_0	db 'Covox',0            ; DATA XREF: seg003:0D66o").produce_c_data_single(), ('"Covox", // _acovox_0\n', 'char _acovox_0[6];\n', 6))

    def test_data_10320(self):
        self.assertEqual(self.parser.action_data(line="_aCriticalErrorT	db 0Dh,0Ah		; DATA XREF: _start+31o").produce_c_data_single(), ('{13,10}, // _acriticalerrort\n', 'db _acriticalerrort[2];\n', 2))

    def test_data_10330(self):
        self.assertEqual(self.parser.action_data(line="_aCtrlDel	db 'Ctrl Del'").produce_c_data_single(), ("{'C','t','r','l',' ','D','e','l'}, // _actrldel\n", 'char _actrldel[8];\n', 8))

    def test_data_10340(self):
        self.assertEqual(self.parser.action_data(line="_aCurrentSoundcard db 0Dh,'Current Soundcard settings:',0Dh,0Ah ; DATA XREF: _start:loc_19057o").produce_c_data_single(), ("{'\\r','C','u','r','r','e','n','t',' ','S','o','u','n','d','c','a','r','d',' ','s','e','t','t','i','n','g','s',':','\\r','\\n'}, // _acurrentsoundcard\n", 'char _acurrentsoundcard[30];\n', 30))

    def test_data_10350(self):
        self.assertEqual(self.parser.action_data(line="_aCurrentTrack	db 'Current Track :'").produce_c_data_single(), ("{'C','u','r','r','e','n','t',' ','T','r','a','c','k',' ',':'}, // _acurrenttrack\n", 'char _acurrenttrack[15];\n', 15))

    def test_data_10360(self):
        self.assertEqual(self.parser.action_data(line="_aCursor		db 7Fh").produce_c_data_single(), ('127, // _acursor\n', 'db _acursor;\n', 1))

    def test_data_10370(self):
        self.assertEqual(self.parser.action_data(line="_aCursor_0	db 'Cursor ',1Bh,' '").produce_c_data_single(), ("{'C','u','r','s','o','r',' ',27,' '}, // _acursor_0\n", 'char _acursor_0[9];\n', 9))

    def test_data_10380(self):
        self.assertEqual(self.parser.action_data(line="_aCursor_1	db 'Cursor '").produce_c_data_single(), ("{'C','u','r','s','o','r',' '}, // _acursor_1\n", 'char _acursor_1[7];\n', 7))

    def test_data_10390(self):
        self.assertEqual(self.parser.action_data(line="_aDecIncAmplify	db 7Eh").produce_c_data_single(), ('126, // _adecincamplify\n', 'db _adecincamplify;\n', 1))

    def test_data_10400(self):
        self.assertEqual(self.parser.action_data(line="_aDecIncAmplify_0 db '  Dec/Inc amplify'").produce_c_data_single(), ("{' ',' ','D','e','c','/','I','n','c',' ','a','m','p','l','i','f','y'}, // _adecincamplify_0\n", 'char _adecincamplify_0[17];\n', 17))

    def test_data_10410(self):
        self.assertEqual(self.parser.action_data(line="_aDecIncVolume	db 7Eh").produce_c_data_single(), ('126, // _adecincvolume\n', 'db _adecincvolume;\n', 1))

    def test_data_10420(self):
        self.assertEqual(self.parser.action_data(line="_aDecIncVolume_0	db '  Dec/Inc volume'").produce_c_data_single(), ("{' ',' ','D','e','c','/','I','n','c',' ','v','o','l','u','m','e'}, // _adecincvolume_0\n", 'char _adecincvolume_0[16];\n', 16))

    def test_data_10430(self):
        self.assertEqual(self.parser.action_data(line="_aDel		db 'Del'").produce_c_data_single(), ("{'D','e','l'}, // _adel\n", 'char _adel[3];\n', 3))

    def test_data_10440(self):
        self.assertEqual(self.parser.action_data(line="_aDeleteAllFilesWhich db	'Delete all files which are marked to delete'").produce_c_data_single(), ("{'D','e','l','e','t','e',' ','a','l','l',' ','f','i','l','e','s',' ','w','h','i','c','h',' ','a','r','e',' ','m','a','r','k','e','d',' ','t','o',' ','d','e','l','e','t','e'}, // _adeleteallfileswhich\n", 'char _adeleteallfileswhich[43];\n', 43))

    def test_data_10450(self):
        self.assertEqual(self.parser.action_data(line="_aDeleteMarkedFil db 'Delete marked files? [Y/N]',0 ; DATA XREF: _start+635o").produce_c_data_single(), ('"Delete marked files? [Y/N]", // _adeletemarkedfil\n', 'char _adeletemarkedfil[27];\n', 27))

    def test_data_10460(self):
        self.assertEqual(self.parser.action_data(line="_aDeletingFile	db 'Deleting file: '    ; DATA XREF: _start+69Fo").produce_c_data_single(), ("{'D','e','l','e','t','i','n','g',' ','f','i','l','e',':',' '}, // _adeletingfile\n", 'char _adeletingfile[15];\n', 15))

    def test_data_10470(self):
        self.assertEqual(self.parser.action_data(line="_aDeviceNotIniti	db 'Device not initialised!',0 ; DATA XREF: sub_12D05+8o").produce_c_data_single(), ('"Device not initialised!", // _adevicenotiniti\n', 'char _adevicenotiniti[24];\n', 24))

    def test_data_10480(self):
        self.assertEqual(self.parser.action_data(line="_aDisableBpmOnOf	db 7Eh").produce_c_data_single(), ('126, // _adisablebpmonof\n', 'db _adisablebpmonof;\n', 1))

    def test_data_10490(self):
        self.assertEqual(self.parser.action_data(line="_aDisableBpmOnOff db ' Disable BPM on/off'").produce_c_data_single(), ("{' ','D','i','s','a','b','l','e',' ','B','P','M',' ','o','n','/','o','f','f'}, // _adisablebpmonoff\n", 'char _adisablebpmonoff[19];\n', 19))

    def test_data_10500(self):
        self.assertEqual(self.parser.action_data(line="_aDma		db ', DMA '").produce_c_data_single(), ("{',',' ','D','M','A',' '}, // _adma\n", 'char _adma[6];\n', 6))

    def test_data_10510(self):
        self.assertEqual(self.parser.action_data(line="_aDosShellTypeEx	db 7Eh").produce_c_data_single(), ('126, // _adosshelltypeex\n', 'db _adosshelltypeex;\n', 1))

    def test_data_10520(self):
        self.assertEqual(self.parser.action_data(line="_aDosShellTypeExitT_0 db	'DOS Shell (Type EXIT to return)'").produce_c_data_single(), ("{'D','O','S',' ','S','h','e','l','l',' ','(','T','y','p','e',' ','E','X','I','T',' ','t','o',' ','r','e','t','u','r','n',')'}, // _adosshelltypeexitt_0\n", 'char _adosshelltypeexitt_0[31];\n', 31))

    def test_data_10530(self):
        self.assertEqual(self.parser.action_data(line="_aDosShellTypeExitToR db	'  DOS Shell (Type EXIT to return)'").produce_c_data_single(), ("{' ',' ','D','O','S',' ','S','h','e','l','l',' ','(','T','y','p','e',' ','E','X','I','T',' ','t','o',' ','r','e','t','u','r','n',')'}, // _adosshelltypeexittor\n", 'char _adosshelltypeexittor[33];\n', 33))

    def test_data_10540(self):
        self.assertEqual(self.parser.action_data(line="_aDramDma	db ', DRAM-DMA '").produce_c_data_single(), ("{',',' ','D','R','A','M','-','D','M','A',' '}, // _adramdma\n", 'char _adramdma[11];\n', 11))

    def test_data_10550(self):
        self.assertEqual(self.parser.action_data(line="_aE_command	db 'E_Command      ',0").produce_c_data_single(), ('"E_Command      ", // _ae_command\n', 'char _ae_command[16];\n', 16))

    def test_data_10560(self):
        self.assertEqual(self.parser.action_data(line="_aE_g_		db 'E.G.'").produce_c_data_single(), ("{'E','.','G','.'}, // _ae_g_\n", 'char _ae_g_[4];\n', 4))

    def test_data_10570(self):
        self.assertEqual(self.parser.action_data(line="_aEnd		db 'End'").produce_c_data_single(), ("{'E','n','d'}, // _aend\n", 'char _aend[3];\n', 3))

    def test_data_10580(self):
        self.assertEqual(self.parser.action_data(line="_aEndPattern	db '  End pattern'").produce_c_data_single(), ("{' ',' ','E','n','d',' ','p','a','t','t','e','r','n'}, // _aendpattern\n", 'char _aendpattern[13];\n', 13))

    def test_data_10590(self):
        self.assertEqual(self.parser.action_data(line="_aEnd_0		db 'End'").produce_c_data_single(), ("{'E','n','d'}, // _aend_0\n", 'char _aend_0[3];\n', 3))

    def test_data_10600(self):
        self.assertEqual(self.parser.action_data(line="_aEnter		db 'Enter'").produce_c_data_single(), ("{'E','n','t','e','r'}, // _aenter\n", 'char _aenter[5];\n', 5))

    def test_data_10610(self):
        self.assertEqual(self.parser.action_data(line="_aErrorCouldNotFi db 'Error: Could not find IRQ/DMA!',0Dh,0Ah,0").produce_c_data_single(), ('"Error: Could not find IRQ/DMA!\\r\\n", // _aerrorcouldnotfi\n', 'char _aerrorcouldnotfi[33];\n', 33))

    def test_data_10620(self):
        self.assertEqual(self.parser.action_data(line="_aErrorCouldNot_0 db 'Error: Could not find IRQ!',0Dh,0Ah,0 ; DATA XREF: _sb_detect_irq+4Co").produce_c_data_single(), ('"Error: Could not find IRQ!\\r\\n", // _aerrorcouldnot_0\n', 'char _aerrorcouldnot_0[29];\n', 29))

    def test_data_10630(self):
        self.assertEqual(self.parser.action_data(line="_aErrorCouldNot_1 db 'Error: Could not find DMA!',0Dh,0Ah,0 ; DATA XREF: _sb_detect_irq+D6o").produce_c_data_single(), ('"Error: Could not find DMA!\\r\\n", // _aerrorcouldnot_1\n', 'char _aerrorcouldnot_1[29];\n', 29))

    def test_data_10640(self):
        self.assertEqual(self.parser.action_data(line="_aErrorSoundcardN db 'Error: Soundcard not found!',0Dh,0Ah,'$',0").produce_c_data_single(), ('"Error: Soundcard not found!\\r\\n$", // _aerrorsoundcardn\n', 'char _aerrorsoundcardn[31];\n', 31))

    def test_data_10650(self):
        self.assertEqual(self.parser.action_data(line="_aEsc		db 'ESC'").produce_c_data_single(), ("{'E','S','C'}, // _aesc\n", 'char _aesc[3];\n', 3))

    def test_data_10660(self):
        self.assertEqual(self.parser.action_data(line="_aExit		db 'EXIT'").produce_c_data_single(), ("{'E','X','I','T'}, // _aexit\n", 'char _aexit[4];\n', 4))

    def test_data_10670(self):
        self.assertEqual(self.parser.action_data(line="_aF1		db 'F-1'").produce_c_data_single(), ("{'F','-','1'}, // _af1\n", 'char _af1[3];\n', 3))

    def test_data_10680(self):
        self.assertEqual(self.parser.action_data(line="_aF10		db 7Fh").produce_c_data_single(), ('127, // _af10\n', 'db _af10;\n', 1))

    def test_data_10690(self):
        self.assertEqual(self.parser.action_data(line="_aF10_0		db 'F-10'").produce_c_data_single(), ("{'F','-','1','0'}, // _af10_0\n", 'char _af10_0[4];\n', 4))

    def test_data_10700(self):
        self.assertEqual(self.parser.action_data(line="_aF10_1		db 'F-10'").produce_c_data_single(), ("{'F','-','1','0'}, // _af10_1\n", 'char _af10_1[4];\n', 4))

    def test_data_10710(self):
        self.assertEqual(self.parser.action_data(line="_aF11		db 7Fh").produce_c_data_single(), ('127, // _af11\n', 'db _af11;\n', 1))

    def test_data_10720(self):
        self.assertEqual(self.parser.action_data(line="_aF11_0		db 'F-11'").produce_c_data_single(), ("{'F','-','1','1'}, // _af11_0\n", 'char _af11_0[4];\n', 4))

    def test_data_10730(self):
        self.assertEqual(self.parser.action_data(line="_aF11_1		db 'F-11'").produce_c_data_single(), ("{'F','-','1','1'}, // _af11_1\n", 'char _af11_1[4];\n', 4))

    def test_data_10740(self):
        self.assertEqual(self.parser.action_data(line="_aF12		db 7Fh").produce_c_data_single(), ('127, // _af12\n', 'db _af12;\n', 1))

    def test_data_10750(self):
        self.assertEqual(self.parser.action_data(line="_aF12_0		db 'F-12'").produce_c_data_single(), ("{'F','-','1','2'}, // _af12_0\n", 'char _af12_0[4];\n', 4))

    def test_data_10760(self):
        self.assertEqual(self.parser.action_data(line="_aF12_1		db 'F-12'").produce_c_data_single(), ("{'F','-','1','2'}, // _af12_1\n", 'char _af12_1[4];\n', 4))

    def test_data_10770(self):
        self.assertEqual(self.parser.action_data(line="_aF2_0		db 'F-2'").produce_c_data_single(), ("{'F','-','2'}, // _af2_0\n", 'char _af2_0[3];\n', 3))

    def test_data_10780(self):
        self.assertEqual(self.parser.action_data(line="_aF3_0		db 'F-3'").produce_c_data_single(), ("{'F','-','3'}, // _af3_0\n", 'char _af3_0[3];\n', 3))

    def test_data_10790(self):
        self.assertEqual(self.parser.action_data(line="_aF4_0		db 'F-4'").produce_c_data_single(), ("{'F','-','4'}, // _af4_0\n", 'char _af4_0[3];\n', 3))

    def test_data_10800(self):
        self.assertEqual(self.parser.action_data(line="_aF5_0		db 'F-5'").produce_c_data_single(), ("{'F','-','5'}, // _af5_0\n", 'char _af5_0[3];\n', 3))

    def test_data_10810(self):
        self.assertEqual(self.parser.action_data(line="_aF8_0		db 'F-8'").produce_c_data_single(), ("{'F','-','8'}, // _af8_0\n", 'char _af8_0[3];\n', 3))

    def test_data_10820(self):
        self.assertEqual(self.parser.action_data(line="_aF8_1		db 'F-8'").produce_c_data_single(), ("{'F','-','8'}, // _af8_1\n", 'char _af8_1[3];\n', 3))

    def test_data_10830(self):
        self.assertEqual(self.parser.action_data(line="_aF9		db ' [F-9]              ',0").produce_c_data_single(), ('" [F-9]              ", // _af9\n', 'char _af9[21];\n', 21))

    def test_data_10840(self):
        self.assertEqual(self.parser.action_data(line="_aF9_0		db ' [F-9]',0").produce_c_data_single(), ('" [F-9]", // _af9_0\n', 'char _af9_0[7];\n', 7))

    def test_data_10850(self):
        self.assertEqual(self.parser.action_data(line="_aF9_1		db 7Fh").produce_c_data_single(), ('127, // _af9_1\n', 'db _af9_1;\n', 1))

    def test_data_10860(self):
        self.assertEqual(self.parser.action_data(line="_aF9_2		db 'F-9'").produce_c_data_single(), ("{'F','-','9'}, // _af9_2\n", 'char _af9_2[3];\n', 3))

    def test_data_10870(self):
        self.assertEqual(self.parser.action_data(line="_aF9_3		db 'F-9'").produce_c_data_single(), ("{'F','-','9'}, // _af9_3\n", 'char _af9_3[3];\n', 3))

    def test_data_10880(self):
        self.assertEqual(self.parser.action_data(line="_aF9_4		db 'F-9'").produce_c_data_single(), ("{'F','-','9'}, // _af9_4\n", 'char _af9_4[3];\n', 3))

    def test_data_10890(self):
        self.assertEqual(self.parser.action_data(line="_aFar		db 'FAR■'").produce_c_data_single(), ("{'F','A','R','\\xfe'}, // _afar\n", 'char _afar[4];\n', 4))

    def test_data_10900(self):
        self.assertEqual(self.parser.action_data(line="_aFarFineTempo	db 'FAR Fine Tempo ',0").produce_c_data_single(), ('"FAR Fine Tempo ", // _afarfinetempo\n', 'char _afarfinetempo[16];\n', 16))

    def test_data_10910(self):
        self.assertEqual(self.parser.action_data(line="_aFarTempo	db 'FAR Tempo      ',0").produce_c_data_single(), ('"FAR Tempo      ", // _afartempo\n', 'char _afartempo[16];\n', 16))

    def test_data_10920(self):
        self.assertEqual(self.parser.action_data(line="_aFastErForward	db '  Fast(er) forward'").produce_c_data_single(), ("{' ',' ','F','a','s','t','(','e','r',')',' ','f','o','r','w','a','r','d'}, // _afasterforward\n", 'char _afasterforward[18];\n', 18))

    def test_data_10930(self):
        self.assertEqual(self.parser.action_data(line="_aFastErRewind	db '  Fast(er) rewind'").produce_c_data_single(), ("{' ',' ','F','a','s','t','(','e','r',')',' ','r','e','w','i','n','d'}, // _afasterrewind\n", 'char _afasterrewind[17];\n', 17))

    def test_data_10940(self):
        self.assertEqual(self.parser.action_data(line="_aFastfourierFrequenc db	'  FastFourier Frequency Analysis'").produce_c_data_single(), ("{' ',' ','F','a','s','t','F','o','u','r','i','e','r',' ','F','r','e','q','u','e','n','c','y',' ','A','n','a','l','y','s','i','s'}, // _afastfourierfrequenc\n", 'char _afastfourierfrequenc[32];\n', 32))

    def test_data_10950(self):
        self.assertEqual(self.parser.action_data(line="_aFidonet	db 'FidoNet  : '").produce_c_data_single(), ("{'F','i','d','o','N','e','t',' ',' ',':',' '}, // _afidonet\n", 'char _afidonet[11];\n', 11))

    def test_data_10960(self):
        self.assertEqual(self.parser.action_data(line="_aFile		db 'File'               ; DATA XREF: _start+689w _start+6A8o").produce_c_data_single(), ("{'F','i','l','e'}, // _afile\n", 'char _afile[4];\n', 4))

    def test_data_10970(self):
        self.assertEqual(self.parser.action_data(line="_aFileSelectorHelp db 'File Selector Help'").produce_c_data_single(), ("{'F','i','l','e',' ','S','e','l','e','c','t','o','r',' ','H','e','l','p'}, // _afileselectorhelp\n", 'char _afileselectorhelp[18];\n', 18))

    def test_data_10980(self):
        self.assertEqual(self.parser.action_data(line="_aFilename_0	db 'Filename      : '").produce_c_data_single(), ("{'F','i','l','e','n','a','m','e',' ',' ',' ',' ',' ',' ',':',' '}, // _afilename_0\n", 'char _afilename_0[16];\n', 16))

    def test_data_10990(self):
        self.assertEqual(self.parser.action_data(line="_aFilename_ext	db 'FileName.Ext'       ; DATA XREF: _read_module:loc_19E41o").produce_c_data_single(), ("{'F','i','l','e','N','a','m','e','.','E','x','t'}, // _afilename_ext\n", 'char _afilename_ext[12];\n', 12))

    def test_data_11000(self):
        self.assertEqual(self.parser.action_data(line="_aFinePanning	db 'Fine Panning   ',0").produce_c_data_single(), ('"Fine Panning   ", // _afinepanning\n', 'char _afinepanning[16];\n', 16))

    def test_data_11010(self):
        self.assertEqual(self.parser.action_data(line="_aFinePortVolsl	db 'Fine Port+VolSl',0").produce_c_data_single(), ('"Fine Port+VolSl", // _afineportvolsl\n', 'char _afineportvolsl[16];\n', 16))

    def test_data_11020(self):
        self.assertEqual(self.parser.action_data(line="_aFinePortaDown	db 'Fine Porta Down',0").produce_c_data_single(), ('"Fine Porta Down", // _afineportadown\n', 'char _afineportadown[16];\n', 16))

    def test_data_11030(self):
        self.assertEqual(self.parser.action_data(line="_aFinePortaUp	db 'Fine Porta Up  ',0").produce_c_data_single(), ('"Fine Porta Up  ", // _afineportaup\n', 'char _afineportaup[16];\n', 16))

    def test_data_11040(self):
        self.assertEqual(self.parser.action_data(line="_aFineTonePorta	db 'Fine Tone Porta',0").produce_c_data_single(), ('"Fine Tone Porta", // _afinetoneporta\n', 'char _afinetoneporta[16];\n', 16))

    def test_data_11050(self):
        self.assertEqual(self.parser.action_data(line="_aFineVibrVolsl	db 'Fine Vibr+VolSl',0").produce_c_data_single(), ('"Fine Vibr+VolSl", // _afinevibrvolsl\n', 'char _afinevibrvolsl[16];\n', 16))

    def test_data_11060(self):
        self.assertEqual(self.parser.action_data(line="_aFineVibrato	db 'Fine Vibrato   ',0").produce_c_data_single(), ('"Fine Vibrato   ", // _afinevibrato\n', 'char _afinevibrato[16];\n', 16))

    def test_data_11070(self):
        self.assertEqual(self.parser.action_data(line="_aFineVolSlide	db 'Fine Vol Slide ',0").produce_c_data_single(), ('"Fine Vol Slide ", // _afinevolslide\n', 'char _afinevolslide[16];\n', 16))

    def test_data_11080(self):
        self.assertEqual(self.parser.action_data(line="_aFineslideDown	db 'FineSlide Down ',0").produce_c_data_single(), ('"FineSlide Down ", // _afineslidedown\n', 'char _afineslidedown[16];\n', 16))

    def test_data_11090(self):
        self.assertEqual(self.parser.action_data(line="_aFineslideUp	db 'FineSlide Up   ',0").produce_c_data_single(), ('"FineSlide Up   ", // _afineslideup\n', 'char _afineslideup[16];\n', 16))

    def test_data_11100(self):
        self.assertEqual(self.parser.action_data(line="_aFinevolumeDown	db 'FineVolume Down',0").produce_c_data_single(), ('"FineVolume Down", // _afinevolumedown\n', 'char _afinevolumedown[16];\n', 16))

    def test_data_11110(self):
        self.assertEqual(self.parser.action_data(line="_aFinevolumeUp	db 'FineVolume Up  ',0").produce_c_data_single(), ('"FineVolume Up  ", // _afinevolumeup\n', 'char _afinevolumeup[16];\n', 16))

    def test_data_11120(self):
        self.assertEqual(self.parser.action_data(line="_aFlt4		db 'FLT4'").produce_c_data_single(), ("{'F','L','T','4'}, // _aflt4\n", 'char _aflt4[4];\n', 4))

    def test_data_11130(self):
        self.assertEqual(self.parser.action_data(line="_aFlt8		db 'FLT8'").produce_c_data_single(), ("{'F','L','T','8'}, // _aflt8\n", 'char _aflt8[4];\n', 4))

    def test_data_11140(self):
        self.assertEqual(self.parser.action_data(line="_aGeneralMidi	db 'General MIDI',0     ; DATA XREF: dseg:02BEo").produce_c_data_single(), ('"General MIDI", // _ageneralmidi\n', 'char _ageneralmidi[13];\n', 13))

    def test_data_11150(self):
        self.assertEqual(self.parser.action_data(line="_aGeneralMidi_0	db 'General MIDI',0     ; DATA XREF: seg003:0D6Eo").produce_c_data_single(), ('"General MIDI", // _ageneralmidi_0\n', 'char _ageneralmidi_0[13];\n', 13))

    def test_data_11160(self):
        self.assertEqual(self.parser.action_data(line="_aGlissandoCtrl	db 'Glissando Ctrl ',0").produce_c_data_single(), ('"Glissando Ctrl ", // _aglissandoctrl\n', 'char _aglissandoctrl[16];\n', 16))

    def test_data_11170(self):
        self.assertEqual(self.parser.action_data(line="_aGraphicalScopesOneF db	'  Graphical scopes, one for each channel'").produce_c_data_single(), ("{' ',' ','G','r','a','p','h','i','c','a','l',' ','s','c','o','p','e','s',',',' ','o','n','e',' ','f','o','r',' ','e','a','c','h',' ','c','h','a','n','n','e','l'}, // _agraphicalscopesonef\n", 'char _agraphicalscopesonef[40];\n', 40))

    def test_data_11180(self):
        self.assertEqual(self.parser.action_data(line="_aGravisMaxCodec	db 'Gravis MAX Codec',0").produce_c_data_single(), ('"Gravis MAX Codec", // _agravismaxcodec\n', 'char _agravismaxcodec[17];\n', 17))

    def test_data_11190(self):
        self.assertEqual(self.parser.action_data(line="_aGravisUltrasou	db 'Gravis UltraSound',0 ; DATA XREF: dseg:_table_sndcrdnameo").produce_c_data_single(), ('"Gravis UltraSound", // _agravisultrasou\n', 'char _agravisultrasou[18];\n', 18))

    def test_data_11200(self):
        self.assertEqual(self.parser.action_data(line="_aGravisUltrasoun db 'Gravis UltraSound',0 ; DATA XREF: seg003:_snd_cards_offso").produce_c_data_single(), ('"Gravis UltraSound", // _agravisultrasoun\n', 'char _agravisultrasoun[18];\n', 18))

    def test_data_11210(self):
        self.assertEqual(self.parser.action_data(line="_aGray		db 7Fh").produce_c_data_single(), ('127, // _agray\n', 'db _agray;\n', 1))

    def test_data_11220(self):
        self.assertEqual(self.parser.action_data(line="_aGray_0		db 'Gray - +'").produce_c_data_single(), ("{'G','r','a','y',' ','-',' ','+'}, // _agray_0\n", 'char _agray_0[8];\n', 8))

    def test_data_11230(self):
        self.assertEqual(self.parser.action_data(line="_aGsft		db 'GSFT'").produce_c_data_single(), ("{'G','S','F','T'}, // _agsft\n", 'char _agsft[4];\n', 4))

    def test_data_11240(self):
        self.assertEqual(self.parser.action_data(line="_aGuess___	db '  Guess...'").produce_c_data_single(), ("{' ',' ','G','u','e','s','s','.','.','.'}, // _aguess___\n", 'char _aguess___[10];\n', 10))

    def test_data_11250(self):
        self.assertEqual(self.parser.action_data(line="_aHGf1Irq	db 'h, GF1-IRQ '").produce_c_data_single(), ("{'h',',',' ','G','F','1','-','I','R','Q',' '}, // _ahgf1irq\n", 'char _ahgf1irq[11];\n', 11))

    def test_data_11260(self):
        self.assertEqual(self.parser.action_data(line="_aHIrq		db 'h, IRQ '").produce_c_data_single(), ("{'h',',',' ','I','R','Q',' '}, // _ahirq\n", 'char _ahirq[7];\n', 7))

    def test_data_11270(self):
        self.assertEqual(self.parser.action_data(line="_aHitBackspaceToRe db 'Hit backspace to return to playmode, F-1 for help, QuickRead='").produce_c_data_single(), ("{'H','i','t',' ','b','a','c','k','s','p','a','c','e',' ','t','o',' ','r','e','t','u','r','n',' ','t','o',' ','p','l','a','y','m','o','d','e',',',' ','F','-','1',' ','f','o','r',' ','h','e','l','p',',',' ','Q','u','i','c','k','R','e','a','d','='}, // _ahitbackspacetore\n", 'char _ahitbackspacetore[61];\n', 61))

    def test_data_11280(self):
        self.assertEqual(self.parser.action_data(line="_aHome		db 'Home'").produce_c_data_single(), ("{'H','o','m','e'}, // _ahome\n", 'char _ahome[4];\n', 4))

    def test_data_11290(self):
        self.assertEqual(self.parser.action_data(line="_aHopeYouLikedUsingTh db	'Hope you liked using the '").produce_c_data_single(), ("{'H','o','p','e',' ','y','o','u',' ','l','i','k','e','d',' ','u','s','i','n','g',' ','t','h','e',' '}, // _ahopeyoulikedusingth\n", 'char _ahopeyoulikedusingth[25];\n', 25))

    def test_data_11300(self):
        self.assertEqual(self.parser.action_data(line="_aIf		db 'if'").produce_c_data_single(), ("{'i','f'}, // _aif\n", 'char _aif[2];\n', 2))

    def test_data_11310(self):
        self.assertEqual(self.parser.action_data(line="_aIfYouHaveBugReports db	'If you have bug-reports, suggestions or comments send a message t'").produce_c_data_single(), ("{'I','f',' ','y','o','u',' ','h','a','v','e',' ','b','u','g','-','r','e','p','o','r','t','s',',',' ','s','u','g','g','e','s','t','i','o','n','s',' ','o','r',' ','c','o','m','m','e','n','t','s',' ','s','e','n','d',' ','a',' ','m','e','s','s','a','g','e',' ','t'}, // _aifyouhavebugreports\n", 'char _aifyouhavebugreports[65];\n', 65))

    def test_data_11320(self):
        self.assertEqual(self.parser.action_data(line="_aIgnoreBpmChanges db ' Ignore BPM changes'").produce_c_data_single(), ("{' ','I','g','n','o','r','e',' ','B','P','M',' ','c','h','a','n','g','e','s'}, // _aignorebpmchanges\n", 'char _aignorebpmchanges[19];\n', 19))

    def test_data_11330(self):
        self.assertEqual(self.parser.action_data(line="_aInertiaMailinglists db	'Inertia Mailinglists'").produce_c_data_single(), ("{'I','n','e','r','t','i','a',' ','M','a','i','l','i','n','g','l','i','s','t','s'}, // _ainertiamailinglists\n", 'char _ainertiamailinglists[20];\n', 20))

    def test_data_11340(self):
        self.assertEqual(self.parser.action_data(line="_aInertiaModule	db 'Inertia Module: ',0 ; DATA XREF: _useless_writeinr+29o").produce_c_data_single(), ('"Inertia Module: ", // _ainertiamodule\n', 'char _ainertiamodule[17];\n', 17))

    def test_data_11350(self):
        self.assertEqual(self.parser.action_data(line="_aInertiaModule_0 db 'Inertia Module: ',0 ; DATA XREF: _useless_writeinr+23o").produce_c_data_single(), ('"Inertia Module: ", // _ainertiamodule_0\n', 'char _ainertiamodule_0[17];\n', 17))

    def test_data_11360(self):
        self.assertEqual(self.parser.action_data(line="_aInertiaModule_1 db 'Inertia Module: '").produce_c_data_single(), ("{'I','n','e','r','t','i','a',' ','M','o','d','u','l','e',':',' '}, // _ainertiamodule_1\n", 'char _ainertiamodule_1[16];\n', 16))

    def test_data_11370(self):
        self.assertEqual(self.parser.action_data(line="_aInertiaPlayer	db 'Inertia Player'").produce_c_data_single(), ("{'I','n','e','r','t','i','a',' ','P','l','a','y','e','r'}, // _ainertiaplayer\n", 'char _ainertiaplayer[14];\n', 14))

    def test_data_11380(self):
        self.assertEqual(self.parser.action_data(line="_aInertiaPlayerV1_ db 'Inertia Player V1.22 written by Stefan Danes and Ramon van Gorkom'").produce_c_data_single(), ("{'I','n','e','r','t','i','a',' ','P','l','a','y','e','r',' ','V','1','.','2','2',' ','w','r','i','t','t','e','n',' ','b','y',' ','S','t','e','f','a','n',' ','D','a','n','e','s',' ','a','n','d',' ','R','a','m','o','n',' ','v','a','n',' ','G','o','r','k','o','m'}, // _ainertiaplayerv1_\n", 'char _ainertiaplayerv1_[65];\n', 65))

    def test_data_11390(self):
        self.assertEqual(self.parser.action_data(line="_aInertiaPlayerV1_22A db	'Inertia Player V1.22 Assembly ',27h,'94 CD Edition by Sound Solution'").produce_c_data_single(), ("{'I','n','e','r','t','i','a',' ','P','l','a','y','e','r',' ','V','1','.','2','2',' ','A','s','s','e','m','b','l','y',' ',39,'9','4',' ','C','D',' ','E','d','i','t','i','o','n',' ','b','y',' ','S','o','u','n','d',' ','S','o','l','u','t','i','o','n'}, // _ainertiaplayerv1_22a\n", 'char _ainertiaplayerv1_22a[62];\n', 62))

    def test_data_11400(self):
        self.assertEqual(self.parser.action_data(line="_aInertiaPlayer_0 db 'Inertia Player',0").produce_c_data_single(), ('"Inertia Player", // _ainertiaplayer_0\n', 'char _ainertiaplayer_0[15];\n', 15))

    def test_data_11410(self):
        self.assertEqual(self.parser.action_data(line="_aInertiaSample	db 'Inertia Sample: '   ; DATA XREF: _useless_writeinr_118+11o").produce_c_data_single(), ("{'I','n','e','r','t','i','a',' ','S','a','m','p','l','e',':',' '}, // _ainertiasample\n", 'char _ainertiasample[16];\n', 16))

    def test_data_11420(self):
        self.assertEqual(self.parser.action_data(line="_aInternet	db 'Internet : '").produce_c_data_single(), ("{'I','n','t','e','r','n','e','t',' ',':',' '}, // _ainternet\n", 'char _ainternet[11];\n', 11))

    def test_data_11430(self):
        self.assertEqual(self.parser.action_data(line="_aInvertLoop	db 'Invert Loop    ',0").produce_c_data_single(), ('"Invert Loop    ", // _ainvertloop\n', 'char _ainvertloop[16];\n', 16))

    def test_data_11440(self):
        self.assertEqual(self.parser.action_data(line="_aJanfebmaraprmayj db '   JanFebMarAprMayJunJulAugSepOctNovDec'").produce_c_data_single(), ("{' ',' ',' ','J','a','n','F','e','b','M','a','r','A','p','r','M','a','y','J','u','n','J','u','l','A','u','g','S','e','p','O','c','t','N','o','v','D','e','c'}, // _ajanfebmaraprmayj\n", 'char _ajanfebmaraprmayj[39];\n', 39))

    def test_data_11450(self):
        self.assertEqual(self.parser.action_data(line="_aJn		db 'JN'").produce_c_data_single(), ("{'J','N'}, // _ajn\n", 'char _ajn[2];\n', 2))

    def test_data_11460(self):
        self.assertEqual(self.parser.action_data(line="_aJumpToLoop	db 'Jump To Loop   ',0").produce_c_data_single(), ('"Jump To Loop   ", // _ajumptoloop\n', 'char _ajumptoloop[16];\n', 16))

    def test_data_11470(self):
        self.assertEqual(self.parser.action_data(line="_aKb		db 'KB',0               ; DATA XREF: _text_init2+1D7o").produce_c_data_single(), ('"KB", // _akb\n', 'char _akb[3];\n', 3))

    def test_data_11480(self):
        self.assertEqual(self.parser.action_data(line="_aKhz		db 'kHz',0              ; DATA XREF: seg003:117Bo seg003:11ADo ...").produce_c_data_single(), ('"kHz", // _akhz\n', 'char _akhz[4];\n', 4))

    def test_data_11490(self):
        self.assertEqual(self.parser.action_data(line="_aListFileNotFou	db 'List file not found.',0Dh,0Ah,'$' ; DATA XREF: _start+D07o").produce_c_data_single(), ("{'L','i','s','t',' ','f','i','l','e',' ','n','o','t',' ','f','o','u','n','d','.','\\r','\\n','$'}, // _alistfilenotfou\n", 'char _alistfilenotfou[23];\n', 23))

    def test_data_11500(self):
        self.assertEqual(self.parser.action_data(line="_aListserver@oliver_s db	'listserver@oliver.sun.ac.za'").produce_c_data_single(), ("{'l','i','s','t','s','e','r','v','e','r','@','o','l','i','v','e','r','.','s','u','n','.','a','c','.','z','a'}, // _alistserverarboliver_s\n", 'char _alistserverarboliver_s[27];\n', 27))

    def test_data_11510(self):
        self.assertEqual(self.parser.action_data(line="_aLoadingModule	db 'Loading module',0   ; DATA XREF: _start+41Ao").produce_c_data_single(), ('"Loading module", // _aloadingmodule\n', 'char _aloadingmodule[15];\n', 15))

    def test_data_11520(self):
        self.assertEqual(self.parser.action_data(line="_aLoopModule	db 7Eh").produce_c_data_single(), ('126, // _aloopmodule\n', 'db _aloopmodule;\n', 1))

    def test_data_11530(self):
        self.assertEqual(self.parser.action_data(line="_aLoopModuleWhenDone db ' Loop Module when done'").produce_c_data_single(), ("{' ','L','o','o','p',' ','M','o','d','u','l','e',' ','w','h','e','n',' ','d','o','n','e'}, // _aloopmodulewhendone\n", 'char _aloopmodulewhendone[22];\n', 22))

    def test_data_11540(self):
        self.assertEqual(self.parser.action_data(line="_aLoopModule_0	db ' Loop module'").produce_c_data_single(), ("{' ','L','o','o','p',' ','m','o','d','u','l','e'}, // _aloopmodule_0\n", 'char _aloopmodule_0[12];\n', 12))

    def test_data_11550(self):
        self.assertEqual(self.parser.action_data(line="_aLoopPattern	db '  Loop pattern'").produce_c_data_single(), ("{' ',' ','L','o','o','p',' ','p','a','t','t','e','r','n'}, // _alooppattern\n", 'char _alooppattern[14];\n', 14))

    def test_data_11560(self):
        self.assertEqual(self.parser.action_data(line="_aMK		db 'M&K!'").produce_c_data_single(), ("{'M','&','K','!'}, // _amk\n", 'char _amk[4];\n', 4))

    def test_data_11570(self):
        self.assertEqual(self.parser.action_data(line="_aMK_0		db 'M!K!'").produce_c_data_single(), ("{'M','!','K','!'}, // _amk_0\n", 'char _amk_0[4];\n', 4))

    def test_data_11580(self):
        self.assertEqual(self.parser.action_data(line="_aM_k_		db 'M.K.'").produce_c_data_single(), ("{'M','.','K','.'}, // _am_k_\n", 'char _am_k_[4];\n', 4))

    def test_data_11590(self):
        self.assertEqual(self.parser.action_data(line="_aMainVolume	db 'Main Volume   :'").produce_c_data_single(), ("{'M','a','i','n',' ','V','o','l','u','m','e',' ',' ',' ',':'}, // _amainvolume\n", 'char _amainvolume[15];\n', 15))

    def test_data_11600(self):
        self.assertEqual(self.parser.action_data(line="_aMarkFileToDelete db 'Mark file to delete'").produce_c_data_single(), ("{'M','a','r','k',' ','f','i','l','e',' ','t','o',' ','d','e','l','e','t','e'}, // _amarkfiletodelete\n", 'char _amarkfiletodelete[19];\n', 19))

    def test_data_11610(self):
        self.assertEqual(self.parser.action_data(line="_aMarkedToDelete	db '<Marked to Delete>    ',0 ; DATA XREF: _filelist_198B8+10Do").produce_c_data_single(), ('"<Marked to Delete>    ", // _amarkedtodelete\n', 'char _amarkedtodelete[23];\n', 23))

    def test_data_11620(self):
        self.assertEqual(self.parser.action_data(line="_aMas_utrack_v	db 'MAS_UTrack_V'").produce_c_data_single(), ("{'M','A','S','_','U','T','r','a','c','k','_','V'}, // _amas_utrack_v\n", 'char _amas_utrack_v[12];\n', 12))

    def test_data_11630(self):
        self.assertEqual(self.parser.action_data(line="_aMixedAt	db ', mixed at ',0      ; DATA XREF: seg003:1173o seg003:11A5o ...").produce_c_data_single(), ('", mixed at ", // _amixedat\n', 'char _amixedat[12];\n', 12))

    def test_data_11640(self):
        self.assertEqual(self.parser.action_data(line="_aModuleIsCorrupt db 'Module is corrupt!',0 ; DATA XREF: _start+439o").produce_c_data_single(), ('"Module is corrupt!", // _amoduleiscorrupt\n', 'char _amoduleiscorrupt[19];\n', 19))

    def test_data_11650(self):
        self.assertEqual(self.parser.action_data(line="_aModuleLoadErro	db 'Module load error.',0Dh,0Ah,'$' ; DATA XREF: _readallmoules+1Bo").produce_c_data_single(), ("{'M','o','d','u','l','e',' ','l','o','a','d',' ','e','r','r','o','r','.','\\r','\\n','$'}, // _amoduleloaderro\n", 'char _amoduleloaderro[21];\n', 21))

    def test_data_11660(self):
        self.assertEqual(self.parser.action_data(line="_aModuleNotFound	db 'Module not found.',0Dh,0Ah,'$' ; DATA XREF: _find_mods+88o").produce_c_data_single(), ("{'M','o','d','u','l','e',' ','n','o','t',' ','f','o','u','n','d','.','\\r','\\n','$'}, // _amodulenotfound\n", 'char _amodulenotfound[20];\n', 20))

    def test_data_11670(self):
        self.assertEqual(self.parser.action_data(line="_aModuleType_0	db 'Module Type   : '").produce_c_data_single(), ("{'M','o','d','u','l','e',' ','T','y','p','e',' ',' ',' ',':',' '}, // _amoduletype_0\n", 'char _amoduletype_0[16];\n', 16))

    def test_data_11680(self):
        self.assertEqual(self.parser.action_data(line="_aMtm		db 'MTM'").produce_c_data_single(), ("{'M','T','M'}, // _amtm\n", 'char _amtm[3];\n', 3))

    def test_data_11690(self):
        self.assertEqual(self.parser.action_data(line="_aMute		db '<Mute>                ',0 ; DATA XREF: seg001:1949o").produce_c_data_single(), ('"<Mute>                ", // _amute\n', 'char _amute[23];\n', 23))

    def test_data_11700(self):
        self.assertEqual(self.parser.action_data(line="_aMuteChannel	db '  Mute channel'").produce_c_data_single(), ("{' ',' ','M','u','t','e',' ','c','h','a','n','n','e','l'}, // _amutechannel\n", 'char _amutechannel[14];\n', 14))

    def test_data_11710(self):
        self.assertEqual(self.parser.action_data(line="_aName		db 'name'               ; DATA XREF: _start+692w").produce_c_data_single(), ("{'n','a','m','e'}, // _aname\n", 'char _aname[4];\n', 4))

    def test_data_11720(self):
        self.assertEqual(self.parser.action_data(line="_aNotEnoughDramOn db 'Not enough DRAM on UltraSound',0Dh,0Ah,0").produce_c_data_single(), ('"Not enough DRAM on UltraSound\\r\\n", // _anotenoughdramon\n', 'char _anotenoughdramon[32];\n', 32))

    def test_data_11730(self):
        self.assertEqual(self.parser.action_data(line="_aNotEnoughDram_0 db 'Not enough DRAM on your UltraSound to load all samples!',0").produce_c_data_single(), ('"Not enough DRAM on your UltraSound to load all samples!", // _anotenoughdram_0\n', 'char _anotenoughdram_0[56];\n', 56))

    def test_data_11740(self):
        self.assertEqual(self.parser.action_data(line="_aNotEnoughMemo_0 db 'Not enough memory available to load all samples!',0").produce_c_data_single(), ('"Not enough memory available to load all samples!", // _anotenoughmemo_0\n', 'char _anotenoughmemo_0[49];\n', 49))

    def test_data_11750(self):
        self.assertEqual(self.parser.action_data(line="_aNotEnoughMemor	db 'Not enough memory.',0Dh,0Ah,'$' ; DATA XREF: _start+23Do").produce_c_data_single(), ("{'N','o','t',' ','e','n','o','u','g','h',' ','m','e','m','o','r','y','.','\\r','\\n','$'}, // _anotenoughmemor\n", 'char _anotenoughmemor[21];\n', 21))

    def test_data_11760(self):
        self.assertEqual(self.parser.action_data(line="_aNotEnoughMemory db 'Not enough Memory available',0Dh,0Ah,0").produce_c_data_single(), ('"Not enough Memory available\\r\\n", // _anotenoughmemory\n', 'char _anotenoughmemory[30];\n', 30))

    def test_data_11770(self):
        self.assertEqual(self.parser.action_data(line="_aNoteCut	db 'Note Cut       ',0").produce_c_data_single(), ('"Note Cut       ", // _anotecut\n', 'char _anotecut[16];\n', 16))

    def test_data_11780(self):
        self.assertEqual(self.parser.action_data(line="_aNoteDelay	db 'Note Delay     ',0").produce_c_data_single(), ('"Note Delay     ", // _anotedelay\n', 'char _anotedelay[16];\n', 16))

    def test_data_11790(self):
        self.assertEqual(self.parser.action_data(line="_aNtsc		db '(NTSC)',0           ; DATA XREF: _txt_draw_bottom+53o").produce_c_data_single(), ('"(NTSC)", // _antsc\n', 'char _antsc[7];\n', 7))

    def test_data_11800(self):
        self.assertEqual(self.parser.action_data(line="_aOcta		db 'OCTA'").produce_c_data_single(), ("{'O','C','T','A'}, // _aocta\n", 'char _aocta[4];\n', 4))

    def test_data_11810(self):
        self.assertEqual(self.parser.action_data(line="_aPal		db '(PAL) ',0           ; DATA XREF: _txt_draw_bottom+49o").produce_c_data_single(), ('"(PAL) ", // _apal\n', 'char _apal[7];\n', 7))

    def test_data_11820(self):
        self.assertEqual(self.parser.action_data(line="_aPatternBreak	db 'Pattern Break  ',0").produce_c_data_single(), ('"Pattern Break  ", // _apatternbreak\n', 'char _apatternbreak[16];\n', 16))

    def test_data_11830(self):
        self.assertEqual(self.parser.action_data(line="_aPatternDelay	db 'Pattern Delay  ',0").produce_c_data_single(), ('"Pattern Delay  ", // _apatterndelay\n', 'char _apatterndelay[16];\n', 16))

    def test_data_11840(self):
        self.assertEqual(self.parser.action_data(line="_aPause		db 'Pause'").produce_c_data_single(), ("{'P','a','u','s','e'}, // _apause\n", 'char _apause[5];\n', 5))

    def test_data_11850(self):
        self.assertEqual(self.parser.action_data(line="_aPcHonker	db 'PC Honker',0        ; DATA XREF: dseg:02BCo").produce_c_data_single(), ('"PC Honker", // _apchonker\n', 'char _apchonker[10];\n', 10))

    def test_data_11860(self):
        self.assertEqual(self.parser.action_data(line="_aPcHonker_0	db 'PC Honker',0        ; DATA XREF: seg003:0D6Co").produce_c_data_single(), ('"PC Honker", // _apchonker_0\n', 'char _apchonker_0[10];\n', 10))

    def test_data_11870(self):
        self.assertEqual(self.parser.action_data(line="_aPgdn		db 'PgDn'").produce_c_data_single(), ("{'P','g','D','n'}, // _apgdn\n", 'char _apgdn[4];\n', 4))

    def test_data_11880(self):
        self.assertEqual(self.parser.action_data(line="_aPgup		db 'PgUp'").produce_c_data_single(), ("{'P','g','U','p'}, // _apgup\n", 'char _apgup[4];\n', 4))

    def test_data_11890(self):
        self.assertEqual(self.parser.action_data(line="_aPlayer13029521	db 'Player: '").produce_c_data_single(), ("{'P','l','a','y','e','r',':',' '}, // _aplayer13029521\n", 'char _aplayer13029521[8];\n', 8))

    def test_data_11900(self):
        self.assertEqual(self.parser.action_data(line="_aPlayingInStereoFree db	' Playing in Stereo, Free:'").produce_c_data_single(), ("{' ','P','l','a','y','i','n','g',' ','i','n',' ','S','t','e','r','e','o',',',' ','F','r','e','e',':'}, // _aplayinginstereofree\n", 'char _aplayinginstereofree[25];\n', 25))

    def test_data_11910(self):
        self.assertEqual(self.parser.action_data(line="_aPlaypausloop	db 'PlayPausLoop'       ; DATA XREF: _txt_draw_bottom+164o").produce_c_data_single(), ("{'P','l','a','y','P','a','u','s','L','o','o','p'}, // _aplaypausloop\n", 'char _aplaypausloop[12];\n', 12))

    def test_data_11920(self):
        self.assertEqual(self.parser.action_data(line="_aPortVolslide	db 'Port + VolSlide',0").produce_c_data_single(), ('"Port + VolSlide", // _aportvolslide\n', 'char _aportvolslide[16];\n', 16))

    def test_data_11930(self):
        self.assertEqual(self.parser.action_data(line="_aPortamentoDown	db 'Portamento Down',0").produce_c_data_single(), ('"Portamento Down", // _aportamentodown\n', 'char _aportamentodown[16];\n', 16))

    def test_data_11940(self):
        self.assertEqual(self.parser.action_data(line="_aPortamentoUp	db 'Portamento Up  ',0").produce_c_data_single(), ('"Portamento Up  ", // _aportamentoup\n', 'char _aportamentoup[16];\n', 16))

    def test_data_11950(self):
        self.assertEqual(self.parser.action_data(line="_aPositionJump	db 'Position Jump  ',0").produce_c_data_single(), ('"Position Jump  ", // _apositionjump\n', 'char _apositionjump[16];\n', 16))

    def test_data_11960(self):
        self.assertEqual(self.parser.action_data(line="_aPress		db 'Press '").produce_c_data_single(), ("{'P','r','e','s','s',' '}, // _apress\n", 'char _apress[6];\n', 6))

    def test_data_11970(self):
        self.assertEqual(self.parser.action_data(line="_aPressAnyKeyToReturn db	'Press any key to return to the fileselector',0").produce_c_data_single(), ('"Press any key to return to the fileselector", // _apressanykeytoreturn\n', 'char _apressanykeytoreturn[44];\n', 44))

    def test_data_11980(self):
        self.assertEqual(self.parser.action_data(line="_aPressF1ForHelpQu db '                 Press F-1 for help, QuickRead='").produce_c_data_single(), ("{' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','P','r','e','s','s',' ','F','-','1',' ','f','o','r',' ','h','e','l','p',',',' ','Q','u','i','c','k','R','e','a','d','='}, // _apressf1forhelpqu\n", 'char _apressf1forhelpqu[47];\n', 47))

    def test_data_11990(self):
        self.assertEqual(self.parser.action_data(line="_aProAudioSpectr	db 'Pro Audio Spectrum 16',0 ; DATA XREF: dseg:02ACo").produce_c_data_single(), ('"Pro Audio Spectrum 16", // _aproaudiospectr\n', 'char _aproaudiospectr[22];\n', 22))

    def test_data_12000(self):
        self.assertEqual(self.parser.action_data(line="_aProAudioSpectrum db 'Pro Audio Spectrum 16',0 ; DATA XREF: seg003:0D5Co").produce_c_data_single(), ('"Pro Audio Spectrum 16", // _aproaudiospectrum\n', 'char _aproaudiospectrum[22];\n', 22))

    def test_data_12010(self):
        self.assertEqual(self.parser.action_data(line="_aProtracker1_0C	db 7Eh").produce_c_data_single(), ('126, // _aprotracker1_0c\n', 'db _aprotracker1_0c;\n', 1))

    def test_data_12020(self):
        self.assertEqual(self.parser.action_data(line="_aProtracker1_0Compat db	'  ProTracker 1.0 compatibility on/off'").produce_c_data_single(), ("{' ',' ','P','r','o','T','r','a','c','k','e','r',' ','1','.','0',' ','c','o','m','p','a','t','i','b','i','l','i','t','y',' ','o','n','/','o','f','f'}, // _aprotracker1_0compat\n", 'char _aprotracker1_0compat[37];\n', 37))

    def test_data_12030(self):
        self.assertEqual(self.parser.action_data(line="_aProtracker1_0_0 db ' ProTracker 1.0'").produce_c_data_single(), ("{' ','P','r','o','T','r','a','c','k','e','r',' ','1','.','0'}, // _aprotracker1_0_0\n", 'char _aprotracker1_0_0[15];\n', 15))

    def test_data_12040(self):
        self.assertEqual(self.parser.action_data(line="_aPsm		db 'PSM■'").produce_c_data_single(), ("{'P','S','M','\\xfe'}, // _apsm\n", 'char _apsm[4];\n', 4))

    def test_data_12050(self):
        self.assertEqual(self.parser.action_data(line="_aQuitIplay	db 'Quit IPLAY'").produce_c_data_single(), ("{'Q','u','i','t',' ','I','P','L','A','Y'}, // _aquitiplay\n", 'char _aquitiplay[10];\n', 10))

    def test_data_12060(self):
        self.assertEqual(self.parser.action_data(line="_aRealtimeVuMeters db '  Realtime VU meters'").produce_c_data_single(), ("{' ',' ','R','e','a','l','t','i','m','e',' ','V','U',' ','m','e','t','e','r','s'}, // _arealtimevumeters\n", 'char _arealtimevumeters[20];\n', 20))

    def test_data_12070(self):
        self.assertEqual(self.parser.action_data(line="_aRetrigVolume	db 'Retrig+Volume  ',0").produce_c_data_single(), ('"Retrig+Volume  ", // _aretrigvolume\n', 'char _aretrigvolume[16];\n', 16))

    def test_data_12080(self):
        self.assertEqual(self.parser.action_data(line="_aRetriggerNote	db 'Retrigger Note ',0").produce_c_data_single(), ('"Retrigger Note ", // _aretriggernote\n', 'char _aretriggernote[16];\n', 16))

    def test_data_12090(self):
        self.assertEqual(self.parser.action_data(line="_aReturnToPlaymodeOnl db	'Return to playmode [Only if the music is playing]'").produce_c_data_single(), ("{'R','e','t','u','r','n',' ','t','o',' ','p','l','a','y','m','o','d','e',' ','[','O','n','l','y',' ','i','f',' ','t','h','e',' ','m','u','s','i','c',' ','i','s',' ','p','l','a','y','i','n','g',']'}, // _areturntoplaymodeonl\n", 'char _areturntoplaymodeonl[49];\n', 49))

    def test_data_12100(self):
        self.assertEqual(self.parser.action_data(line="_aSamplename	db '# SampleName   '    ; DATA XREF: seg001:1B7Co").produce_c_data_single(), ("{'#',' ','S','a','m','p','l','e','N','a','m','e',' ',' ',' '}, // _asamplename\n", 'char _asamplename[15];\n', 15))

    def test_data_12110(self):
        self.assertEqual(self.parser.action_data(line="_aSamplesUsed	db 'Samples Used  :'").produce_c_data_single(), ("{'S','a','m','p','l','e','s',' ','U','s','e','d',' ',' ',':'}, // _asamplesused\n", 'char _asamplesused[15];\n', 15))

    def test_data_12120(self):
        self.assertEqual(self.parser.action_data(line="_aScream		db '!Scream!'").produce_c_data_single(), ("{'!','S','c','r','e','a','m','!'}, // _ascream\n", 'char _ascream[8];\n', 8))

    def test_data_12130(self):
        self.assertEqual(self.parser.action_data(line="_aScrm		db 'SCRM'").produce_c_data_single(), ("{'S','C','R','M'}, // _ascrm\n", 'char _ascrm[4];\n', 4))

    def test_data_12140(self):
        self.assertEqual(self.parser.action_data(line="_aScrolllock	db 'ScrollLock'").produce_c_data_single(), ("{'S','c','r','o','l','l','L','o','c','k'}, // _ascrolllock\n", 'char _ascrolllock[10];\n', 10))

    def test_data_12150(self):
        self.assertEqual(self.parser.action_data(line="_aSdanes@marvels_hack db	'sdanes@marvels.hacktic.nl'").produce_c_data_single(), ("{'s','d','a','n','e','s','@','m','a','r','v','e','l','s','.','h','a','c','k','t','i','c','.','n','l'}, // _asdanesarbmarvels_hack\n", 'char _asdanesarbmarvels_hack[25];\n', 25))

    def test_data_12160(self):
        self.assertEqual(self.parser.action_data(line="_aSendEmailTo	db 'Send email to '").produce_c_data_single(), ("{'S','e','n','d',' ','e','m','a','i','l',' ','t','o',' '}, // _asendemailto\n", 'char _asendemailto[14];\n', 14))

    def test_data_12170(self):
        self.assertEqual(self.parser.action_data(line="_aSetAmplify	db 'Set Amplify    ',0").produce_c_data_single(), ('"Set Amplify    ", // _asetamplify\n', 'char _asetamplify[16];\n', 16))

    def test_data_12180(self):
        self.assertEqual(self.parser.action_data(line="_aSetFilter	db 'Set Filter     ',0  ; DATA XREF: seg001:1A9Ao").produce_c_data_single(), ('"Set Filter     ", // _asetfilter\n', 'char _asetfilter[16];\n', 16))

    def test_data_12190(self):
        self.assertEqual(self.parser.action_data(line="_aSetFinetune	db 'Set FineTune   ',0").produce_c_data_single(), ('"Set FineTune   ", // _asetfinetune\n', 'char _asetfinetune[16];\n', 16))

    def test_data_12200(self):
        self.assertEqual(self.parser.action_data(line="_aSetLoopPoint	db 'Set Loop Point ',0  ; DATA XREF: seg001:1A8Fo").produce_c_data_single(), ('"Set Loop Point ", // _asetlooppoint\n', 'char _asetlooppoint[16];\n', 16))

    def test_data_12210(self):
        self.assertEqual(self.parser.action_data(line="_aSetPanning	db 'Set Panning    ',0").produce_c_data_single(), ('"Set Panning    ", // _asetpanning\n', 'char _asetpanning[16];\n', 16))

    def test_data_12220(self):
        self.assertEqual(self.parser.action_data(line="_aSetSampleOfs	db 'Set Sample Ofs ',0").produce_c_data_single(), ('"Set Sample Ofs ", // _asetsampleofs\n', 'char _asetsampleofs[16];\n', 16))

    def test_data_12230(self):
        self.assertEqual(self.parser.action_data(line="_aSetSpeed	db 'Set Speed      ',0").produce_c_data_single(), ('"Set Speed      ", // _asetspeed\n', 'char _asetspeed[16];\n', 16))

    def test_data_12240(self):
        self.assertEqual(self.parser.action_data(line="_aSetSpeedBpm	db 'Set Speed/BPM  ',0").produce_c_data_single(), ('"Set Speed/BPM  ", // _asetspeedbpm\n', 'char _asetspeedbpm[16];\n', 16))

    def test_data_12250(self):
        self.assertEqual(self.parser.action_data(line="_aSetStmSpeed	db 'Set STM Speed  ',0").produce_c_data_single(), ('"Set STM Speed  ", // _asetstmspeed\n', 'char _asetstmspeed[16];\n', 16))

    def test_data_12260(self):
        self.assertEqual(self.parser.action_data(line="_aShell130295211	db 'Shell: 13/02/95 21:15:58'").produce_c_data_single(), ("{'S','h','e','l','l',':',' ','1','3','/','0','2','/','9','5',' ','2','1',':','1','5',':','5','8'}, // _ashell130295211\n", 'char _ashell130295211[24];\n', 24))

    def test_data_12270(self):
        self.assertEqual(self.parser.action_data(line="_aShellingToOperating db	'Shelling to Operating System...'").produce_c_data_single(), ("{'S','h','e','l','l','i','n','g',' ','t','o',' ','O','p','e','r','a','t','i','n','g',' ','S','y','s','t','e','m','.','.','.'}, // _ashellingtooperating\n", 'char _ashellingtooperating[31];\n', 31))

    def test_data_12280(self):
        self.assertEqual(self.parser.action_data(line="_aSizeVolModeC2T	db '~   Size Vol Mode  C-2 Tune LoopPos LoopEnd',0").produce_c_data_single(), ('"~   Size Vol Mode  C-2 Tune LoopPos LoopEnd", // _asizevolmodec2t\n', 'char _asizevolmodec2t[44];\n', 44))

    def test_data_12290(self):
        self.assertEqual(self.parser.action_data(line="_aSoYouWantedSomeHelp db	'So you wanted some help?'").produce_c_data_single(), ("{'S','o',' ','y','o','u',' ','w','a','n','t','e','d',' ','s','o','m','e',' ','h','e','l','p','?'}, // _asoyouwantedsomehelp\n", 'char _asoyouwantedsomehelp[24];\n', 24))

    def test_data_12300(self):
        self.assertEqual(self.parser.action_data(line="_aSomeFunctionsOf db 'Some functions of the UltraSound do not work!',0Dh,0Ah").produce_c_data_single(), ("{'S','o','m','e',' ','f','u','n','c','t','i','o','n','s',' ','o','f',' ','t','h','e',' ','U','l','t','r','a','S','o','u','n','d',' ','d','o',' ','n','o','t',' ','w','o','r','k','!','\\r','\\n'}, // _asomefunctionsof\n", 'char _asomefunctionsof[47];\n', 47))

    def test_data_12310(self):
        self.assertEqual(self.parser.action_data(line="_aSoundBlaster	db 'Sound Blaster',0    ; DATA XREF: dseg:02B4o").produce_c_data_single(), ('"Sound Blaster", // _asoundblaster\n', 'char _asoundblaster[14];\n', 14))

    def test_data_12320(self):
        self.assertEqual(self.parser.action_data(line="_aSoundBlaster16	db 'Sound Blaster 16/16ASP',0 ; DATA XREF: dseg:02B0o").produce_c_data_single(), ('"Sound Blaster 16/16ASP", // _asoundblaster16\n', 'char _asoundblaster16[23];\n', 23))

    def test_data_12330(self):
        self.assertEqual(self.parser.action_data(line="_aSoundBlaster1616 db 'Sound Blaster 16/16ASP',0 ; DATA XREF: seg003:0D60o").produce_c_data_single(), ('"Sound Blaster 16/16ASP", // _asoundblaster1616\n', 'char _asoundblaster1616[23];\n', 23))

    def test_data_12340(self):
        self.assertEqual(self.parser.action_data(line="_aSoundBlasterPr	db 'Sound Blaster Pro',0 ; DATA XREF: dseg:02B2o").produce_c_data_single(), ('"Sound Blaster Pro", // _asoundblasterpr\n', 'char _asoundblasterpr[18];\n', 18))

    def test_data_12350(self):
        self.assertEqual(self.parser.action_data(line="_aSoundBlasterPro db 'Sound Blaster Pro',0 ; DATA XREF: seg003:0D62o").produce_c_data_single(), ('"Sound Blaster Pro", // _asoundblasterpro\n', 'char _asoundblasterpro[18];\n', 18))

    def test_data_12360(self):
        self.assertEqual(self.parser.action_data(line="_aSoundBlaster_0	db 'Sound Blaster',0    ; DATA XREF: seg003:0D64o").produce_c_data_single(), ('"Sound Blaster", // _asoundblaster_0\n', 'char _asoundblaster_0[14];\n', 14))

    def test_data_12370(self):
        self.assertEqual(self.parser.action_data(line="_aSpeed		db 'Speed'").produce_c_data_single(), ("{'S','p','e','e','d'}, // _aspeed\n", 'char _aspeed[5];\n', 5))

    def test_data_12380(self):
        self.assertEqual(self.parser.action_data(line="_aStereoOn1	db 'Stereo-On-1',0      ; DATA XREF: dseg:02B8o").produce_c_data_single(), ('"Stereo-On-1", // _astereoon1\n', 'char _astereoon1[12];\n', 12))

    def test_data_12390(self):
        self.assertEqual(self.parser.action_data(line="_aStereoOn1_0	db 'Stereo-On-1',0      ; DATA XREF: seg003:0D68o").produce_c_data_single(), ('"Stereo-On-1", // _astereoon1_0\n', 'char _astereoon1_0[12];\n', 12))

    def test_data_12400(self):
        self.assertEqual(self.parser.action_data(line="_aSubscribeInertiaLis db	'subscribe inertia-list YourRealName'").produce_c_data_single(), ("{'s','u','b','s','c','r','i','b','e',' ','i','n','e','r','t','i','a','-','l','i','s','t',' ','Y','o','u','r','R','e','a','l','N','a','m','e'}, // _asubscribeinertialis\n", 'char _asubscribeinertialis[35];\n', 35))

    def test_data_12410(self):
        self.assertEqual(self.parser.action_data(line="_aSubscribeInertiaTal db	'subscribe inertia-talk YourRealName',0").produce_c_data_single(), ('"subscribe inertia-talk YourRealName", // _asubscribeinertiatal\n', 'char _asubscribeinertiatal[36];\n', 36))

    def test_data_12420(self):
        self.assertEqual(self.parser.action_data(line="_aTab		db 'Tab'").produce_c_data_single(), ("{'T','a','b'}, // _atab\n", 'char _atab[3];\n', 3))

    def test_data_12430(self):
        self.assertEqual(self.parser.action_data(line="_aTab_0		db 'Tab'").produce_c_data_single(), ("{'T','a','b'}, // _atab_0\n", 'char _atab_0[3];\n', 3))

    def test_data_12440(self):
        self.assertEqual(self.parser.action_data(line="_aTdz		db 'TDZ'").produce_c_data_single(), ("{'T','D','Z'}, // _atdz\n", 'char _atdz[3];\n', 3))

    def test_data_12450(self):
        self.assertEqual(self.parser.action_data(line="_aThe		db 'the '").produce_c_data_single(), ("{'t','h','e',' '}, // _athe\n", 'char _athe[4];\n', 4))

    def test_data_12460(self):
        self.assertEqual(self.parser.action_data(line="_aThisHelpScreenButIG db	'This help screen, but I guess you already found it...'").produce_c_data_single(), ("{'T','h','i','s',' ','h','e','l','p',' ','s','c','r','e','e','n',',',' ','b','u','t',' ','I',' ','g','u','e','s','s',' ','y','o','u',' ','a','l','r','e','a','d','y',' ','f','o','u','n','d',' ','i','t','.','.','.'}, // _athishelpscreenbutig\n", 'char _athishelpscreenbutig[53];\n', 53))

    def test_data_12470(self):
        self.assertEqual(self.parser.action_data(line="_aThisProgramRequ db 'This program requires the soundcards device driver.',0Dh,0Ah,0").produce_c_data_single(), ('"This program requires the soundcards device driver.\\r\\n", // _athisprogramrequ\n', 'char _athisprogramrequ[54];\n', 54))

    def test_data_12480(self):
        self.assertEqual(self.parser.action_data(line="_aToConnectToBinaryIn db	'To connect to Binary Inertia releases: '").produce_c_data_single(), ("{'T','o',' ','c','o','n','n','e','c','t',' ','t','o',' ','B','i','n','a','r','y',' ','I','n','e','r','t','i','a',' ','r','e','l','e','a','s','e','s',':',' '}, // _atoconnecttobinaryin\n", 'char _atoconnecttobinaryin[39];\n', 39))

    def test_data_12490(self):
        self.assertEqual(self.parser.action_data(line="_aToConnectToDiscussi db	'To connect to Discussion Mailing list: '").produce_c_data_single(), ("{'T','o',' ','c','o','n','n','e','c','t',' ','t','o',' ','D','i','s','c','u','s','s','i','o','n',' ','M','a','i','l','i','n','g',' ','l','i','s','t',':',' '}, // _atoconnecttodiscussi\n", 'char _atoconnecttodiscussi[39];\n', 39))

    def test_data_12500(self):
        self.assertEqual(self.parser.action_data(line="_aToMoveTheHighlighte db	' to move the highlighted bar'").produce_c_data_single(), ("{' ','t','o',' ','m','o','v','e',' ','t','h','e',' ','h','i','g','h','l','i','g','h','t','e','d',' ','b','a','r'}, // _atomovethehighlighte\n", 'char _atomovethehighlighte[28];\n', 28))

    def test_data_12510(self):
        self.assertEqual(self.parser.action_data(line="_aToPlayTheModuleOrSe db	' to play the module or select the drive/directory'").produce_c_data_single(), ("{' ','t','o',' ','p','l','a','y',' ','t','h','e',' ','m','o','d','u','l','e',' ','o','r',' ','s','e','l','e','c','t',' ','t','h','e',' ','d','r','i','v','e','/','d','i','r','e','c','t','o','r','y'}, // _atoplaythemoduleorse\n", 'char _atoplaythemoduleorse[49];\n', 49))

    def test_data_12520(self):
        self.assertEqual(self.parser.action_data(line="_aToReturnTo	db ' to return to '").produce_c_data_single(), ("{' ','t','o',' ','r','e','t','u','r','n',' ','t','o',' '}, // _atoreturnto\n", 'char _atoreturnto[14];\n', 14))

    def test_data_12530(self):
        self.assertEqual(self.parser.action_data(line="_aToSubscribeToOneOrB db	' to subscribe to one or both of'").produce_c_data_single(), ("{' ','t','o',' ','s','u','b','s','c','r','i','b','e',' ','t','o',' ','o','n','e',' ','o','r',' ','b','o','t','h',' ','o','f'}, // _atosubscribetooneorb\n", 'char _atosubscribetooneorb[31];\n', 31))

    def test_data_12540(self):
        self.assertEqual(self.parser.action_data(line="_aToggle24bitInt	db 7Eh").produce_c_data_single(), ('126, // _atoggle24bitint\n', 'db _atoggle24bitint;\n', 1))

    def test_data_12550(self):
        self.assertEqual(self.parser.action_data(line="_aToggle24bitInterpol db	' Toggle 24bit Interpolation'").produce_c_data_single(), ("{' ','T','o','g','g','l','e',' ','2','4','b','i','t',' ','I','n','t','e','r','p','o','l','a','t','i','o','n'}, // _atoggle24bitinterpol\n", 'char _atoggle24bitinterpol[27];\n', 27))

    def test_data_12560(self):
        self.assertEqual(self.parser.action_data(line="_aTogglePalNtsc	db '  Toggle PAL/NTSC',0").produce_c_data_single(), ('"  Toggle PAL/NTSC", // _atogglepalntsc\n', 'char _atogglepalntsc[18];\n', 18))

    def test_data_12570(self):
        self.assertEqual(self.parser.action_data(line="_aToggleQuickreadingO db	'Toggle QuickReading of module name'").produce_c_data_single(), ("{'T','o','g','g','l','e',' ','Q','u','i','c','k','R','e','a','d','i','n','g',' ','o','f',' ','m','o','d','u','l','e',' ','n','a','m','e'}, // _atogglequickreadingo\n", 'char _atogglequickreadingo[34];\n', 34))

    def test_data_12580(self):
        self.assertEqual(self.parser.action_data(line="_aTonePortamento	db 'Tone Portamento',0").produce_c_data_single(), ('"Tone Portamento", // _atoneportamento\n', 'char _atoneportamento[16];\n', 16))

    def test_data_12590(self):
        self.assertEqual(self.parser.action_data(line="_aTrackPosition	db 'Track Position:'").produce_c_data_single(), ("{'T','r','a','c','k',' ','P','o','s','i','t','i','o','n',':'}, // _atrackposition\n", 'char _atrackposition[15];\n', 15))

    def test_data_12600(self):
        self.assertEqual(self.parser.action_data(line="_aTremolo	db 'Tremolo        ',0").produce_c_data_single(), ('"Tremolo        ", // _atremolo\n', 'char _atremolo[16];\n', 16))

    def test_data_12610(self):
        self.assertEqual(self.parser.action_data(line="_aTremoloControl	db 'Tremolo Control',0").produce_c_data_single(), ('"Tremolo Control", // _atremolocontrol\n', 'char _atremolocontrol[16];\n', 16))

    def test_data_12620(self):
        self.assertEqual(self.parser.action_data(line="_aTremor		db 'Tremor         ',0").produce_c_data_single(), ('"Tremor         ", // _atremor\n', 'char _atremor[16];\n', 16))

    def test_data_12630(self):
        self.assertEqual(self.parser.action_data(line="_aTriller	db 'Triller        ',0").produce_c_data_single(), ('"Triller        ", // _atriller\n', 'char _atriller[16];\n', 16))

    def test_data_12640(self):
        self.assertEqual(self.parser.action_data(line="_aType		db 'Type '").produce_c_data_single(), ("{'T','y','p','e',' '}, // _atype\n", 'char _atype[5];\n', 5))

    def test_data_12650(self):
        self.assertEqual(self.parser.action_data(line="_aUnused256	db ' Unused'").produce_c_data_single(), ("{'\x7f',' ','U','n','u','s','e','d'}, // _aunused256\n", 'char _aunused256[8];\n', 8))

    def test_data_12660(self):
        self.assertEqual(self.parser.action_data(line="_aUse		db 'Use '").produce_c_data_single(), ("{'U','s','e',' '}, // _ause\n", 'char _ause[4];\n', 4))

    def test_data_12670(self):
        self.assertEqual(self.parser.action_data(line="_aVibrVolslide	db 'Vibr + VolSlide',0").produce_c_data_single(), ('"Vibr + VolSlide", // _avibrvolslide\n', 'char _avibrvolslide[16];\n', 16))

    def test_data_12680(self):
        self.assertEqual(self.parser.action_data(line="_aVibrato	db 'Vibrato        ',0").produce_c_data_single(), ('"Vibrato        ", // _avibrato\n', 'char _avibrato[16];\n', 16))

    def test_data_12690(self):
        self.assertEqual(self.parser.action_data(line="_aVibratoControl	db 'Vibrato Control',0").produce_c_data_single(), ('"Vibrato Control", // _avibratocontrol\n', 'char _avibratocontrol[16];\n', 16))

    def test_data_12700(self):
        self.assertEqual(self.parser.action_data(line="_aViewSampleNamesTwic db	'  View sample names (twice for more)'").produce_c_data_single(), ("{' ',' ','V','i','e','w',' ','s','a','m','p','l','e',' ','n','a','m','e','s',' ','(','t','w','i','c','e',' ','f','o','r',' ','m','o','r','e',')'}, // _aviewsamplenamestwic\n", 'char _aviewsamplenamestwic[36];\n', 36))

    def test_data_12710(self):
        self.assertEqual(self.parser.action_data(line="_aVolumeAmplify	db 'Volume Amplify:'").produce_c_data_single(), ("{'V','o','l','u','m','e',' ','A','m','p','l','i','f','y',':'}, // _avolumeamplify\n", 'char _avolumeamplify[15];\n', 15))

    def test_data_12720(self):
        self.assertEqual(self.parser.action_data(line="_aVolumeChange	db 'Volume Change  ',0").produce_c_data_single(), ('"Volume Change  ", // _avolumechange\n', 'char _avolumechange[16];\n', 16))

    def test_data_12730(self):
        self.assertEqual(self.parser.action_data(line="_aVolumeSliding	db 'Volume Sliding ',0").produce_c_data_single(), ('"Volume Sliding ", // _avolumesliding\n', 'char _avolumesliding[16];\n', 16))

    def test_data_12740(self):
        self.assertEqual(self.parser.action_data(line="_aWhichIsWrittenIn db ' which is written in '").produce_c_data_single(), ("{' ','w','h','i','c','h',' ','i','s',' ','w','r','i','t','t','e','n',' ','i','n',' '}, // _awhichiswrittenin\n", 'char _awhichiswrittenin[21];\n', 21))

    def test_data_12750(self):
        self.assertEqual(self.parser.action_data(line="_aWindowsSoundSy	db 'Windows Sound System',0 ; DATA XREF: dseg:02AEo").produce_c_data_single(), ('"Windows Sound System", // _awindowssoundsy\n', 'char _awindowssoundsy[21];\n', 21))

    def test_data_12760(self):
        self.assertEqual(self.parser.action_data(line="_aWindowsSoundSyst db 'Windows Sound System',0 ; DATA XREF: seg003:0D5Eo").produce_c_data_single(), ('"Windows Sound System", // _awindowssoundsyst\n', 'char _awindowssoundsyst[21];\n', 21))

    def test_data_12770(self):
        self.assertEqual(self.parser.action_data(line="_aXpressF4ForMor	db 'xPress F-4 for more'").produce_c_data_single(), ("{'x','P','r','e','s','s',' ','F','-','4',' ','f','o','r',' ','m','o','r','e'}, // _axpressf4formor\n", 'char _axpressf4formor[19];\n', 19))

    def test_data_12780(self):
        self.assertEqual(self.parser.action_data(line="_a_ext		db '.Ext'               ; DATA XREF: _start+69Bw").produce_c_data_single(), ("{'.','E','x','t'}, // _a_ext\n", 'char _a_ext[4];\n', 4))

    def test_data_12790(self):
        self.assertEqual(self.parser.action_data(line="_a_m_k		db '.M.K'").produce_c_data_single(), ("{'.','M','.','K'}, // _a_m_k\n", 'char _a_m_k[4];\n', 4))

    def test_data_12800(self):
        self.assertEqual(self.parser.action_data(line="_a_mod_nst_669_s	db '.MOD.NST.669.STM.S3M.MTM.PSM.WOW.INR.FAR.ULT.OKT.OCT',0,0,0,0").produce_c_data_single(), ('".MOD.NST.669.STM.S3M.MTM.PSM.WOW.INR.FAR.ULT.OKT.OCT\\0\\0\\0", // _a_mod_nst_669_s\n', 'char _a_mod_nst_669_s[56];\n', 56))

    def test_data_12810(self):
        self.assertEqual(self.parser.action_data(line="_amount_of_x	dw 0			; DATA XREF: _read_module+75w").produce_c_data_single(), ('0, // _amount_of_x\n', 'dw _amount_of_x;\n', 2))

    def test_data_12820(self):
        self.assertEqual(self.parser.action_data(line="_amplification	dw 100			; DATA XREF: _clean_11C43+83w").produce_c_data_single(), ('100, // _amplification\n', 'dw _amplification;\n', 2))

    def test_data_12830(self):
        self.assertEqual(self.parser.action_data(line="_asmprintf_tbl	dw offset _mysprintf_0_nop ; DATA XREF: _myasmsprintf+1Cr").produce_c_data_single(), ('_mysprintf_0_nop, // _asmprintf_tbl\n', 'dw _asmprintf_tbl;\n', 2))

    def test_data_12840(self):
        self.assertEqual(self.parser.action_data(line="_atop_title	dw 152h			; DATA XREF: _txt_draw_top_title+12o").produce_c_data_single(), ('338, // _atop_title\n', 'dw _atop_title;\n', 2))

    def test_data_12850(self):
        self.assertEqual(self.parser.action_data(line="_base_port2	dw 0			; DATA XREF: _wss_init:loc_147C3w").produce_c_data_single(), ('0, // _base_port2\n', 'dw _base_port2;\n', 2))

    def test_data_12860(self):
        self.assertEqual(self.parser.action_data(line="_bit_mode	db 8			; DATA XREF: sub_12DA8+55w").produce_c_data_single(), ('8, // _bit_mode\n', 'db _bit_mode;\n', 1))

    def test_data_12870(self):
        self.assertEqual(self.parser.action_data(line="_bottom_menu	dw 0Ah			; DATA XREF: _text_init2+21Fo").produce_c_data_single(), ('10, // _bottom_menu\n', 'dw _bottom_menu;\n', 2))

    def test_data_12880(self):
        self.assertEqual(self.parser.action_data(line="_buffer_1DBEC	db 0			; DATA XREF: _find_mods+32o").produce_c_data_single(), ('0, // _buffer_1dbec\n', 'db _buffer_1dbec;\n', 1))

    def test_data_12890(self):
        self.assertEqual(self.parser.action_data(line="_buffer_1DC6C	dd 0			; DATA XREF: _start+2C5w _start+2D3o ...").produce_c_data_single(), ('0, // _buffer_1dc6c\n', 'dd _buffer_1dc6c;\n', 4))

    def test_data_12900(self):
        self.assertEqual(self.parser.action_data(line="_buffer_1seg	dw 0			; DATA XREF: _text_init2+18Bw").produce_c_data_single(), ('0, // _buffer_1seg\n', 'dw _buffer_1seg;\n', 2))

    def test_data_12910(self):
        self.assertEqual(self.parser.action_data(line="_buffer_2seg	dw 0			; DATA XREF: seg001:loc_1A913w").produce_c_data_single(), ('0, // _buffer_2seg\n', 'dw _buffer_2seg;\n', 2))

    def test_data_12920(self):
        self.assertEqual(self.parser.action_data(line="_byte_11C29	db 0			; DATA XREF: sub_11C0C:loc_11C14r").produce_c_data_single(), ('0, // _byte_11c29\n', 'db _byte_11c29;\n', 1))

    def test_data_12930(self):
        self.assertEqual(self.parser.action_data(line="_byte_13C54	db 0,9,12h,1Bh,24h,2Dh,36h,40h,40h,4Ah,53h,5Ch,65h,6Eh").produce_c_data_single(), ('{0,9,18,27,36,45,54,64,64,74,83,92,101,110}, // _byte_13c54\n', 'db _byte_13c54[14];\n', 14))

    def test_data_12940(self):
        self.assertEqual(self.parser.action_data(line="_byte_14F70	db 0			; DATA XREF: _configure_timer+12w").produce_c_data_single(), ('0, // _byte_14f70\n', 'db _byte_14f70;\n', 1))

    def test_data_12950(self):
        self.assertEqual(self.parser.action_data(line="_byte_14F71	db 0			; DATA XREF: sub_12D35:loc_12D41w").produce_c_data_single(), ('0, // _byte_14f71\n', 'db _byte_14f71;\n', 1))

    def test_data_12960(self):
        self.assertEqual(self.parser.action_data(line="_byte_14F72	db 0			; DATA XREF: sub_13CF6+Dw _text:4F51r").produce_c_data_single(), ('0, // _byte_14f72\n', 'db _byte_14f72;\n', 1))

    def test_data_12970(self):
        self.assertEqual(self.parser.action_data(line="_byte_14F73	db 0			; DATA XREF: sub_13CF6+11w").produce_c_data_single(), ('0, // _byte_14f73\n', 'db _byte_14f73;\n', 1))

    def test_data_12980(self):
        self.assertEqual(self.parser.action_data(line="_byte_1C1B8	db 0			; DATA XREF: _int9_keybr _dosexec+58w ...").produce_c_data_single(), ('0, // _byte_1c1b8\n', 'db _byte_1c1b8;\n', 1))

    def test_data_12990(self):
        self.assertEqual(self.parser.action_data(line="_byte_1CCEB	db 78h			; DATA XREF: _text_init2:loc_1A6C2w").produce_c_data_single(), ('120, // _byte_1cceb\n', 'db _byte_1cceb;\n', 1))

    def test_data_13000(self):
        self.assertEqual(self.parser.action_data(line="_byte_1D616	db 20h			; DATA XREF: _useless_197F2+Dw").produce_c_data_single(), ('32, // _byte_1d616\n', 'db _byte_1d616;\n', 1))

    def test_data_13010(self):
        self.assertEqual(self.parser.action_data(line="_byte_1D66B	db 20h			; DATA XREF: _useless_197F2+18w").produce_c_data_single(), ('32, // _byte_1d66b\n', 'db _byte_1d66b;\n', 1))

    def test_data_13020(self):
        self.assertEqual(self.parser.action_data(line="_byte_1DC0A	db 62h dup(0)		; DATA XREF: _find_mods+6Fo").produce_c_data_single(), ('{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, // _byte_1dc0a\n', 'db _byte_1dc0a[98];\n', 98))

    def test_data_13030(self):
        self.assertEqual(self.parser.action_data(line="_byte_1DCF7	db 0FFh			; DATA XREF: _callsubx+1Cr _callsubx+55w").produce_c_data_single(), ('255, // _byte_1dcf7\n', 'db _byte_1dcf7;\n', 1))

    def test_data_13040(self):
        self.assertEqual(self.parser.action_data(line="_byte_1DCF8	db 14h			; DATA XREF: _start+DAr	_callsubx+20r ...").produce_c_data_single(), ('20, // _byte_1dcf8\n', 'db _byte_1dcf8;\n', 1))

    def test_data_13050(self):
        self.assertEqual(self.parser.action_data(line="_byte_1DCFB	db 4Bh			; DATA XREF: _callsubx+13r").produce_c_data_single(), ('75, // _byte_1dcfb\n', 'db _byte_1dcfb;\n', 1))

    def test_data_13060(self):
        self.assertEqual(self.parser.action_data(line="_byte_1DE70	db 0			; DATA XREF: _start+168w _start+268w ...").produce_c_data_single(), ('0, // _byte_1de70\n', 'db _byte_1de70;\n', 1))

    def test_data_13070(self):
        self.assertEqual(self.parser.action_data(line="_byte_24629	db 20h			; DATA XREF: _someplaymode+64r").produce_c_data_single(), ('32, // _byte_24629\n', 'db _byte_24629;\n', 1))

    def test_data_13080(self):
        self.assertEqual(self.parser.action_data(line="_byte_257DA	db 10h			; DATA XREF: _useless_writeinr+3Fw").produce_c_data_single(), ('16, // _byte_257da\n', 'db _byte_257da;\n', 1))

    def test_data_13090(self):
        self.assertEqual(self.parser.action_data(line="_byte_280E7	db ?			; DATA XREF: _s3m_module+1F3w").produce_c_data_single(), ('0, // _byte_280e7\n', 'db _byte_280e7;\n', 1))

    def test_data_13100(self):
        self.assertEqual(self.parser.action_data(line="_byte_282E8	db 20h dup( ?)		; DATA XREF: _clean_11C43+AEo").produce_c_data_single(), ('{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, // _byte_282e8\n', 'db _byte_282e8[32];\n', 32))

    def test_data_13110(self):
        self.assertEqual(self.parser.action_data(line="_byte_30577	db ?			; DATA XREF: _e669_module+32r").produce_c_data_single(), ('0, // _byte_30577\n', 'db _byte_30577;\n', 1))

    def test_data_13120(self):
        self.assertEqual(self.parser.action_data(line="_byte_30579	db 21h dup( ?)		; DATA XREF: _e669_module:loc_1096Fr").produce_c_data_single(), ('{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, // _byte_30579\n', 'db _byte_30579[33];\n', 33))

    def test_data_13130(self):
        self.assertEqual(self.parser.action_data(line="_byte_30639	db ?			; DATA XREF: _ult_module+169r").produce_c_data_single(), ('0, // _byte_30639\n', 'db _byte_30639;\n', 1))

    def test_data_13140(self):
        self.assertEqual(self.parser.action_data(line="_byte_3150A	db ?			; DATA XREF: _psm_module+139r").produce_c_data_single(), ('0, // _byte_3150a\n', 'db _byte_3150a;\n', 1))

    def test_data_13150(self):
        self.assertEqual(self.parser.action_data(line="_cfg_buffer	db    4			; DATA XREF: _loadcfg+Co _loadcfg+1Er").produce_c_data_single(), ('4, // _cfg_buffer\n', 'db _cfg_buffer;\n', 1))

    def test_data_13160(self):
        self.assertEqual(self.parser.action_data(line="_chrin		dd ?			; DATA XREF: _moduleread:loc_10033o").produce_c_data_single(), ('0, // _chrin\n', 'dd _chrin;\n', 4))

    def test_data_13170(self):
        self.assertEqual(self.parser.action_data(line="_config_word	dw 0			; DATA XREF: _ems_init+8r").produce_c_data_single(), ('0, // _config_word\n', 'dw _config_word;\n', 2))

    def test_data_13180(self):
        self.assertEqual(self.parser.action_data(line="_configword	dw 218Bh		; DATA XREF: _start+60w	_start+6Cw ...").produce_c_data_single(), ('8587, // _configword\n', 'dw _configword;\n', 2))

    def test_data_13190(self):
        self.assertEqual(self.parser.action_data(line="_covox_txt	db    2			; DATA XREF: seg003:0D7Co seg003:0D7Eo").produce_c_data_single(), ('2, // _covox_txt\n', 'db _covox_txt;\n', 1))

    def test_data_13200(self):
        self.assertEqual(self.parser.action_data(line="_critsectpoint_off dw 0			; DATA XREF: _start+150w").produce_c_data_single(), ('0, // _critsectpoint_off\n', 'dw _critsectpoint_off;\n', 2))

    def test_data_13210(self):
        self.assertEqual(self.parser.action_data(line="_critsectpoint_seg dw 0			; DATA XREF: _start+154w").produce_c_data_single(), ('0, // _critsectpoint_seg\n', 'dw _critsectpoint_seg;\n', 2))

    def test_data_13220(self):
        self.assertEqual(self.parser.action_data(line="_current_patterns dw 0			; DATA XREF: _read_module+5Fw").produce_c_data_single(), ('0, // _current_patterns\n', 'dw _current_patterns;\n', 2))

    def test_data_13230(self):
        self.assertEqual(self.parser.action_data(line="_dma_buf_pointer	dd 0			; DATA XREF: _mod_readfile_11F4E+9Cw").produce_c_data_single(), ('0, // _dma_buf_pointer\n', 'dd _dma_buf_pointer;\n', 4))

    def test_data_13240(self):
        self.assertEqual(self.parser.action_data(line="_dma_channel	db 0			; DATA XREF: _read_sndsettings+11r").produce_c_data_single(), ('0, // _dma_channel\n', 'db _dma_channel;\n', 1))

    def test_data_13250(self):
        self.assertEqual(self.parser.action_data(line="_dma_channel2	db 0			; DATA XREF: _wss_init:loc_147DCw").produce_c_data_single(), ('0, // _dma_channel2\n', 'db _dma_channel2;\n', 1))

    def test_data_13260(self):
        self.assertEqual(self.parser.action_data(line="_dma_channel_0	db 0			; DATA XREF: _mod_readfile_11F4E+8Er").produce_c_data_single(), ('0, // _dma_channel_0\n', 'db _dma_channel_0;\n', 1))

    def test_data_13270(self):
        self.assertEqual(self.parser.action_data(line="_dma_channel_1	db 0FFh			; DATA XREF: _callsubx+Br _callsubx+4Dw").produce_c_data_single(), ('255, // _dma_channel_1\n', 'db _dma_channel_1;\n', 1))

    def test_data_13280(self):
        self.assertEqual(self.parser.action_data(line="_dma_chn_mask	db 0			; DATA XREF: _sb16_init+4Bw").produce_c_data_single(), ('0, // _dma_chn_mask\n', 'db _dma_chn_mask;\n', 1))

    def test_data_13290(self):
        self.assertEqual(self.parser.action_data(line="_dma_mode	db 0			; DATA XREF: _proaud_set+3w _wss_set+3w	...").produce_c_data_single(), ('0, // _dma_mode\n', 'db _dma_mode;\n', 1))

    def test_data_13300(self):
        self.assertEqual(self.parser.action_data(line="_dword_1DCEC	dd 10524E49h		; DATA XREF: _loadcfg+1Ar").produce_c_data_single(), ('273829449, // _dword_1dcec\n', 'dd _dword_1dcec;\n', 4))

    def test_data_13310(self):
        self.assertEqual(self.parser.action_data(line="_dword_1DE2C	dd 0			; DATA XREF: _text_init2+22Aw").produce_c_data_single(), ('0, // _dword_1de2c\n', 'dd _dword_1de2c;\n', 4))

    def test_data_13320(self):
        self.assertEqual(self.parser.action_data(line="_dword_3063D	dd ?			; DATA XREF: _ult_module+225r").produce_c_data_single(), ('0, // _dword_3063d\n', 'dd _dword_3063d;\n', 4))

    def test_data_13330(self):
        self.assertEqual(self.parser.action_data(line="_eModuleNotFound	db 'Module not found',0Dh,0Ah,0 ; DATA XREF: _moduleread+1Co").produce_c_data_single(), ('"Module not found\\r\\n", // _emodulenotfound\n', 'char _emodulenotfound[19];\n', 19))

    @unittest.skip("to check")
    def test_data_13340(self):
        self.assertEqual(self.parser.action_data(line="_effoff_18F60	dw offset _eff_nullsub	; DATA XREF: sub_137D5+16r").produce_c_data_single(), ('k_eff_nullsub, // _effoff_18f60\n', 'dw _effoff_18f60;\n', 2))

    def test_data_13350(self):
        self.assertEqual(self.parser.action_data(line="_ems_enabled	db 0			; DATA XREF: _ems_initw	_ems_init+78w ...").produce_c_data_single(), ('0, // _ems_enabled\n', 'db _ems_enabled;\n', 1))

    def test_data_13360(self):
        self.assertEqual(self.parser.action_data(line="_ems_handle	dw 0			; DATA XREF: _ems_init+74w").produce_c_data_single(), ('0, // _ems_handle\n', 'dw _ems_handle;\n', 2))

    def test_data_13370(self):
        self.assertEqual(self.parser.action_data(line="_ems_log_pagenum	dw 0			; DATA XREF: _ems_init+7Dw").produce_c_data_single(), ('0, // _ems_log_pagenum\n', 'dw _ems_log_pagenum;\n', 2))

    def test_data_13380(self):
        self.assertEqual(self.parser.action_data(line="_ems_pageframe	dw 0			; DATA XREF: _useless_11787+3Er").produce_c_data_single(), ('0, // _ems_pageframe\n', 'dw _ems_pageframe;\n', 2))

    def test_data_13390(self):
        self.assertEqual(self.parser.action_data(line="_esseg_atstart	dw 0			; DATA XREF: _start+5w _parse_cmdline+7r ...").produce_c_data_single(), ('0, // _esseg_atstart\n', 'dw _esseg_atstart;\n', 2))

    def test_data_13400(self):
        self.assertEqual(self.parser.action_data(line="_f1_help_text	dw 3F8h			; DATA XREF: seg001:1CD8o").produce_c_data_single(), ('1016, // _f1_help_text\n', 'dw _f1_help_text;\n', 2))

    def test_data_13410(self):
        self.assertEqual(self.parser.action_data(line="_fhandle_1DE68	dw 0			; DATA XREF: _init_vga_waves+42w").produce_c_data_single(), ('0, // _fhandle_1de68\n', 'dw _fhandle_1de68;\n', 2))

    def test_data_13420(self):
        self.assertEqual(self.parser.action_data(line="_fhandle_module	dw 0			; DATA XREF: _moduleread+19w").produce_c_data_single(), ('0, // _fhandle_module\n', 'dw _fhandle_module;\n', 2))

    def test_data_13430(self):
        self.assertEqual(self.parser.action_data(line="_flag_playsetttings db 0			; DATA XREF: _clean_11C43+68r").produce_c_data_single(), ('0, // _flag_playsetttings\n', 'db _flag_playsetttings;\n', 1))

    def test_data_13440(self):
        self.assertEqual(self.parser.action_data(line="_flg_play_settings db 0			; DATA XREF: _keyb_screen_loop+2Fw").produce_c_data_single(), ('0, // _flg_play_settings\n', 'db _flg_play_settings;\n', 1))

    def test_data_13450(self):
        self.assertEqual(self.parser.action_data(line="_frameborder	db '      ██████╔╗╚╝═║┌┐└┘─│╓╖╙╜─║╒╕╘╛═│',0 ; DATA XREF: _draw_frame+3Do").produce_c_data_single(), ('"      '
 '\\xdb\\xdb\\xdb\\xdb\\xdb\\xdb\\xc9\\xbb\\xc8\\xbc\\xcd\\xba\\xda\\xbf\\xc0\\xd9\\xc4\\xb3\\xd6\\xb7\\xd3\\xbd\\xc4\\xba\\xd5\\xb8\\xd4\\xbe\\xcd\\xb3", '
 '// _frameborder\n',
 'char _frameborder[37];\n',
                                                                                                                                                                                     37))

    def test_data_13460(self):
        self.assertEqual(self.parser.action_data(line="_freq1		dw 22050		; DATA XREF: _volume_prepare_waves+48r").produce_c_data_single(), ('22050, // _freq1\n', 'dw _freq1;\n', 2))

    def test_data_13470(self):
        self.assertEqual(self.parser.action_data(line="_freq2		dw 0			; DATA XREF: _read_sndsettings+2Cr").produce_c_data_single(), ('0, // _freq2\n', 'dw _freq2;\n', 2))

    def test_data_13480(self):
        self.assertEqual(self.parser.action_data(line="_freq_1DCF6	db 2Ch			; DATA XREF: _callsubx+Fr _callsubx+51w").produce_c_data_single(), ('44, // _freq_1dcf6\n', 'db _freq_1dcf6;\n', 1))

    def test_data_13490(self):
        self.assertEqual(self.parser.action_data(line="_freq_245DE	dw 0			; DATA XREF: _mod_1024A+40r").produce_c_data_single(), ('0, // _freq_245de\n', 'dw _freq_245de;\n', 2))

    def test_data_13500(self):
        self.assertEqual(self.parser.action_data(line="_freq_246D7	db 0			; DATA XREF: _read_sndsettings+15r").produce_c_data_single(), ('0, // _freq_246d7\n', 'db _freq_246d7;\n', 1))

    def test_data_13510(self):
        self.assertEqual(self.parser.action_data(line="_gravis_port	dw 0			; DATA XREF: _volume_prep+61r").produce_c_data_single(), ('0, // _gravis_port\n', 'dw _gravis_port;\n', 2))

    def test_data_13520(self):
        self.assertEqual(self.parser.action_data(line="_gravis_txt	db    1			; DATA XREF: seg003:_sndcards_text_tblo").produce_c_data_single(), ('1, // _gravis_txt\n', 'db _gravis_txt;\n', 1))

    def test_data_13530(self):
        self.assertEqual(self.parser.action_data(line="_hopeyoulike	dw 3C6h			; DATA XREF: _start+204o").produce_c_data_single(), ('966, // _hopeyoulike\n', 'dw _hopeyoulike;\n', 2))

    def test_data_13540(self):
        self.assertEqual(self.parser.action_data(line="_int1Avect	dd 0			; DATA XREF: _int1a_timer+12r").produce_c_data_single(), ('0, // _int1avect\n', 'dd _int1avect;\n', 4))

    def test_data_13550(self):
        self.assertEqual(self.parser.action_data(line="_int8addr	dd 0			; DATA XREF: sub_12DA8+6Aw").produce_c_data_single(), ('0, // _int8addr\n', 'dd _int8addr;\n', 4))

    def test_data_13560(self):
        self.assertEqual(self.parser.action_data(line="_interrupt_mask	dw 0			; DATA XREF: _setsnd_handler+Cw").produce_c_data_single(), ('0, // _interrupt_mask\n', 'dw _interrupt_mask;\n', 2))

    def test_data_13570(self):
        self.assertEqual(self.parser.action_data(line="_intvectoffset	dw 0			; DATA XREF: _setsnd_handler+2Dw").produce_c_data_single(), ('0, // _intvectoffset\n', 'dw _intvectoffset;\n', 2))

    def test_data_13580(self):
        self.assertEqual(self.parser.action_data(line="_irq_number	db 0			; DATA XREF: _read_sndsettings+Dr").produce_c_data_single(), ('0, // _irq_number\n', 'db _irq_number;\n', 1))

    def test_data_13590(self):
        self.assertEqual(self.parser.action_data(line="_irq_number2	db 0			; DATA XREF: _wss_init:loc_147D0w").produce_c_data_single(), ('0, // _irq_number2\n', 'db _irq_number2;\n', 1))

    def test_data_13600(self):
        self.assertEqual(self.parser.action_data(line="_irq_number_0	db 0			; DATA XREF: _gravis_init+35w").produce_c_data_single(), ('0, // _irq_number_0\n', 'db _irq_number_0;\n', 1))

    def test_data_13610(self):
        self.assertEqual(self.parser.action_data(line="_irq_number_1	db 0FFh			; DATA XREF: _callsubx+7r _callsubx+49w").produce_c_data_single(), ('255, // _irq_number_1\n', 'db _irq_number_1;\n', 1))

    def test_data_13620(self):
        self.assertEqual(self.parser.action_data(line="_is_stereo	db 0			; DATA XREF: sub_1265D+33r").produce_c_data_single(), ('0, // _is_stereo\n', 'db _is_stereo;\n', 1))

    def test_data_13630(self):
        self.assertEqual(self.parser.action_data(line="_key_code	dw 0			; DATA XREF: _start:loc_193FFr").produce_c_data_single(), ('0, // _key_code\n', 'dw _key_code;\n', 2))

    def test_data_13640(self):
        self.assertEqual(self.parser.action_data(line="_keyb_switches	dw 0			; DATA XREF: _start+5D8r").produce_c_data_single(), ('0, // _keyb_switches\n', 'dw _keyb_switches;\n', 2))

    def test_data_13650(self):
        self.assertEqual(self.parser.action_data(line="_memflg_2469A	db 0			; DATA XREF: _alloc_dma_buf+8w").produce_c_data_single(), ('0, // _memflg_2469a\n', 'db _memflg_2469a;\n', 1))

    def test_data_13660(self):
        self.assertEqual(self.parser.action_data(line="_messagepointer	dd 0			; DATA XREF: _start+228r _start+23Dw ...").produce_c_data_single(), ('0, // _messagepointer\n', 'dd _messagepointer;\n', 4))

    def test_data_13670(self):
        self.assertEqual(self.parser.action_data(line="_midi_txt	db    2			; DATA XREF: seg003:0D84o").produce_c_data_single(), ('2, // _midi_txt\n', 'db _midi_txt;\n', 1))

    def test_data_13680(self):
        self.assertEqual(self.parser.action_data(line="_mod_channels_number	dw 0			; DATA XREF: _moduleread+81r").produce_c_data_single(), ('0, // _mod_channels_number\n', 'dw _mod_channels_number;\n', 2))

    def test_data_13690(self):
        self.assertEqual(self.parser.action_data(line="_module_type_text dd 20202020h		; DATA XREF: _mod_n_t_modulew").produce_c_data_single(), ('538976288, // _module_type_text\n', 'dd _module_type_text;\n', 4))

    def test_data_13700(self):
        self.assertEqual(self.parser.action_data(line="_module_type_txt	db '    '               ; DATA XREF: _read_module+6Fw").produce_c_data_single(), ("{' ',' ',' ',' '}, // _module_type_txt\n", 'char _module_type_txt[4];\n', 4))

    def test_data_13710(self):
        self.assertEqual(self.parser.action_data(line="_moduleflag_246D0 dw 0			; DATA XREF: _mod_n_t_module+3Dw").produce_c_data_single(), ('0, // _moduleflag_246d0\n', 'dw _moduleflag_246d0;\n', 2))

    def test_data_13720(self):
        self.assertEqual(self.parser.action_data(line="_mouse_exist_flag db 0			; DATA XREF: _mouse_init:loc_1C6EFw").produce_c_data_single(), ('0, // _mouse_exist_flag\n', 'db _mouse_exist_flag;\n', 1))

    def test_data_13730(self):
        self.assertEqual(self.parser.action_data(line="_mouse_visible	db 0Ah dup(0)		; DATA XREF: _mouse_initw").produce_c_data_single(), ('{0,0,0,0,0,0,0,0,0,0}, // _mouse_visible\n', 'db _mouse_visible[10];\n', 10))

    def test_data_13740(self):
        self.assertEqual(self.parser.action_data(line="_mousecolumn	dw 0			; DATA XREF: _start+7A0r _start+7BCr ...").produce_c_data_single(), ('0, // _mousecolumn\n', 'dw _mousecolumn;\n', 2))

    def test_data_13750(self):
        self.assertEqual(self.parser.action_data(line="_mouserow	dw 0			; DATA XREF: _start+7A3r _start+7BFr ...").produce_c_data_single(), ('0, // _mouserow\n', 'dw _mouserow;\n', 2))

    def test_data_13760(self):
        self.assertEqual(self.parser.action_data(line="_msg		db 'Searching directory for modules  ',0 ; DATA XREF: _start+2F7o").produce_c_data_single(), ('"Searching directory for modules  ", // _msg\n', 'char _msg[34];\n', 34))

    def test_data_13770(self):
        self.assertEqual(self.parser.action_data(line="_multip_244CC	dd 0			; DATA XREF: _spectr_1B084+2Fw").produce_c_data_single(), ('0, // _multip_244cc\n', 'dd _multip_244cc;\n', 4))

    def test_data_13780(self):
        self.assertEqual(self.parser.action_data(line="_multip_244D0	dd 0			; DATA XREF: _spectr_1B084+25w").produce_c_data_single(), ('0, // _multip_244d0\n', 'dd _multip_244d0;\n', 4))

    def test_data_13790(self):
        self.assertEqual(self.parser.action_data(line="_my_in		db ?			; DATA XREF: __2stm_module+50o").produce_c_data_single(), ('0, // _my_in\n', 'db _my_in;\n', 1))

    def test_data_13800(self):
        self.assertEqual(self.parser.action_data(line="_my_seg_index	dw 0			; DATA XREF: _psm_module+136r").produce_c_data_single(), ('0, // _my_seg_index\n', 'dw _my_seg_index;\n', 2))

    def test_data_13810(self):
        self.assertEqual(self.parser.action_data(line="_my_size		dw 0			; DATA XREF: _volume_prep+9w").produce_c_data_single(), ('0, // _my_size\n', 'dw _my_size;\n', 2))

    def test_data_13820(self):
        self.assertEqual(self.parser.action_data(line="_myendl		db 0Dh,0Ah,'$'          ; DATA XREF: _start-1Do").produce_c_data_single(), ("{'\\r','\\n','$'}, // _myendl\n", 'char _myendl[3];\n', 3))

    def test_data_13830(self):
        self.assertEqual(self.parser.action_data(line="_myin		dd ?			; DATA XREF: _mtm_module+22o").produce_c_data_single(), ('0, // _myin\n', 'dd _myin;\n', 4))

    def test_data_13840(self):
        self.assertEqual(self.parser.action_data(line="_myin_0		db ?			; DATA XREF: _ult_module+3Ao").produce_c_data_single(), ('0, // _myin_0\n', 'db _myin_0;\n', 1))

    def test_data_13850(self):
        self.assertEqual(self.parser.action_data(line="_myseg_24698	dw 0			; DATA XREF: _alloc_dma_buf+31w").produce_c_data_single(), ('0, // _myseg_24698\n', 'dw _myseg_24698;\n', 2))

    def test_data_13860(self):
        self.assertEqual(self.parser.action_data(line="_mystr		db 42h dup(0)		; DATA XREF: _start:loc_192E0o").produce_c_data_single(), ('{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, // _mystr\n', 'db _mystr[66];\n', 66))

    def test_data_13870(self):
        self.assertEqual(self.parser.action_data(line="_notes		db '  C-C#D-D#E-F-F#G-G#A-A#B-' ; DATA XREF: seg001:1930r").produce_c_data_single(), ("{' ',' ','C','-','C','#','D','-','D','#','E','-','F','-','F','#','G','-','G','#','A','-','A','#','B','-'}, // _notes\n", 'char _notes[26];\n', 26))

    @unittest.skip("to check")
    def test_data_13880(self):
        self.assertEqual(self.parser.action_data(line="_offs_draw	dw offset loc_19050	; DATA XREF: _keyb_screen_loop+32r").produce_c_data_single(), ('kloc_19050, // _offs_draw\n', 'dw _offs_draw;\n', 2))

    def test_data_13890(self):
        self.assertEqual(self.parser.action_data(line="_oint24_1C1AC	dd 0			; DATA XREF: _start+115w _start+1D4r ...").produce_c_data_single(), ('0, // _oint24_1c1ac\n', 'dd _oint24_1c1ac;\n', 4))

    def test_data_13900(self):
        self.assertEqual(self.parser.action_data(line="_oint2f_1C1B4	dd 0			; DATA XREF: _start+124w _start+1C8r ...").produce_c_data_single(), ('0, // _oint2f_1c1b4\n', 'dd _oint2f_1c1b4;\n', 4))

    def test_data_13910(self):
        self.assertEqual(self.parser.action_data(line="_oint8off_1DE14	dw 0			; DATA XREF: _start+F9w").produce_c_data_single(), ('0, // _oint8off_1de14\n', 'dw _oint8off_1de14;\n', 2))

    def test_data_13920(self):
        self.assertEqual(self.parser.action_data(line="_oint8seg_1DE16	dw 0			; DATA XREF: _start+FDw").produce_c_data_single(), ('0, // _oint8seg_1de16\n', 'dw _oint8seg_1de16;\n', 2))

    def test_data_13930(self):
        self.assertEqual(self.parser.action_data(line="_oint9_1C1A4	dd 0			; DATA XREF: _start+106w _start+1E0r ...").produce_c_data_single(), ('0, // _oint9_1c1a4\n', 'dd _oint9_1c1a4;\n', 4))

    def test_data_13940(self):
        self.assertEqual(self.parser.action_data(line="_old_intprocoffset dw 0			; DATA XREF: _setsnd_handler+3Aw").produce_c_data_single(), ('0, // _old_intprocoffset\n', 'dw _old_intprocoffset;\n', 2))

    def test_data_13950(self):
        self.assertEqual(self.parser.action_data(line="_old_intprocseg	dw 0			; DATA XREF: _setsnd_handler+3Ew").produce_c_data_single(), ('0, // _old_intprocseg\n', 'dw _old_intprocseg;\n', 2))

    def test_data_13960(self):
        self.assertEqual(self.parser.action_data(line="_outp_freq	dw 0			; DATA XREF: _read_module+82w").produce_c_data_single(), ('0, // _outp_freq\n', 'dw _outp_freq;\n', 2))

    def test_data_13970(self):
        self.assertEqual(self.parser.action_data(line="_palette_24404	db    0			; DATA XREF: _init_vga_waves+17o").produce_c_data_single(), ('0, // _palette_24404\n', 'db _palette_24404;\n', 1))

    def test_data_13980(self):
        self.assertEqual(self.parser.action_data(line="_pc_timer_tbl	db 40h,40h,40h,40h,40h,40h,40h,40h,40h,40h,3Fh,3Fh,3Fh").produce_c_data_single(), ('{64,64,64,64,64,64,64,64,64,64,63,63,63}, // _pc_timer_tbl\n', 'db _pc_timer_tbl[13];\n', 13))

    def test_data_13990(self):
        self.assertEqual(self.parser.action_data(line="_pcspeaker_txt	db    2			; DATA XREF: seg003:0D80o seg003:0D82o").produce_c_data_single(), ('2, // _pcspeaker_txt\n', 'db _pcspeaker_txt;\n', 1))

    def test_data_14000(self):
        self.assertEqual(self.parser.action_data(line="_play_state	db 0			; DATA XREF: _getset_playstate+Bw").produce_c_data_single(), ('0, // _play_state\n', 'db _play_state;\n', 1))

    def test_data_14010(self):
        self.assertEqual(self.parser.action_data(line="_pointer_245B4	dd 0			; DATA XREF: sub_135CA+1Cr").produce_c_data_single(), ('0, // _pointer_245b4\n', 'dd _pointer_245b4;\n', 4))

    def test_data_14020(self):
        self.assertEqual(self.parser.action_data(line="_prev_scan_code	db 0			; DATA XREF: _int9_keyb+19r").produce_c_data_single(), ('0, // _prev_scan_code\n', 'db _prev_scan_code;\n', 1))

    def test_data_14030(self):
        self.assertEqual(self.parser.action_data(line="_s3mtable_108D6	db 0FFh,10h,0Bh,0Dh,15h,12h,11h,13h,14h,1Bh,1Dh,17h,16h").produce_c_data_single(), ('{255,16,11,13,21,18,17,19,20,27,29,23,22}, // _s3mtable_108d6\n', 'db _s3mtable_108d6[13];\n', 13))

    def test_data_14040(self):
        self.assertEqual(self.parser.action_data(line="_s3mtable_108F0	db 0,3,5,4,7,0FFh,0FFh,0FFh,8,0FFh,0FFh,6,0Ch,0Dh,0FFh").produce_c_data_single(), ('{0,3,5,4,7,255,255,255,8,255,255,6,12,13,255}, // _s3mtable_108f0\n', 'db _s3mtable_108f0[15];\n', 15))

    def test_data_14050(self):
        self.assertEqual(self.parser.action_data(line="_sIplay_cfg	db 'IPLAY.CFG',0     ; DATA XREF: _loadcfgo").produce_c_data_single(), ('"IPLAY.CFG", // _siplay_cfg\n', 'char _siplay_cfg[10];\n', 10))

    def test_data_14060(self):
        self.assertEqual(self.parser.action_data(line="_samples_outoffs_24600	dw 0			; DATA XREF: sub_12EBA+2Cw").produce_c_data_single(), ('0, // _samples_outoffs_24600\n', 'dw _samples_outoffs_24600;\n', 2))

    def test_data_14070(self):
        self.assertEqual(self.parser.action_data(line="_savesp_245D0	dw 0			; DATA XREF: _moduleread+15w").produce_c_data_single(), ('0, // _savesp_245d0\n', 'dw _savesp_245d0;\n', 2))

    def test_data_14080(self):
        self.assertEqual(self.parser.action_data(line="_sb16_txt	db    2			; DATA XREF: seg003:0D72o seg003:0D74o ...").produce_c_data_single(), ('2, // _sb16_txt\n', 'db _sb16_txt;\n', 1))

    def test_data_14090(self):
        self.assertEqual(self.parser.action_data(line="_sb_base_port	dw 0			; DATA XREF: _sb16_on+17r _sb16_on+44r ...").produce_c_data_single(), ('0, // _sb_base_port\n', 'dw _sb_base_port;\n', 2))

    def test_data_14100(self):
        self.assertEqual(self.parser.action_data(line="_sb_int_counter	db 0			; DATA XREF: _sb_test_interruptw").produce_c_data_single(), ('0, // _sb_int_counter\n', 'db _sb_int_counter;\n', 1))

    def test_data_14110(self):
        self.assertEqual(self.parser.action_data(line="_sb_irq_number	db 0			; DATA XREF: _sb16_init+1Cw").produce_c_data_single(), ('0, // _sb_irq_number\n', 'db _sb_irq_number;\n', 1))

    def test_data_14120(self):
        self.assertEqual(self.parser.action_data(line="_sb_timeconst	db 0			; DATA XREF: _sbpro_init+51w _sb_set-D1r ...").produce_c_data_single(), ('0, // _sb_timeconst\n', 'db _sb_timeconst;\n', 1))

    def test_data_14130(self):
        self.assertEqual(self.parser.action_data(line="_segfsbx_1DE28	dd 0			; DATA XREF: _read_module+99w").produce_c_data_single(), ('0, // _segfsbx_1de28\n', 'dd _segfsbx_1de28;\n', 4))

    def test_data_14140(self):
        self.assertEqual(
            self.parser.action_data(line=r"_slider		db '─\|/─\|/'").produce_c_data_single(),
            (r"{'\xc4','\\','|','/','\xc4','\\','|','/'}, // _slider"+"\n",
             'char _slider[8];\n',
             8))

    def test_data_14150(self):
        self.assertEqual(self.parser.action_data(line="_snd_base_port	dw 0			; DATA XREF: _read_sndsettings+9r").produce_c_data_single(), ('0, // _snd_base_port\n', 'dw _snd_base_port;\n', 2))

    def test_data_14160(self):
        self.assertEqual(self.parser.action_data(line="_snd_base_port_0	dw 0FFFFh		; DATA XREF: _callsubx+3r _callsubx+45w").produce_c_data_single(), ('65535, // _snd_base_port_0\n', 'dw _snd_base_port_0;\n', 2))

    def test_data_14170(self):
        self.assertEqual(self.parser.action_data(line="_snd_card_type	db 3			; DATA XREF: _text_init2+18Er").produce_c_data_single(), ('3, // _snd_card_type\n', 'db _snd_card_type;\n', 1))

    def test_data_14180(self):
        self.assertEqual(self.parser.action_data(line="_aGravisUltrasoun db 'Gravis UltraSound',0 ; DATA XREF: seg003:_snd_cards_offso").produce_c_data_single(), ('"Gravis UltraSound", // _agravisultrasoun\n', 'char _agravisultrasoun[18];\n', 18))
        self.assertEqual(self.parser.action_data(line="_snd_cards_offs	dw offset _aGravisUltrasoun ; DATA XREF:	seg003:114Eo").produce_c_data_single(), ('offset(default_seg,_agravisultrasoun), // _snd_cards_offs\n', 'dw _snd_cards_offs;\n', 2))

    def test_data_14190(self):
        self.assertEqual(self.parser.action_data(line="_snd_init	db 0			; DATA XREF: sub_12D05+Br").produce_c_data_single(), ('0, // _snd_init\n', 'db _snd_init;\n', 1))

    def test_data_14200(self):
        self.assertEqual(self.parser.action_data(line="_snd_set_flag	db 0			; DATA XREF: sub_12DA8+60w _snd_on+7r ...").produce_c_data_single(), ('0, // _snd_set_flag\n', 'db _snd_set_flag;\n', 1))

    def test_data_14210(self):
        self.assertEqual(self.parser.action_data(line="_sndcard_type	db 0			; DATA XREF: _mtm_module+2Er").produce_c_data_single(), ('0, // _sndcard_type\n', 'db _sndcard_type;\n', 1))

    def test_data_14220(self):
        self.assertEqual(self.parser.action_data(line="_sndflags_24622	db 0			; DATA XREF: _useless_11787+9r").produce_c_data_single(), ('0, // _sndflags_24622\n', 'db _sndflags_24622;\n', 1))

    def test_data_14230(self):
        self.assertEqual(self.parser.action_data(line="_sound_port	dw 0			; DATA XREF: _proaud_init+42w").produce_c_data_single(), ('0, // _sound_port\n', 'dw _sound_port;\n', 2))

    def test_data_14240(self):
        self.assertEqual(self.parser.action_data(line="_swapdata_off	dw 0			; DATA XREF: _start+161w").produce_c_data_single(), ('0, // _swapdata_off\n', 'dw _swapdata_off;\n', 2))

    def test_data_14250(self):
        self.assertEqual(self.parser.action_data(line="_swapdata_seg	dw 0			; DATA XREF: _start+165w").produce_c_data_single(), ('0, // _swapdata_seg\n', 'dw _swapdata_seg;\n', 2))

    def test_data_14260(self):
        self.assertEqual(self.parser.action_data(line="_table_13EC3	db 140,50,25,15,10,7,6,4,3,3,2,2,2,2,1,1 ; DATA	XREF: sub_13E9B+Dr").produce_c_data_single(), ('{140,50,25,15,10,7,6,4,3,3,2,2,2,2,1,1}, // _table_13ec3\n', 'db _table_13ec3[16];\n', 16))

    def test_data_14270(self):
        self.assertEqual(self.parser.action_data(line="_table_14057	db 0FFh,80h,40h,2Ah,20h,19h,15h,12h,10h,0Eh,0Ch,0Bh,0Ah").produce_c_data_single(), ('{255,128,64,42,32,25,21,18,16,14,12,11,10}, // _table_14057\n', 'db _table_14057[13];\n', 13))

    def test_data_14280(self):
        self.assertEqual(self.parser.action_data(line="_table_246F6	dw 8363,8422,8482,8543,8604,8667,8730,8794,7901,7954,8007").produce_c_data_single(), ('{8363,8422,8482,8543,8604,8667,8730,8794,7901,7954,8007}, // _table_246f6\n', 'dw _table_246f6[11];\n', 22))

    def test_data_14290(self):
        self.assertEqual(self.parser.action_data(line="_table_24716	dw 8000h,9000h,0A000h,0A952h,0B000h,0B521h,0B952h,0BCDEh").produce_c_data_single(), ('{32768,36864,40960,43346,45056,46369,47442,48350}, // _table_24716\n', 'dw _table_24716[8];\n', 16))

    def test_data_14300(self):
        self.assertEqual(self.parser.action_data(line="_table_24798	dw 8000h,9800h,0A000h,0A800h,0B000h,0B400h,0B800h,0BC00h").produce_c_data_single(), ('{32768,38912,40960,43008,45056,46080,47104,48128}, // _table_24798\n', 'dw _table_24798[8];\n', 16))

    def test_data_14310(self):
        self.assertEqual(self.parser.action_data(line="_table_24818	dw 8000h,9800h,0A000h,0A800h,0B000h,0B400h,0B800h,0BC00h").produce_c_data_single(), ('{32768,38912,40960,43008,45056,46080,47104,48128}, // _table_24818\n', 'dw _table_24818[8];\n', 16))

    def test_data_14320(self):
        self.assertEqual(self.parser.action_data(line="_table_24898	db 1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh").produce_c_data_single(), ('{30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30}, // _table_24898\n', 'db _table_24898[16];\n', 16))

    def test_data_14330(self):
        self.assertEqual(self.parser.action_data(line="_table_25118	dw 1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906,856,808,762,720,678,640,604,570,538,508,480,453").produce_c_data_single(), ('{1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906,856,808,762,720,678,640,604,570,538,508,480,453}, // _table_25118\n', 'dw _table_25118[24];\n', 48))

    def test_data_14340(self):
        self.assertEqual(self.parser.action_data(line="_table_251C0	db  0,18h,31h,4Ah,61h,78h,8Dh,0A1h,0B4h,0C5h,0D4h,0E0h").produce_c_data_single(), ('{0,24,49,74,97,120,141,161,180,197,212,224}, // _table_251c0\n', 'db _table_251c0[12];\n', 12))

    def test_data_14350(self):
        self.assertEqual(self.parser.action_data(line="_table_251E0	db  0,15h,20h,29h,30h,37h,3Dh,44h,49h,4Fh,54h,59h,5Eh").produce_c_data_single(), ('{0,21,32,41,48,55,61,68,73,79,84,89,94}, // _table_251e0\n', 'db _table_251e0[13];\n', 13))

    def test_data_14360(self):
        self.assertEqual(self.parser.action_data(line="_table_25221	db  0, 4, 8,0Ch,10h,14h,18h,1Ch,20h,24h,28h,2Ch,30h,34h").produce_c_data_single(), ('{0,4,8,12,16,20,24,28,32,36,40,44,48,52}, // _table_25221\n', 'db _table_25221[14];\n', 14))

    def test_data_14370(self):
        self.assertEqual(self.parser.action_data(line="_table_25261	db  0, 4, 8,0Ch,10h,14h,18h,1Ch,20h,24h,28h,2Ch,30h,34h").produce_c_data_single(), ('{0,4,8,12,16,20,24,28,32,36,40,44,48,52}, // _table_25261\n', 'db _table_25261[14];\n', 14))

    @unittest.skip("to check")
    def test_data_14380(self):
        self.assertEqual(self.parser.action_data(line="_table_sndcrdname dw offset _aGravisUltrasou ; DATA XREF:	_text_init2+19Dr").produce_c_data_single(), ('0, // _table_sndcrdname\n', 'dw _table_sndcrdname;\n', 2))

    def test_data_14390(self):
        self.assertEqual(self.parser.action_data(line="_tabledword_24526 dd    0,65536,46340,25079,12785,6423,3215,1608, 804, 402").produce_c_data_single(), ('{0,65536,46340,25079,12785,6423,3215,1608,804,402}, // _tabledword_24526\n', 'dd _tabledword_24526[10];\n', 40))

    def test_data_14400(self):
        self.assertEqual(self.parser.action_data(line="_tabledword_24562 dd -131072,-65536,-19196,-4989,-1260,-316, -79, -20,  -5").produce_c_data_single(), ('{4294836224,4294901760,4294948100,4294962307,4294966036,4294966980,4294967217,4294967276,4294967291}, // _tabledword_24562\n', 'dd _tabledword_24562[9];\n', 36))

    def test_data_14410(self):
        self.assertEqual(self.parser.action_data(line="_timer_word_14F6E dw 0			; DATA XREF: _set_timerw _text:4F59r").produce_c_data_single(), ('0, // _timer_word_14f6e\n', 'dw _timer_word_14f6e;\n', 2))

    def test_data_14420(self):
        self.assertEqual(self.parser.action_data(line="_vga_palette	db 0,0,0		; DATA XREF: _init_vga_waves+1Fo").produce_c_data_single(), ('{0,0,0}, // _vga_palette\n', 'db _vga_palette[3];\n', 3))

    def test_data_14430(self):
        self.assertEqual(self.parser.action_data(line="_videomempointer	dd 0			; DATA XREF: _start:loc_1917Dw").produce_c_data_single(), ('0, // _videomempointer\n', 'dd _videomempointer;\n', 4))

    def test_data_14440(self):
        self.assertEqual(self.parser.action_data(line="_videopoint_shiftd dd 0			; DATA XREF: _text_init2+5Fw").produce_c_data_single(), ('0, // _videopoint_shiftd\n', 'dd _videopoint_shiftd;\n', 4))

    def test_data_14450(self):
        self.assertEqual(self.parser.action_data(line="_volume_1DE34	dd 0			; DATA XREF: _read_module+DAw").produce_c_data_single(), ('0, // _volume_1de34\n', 'dd _volume_1de34;\n', 4))

    def test_data_14460(self):
        self.assertEqual(self.parser.action_data(line="_volume_245FC	dw 100h			; DATA XREF: sub_1265D+5r").produce_c_data_single(), ('256, // _volume_245fc\n', 'dw _volume_245fc;\n', 2))

    def test_data_14470(self):
        self.assertEqual(self.parser.action_data(line="_word_14913	dw 536h			; DATA XREF: _wss_set+14w").produce_c_data_single(), ('1334, // _word_14913\n', 'dw _word_14913;\n', 2))

    def test_data_14480(self):
        self.assertEqual(self.parser.action_data(line="_word_14BBB	dw 22Fh			; DATA XREF: _sb16_on+49w _sb16_on+57w").produce_c_data_single(), ('559, // _word_14bbb\n', 'dw _word_14bbb;\n', 2))

    def test_data_14490(self):
        self.assertEqual(self.parser.action_data(line="_word_14CEB	dw 22Eh			; DATA XREF: _sb_set-108w").produce_c_data_single(), ('558, // _word_14ceb\n', 'dw _word_14ceb;\n', 2))

    def test_data_14500(self):
        self.assertEqual(self.parser.action_data(line="_word_14FC0	dw 1000h		; DATA XREF: _covox_init+33w").produce_c_data_single(), ('4096, // _word_14fc0\n', 'dw _word_14fc0;\n', 2))

    def test_data_14510(self):
        self.assertEqual(self.parser.action_data(line="_word_14FC8	dw 378h			; DATA XREF: _covox_init+24w").produce_c_data_single(), ('888, // _word_14fc8\n', 'dw _word_14fc8;\n', 2))

    def test_data_14520(self):
        self.assertEqual(self.parser.action_data(line="_word_1504D	dw 37Ah			; DATA XREF: _stereo_init+27w").produce_c_data_single(), ('890, // _word_1504d\n', 'dw _word_1504d;\n', 2))

    def test_data_14530(self):
        self.assertEqual(self.parser.action_data(line="_word_15056	dw 1234h		; DATA XREF: _stereo_init+3Aw").produce_c_data_single(), ('4660, // _word_15056\n', 'dw _word_15056;\n', 2))

    def test_data_14540(self):
        self.assertEqual(self.parser.action_data(line="_word_1519B	dw 1000h		; DATA XREF: _pcspeaker_init+1Ew").produce_c_data_single(), ('4096, // _word_1519b\n', 'dw _word_1519b;\n', 2))

    def test_data_14550(self):
        self.assertEqual(self.parser.action_data(line="_word_151A3	dw 1234h		; DATA XREF: _pcspeaker_init+22w").produce_c_data_single(), ('4660, // _word_151a3\n', 'dw _word_151a3;\n', 2))

    def test_data_14560(self):
        self.assertEqual(self.parser.action_data(line="_word_1D26D	dw 3F2h			; DATA XREF: _dosexec+19o").produce_c_data_single(), ('1010, // _word_1d26d\n', 'dw _word_1d26d;\n', 2))

    def test_data_14570(self):
        self.assertEqual(self.parser.action_data(line="_word_1D3B0	dw 49Eh			; DATA XREF: _start+723o").produce_c_data_single(), ('1182, // _word_1d3b0\n', 'dw _word_1d3b0;\n', 2))

    def test_data_14580(self):
        self.assertEqual(self.parser.action_data(line="_word_1D614	dw 2020h		; DATA XREF: _useless_197F2+7w").produce_c_data_single(), ('8224, // _word_1d614\n', 'dw _word_1d614;\n', 2))

    def test_data_14590(self):
        self.assertEqual(self.parser.action_data(line="_word_1D669	dw 2020h		; DATA XREF: _useless_197F2+12w").produce_c_data_single(), ('8224, // _word_1d669\n', 'dw _word_1d669;\n', 2))

    def test_data_14600(self):
        self.assertEqual(self.parser.action_data(line="_word_1DE46	dw 0			; DATA XREF: _keyb_screen_loop+316r").produce_c_data_single(), ('0, // _word_1de46\n', 'dw _word_1de46;\n', 2))

    def test_data_14610(self):
        self.assertEqual(self.parser.action_data(line="_word_246DE	dw 6B00h,6500h,5F40h,5A00h,54C0h,5000h,4B80h,4740h,4340h").produce_c_data_single(), ('{27392,25856,24384,23040,21696,20480,19328,18240,17216}, // _word_246de\n', 'dw _word_246de[9];\n', 18))

    def test_data_14620(self):
        self.assertEqual(self.parser.action_data(line="_word_24998	dw 6B00h,6500h,5F40h,5A00h,54C0h,5000h,4B80h,4740h,4340h").produce_c_data_single(), ('{27392,25856,24384,23040,21696,20480,19328,18240,17216}, // _word_24998\n', 'dw _word_24998[9];\n', 18))

    def test_data_14630(self):
        self.assertEqual(self.parser.action_data(line="_word_257A4	dw 0			; DATA XREF: _useless_writeinr+106w").produce_c_data_single(), ('0, // _word_257a4\n', 'dw _word_257a4;\n', 2))

    def test_data_14640(self):
        self.assertEqual(self.parser.action_data(line="_word_257E6	dw 4			; DATA XREF: _useless_writeinr+53w").produce_c_data_single(), ('4, // _word_257e6\n', 'dw _word_257e6;\n', 2))

    def test_data_14650(self):
        self.assertEqual(self.parser.action_data(line="_word_257E8	dw 0			; DATA XREF: _useless_writeinr+59w").produce_c_data_single(), ('0, // _word_257e8\n', 'dw _word_257e8;\n', 2))

    def test_data_14660(self):
        self.assertEqual(self.parser.action_data(line="_word_31508	dw ?			; DATA XREF: _mod_read_10311+5o").produce_c_data_single(), ('0, // _word_31508\n', 'dw _word_31508;\n', 2))

    def test_data_14670(self):
        self.assertEqual(self.parser.action_data(line="_wss_freq_table	dw 5513			; DATA XREF: _wss_test+3Er").produce_c_data_single(), ('5513, // _wss_freq_table\n', 'dw _wss_freq_table;\n', 2))

    def test_data_14680(self):
        self.assertEqual(self.parser.action_data(line="_wss_freq_table2	dw  1,19D7h,0Fh,1F40h, 0,2580h,0Eh,2B11h, 3,3E80h, 2,49D4h").produce_c_data_single(), ('{1,6615,15,8000,0,9600,14,11025,3,16000,2,18900}, // _wss_freq_table2\n', 'dw _wss_freq_table2[12];\n', 24))

    def test_data_14690(self):
        self.assertEqual(self.parser.action_data(line="_x_storage	dw  0, 0, 0, 0,	0, 0, 0, 0, 0, 0, 0, 0,	0, 0, 0, 0, 0").produce_c_data_single(), ('{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, // _x_storage\n', 'dw _x_storage[17];\n', 34))

    def test_data_14700(self):
        self.assertEqual(self.parser.action_data(line="a db 0ffh,0dfh,0h").produce_c_data_single(), ('{255,223,0}, // a\n', 'db a[3];\n', 3))

    def test_data_14710(self):
        self.assertEqual(self.parser.action_data(line="asc_1058C	db 0,18h,0Bh,0Dh,0Ah	; DATA XREF: __2stm_module+171r").produce_c_data_single(), ('{0,24,11,13,10}, // asc_1058c\n', 'db asc_1058c[5];\n', 5))

    def test_data_14720(self):
        self.assertEqual(self.parser.action_data(line="asc_182C3	db 0,0,1,3,0,2,0,4,0,0,0,5,6,0,0,7 ; DATA XREF:	_gravis_18216+5r").produce_c_data_single(), ('{0,0,1,3,0,2,0,4,0,0,0,5,6,0,0,7}, // asc_182c3\n', 'db asc_182c3[16];\n', 16))

    def test_data_14730(self):
        self.assertEqual(self.parser.action_data(line="asc_182D3	db 0,1,0,2,0,3,4,5	; DATA XREF: _gravis_18216+19r").produce_c_data_single(), ('{0,1,0,2,0,3,4,5}, // asc_182d3\n', 'db asc_182d3[8];\n', 8))

    def test_data_14740(self):
        self.assertEqual(self.parser.action_data(line="asc_1CC2D	db '                              ' ; DATA XREF: _read_module+A3o").produce_c_data_single(), ("{' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '}, // asc_1cc2d\n", 'char asc_1cc2d[30];\n', 30))

    def test_data_14750(self):
        self.assertEqual(self.parser.action_data(line="asc_1D6E0	db '               ',0  ; DATA XREF: seg001:1A80o").produce_c_data_single(), ('"               ", // asc_1d6e0\n', 'char asc_1d6e0[16];\n', 16))

    def test_data_14760(self):
        self.assertEqual(self.parser.action_data(line="asc_1DA00	db '                      ',0 ; DATA XREF: _modules_search:loc_19BDDo").produce_c_data_single(), ('"                      ", // asc_1da00\n', 'char asc_1da00[23];\n', 23))

    def test_data_14770(self):
        self.assertEqual(self.parser.action_data(line="asc_246B0	db '                                ' ; DATA XREF: _mod_1021E+22o").produce_c_data_single(), ("{' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '}, // asc_246b0\n", 'char asc_246b0[32];\n', 32))

    def test_data_14780(self):
        self.assertEqual(self.parser.action_data(line="asc_25856	db '                                ',0Dh,0Ah,1Ah").produce_c_data_single(), ("{' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','\\r','\\n',26}, // asc_25856\n", 'char asc_25856[35];\n', 35))

    def test_data_14790(self):
        self.assertEqual(self.parser.action_data(line="audio_len	dw 0			; DATA XREF: _configure_timer+1Bw").produce_c_data_single(), ('0, // audio_len\n', 'dw audio_len;\n', 2))

    def test_data_14800(self):
        self.assertEqual(self.parser.action_data(line="b dw 2").produce_c_data_single(), ('2, // b\n', 'dw b;\n', 2))

    def test_data_14810(self):
        self.assertEqual(self.parser.action_data(line="beginningdata db 4").produce_c_data_single(), ('4, // beginningdata\n', 'db beginningdata;\n', 1))

    def test_data_14820(self):
        self.assertEqual(self.parser.action_data(line="cc db 3").produce_c_data_single(), ('3, // cc\n', 'db cc;\n', 1))

    def test_data_14830(self):
        self.assertEqual(self.parser.action_data(line="d db 4").produce_c_data_single(), ('4, // d\n', 'db d;\n', 1))

    def test_data_14840(self):
        self.assertEqual(self.parser.action_data(line="db    0").produce_c_data_single(), ('0, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_14850(self):
        self.assertEqual(self.parser.action_data(line="db    ?	;").produce_c_data_single(), ('0, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_14860(self):
        self.assertEqual(self.parser.action_data(line="db  0Ah").produce_c_data_single(), ('10, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_14870(self):
        self.assertEqual(self.parser.action_data(line="db  20h").produce_c_data_single(), ('32, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_14880(self):
        self.assertEqual(self.parser.action_data(line="db  20h").produce_c_data_single(), ('32, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_14890(self):
        self.assertEqual(self.parser.action_data(line="db  2Ch	; ,").produce_c_data_single(), ('44, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_14900(self):
        self.assertEqual(self.parser.action_data(line="db  80h	; Ç").produce_c_data_single(), ('128, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_14910(self):
        self.assertEqual(self.parser.action_data(line="db  8Ah	; è").produce_c_data_single(), ('138, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_14920(self):
        self.assertEqual(self.parser.action_data(line="db ' '").produce_c_data_single(), ("{' '}, // dummy1\n", 'char dummy1[1];\n', 1))

    def test_data_14930(self):
        self.assertEqual(self.parser.action_data(line="db ' /?  This help screen',0Dh,0Ah").produce_c_data_single(), ("{' ','/','?',' ',' ','T','h','i','s',' ','h','e','l','p',' ','s','c','r','e','e','n','\\r','\\n'}, // dummy1\n", 'char dummy1[23];\n', 23))

    def test_data_14940(self):
        self.assertEqual(self.parser.action_data(line="db ','").produce_c_data_single(), ("{','}, // dummy1\n", 'char dummy1[1];\n', 1))

    def test_data_14950(self):
        self.assertEqual(self.parser.action_data(line="db '- +'").produce_c_data_single(), ("{'-',' ','+'}, // dummy1\n", 'char dummy1[3];\n', 3))

    def test_data_14960(self):
        self.assertEqual(self.parser.action_data(line="db ':'").produce_c_data_single(), ("{':'}, // dummy1\n", 'char dummy1[1];\n', 1))

    def test_data_14970(self):
        self.assertEqual(self.parser.action_data(line="db 'ABC',0").produce_c_data_single(), ('"ABC", // dummy1\n', 'char dummy1[4];\n', 4))

    def test_data_14980(self):
        self.assertEqual(self.parser.action_data(line="db 'Close this DOS session first with the \"EXIT\" command.',0Dh,0Ah").produce_c_data_single(), ("{'C','l','o','s','e',' ','t','h','i','s',' ','D','O','S',' ','s','e','s','s','i','o','n',' ','f','i','r','s','t',' ','w','i','t','h',' ','t','h','e',' ','\\\"','E','X','I','T','\\\"',' ','c','o','m','m','a','n','d','.','\\r','\\n'}, // dummy1\n", 'char dummy1[55];\n', 55))

    def test_data_14990(self):
        self.assertEqual(self.parser.action_data(line="db 'OKOKOKOK'").produce_c_data_single(), ("{'O','K','O','K','O','K','O','K'}, // dummy1\n", 'char dummy1[8];\n', 8))

    def test_data_15000(self):
        self.assertEqual(self.parser.action_data(line="db 'OKOKOKOK',10,13").produce_c_data_single(), ("{'O','K','O','K','O','K','O','K','\\n','\\r'}, // dummy1\n", 'char dummy1[10];\n', 10))

    def test_data_15010(self):
        self.assertEqual(self.parser.action_data(line="db 'Try changing the AT-BUS Clock in the CMOS Setup.',0Dh,0Ah,0").produce_c_data_single(), ('"Try changing the AT-BUS Clock in the CMOS Setup.\\r\\n", // dummy1\n', 'char dummy1[51];\n', 51))

    def test_data_15020(self):
        self.assertEqual(self.parser.action_data(line="db 'Usage: IPLAY [Switches] [FileName.Ext|@FileList.Ext]',0Dh,0Ah").produce_c_data_single(), ("{'U','s','a','g','e',':',' ','I','P','L','A','Y',' ','[','S','w','i','t','c','h','e','s',']',' ','[','F','i','l','e','N','a','m','e','.','E','x','t','|','@','F','i','l','e','L','i','s','t','.','E','x','t',']','\\r','\\n'}, // dummy1\n", 'char dummy1[54];\n', 54))

    def test_data_15030(self):
        self.assertEqual(self.parser.action_data(line="db '[ ]'").produce_c_data_single(), ("{'[',' ',']'}, // dummy1\n", 'char dummy1[3];\n', 3))

    def test_data_15040(self):
        self.assertEqual(self.parser.action_data(line="db '[ ]',0").produce_c_data_single(), ('"[ ]", // dummy1\n', 'char dummy1[4];\n', 4))

    def test_data_15050(self):
        self.assertEqual(self.parser.action_data(line="db 'ed again.',0Dh,0Ah").produce_c_data_single(), ("{'e','d',' ','a','g','a','i','n','.','\\r','\\n'}, // dummy1\n", 'char dummy1[11];\n', 11))

    def test_data_15060(self):
        self.assertEqual(self.parser.action_data(line="db 'h'").produce_c_data_single(), ("{'h'}, // dummy1\n", 'char dummy1[1];\n', 1))

    def test_data_15070(self):
        self.assertEqual(self.parser.action_data(line="db 'o:'").produce_c_data_single(), ("{'o',':'}, // dummy1\n", 'char dummy1[2];\n', 2))

    def test_data_15080(self):
        self.assertEqual(self.parser.action_data(line="db 's'").produce_c_data_single(), ("{'s'}, // dummy1\n", 'char dummy1[1];\n', 1))

    def test_data_15090(self):
        self.assertEqual(self.parser.action_data(line="db 's',0Dh,0Ah,0").produce_c_data_single(), ('"s\\r\\n", // dummy1\n', 'char dummy1[4];\n', 4))

    def test_data_15100(self):
        self.assertEqual(self.parser.action_data(line="db '─asdkweorjwoerj3434',13,10,92").produce_c_data_single(), ("{'\\xc4','a','s','d','k','w','e','o','r','j','w','o','e','r','j','3','4','3','4','\\r','\\n',92}, // dummy1\n", 'char dummy1[22];\n', 22))

    def test_data_15110(self):
        self.assertEqual(self.parser.action_data(line="db 0").produce_c_data_single(), ('0, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15120(self):
        self.assertEqual(self.parser.action_data(line="db 0,2Ah,2Ah").produce_c_data_single(), ('{0,42,42}, // dummy1\n', 'db dummy1[3];\n', 3))

    def test_data_15130(self):
        self.assertEqual(self.parser.action_data(line="db 0A0h	; á		; self modifying").produce_c_data_single(), ('160, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15140(self):
        self.assertEqual(self.parser.action_data(line="db 0A0h	; á").produce_c_data_single(), ('160, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15150(self):
        self.assertEqual(self.parser.action_data(line="db 0A0h,0A4h,0A8h,0ACh,0B0h,0B4h,0B8h,0BCh,0C0h,0C4h,0C8h").produce_c_data_single(), ('{160,164,168,172,176,180,184,188,192,196,200}, // dummy1\n', 'db dummy1[11];\n', 11))

    def test_data_15160(self):
        self.assertEqual(self.parser.action_data(line="db 0A1h").produce_c_data_single(), ('161, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15170(self):
        self.assertEqual(self.parser.action_data(line="db 0A1h,0A5h,0AAh,0AEh,0B2h,0B6h,0BAh,0BEh,0C2h,0C6h,0CAh").produce_c_data_single(), ('{161,165,170,174,178,182,186,190,194,198,202}, // dummy1\n', 'db dummy1[11];\n', 11))

    def test_data_15180(self):
        self.assertEqual(self.parser.action_data(line="db 0AAh	; ¬").produce_c_data_single(), ('170, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15190(self):
        self.assertEqual(self.parser.action_data(line="db 0Ah").produce_c_data_single(), ('10, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15200(self):
        self.assertEqual(self.parser.action_data(line="db 0Ah,'$'").produce_c_data_single(), ("{'\\n','$'}, // dummy1\n", 'char dummy1[2];\n', 2))

    def test_data_15210(self):
        self.assertEqual(self.parser.action_data(line="db 0Ah,0Bh,1Bh").produce_c_data_single(), ('{10,11,27}, // dummy1\n', 'db dummy1[3];\n', 3))

    def test_data_15220(self):
        self.assertEqual(self.parser.action_data(line="db 0B8h,0BBh,0BEh,0C1h,0C3h,0C6h,0C9h,0CCh,0CFh,0D1h,0D4h").produce_c_data_single(), ('{184,187,190,193,195,198,201,204,207,209,212}, // dummy1\n', 'db dummy1[11];\n', 11))

    def test_data_15230(self):
        self.assertEqual(self.parser.action_data(line="db 0C5h,0B4h,0A1h,8Dh,78h,61h,4Ah,31h,18h").produce_c_data_single(), ('{197,180,161,141,120,97,74,49,24}, // dummy1\n', 'db dummy1[9];\n', 9))

    def test_data_15240(self):
        self.assertEqual(self.parser.action_data(line="db 0Dh,0Ah").produce_c_data_single(), ('{13,10}, // dummy1\n', 'db dummy1[2];\n', 2))

    def test_data_15250(self):
        self.assertEqual(self.parser.action_data(line="db 0Dh,0Ah,'$'").produce_c_data_single(), ("{'\\r','\\n','$'}, // dummy1\n", 'char dummy1[3];\n', 3))

    def test_data_15260(self):
        self.assertEqual(self.parser.action_data(line="db 1").produce_c_data_single(), ('1, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15270(self):
        self.assertEqual(self.parser.action_data(line="db 1,1,1,1,1").produce_c_data_single(), ('{1,1,1,1,1}, // dummy1\n', 'db dummy1[5];\n', 5))

    def test_data_15280(self):
        self.assertEqual(self.parser.action_data(line="db 1,2,3,4").produce_c_data_single(), ('{1,2,3,4}, // dummy1\n', 'db dummy1[4];\n', 4))

    def test_data_15290(self):
        self.assertEqual(self.parser.action_data(line="db 10h,11h,2Ah").produce_c_data_single(), ('{16,17,42}, // dummy1\n', 'db dummy1[3];\n', 3))

    def test_data_15300(self):
        self.assertEqual(self.parser.action_data(line="db 12").produce_c_data_single(), ('12, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15310(self):
        self.assertEqual(self.parser.action_data(line="db 141").produce_c_data_single(), ('141, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15320(self):
        self.assertEqual(self.parser.action_data(line="db 7Fh").produce_c_data_single(), ('127, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15330(self):
        self.assertEqual(self.parser.action_data(line="db 8,8,8,7,7,7,7,6,6,6,6,6,6,5,5,5").produce_c_data_single(), ('{8,8,8,7,7,7,7,6,6,6,6,6,6,5,5,5}, // dummy1\n', 'db dummy1[16];\n', 16))

    def test_data_15340(self):
        self.assertEqual(self.parser.action_data(line="db 80h").produce_c_data_single(), ('128, // dummy1\n', 'db dummy1;\n', 1))

    def test_data_15350(self):
        self.assertEqual(self.parser.action_data(line="db 9,9,8").produce_c_data_single(), ('{9,9,8}, // dummy1\n', 'db dummy1[3];\n', 3))

    def test_data_15360(self):
        self.assertEqual(self.parser.action_data(line="dd   -2,  -1,  -1,  -1,	 -1,   0").produce_c_data_single(), ('{4294967294,4294967295,4294967295,4294967295,4294967295,0}, // dummy1\n', 'dd dummy1[6];\n', 24))

    def test_data_15370(self):
        self.assertEqual(self.parser.action_data(line="dd  201, 100,  50,  25,	 12").produce_c_data_single(), ('{201,100,50,25,12}, // dummy1\n', 'dd dummy1[5];\n', 20))

    def test_data_15380(self):
        self.assertEqual(self.parser.action_data(line="dd 111,1").produce_c_data_single(), ('{111,1}, // dummy1\n', 'dd dummy1[2];\n', 8))

    @unittest.skip("to check")
    def test_data_15390(self):
        self.assertEqual(self.parser.action_data(line="dd offset var5").produce_c_data_single(), ('offset(_data,var5), // dummy1\n', 'dw dummy1;\n', 4))

    def test_data_15400(self):
        self.assertEqual(self.parser.action_data(line="dd unk_24453").produce_c_data_single(), ('unk_24453, // dummy1\n', 'dd dummy1;\n', 4))

    def test_data_15410(self):
        self.assertEqual(self.parser.action_data(line="doublequote db 'ab''cd',\"e\"").produce_c_data_single(), ("{'a','b','\\'','c','d','e'}, // doublequote\n", 'char doublequote[6];\n', 6))

    def test_data_15420(self):
        self.assertEqual(self.parser.action_data(line="dw  0, 0, 0, 0,	0, 0, 0, 0, 0, 0, 0, 0,	0, 0, 0, 0").produce_c_data_single(), ('{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, // dummy1\n', 'dw dummy1[16];\n', 32))

    def test_data_15430(self):
        self.assertEqual(self.parser.action_data(line="dw  5,5622h, 7,6B25h, 4,7D00h, 6,8133h,0Dh,93A8h, 9,0AC44h").produce_c_data_single(), ('{5,22050,7,27429,4,32000,6,33075,13,37800,9,44100}, // dummy1\n', 'dw dummy1[12];\n', 24))

    def test_data_15440(self):
        self.assertEqual(self.parser.action_data(line="dw 0A06h").produce_c_data_single(), ('2566, // dummy1\n', 'dw dummy1;\n', 2))

    def test_data_15450(self):
        self.assertEqual(self.parser.action_data(line="dw 0BE0h,0B40h,0AA0h,0A00h,970h,8F0h,870h,7F0h,780h,710h").produce_c_data_single(), ('{3040,2880,2720,2560,2416,2288,2160,2032,1920,1808}, // dummy1\n', 'dw dummy1[10];\n', 20))

    def test_data_15460(self):
        self.assertEqual(self.parser.action_data(line="dw 0Bh,0BB80h,0Ch").produce_c_data_single(), ('{11,48000,12}, // dummy1\n', 'dw dummy1[3];\n', 6))

    def test_data_15470(self):
        self.assertEqual(self.parser.action_data(line="dw 32Ah").produce_c_data_single(), ('810, // dummy1\n', 'dw dummy1;\n', 2))

    @unittest.skip("to check")
    def test_data_15480(self):
        self.assertEqual(self.parser.action_data(line="dw @df@@@@8").produce_c_data_single(), ('karbdfarbarbarbarb8, // dummy1\n', 'dw dummy1;\n', 2))

    @unittest.skip("to check")
    def test_data_15490(self):
        self.assertEqual(self.parser.action_data(line="dw offset __2stm_module	; 2STM").produce_c_data_single(), ('k__2stm_module, // dummy1\n', 'dw dummy1;\n', 2))

    @unittest.skip("to check")
    def test_data_15500(self):
        self.assertEqual(self.parser.action_data(line="dw offset loc_17BEB").produce_c_data_single(), ('kloc_17beb, // dummy1\n', 'dw dummy1;\n', 2))

    def test_data_15510(self):
        self.assertEqual(self.parser.action_data(line="e db 5").produce_c_data_single(), ('5, // e\n', 'db e;\n', 1))

    def test_data_15520(self):
        self.assertEqual(self.parser.action_data(line="enddata db 4").produce_c_data_single(), ('4, // enddata\n', 'db enddata;\n', 1))

    def test_data_15530(self):
        self.assertEqual(self.parser.action_data(line="f db 6").produce_c_data_single(), ('6, // f\n', 'db f;\n', 1))

    def test_data_15540(self):
        self.assertEqual(self.parser.action_data(line="fileName db 'file1.txt',0").produce_c_data_single(), ('"file1.txt", // filename\n', 'char filename[10];\n', 10))

    def test_data_15550(self):
        self.assertEqual(self.parser.action_data(line="g dd 12345").produce_c_data_single(), ('12345, // g\n', 'dd g;\n', 4))

    def test_data_15560(self):
        self.assertEqual(self.parser.action_data(line="h db -1").produce_c_data_single(), ('255, // h\n', 'db h;\n', 1))

    def test_data_15570(self):
        self.assertEqual(self.parser.action_data(line="h2 db 1").produce_c_data_single(), ('1, // h2\n', 'db h2;\n', 1))

    def test_data_15580(self):
        self.assertEqual(self.parser.action_data(line="load_handle dd 0").produce_c_data_single(), ('0, // load_handle\n', 'dd load_handle;\n', 4))

    def test_data_15590(self):
        self.assertEqual(self.parser.action_data(line="myoffs		dw offset label2").produce_c_data_single(), ('label2, // myoffs\n', 'dw myoffs;\n', 2))

    @unittest.skip("to check")
    def test_data_15600(self):
        self.assertEqual(self.parser.action_data(line="off_18E00	dw offset loc_16A89	; DATA XREF: sub_1609F:loc_16963r").produce_c_data_single(), ('kloc_16a89, // off_18e00\n', 'dw off_18e00;\n', 2))

    @unittest.skip("to check")
    def test_data_15610(self):
        self.assertEqual(self.parser.action_data(line="off_25326	dw offset _inr_module	; DATA XREF: _moduleread:loc_10040o").produce_c_data_single(), ('k_inr_module, // off_25326\n', 'dw off_25326;\n', 2))

    def test_data_15620(self):
        self.assertEqual(self.parser.action_data(line="pal_jeu db 000,000,000,000,000,021,000,000,042,000,000,063,009,000,000,009").produce_c_data_single(), ('{0,0,0,0,0,21,0,0,42,0,0,63,9,0,0,9}, // pal_jeu\n', 'db pal_jeu[16];\n', 16))

    def test_data_15630(self):
        self.assertEqual(self.parser.action_data(line="pas_de_mem  db 'NOT enought memory for VGA display, controls work for network games',13,10,'$'").produce_c_data_single(), ("{'N','O','T',' ','e','n','o','u','g','h','t',' ','m','e','m','o','r','y',' ','f','o','r',' ','V','G','A',' ','d','i','s','p','l','a','y',',',' ','c','o','n','t','r','o','l','s',' ','w','o','r','k',' ','f','o','r',' ','n','e','t','w','o','r','k',' ','g','a','m','e','s','\\r','\\n','$'}, // pas_de_mem\n", 'char pas_de_mem[70];\n', 70))

    def test_data_15640(self):
        self.assertEqual(self.parser.action_data(line="pbs1        db 'probleme dans allocation de descriptor..',13,10,'$'").produce_c_data_single(), ("{'p','r','o','b','l','e','m','e',' ','d','a','n','s',' ','a','l','l','o','c','a','t','i','o','n',' ','d','e',' ','d','e','s','c','r','i','p','t','o','r','.','.','\\r','\\n','$'}, // pbs1\n", 'char pbs1[43];\n', 43))

    def test_data_15650(self):
        self.assertEqual(self.parser.action_data(line="pbs2        db 'probleme dans dans definition de la taille du segment',13,10,'$'").produce_c_data_single(), ("{'p','r','o','b','l','e','m','e',' ','d','a','n','s',' ','d','a','n','s',' ','d','e','f','i','n','i','t','i','o','n',' ','d','e',' ','l','a',' ','t','a','i','l','l','e',' ','d','u',' ','s','e','g','m','e','n','t','\\r','\\n','$'}, // pbs2\n", 'char pbs2[56];\n', 56))

    def test_data_15660(self):
        self.assertEqual(self.parser.action_data(line="str1 db 'abcde'").produce_c_data_single(), ("{'a','b','c','d','e'}, // str1\n", 'char str1[5];\n', 5))

    def test_data_15670(self):
        self.assertEqual(self.parser.action_data(line="str2 db 'abcde'").produce_c_data_single(), ("{'a','b','c','d','e'}, // str2\n", 'char str2[5];\n', 5))

    def test_data_15680(self):
        self.assertEqual(self.parser.action_data(line="str3 db 'cdeab'").produce_c_data_single(), ("{'c','d','e','a','b'}, // str3\n", 'char str3[5];\n', 5))

    def test_data_15690(self):
        self.assertEqual(self.parser.action_data(line="str4 db 33,'cdeab',34").produce_c_data_single(), ("{33,'c','d','e','a','b',34}, // str4\n", 'char str4[7];\n', 7))

    def test_data_15700(self):
        self.assertEqual(self.parser.action_data(line="table   dw 0").produce_c_data_single(), ('0, // table\n', 'dw table;\n', 2))

    def test_data_15710(self):
        self.assertEqual(self.parser.action_data(line="testOVerlap db 1,2,3,4,5,6,7,8,9,10,11,12,13,14").produce_c_data_single(), ('{1,2,3,4,5,6,7,8,9,10,11,12,13,14}, // testoverlap\n', 'db testoverlap[14];\n', 14))

    def test_data_15720(self):
        self.assertEqual(self.parser.action_data(line="unk_16464	db    0			; DATA XREF: sub_1609F+235w").produce_c_data_single(), ('0, // unk_16464\n', 'db unk_16464;\n', 1))

    def test_data_15730(self):
        self.assertEqual(self.parser.action_data(line="unk_165AD	db    0			; DATA XREF: sub_1609F+251w").produce_c_data_single(), ('0, // unk_165ad\n', 'db unk_165ad;\n', 1))

    def test_data_15740(self):
        self.assertEqual(self.parser.action_data(line="unk_1D516	db    2").produce_c_data_single(), ('2, // unk_1d516\n', 'db unk_1d516;\n', 1))

    def test_data_15750(self):
        self.assertEqual(self.parser.action_data(line="unk_1D6C3	db    2			; DATA XREF: seg001:1BDAo").produce_c_data_single(), ('2, // unk_1d6c3\n', 'db unk_1d6c3;\n', 1))

    def test_data_15760(self):
        self.assertEqual(self.parser.action_data(line="unk_1DC01	db    0			; DATA XREF: _modules_search+8Fr").produce_c_data_single(), ('0, // unk_1dc01\n', 'db unk_1dc01;\n', 1))

    def test_data_15770(self):
        self.assertEqual(self.parser.action_data(line="unk_24456	db  20h			; DATA XREF: dseg:7C5Bo dseg:7C5Fo").produce_c_data_single(), ('32, // unk_24456\n', 'db unk_24456;\n', 1))

    def test_data_15780(self):
        self.assertEqual(self.parser.action_data(line="unk_244C4	db    0			; DATA XREF: _spectr_1B084+14Ew").produce_c_data_single(), ('0, // unk_244c4\n', 'db unk_244c4;\n', 1))

    def test_data_15790(self):
        self.assertEqual(self.parser.action_data(line="unk_257D9	db    0").produce_c_data_single(), ('0, // unk_257d9\n', 'db unk_257d9;\n', 1))

    def test_data_15800(self):
        self.assertEqual(self.parser.action_data(line="unk_258A6	db  49h	; I		; DATA XREF: _useless_writeinr_118+Eo").produce_c_data_single(), ('73, // unk_258a6\n', 'db unk_258a6;\n', 1))

    def test_data_15810(self):
        self.assertEqual(self.parser.action_data(line="unk_30528	db    ?	;		; DATA XREF: _s3m_module+102r").produce_c_data_single(), ('0, // unk_30528\n', 'db unk_30528;\n', 1))

    def test_data_15820(self):
        self.assertEqual(self.parser.action_data(line="unk_3054A	db    ?	;		; DATA XREF: _mtm_module+7Bo").produce_c_data_single(), ('0, // unk_3054a\n', 'db unk_3054a;\n', 1))

    def test_data_15830(self):
        self.assertEqual(self.parser.action_data(line="unk_30941	db    ?	;		; DATA XREF: _mod_n_t_module+ACr").produce_c_data_single(), ('0, // unk_30941\n', 'db unk_30941;\n', 1))

    def test_data_15840(self):
        self.assertEqual(self.parser.action_data(line="var db 4 dup (5)").produce_c_data_single(), ('{5,5,5,5}, // var\n', 'db var[4];\n', 4))

    def test_data_15850(self):
        self.assertEqual(self.parser.action_data(line="var0 db 10 dup (?)").produce_c_data_single(), ('{0,0,0,0,0,0,0,0,0,0}, // var0\n', 'db var0[10];\n', 10))

    def test_data_15860(self):
        self.assertEqual(self.parser.action_data(line="var1 db 1,2,3").produce_c_data_single(), ('{1,2,3}, // var1\n', 'db var1[3];\n', 3))

    def test_data_15870(self):
        self.assertEqual(self.parser.action_data(line="var2 db 5 dup (0)").produce_c_data_single(), ('{0,0,0,0,0}, // var2\n', 'db var2[5];\n', 5))

    def test_data_15880(self):
        self.assertEqual(self.parser.action_data(line="var3 db 5*5 dup (0,testEqu*2,2*2*3,3)").produce_c_data_single(),
                         (
                         '{0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3,0,testequ*2,2*2*3,3}, '
                         '// var3\n',
                         'db var3[100];\n',
                         100))

    def test_data_15890(self):
        self.assertEqual(self.parser.action_data(line="var4 db 131").produce_c_data_single(), ('131, // var4\n', 'db var4;\n', 1))

    def test_data_15900(self):
        self.assertEqual(self.parser.action_data(line="var5 db 'abcd'").produce_c_data_single(), ("{'a','b','c','d'}, // var5\n", 'char var5[4];\n', 4))

    def test_data_15910(self):
        self.assertEqual(self.parser.action_data(line="var6 dd 9,8,7,1").produce_c_data_single(), ('{9,8,7,1}, // var6\n', 'dd var6[4];\n', 16))

    def test_data_15920(self):
        self.assertEqual(self.parser.action_data(line="db 000,009,000,000,009,021,000,009,042,000,009,063,009,009,000,009").produce_c_data_single(), ('{0,9,0,0,9,21,0,9,42,0,9,63,9,9,0,9}, // dummy1\n', 'db dummy1[16];\n', 16))


if __name__ == "__main__":
    unittest.main()
