# Generated from Patito.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,33,295,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,
        0,1,0,1,1,1,1,3,1,86,8,1,1,2,1,2,1,2,1,2,3,2,92,8,2,1,3,1,3,1,3,
        1,4,1,4,1,4,1,4,3,4,101,8,4,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,7,
        1,7,1,7,1,7,3,7,115,8,7,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,
        1,9,1,9,1,9,1,10,1,10,3,10,132,8,10,1,11,1,11,3,11,136,8,11,1,12,
        1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,13,3,13,150,
        8,13,1,14,1,14,1,14,1,14,1,14,1,15,1,15,3,15,159,8,15,1,16,1,16,
        1,16,1,17,1,17,1,17,1,17,1,17,3,17,169,8,17,1,18,1,18,1,18,1,18,
        1,19,1,19,1,19,1,19,3,19,179,8,19,1,20,1,20,1,20,1,20,1,20,1,20,
        1,20,3,20,188,8,20,1,21,1,21,1,21,1,21,1,21,1,22,1,22,1,22,1,22,
        1,22,1,22,1,22,1,22,1,23,1,23,1,23,3,23,206,8,23,1,24,1,24,1,24,
        1,24,1,24,1,24,1,24,1,24,1,25,1,25,1,25,1,25,1,25,1,25,1,26,1,26,
        1,26,1,27,1,27,1,27,1,27,1,27,3,27,230,8,27,1,28,1,28,3,28,234,8,
        28,1,29,1,29,1,29,1,30,1,30,1,30,1,30,3,30,243,8,30,1,31,1,31,1,
        32,1,32,1,32,1,32,1,32,1,32,1,32,1,32,1,32,5,32,256,8,32,10,32,12,
        32,259,9,32,1,33,1,33,1,33,1,33,1,33,1,33,1,33,1,33,1,33,5,33,270,
        8,33,10,33,12,33,273,9,33,1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,
        1,34,1,34,1,34,3,34,286,8,34,1,35,1,35,1,35,3,35,291,8,35,1,36,1,
        36,1,36,0,2,64,66,37,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,
        32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,0,
        3,1,0,5,6,1,0,17,20,1,0,30,31,284,0,74,1,0,0,0,2,85,1,0,0,0,4,91,
        1,0,0,0,6,93,1,0,0,0,8,100,1,0,0,0,10,102,1,0,0,0,12,107,1,0,0,0,
        14,114,1,0,0,0,16,116,1,0,0,0,18,118,1,0,0,0,20,131,1,0,0,0,22,135,
        1,0,0,0,24,137,1,0,0,0,26,149,1,0,0,0,28,151,1,0,0,0,30,158,1,0,
        0,0,32,160,1,0,0,0,34,168,1,0,0,0,36,170,1,0,0,0,38,178,1,0,0,0,
        40,187,1,0,0,0,42,189,1,0,0,0,44,194,1,0,0,0,46,205,1,0,0,0,48,207,
        1,0,0,0,50,215,1,0,0,0,52,221,1,0,0,0,54,229,1,0,0,0,56,233,1,0,
        0,0,58,235,1,0,0,0,60,242,1,0,0,0,62,244,1,0,0,0,64,246,1,0,0,0,
        66,260,1,0,0,0,68,285,1,0,0,0,70,290,1,0,0,0,72,292,1,0,0,0,74,75,
        5,1,0,0,75,76,5,29,0,0,76,77,5,22,0,0,77,78,3,2,1,0,78,79,3,4,2,
        0,79,80,5,2,0,0,80,81,3,36,18,0,81,82,5,3,0,0,82,1,1,0,0,0,83,86,
        3,6,3,0,84,86,1,0,0,0,85,83,1,0,0,0,85,84,1,0,0,0,86,3,1,0,0,0,87,
        88,3,18,9,0,88,89,3,4,2,0,89,92,1,0,0,0,90,92,1,0,0,0,91,87,1,0,
        0,0,91,90,1,0,0,0,92,5,1,0,0,0,93,94,5,4,0,0,94,95,3,8,4,0,95,7,
        1,0,0,0,96,97,3,10,5,0,97,98,3,8,4,0,98,101,1,0,0,0,99,101,3,10,
        5,0,100,96,1,0,0,0,100,99,1,0,0,0,101,9,1,0,0,0,102,103,3,12,6,0,
        103,104,5,24,0,0,104,105,3,16,8,0,105,106,5,22,0,0,106,11,1,0,0,
        0,107,108,5,29,0,0,108,109,3,14,7,0,109,13,1,0,0,0,110,111,5,23,
        0,0,111,112,5,29,0,0,112,115,3,14,7,0,113,115,1,0,0,0,114,110,1,
        0,0,0,114,113,1,0,0,0,115,15,1,0,0,0,116,117,7,0,0,0,117,17,1,0,
        0,0,118,119,3,20,10,0,119,120,5,29,0,0,120,121,5,25,0,0,121,122,
        3,22,11,0,122,123,5,26,0,0,123,124,5,27,0,0,124,125,3,2,1,0,125,
        126,3,36,18,0,126,127,5,28,0,0,127,128,5,22,0,0,128,19,1,0,0,0,129,
        132,5,12,0,0,130,132,3,16,8,0,131,129,1,0,0,0,131,130,1,0,0,0,132,
        21,1,0,0,0,133,136,3,24,12,0,134,136,1,0,0,0,135,133,1,0,0,0,135,
        134,1,0,0,0,136,23,1,0,0,0,137,138,5,29,0,0,138,139,5,24,0,0,139,
        140,3,16,8,0,140,141,3,26,13,0,141,25,1,0,0,0,142,143,5,23,0,0,143,
        144,5,29,0,0,144,145,5,24,0,0,145,146,3,16,8,0,146,147,3,26,13,0,
        147,150,1,0,0,0,148,150,1,0,0,0,149,142,1,0,0,0,149,148,1,0,0,0,
        150,27,1,0,0,0,151,152,5,29,0,0,152,153,5,25,0,0,153,154,3,30,15,
        0,154,155,5,26,0,0,155,29,1,0,0,0,156,159,3,32,16,0,157,159,1,0,
        0,0,158,156,1,0,0,0,158,157,1,0,0,0,159,31,1,0,0,0,160,161,3,58,
        29,0,161,162,3,34,17,0,162,33,1,0,0,0,163,164,5,23,0,0,164,165,3,
        58,29,0,165,166,3,34,17,0,166,169,1,0,0,0,167,169,1,0,0,0,168,163,
        1,0,0,0,168,167,1,0,0,0,169,35,1,0,0,0,170,171,5,27,0,0,171,172,
        3,38,19,0,172,173,5,28,0,0,173,37,1,0,0,0,174,175,3,40,20,0,175,
        176,3,38,19,0,176,179,1,0,0,0,177,179,1,0,0,0,178,174,1,0,0,0,178,
        177,1,0,0,0,179,39,1,0,0,0,180,188,3,42,21,0,181,188,3,44,22,0,182,
        188,3,48,24,0,183,184,3,28,14,0,184,185,5,22,0,0,185,188,1,0,0,0,
        186,188,3,50,25,0,187,180,1,0,0,0,187,181,1,0,0,0,187,182,1,0,0,
        0,187,183,1,0,0,0,187,186,1,0,0,0,188,41,1,0,0,0,189,190,5,29,0,
        0,190,191,5,21,0,0,191,192,3,58,29,0,192,193,5,22,0,0,193,43,1,0,
        0,0,194,195,5,8,0,0,195,196,5,25,0,0,196,197,3,58,29,0,197,198,5,
        26,0,0,198,199,3,36,18,0,199,200,3,46,23,0,200,201,5,22,0,0,201,
        45,1,0,0,0,202,203,5,9,0,0,203,206,3,36,18,0,204,206,1,0,0,0,205,
        202,1,0,0,0,205,204,1,0,0,0,206,47,1,0,0,0,207,208,5,10,0,0,208,
        209,5,25,0,0,209,210,3,58,29,0,210,211,5,26,0,0,211,212,5,11,0,0,
        212,213,3,36,18,0,213,214,5,22,0,0,214,49,1,0,0,0,215,216,5,7,0,
        0,216,217,5,25,0,0,217,218,3,52,26,0,218,219,5,26,0,0,219,220,5,
        22,0,0,220,51,1,0,0,0,221,222,3,56,28,0,222,223,3,54,27,0,223,53,
        1,0,0,0,224,225,5,23,0,0,225,226,3,56,28,0,226,227,3,54,27,0,227,
        230,1,0,0,0,228,230,1,0,0,0,229,224,1,0,0,0,229,228,1,0,0,0,230,
        55,1,0,0,0,231,234,3,58,29,0,232,234,5,32,0,0,233,231,1,0,0,0,233,
        232,1,0,0,0,234,57,1,0,0,0,235,236,3,64,32,0,236,237,3,60,30,0,237,
        59,1,0,0,0,238,239,3,62,31,0,239,240,3,64,32,0,240,243,1,0,0,0,241,
        243,1,0,0,0,242,238,1,0,0,0,242,241,1,0,0,0,243,61,1,0,0,0,244,245,
        7,1,0,0,245,63,1,0,0,0,246,247,6,32,-1,0,247,248,3,66,33,0,248,257,
        1,0,0,0,249,250,10,3,0,0,250,251,5,13,0,0,251,256,3,66,33,0,252,
        253,10,2,0,0,253,254,5,14,0,0,254,256,3,66,33,0,255,249,1,0,0,0,
        255,252,1,0,0,0,256,259,1,0,0,0,257,255,1,0,0,0,257,258,1,0,0,0,
        258,65,1,0,0,0,259,257,1,0,0,0,260,261,6,33,-1,0,261,262,3,68,34,
        0,262,271,1,0,0,0,263,264,10,3,0,0,264,265,5,15,0,0,265,270,3,68,
        34,0,266,267,10,2,0,0,267,268,5,16,0,0,268,270,3,68,34,0,269,263,
        1,0,0,0,269,266,1,0,0,0,270,273,1,0,0,0,271,269,1,0,0,0,271,272,
        1,0,0,0,272,67,1,0,0,0,273,271,1,0,0,0,274,275,5,25,0,0,275,276,
        3,58,29,0,276,277,5,26,0,0,277,286,1,0,0,0,278,286,3,28,14,0,279,
        280,3,70,35,0,280,281,5,29,0,0,281,286,1,0,0,0,282,283,3,70,35,0,
        283,284,3,72,36,0,284,286,1,0,0,0,285,274,1,0,0,0,285,278,1,0,0,
        0,285,279,1,0,0,0,285,282,1,0,0,0,286,69,1,0,0,0,287,291,5,13,0,
        0,288,291,5,14,0,0,289,291,1,0,0,0,290,287,1,0,0,0,290,288,1,0,0,
        0,290,289,1,0,0,0,291,71,1,0,0,0,292,293,7,2,0,0,293,73,1,0,0,0,
        21,85,91,100,114,131,135,149,158,168,178,187,205,229,233,242,255,
        257,269,271,285,290
    ]

class PatitoParser ( Parser ):

    grammarFileName = "Patito.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'programa'", "'inicio'", "'fin'", "'vars'", 
                     "'entero'", "'flotante'", "'escribe'", "'si'", "'sino'", 
                     "'mientras'", "'haz'", "'nula'", "'+'", "'-'", "'*'", 
                     "'/'", "'>'", "'<'", "'!='", "'=='", "'='", "';'", 
                     "','", "':'", "'('", "')'", "'{'", "'}'" ]

    symbolicNames = [ "<INVALID>", "PROGRAMA", "INICIO", "FIN", "VARS", 
                      "ENTERO", "FLOTANTE", "ESCRIBE", "SI", "SINO", "MIENTRAS", 
                      "HAZ", "NULA", "MAS", "MENOS", "POR", "ENTRE", "MAYOR", 
                      "MENOR", "DISTINTO", "IGUAL2", "IGUAL", "PCOMA", "COMA", 
                      "DPUNTOS", "PIZQ", "PDER", "LLAVEIZQ", "LLAVEDER", 
                      "ID", "CTE_FLOT", "CTE_ENT", "LETRERO", "WS" ]

    RULE_programa = 0
    RULE_varsOpc = 1
    RULE_funcsOpc = 2
    RULE_vars = 3
    RULE_declaracionList = 4
    RULE_declaracion = 5
    RULE_idLista = 6
    RULE_idResto = 7
    RULE_tipo = 8
    RULE_funcs = 9
    RULE_tipoFunc = 10
    RULE_paramsOpc = 11
    RULE_paramLista = 12
    RULE_paramResto = 13
    RULE_llamada = 14
    RULE_argsOpc = 15
    RULE_argLista = 16
    RULE_argResto = 17
    RULE_cuerpo = 18
    RULE_estatutoList = 19
    RULE_estatuto = 20
    RULE_asigna = 21
    RULE_condicion = 22
    RULE_sinoOpc = 23
    RULE_ciclo = 24
    RULE_imprime = 25
    RULE_impLista = 26
    RULE_impResto = 27
    RULE_impElem = 28
    RULE_expresion = 29
    RULE_relOpc = 30
    RULE_opRel = 31
    RULE_exp = 32
    RULE_termino = 33
    RULE_factor = 34
    RULE_signoOpc = 35
    RULE_cte = 36

    ruleNames =  [ "programa", "varsOpc", "funcsOpc", "vars", "declaracionList", 
                   "declaracion", "idLista", "idResto", "tipo", "funcs", 
                   "tipoFunc", "paramsOpc", "paramLista", "paramResto", 
                   "llamada", "argsOpc", "argLista", "argResto", "cuerpo", 
                   "estatutoList", "estatuto", "asigna", "condicion", "sinoOpc", 
                   "ciclo", "imprime", "impLista", "impResto", "impElem", 
                   "expresion", "relOpc", "opRel", "exp", "termino", "factor", 
                   "signoOpc", "cte" ]

    EOF = Token.EOF
    PROGRAMA=1
    INICIO=2
    FIN=3
    VARS=4
    ENTERO=5
    FLOTANTE=6
    ESCRIBE=7
    SI=8
    SINO=9
    MIENTRAS=10
    HAZ=11
    NULA=12
    MAS=13
    MENOS=14
    POR=15
    ENTRE=16
    MAYOR=17
    MENOR=18
    DISTINTO=19
    IGUAL2=20
    IGUAL=21
    PCOMA=22
    COMA=23
    DPUNTOS=24
    PIZQ=25
    PDER=26
    LLAVEIZQ=27
    LLAVEDER=28
    ID=29
    CTE_FLOT=30
    CTE_ENT=31
    LETRERO=32
    WS=33

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROGRAMA(self):
            return self.getToken(PatitoParser.PROGRAMA, 0)

        def ID(self):
            return self.getToken(PatitoParser.ID, 0)

        def PCOMA(self):
            return self.getToken(PatitoParser.PCOMA, 0)

        def varsOpc(self):
            return self.getTypedRuleContext(PatitoParser.VarsOpcContext,0)


        def funcsOpc(self):
            return self.getTypedRuleContext(PatitoParser.FuncsOpcContext,0)


        def INICIO(self):
            return self.getToken(PatitoParser.INICIO, 0)

        def cuerpo(self):
            return self.getTypedRuleContext(PatitoParser.CuerpoContext,0)


        def FIN(self):
            return self.getToken(PatitoParser.FIN, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_programa

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrograma" ):
                listener.enterPrograma(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrograma" ):
                listener.exitPrograma(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrograma" ):
                return visitor.visitPrograma(self)
            else:
                return visitor.visitChildren(self)




    def programa(self):

        localctx = PatitoParser.ProgramaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_programa)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.match(PatitoParser.PROGRAMA)
            self.state = 75
            self.match(PatitoParser.ID)
            self.state = 76
            self.match(PatitoParser.PCOMA)
            self.state = 77
            self.varsOpc()
            self.state = 78
            self.funcsOpc()
            self.state = 79
            self.match(PatitoParser.INICIO)
            self.state = 80
            self.cuerpo()
            self.state = 81
            self.match(PatitoParser.FIN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarsOpcContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def vars_(self):
            return self.getTypedRuleContext(PatitoParser.VarsContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_varsOpc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarsOpc" ):
                listener.enterVarsOpc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarsOpc" ):
                listener.exitVarsOpc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarsOpc" ):
                return visitor.visitVarsOpc(self)
            else:
                return visitor.visitChildren(self)




    def varsOpc(self):

        localctx = PatitoParser.VarsOpcContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_varsOpc)
        try:
            self.state = 85
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 83
                self.vars_()
                pass
            elif token in [2, 5, 6, 12, 27]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncsOpcContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def funcs(self):
            return self.getTypedRuleContext(PatitoParser.FuncsContext,0)


        def funcsOpc(self):
            return self.getTypedRuleContext(PatitoParser.FuncsOpcContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_funcsOpc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncsOpc" ):
                listener.enterFuncsOpc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncsOpc" ):
                listener.exitFuncsOpc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncsOpc" ):
                return visitor.visitFuncsOpc(self)
            else:
                return visitor.visitChildren(self)




    def funcsOpc(self):

        localctx = PatitoParser.FuncsOpcContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_funcsOpc)
        try:
            self.state = 91
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5, 6, 12]:
                self.enterOuterAlt(localctx, 1)
                self.state = 87
                self.funcs()
                self.state = 88
                self.funcsOpc()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VARS(self):
            return self.getToken(PatitoParser.VARS, 0)

        def declaracionList(self):
            return self.getTypedRuleContext(PatitoParser.DeclaracionListContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_vars

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVars" ):
                listener.enterVars(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVars" ):
                listener.exitVars(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVars" ):
                return visitor.visitVars(self)
            else:
                return visitor.visitChildren(self)




    def vars_(self):

        localctx = PatitoParser.VarsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_vars)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self.match(PatitoParser.VARS)
            self.state = 94
            self.declaracionList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclaracionListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declaracion(self):
            return self.getTypedRuleContext(PatitoParser.DeclaracionContext,0)


        def declaracionList(self):
            return self.getTypedRuleContext(PatitoParser.DeclaracionListContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_declaracionList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaracionList" ):
                listener.enterDeclaracionList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaracionList" ):
                listener.exitDeclaracionList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaracionList" ):
                return visitor.visitDeclaracionList(self)
            else:
                return visitor.visitChildren(self)




    def declaracionList(self):

        localctx = PatitoParser.DeclaracionListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_declaracionList)
        try:
            self.state = 100
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 96
                self.declaracion()
                self.state = 97
                self.declaracionList()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 99
                self.declaracion()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclaracionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def idLista(self):
            return self.getTypedRuleContext(PatitoParser.IdListaContext,0)


        def DPUNTOS(self):
            return self.getToken(PatitoParser.DPUNTOS, 0)

        def tipo(self):
            return self.getTypedRuleContext(PatitoParser.TipoContext,0)


        def PCOMA(self):
            return self.getToken(PatitoParser.PCOMA, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_declaracion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaracion" ):
                listener.enterDeclaracion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaracion" ):
                listener.exitDeclaracion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaracion" ):
                return visitor.visitDeclaracion(self)
            else:
                return visitor.visitChildren(self)




    def declaracion(self):

        localctx = PatitoParser.DeclaracionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_declaracion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.idLista()
            self.state = 103
            self.match(PatitoParser.DPUNTOS)
            self.state = 104
            self.tipo()
            self.state = 105
            self.match(PatitoParser.PCOMA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdListaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PatitoParser.ID, 0)

        def idResto(self):
            return self.getTypedRuleContext(PatitoParser.IdRestoContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_idLista

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdLista" ):
                listener.enterIdLista(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdLista" ):
                listener.exitIdLista(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdLista" ):
                return visitor.visitIdLista(self)
            else:
                return visitor.visitChildren(self)




    def idLista(self):

        localctx = PatitoParser.IdListaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_idLista)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.match(PatitoParser.ID)
            self.state = 108
            self.idResto()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdRestoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMA(self):
            return self.getToken(PatitoParser.COMA, 0)

        def ID(self):
            return self.getToken(PatitoParser.ID, 0)

        def idResto(self):
            return self.getTypedRuleContext(PatitoParser.IdRestoContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_idResto

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdResto" ):
                listener.enterIdResto(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdResto" ):
                listener.exitIdResto(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdResto" ):
                return visitor.visitIdResto(self)
            else:
                return visitor.visitChildren(self)




    def idResto(self):

        localctx = PatitoParser.IdRestoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_idResto)
        try:
            self.state = 114
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 110
                self.match(PatitoParser.COMA)
                self.state = 111
                self.match(PatitoParser.ID)
                self.state = 112
                self.idResto()
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TipoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENTERO(self):
            return self.getToken(PatitoParser.ENTERO, 0)

        def FLOTANTE(self):
            return self.getToken(PatitoParser.FLOTANTE, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_tipo

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTipo" ):
                listener.enterTipo(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTipo" ):
                listener.exitTipo(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTipo" ):
                return visitor.visitTipo(self)
            else:
                return visitor.visitChildren(self)




    def tipo(self):

        localctx = PatitoParser.TipoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_tipo)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            _la = self._input.LA(1)
            if not(_la==5 or _la==6):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def tipoFunc(self):
            return self.getTypedRuleContext(PatitoParser.TipoFuncContext,0)


        def ID(self):
            return self.getToken(PatitoParser.ID, 0)

        def PIZQ(self):
            return self.getToken(PatitoParser.PIZQ, 0)

        def paramsOpc(self):
            return self.getTypedRuleContext(PatitoParser.ParamsOpcContext,0)


        def PDER(self):
            return self.getToken(PatitoParser.PDER, 0)

        def LLAVEIZQ(self):
            return self.getToken(PatitoParser.LLAVEIZQ, 0)

        def varsOpc(self):
            return self.getTypedRuleContext(PatitoParser.VarsOpcContext,0)


        def cuerpo(self):
            return self.getTypedRuleContext(PatitoParser.CuerpoContext,0)


        def LLAVEDER(self):
            return self.getToken(PatitoParser.LLAVEDER, 0)

        def PCOMA(self):
            return self.getToken(PatitoParser.PCOMA, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_funcs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncs" ):
                listener.enterFuncs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncs" ):
                listener.exitFuncs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncs" ):
                return visitor.visitFuncs(self)
            else:
                return visitor.visitChildren(self)




    def funcs(self):

        localctx = PatitoParser.FuncsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_funcs)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.tipoFunc()
            self.state = 119
            self.match(PatitoParser.ID)
            self.state = 120
            self.match(PatitoParser.PIZQ)
            self.state = 121
            self.paramsOpc()
            self.state = 122
            self.match(PatitoParser.PDER)
            self.state = 123
            self.match(PatitoParser.LLAVEIZQ)
            self.state = 124
            self.varsOpc()
            self.state = 125
            self.cuerpo()
            self.state = 126
            self.match(PatitoParser.LLAVEDER)
            self.state = 127
            self.match(PatitoParser.PCOMA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TipoFuncContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NULA(self):
            return self.getToken(PatitoParser.NULA, 0)

        def tipo(self):
            return self.getTypedRuleContext(PatitoParser.TipoContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_tipoFunc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTipoFunc" ):
                listener.enterTipoFunc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTipoFunc" ):
                listener.exitTipoFunc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTipoFunc" ):
                return visitor.visitTipoFunc(self)
            else:
                return visitor.visitChildren(self)




    def tipoFunc(self):

        localctx = PatitoParser.TipoFuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_tipoFunc)
        try:
            self.state = 131
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [12]:
                self.enterOuterAlt(localctx, 1)
                self.state = 129
                self.match(PatitoParser.NULA)
                pass
            elif token in [5, 6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 130
                self.tipo()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamsOpcContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def paramLista(self):
            return self.getTypedRuleContext(PatitoParser.ParamListaContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_paramsOpc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamsOpc" ):
                listener.enterParamsOpc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamsOpc" ):
                listener.exitParamsOpc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamsOpc" ):
                return visitor.visitParamsOpc(self)
            else:
                return visitor.visitChildren(self)




    def paramsOpc(self):

        localctx = PatitoParser.ParamsOpcContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_paramsOpc)
        try:
            self.state = 135
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [29]:
                self.enterOuterAlt(localctx, 1)
                self.state = 133
                self.paramLista()
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PatitoParser.ID, 0)

        def DPUNTOS(self):
            return self.getToken(PatitoParser.DPUNTOS, 0)

        def tipo(self):
            return self.getTypedRuleContext(PatitoParser.TipoContext,0)


        def paramResto(self):
            return self.getTypedRuleContext(PatitoParser.ParamRestoContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_paramLista

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamLista" ):
                listener.enterParamLista(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamLista" ):
                listener.exitParamLista(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamLista" ):
                return visitor.visitParamLista(self)
            else:
                return visitor.visitChildren(self)




    def paramLista(self):

        localctx = PatitoParser.ParamListaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_paramLista)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self.match(PatitoParser.ID)
            self.state = 138
            self.match(PatitoParser.DPUNTOS)
            self.state = 139
            self.tipo()
            self.state = 140
            self.paramResto()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamRestoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMA(self):
            return self.getToken(PatitoParser.COMA, 0)

        def ID(self):
            return self.getToken(PatitoParser.ID, 0)

        def DPUNTOS(self):
            return self.getToken(PatitoParser.DPUNTOS, 0)

        def tipo(self):
            return self.getTypedRuleContext(PatitoParser.TipoContext,0)


        def paramResto(self):
            return self.getTypedRuleContext(PatitoParser.ParamRestoContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_paramResto

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamResto" ):
                listener.enterParamResto(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamResto" ):
                listener.exitParamResto(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamResto" ):
                return visitor.visitParamResto(self)
            else:
                return visitor.visitChildren(self)




    def paramResto(self):

        localctx = PatitoParser.ParamRestoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_paramResto)
        try:
            self.state = 149
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 142
                self.match(PatitoParser.COMA)
                self.state = 143
                self.match(PatitoParser.ID)
                self.state = 144
                self.match(PatitoParser.DPUNTOS)
                self.state = 145
                self.tipo()
                self.state = 146
                self.paramResto()
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LlamadaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PatitoParser.ID, 0)

        def PIZQ(self):
            return self.getToken(PatitoParser.PIZQ, 0)

        def argsOpc(self):
            return self.getTypedRuleContext(PatitoParser.ArgsOpcContext,0)


        def PDER(self):
            return self.getToken(PatitoParser.PDER, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_llamada

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLlamada" ):
                listener.enterLlamada(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLlamada" ):
                listener.exitLlamada(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLlamada" ):
                return visitor.visitLlamada(self)
            else:
                return visitor.visitChildren(self)




    def llamada(self):

        localctx = PatitoParser.LlamadaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_llamada)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self.match(PatitoParser.ID)
            self.state = 152
            self.match(PatitoParser.PIZQ)
            self.state = 153
            self.argsOpc()
            self.state = 154
            self.match(PatitoParser.PDER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgsOpcContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def argLista(self):
            return self.getTypedRuleContext(PatitoParser.ArgListaContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_argsOpc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgsOpc" ):
                listener.enterArgsOpc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgsOpc" ):
                listener.exitArgsOpc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgsOpc" ):
                return visitor.visitArgsOpc(self)
            else:
                return visitor.visitChildren(self)




    def argsOpc(self):

        localctx = PatitoParser.ArgsOpcContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_argsOpc)
        try:
            self.state = 158
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [13, 14, 25, 29, 30, 31]:
                self.enterOuterAlt(localctx, 1)
                self.state = 156
                self.argLista()
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgListaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expresion(self):
            return self.getTypedRuleContext(PatitoParser.ExpresionContext,0)


        def argResto(self):
            return self.getTypedRuleContext(PatitoParser.ArgRestoContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_argLista

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgLista" ):
                listener.enterArgLista(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgLista" ):
                listener.exitArgLista(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgLista" ):
                return visitor.visitArgLista(self)
            else:
                return visitor.visitChildren(self)




    def argLista(self):

        localctx = PatitoParser.ArgListaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_argLista)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 160
            self.expresion()
            self.state = 161
            self.argResto()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgRestoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMA(self):
            return self.getToken(PatitoParser.COMA, 0)

        def expresion(self):
            return self.getTypedRuleContext(PatitoParser.ExpresionContext,0)


        def argResto(self):
            return self.getTypedRuleContext(PatitoParser.ArgRestoContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_argResto

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgResto" ):
                listener.enterArgResto(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgResto" ):
                listener.exitArgResto(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgResto" ):
                return visitor.visitArgResto(self)
            else:
                return visitor.visitChildren(self)




    def argResto(self):

        localctx = PatitoParser.ArgRestoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_argResto)
        try:
            self.state = 168
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 163
                self.match(PatitoParser.COMA)
                self.state = 164
                self.expresion()
                self.state = 165
                self.argResto()
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CuerpoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LLAVEIZQ(self):
            return self.getToken(PatitoParser.LLAVEIZQ, 0)

        def estatutoList(self):
            return self.getTypedRuleContext(PatitoParser.EstatutoListContext,0)


        def LLAVEDER(self):
            return self.getToken(PatitoParser.LLAVEDER, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_cuerpo

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCuerpo" ):
                listener.enterCuerpo(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCuerpo" ):
                listener.exitCuerpo(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCuerpo" ):
                return visitor.visitCuerpo(self)
            else:
                return visitor.visitChildren(self)




    def cuerpo(self):

        localctx = PatitoParser.CuerpoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_cuerpo)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            self.match(PatitoParser.LLAVEIZQ)
            self.state = 171
            self.estatutoList()
            self.state = 172
            self.match(PatitoParser.LLAVEDER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EstatutoListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def estatuto(self):
            return self.getTypedRuleContext(PatitoParser.EstatutoContext,0)


        def estatutoList(self):
            return self.getTypedRuleContext(PatitoParser.EstatutoListContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_estatutoList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEstatutoList" ):
                listener.enterEstatutoList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEstatutoList" ):
                listener.exitEstatutoList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEstatutoList" ):
                return visitor.visitEstatutoList(self)
            else:
                return visitor.visitChildren(self)




    def estatutoList(self):

        localctx = PatitoParser.EstatutoListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_estatutoList)
        try:
            self.state = 178
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7, 8, 10, 29]:
                self.enterOuterAlt(localctx, 1)
                self.state = 174
                self.estatuto()
                self.state = 175
                self.estatutoList()
                pass
            elif token in [28]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EstatutoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def asigna(self):
            return self.getTypedRuleContext(PatitoParser.AsignaContext,0)


        def condicion(self):
            return self.getTypedRuleContext(PatitoParser.CondicionContext,0)


        def ciclo(self):
            return self.getTypedRuleContext(PatitoParser.CicloContext,0)


        def llamada(self):
            return self.getTypedRuleContext(PatitoParser.LlamadaContext,0)


        def PCOMA(self):
            return self.getToken(PatitoParser.PCOMA, 0)

        def imprime(self):
            return self.getTypedRuleContext(PatitoParser.ImprimeContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_estatuto

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEstatuto" ):
                listener.enterEstatuto(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEstatuto" ):
                listener.exitEstatuto(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEstatuto" ):
                return visitor.visitEstatuto(self)
            else:
                return visitor.visitChildren(self)




    def estatuto(self):

        localctx = PatitoParser.EstatutoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_estatuto)
        try:
            self.state = 187
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 180
                self.asigna()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 181
                self.condicion()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 182
                self.ciclo()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 183
                self.llamada()
                self.state = 184
                self.match(PatitoParser.PCOMA)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 186
                self.imprime()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AsignaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PatitoParser.ID, 0)

        def IGUAL(self):
            return self.getToken(PatitoParser.IGUAL, 0)

        def expresion(self):
            return self.getTypedRuleContext(PatitoParser.ExpresionContext,0)


        def PCOMA(self):
            return self.getToken(PatitoParser.PCOMA, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_asigna

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAsigna" ):
                listener.enterAsigna(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAsigna" ):
                listener.exitAsigna(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAsigna" ):
                return visitor.visitAsigna(self)
            else:
                return visitor.visitChildren(self)




    def asigna(self):

        localctx = PatitoParser.AsignaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_asigna)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 189
            self.match(PatitoParser.ID)
            self.state = 190
            self.match(PatitoParser.IGUAL)
            self.state = 191
            self.expresion()
            self.state = 192
            self.match(PatitoParser.PCOMA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CondicionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SI(self):
            return self.getToken(PatitoParser.SI, 0)

        def PIZQ(self):
            return self.getToken(PatitoParser.PIZQ, 0)

        def expresion(self):
            return self.getTypedRuleContext(PatitoParser.ExpresionContext,0)


        def PDER(self):
            return self.getToken(PatitoParser.PDER, 0)

        def cuerpo(self):
            return self.getTypedRuleContext(PatitoParser.CuerpoContext,0)


        def sinoOpc(self):
            return self.getTypedRuleContext(PatitoParser.SinoOpcContext,0)


        def PCOMA(self):
            return self.getToken(PatitoParser.PCOMA, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_condicion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondicion" ):
                listener.enterCondicion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondicion" ):
                listener.exitCondicion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondicion" ):
                return visitor.visitCondicion(self)
            else:
                return visitor.visitChildren(self)




    def condicion(self):

        localctx = PatitoParser.CondicionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_condicion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self.match(PatitoParser.SI)
            self.state = 195
            self.match(PatitoParser.PIZQ)
            self.state = 196
            self.expresion()
            self.state = 197
            self.match(PatitoParser.PDER)
            self.state = 198
            self.cuerpo()
            self.state = 199
            self.sinoOpc()
            self.state = 200
            self.match(PatitoParser.PCOMA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SinoOpcContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SINO(self):
            return self.getToken(PatitoParser.SINO, 0)

        def cuerpo(self):
            return self.getTypedRuleContext(PatitoParser.CuerpoContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_sinoOpc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSinoOpc" ):
                listener.enterSinoOpc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSinoOpc" ):
                listener.exitSinoOpc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSinoOpc" ):
                return visitor.visitSinoOpc(self)
            else:
                return visitor.visitChildren(self)




    def sinoOpc(self):

        localctx = PatitoParser.SinoOpcContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_sinoOpc)
        try:
            self.state = 205
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 202
                self.match(PatitoParser.SINO)
                self.state = 203
                self.cuerpo()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CicloContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MIENTRAS(self):
            return self.getToken(PatitoParser.MIENTRAS, 0)

        def PIZQ(self):
            return self.getToken(PatitoParser.PIZQ, 0)

        def expresion(self):
            return self.getTypedRuleContext(PatitoParser.ExpresionContext,0)


        def PDER(self):
            return self.getToken(PatitoParser.PDER, 0)

        def HAZ(self):
            return self.getToken(PatitoParser.HAZ, 0)

        def cuerpo(self):
            return self.getTypedRuleContext(PatitoParser.CuerpoContext,0)


        def PCOMA(self):
            return self.getToken(PatitoParser.PCOMA, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_ciclo

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCiclo" ):
                listener.enterCiclo(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCiclo" ):
                listener.exitCiclo(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCiclo" ):
                return visitor.visitCiclo(self)
            else:
                return visitor.visitChildren(self)




    def ciclo(self):

        localctx = PatitoParser.CicloContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_ciclo)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
            self.match(PatitoParser.MIENTRAS)
            self.state = 208
            self.match(PatitoParser.PIZQ)
            self.state = 209
            self.expresion()
            self.state = 210
            self.match(PatitoParser.PDER)
            self.state = 211
            self.match(PatitoParser.HAZ)
            self.state = 212
            self.cuerpo()
            self.state = 213
            self.match(PatitoParser.PCOMA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImprimeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ESCRIBE(self):
            return self.getToken(PatitoParser.ESCRIBE, 0)

        def PIZQ(self):
            return self.getToken(PatitoParser.PIZQ, 0)

        def impLista(self):
            return self.getTypedRuleContext(PatitoParser.ImpListaContext,0)


        def PDER(self):
            return self.getToken(PatitoParser.PDER, 0)

        def PCOMA(self):
            return self.getToken(PatitoParser.PCOMA, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_imprime

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImprime" ):
                listener.enterImprime(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImprime" ):
                listener.exitImprime(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImprime" ):
                return visitor.visitImprime(self)
            else:
                return visitor.visitChildren(self)




    def imprime(self):

        localctx = PatitoParser.ImprimeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_imprime)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 215
            self.match(PatitoParser.ESCRIBE)
            self.state = 216
            self.match(PatitoParser.PIZQ)
            self.state = 217
            self.impLista()
            self.state = 218
            self.match(PatitoParser.PDER)
            self.state = 219
            self.match(PatitoParser.PCOMA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImpListaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def impElem(self):
            return self.getTypedRuleContext(PatitoParser.ImpElemContext,0)


        def impResto(self):
            return self.getTypedRuleContext(PatitoParser.ImpRestoContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_impLista

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImpLista" ):
                listener.enterImpLista(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImpLista" ):
                listener.exitImpLista(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImpLista" ):
                return visitor.visitImpLista(self)
            else:
                return visitor.visitChildren(self)




    def impLista(self):

        localctx = PatitoParser.ImpListaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_impLista)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 221
            self.impElem()
            self.state = 222
            self.impResto()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImpRestoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMA(self):
            return self.getToken(PatitoParser.COMA, 0)

        def impElem(self):
            return self.getTypedRuleContext(PatitoParser.ImpElemContext,0)


        def impResto(self):
            return self.getTypedRuleContext(PatitoParser.ImpRestoContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_impResto

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImpResto" ):
                listener.enterImpResto(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImpResto" ):
                listener.exitImpResto(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImpResto" ):
                return visitor.visitImpResto(self)
            else:
                return visitor.visitChildren(self)




    def impResto(self):

        localctx = PatitoParser.ImpRestoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_impResto)
        try:
            self.state = 229
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 224
                self.match(PatitoParser.COMA)
                self.state = 225
                self.impElem()
                self.state = 226
                self.impResto()
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImpElemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expresion(self):
            return self.getTypedRuleContext(PatitoParser.ExpresionContext,0)


        def LETRERO(self):
            return self.getToken(PatitoParser.LETRERO, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_impElem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImpElem" ):
                listener.enterImpElem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImpElem" ):
                listener.exitImpElem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImpElem" ):
                return visitor.visitImpElem(self)
            else:
                return visitor.visitChildren(self)




    def impElem(self):

        localctx = PatitoParser.ImpElemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_impElem)
        try:
            self.state = 233
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [13, 14, 25, 29, 30, 31]:
                self.enterOuterAlt(localctx, 1)
                self.state = 231
                self.expresion()
                pass
            elif token in [32]:
                self.enterOuterAlt(localctx, 2)
                self.state = 232
                self.match(PatitoParser.LETRERO)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpresionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exp(self):
            return self.getTypedRuleContext(PatitoParser.ExpContext,0)


        def relOpc(self):
            return self.getTypedRuleContext(PatitoParser.RelOpcContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_expresion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpresion" ):
                listener.enterExpresion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpresion" ):
                listener.exitExpresion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpresion" ):
                return visitor.visitExpresion(self)
            else:
                return visitor.visitChildren(self)




    def expresion(self):

        localctx = PatitoParser.ExpresionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_expresion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 235
            self.exp(0)
            self.state = 236
            self.relOpc()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelOpcContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def opRel(self):
            return self.getTypedRuleContext(PatitoParser.OpRelContext,0)


        def exp(self):
            return self.getTypedRuleContext(PatitoParser.ExpContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_relOpc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelOpc" ):
                listener.enterRelOpc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelOpc" ):
                listener.exitRelOpc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelOpc" ):
                return visitor.visitRelOpc(self)
            else:
                return visitor.visitChildren(self)




    def relOpc(self):

        localctx = PatitoParser.RelOpcContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_relOpc)
        try:
            self.state = 242
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17, 18, 19, 20]:
                self.enterOuterAlt(localctx, 1)
                self.state = 238
                self.opRel()
                self.state = 239
                self.exp(0)
                pass
            elif token in [22, 23, 26]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OpRelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MAYOR(self):
            return self.getToken(PatitoParser.MAYOR, 0)

        def MENOR(self):
            return self.getToken(PatitoParser.MENOR, 0)

        def DISTINTO(self):
            return self.getToken(PatitoParser.DISTINTO, 0)

        def IGUAL2(self):
            return self.getToken(PatitoParser.IGUAL2, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_opRel

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOpRel" ):
                listener.enterOpRel(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOpRel" ):
                listener.exitOpRel(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOpRel" ):
                return visitor.visitOpRel(self)
            else:
                return visitor.visitChildren(self)




    def opRel(self):

        localctx = PatitoParser.OpRelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_opRel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 244
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1966080) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def termino(self):
            return self.getTypedRuleContext(PatitoParser.TerminoContext,0)


        def exp(self):
            return self.getTypedRuleContext(PatitoParser.ExpContext,0)


        def MAS(self):
            return self.getToken(PatitoParser.MAS, 0)

        def MENOS(self):
            return self.getToken(PatitoParser.MENOS, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_exp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExp" ):
                listener.enterExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExp" ):
                listener.exitExp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExp" ):
                return visitor.visitExp(self)
            else:
                return visitor.visitChildren(self)



    def exp(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = PatitoParser.ExpContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 64
        self.enterRecursionRule(localctx, 64, self.RULE_exp, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 247
            self.termino(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 257
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,16,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 255
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
                    if la_ == 1:
                        localctx = PatitoParser.ExpContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_exp)
                        self.state = 249
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 250
                        self.match(PatitoParser.MAS)
                        self.state = 251
                        self.termino(0)
                        pass

                    elif la_ == 2:
                        localctx = PatitoParser.ExpContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_exp)
                        self.state = 252
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 253
                        self.match(PatitoParser.MENOS)
                        self.state = 254
                        self.termino(0)
                        pass

             
                self.state = 259
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,16,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class TerminoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self):
            return self.getTypedRuleContext(PatitoParser.FactorContext,0)


        def termino(self):
            return self.getTypedRuleContext(PatitoParser.TerminoContext,0)


        def POR(self):
            return self.getToken(PatitoParser.POR, 0)

        def ENTRE(self):
            return self.getToken(PatitoParser.ENTRE, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_termino

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTermino" ):
                listener.enterTermino(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTermino" ):
                listener.exitTermino(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTermino" ):
                return visitor.visitTermino(self)
            else:
                return visitor.visitChildren(self)



    def termino(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = PatitoParser.TerminoContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 66
        self.enterRecursionRule(localctx, 66, self.RULE_termino, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 261
            self.factor()
            self._ctx.stop = self._input.LT(-1)
            self.state = 271
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,18,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 269
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
                    if la_ == 1:
                        localctx = PatitoParser.TerminoContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_termino)
                        self.state = 263
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 264
                        self.match(PatitoParser.POR)
                        self.state = 265
                        self.factor()
                        pass

                    elif la_ == 2:
                        localctx = PatitoParser.TerminoContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_termino)
                        self.state = 266
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 267
                        self.match(PatitoParser.ENTRE)
                        self.state = 268
                        self.factor()
                        pass

             
                self.state = 273
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class FactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PIZQ(self):
            return self.getToken(PatitoParser.PIZQ, 0)

        def expresion(self):
            return self.getTypedRuleContext(PatitoParser.ExpresionContext,0)


        def PDER(self):
            return self.getToken(PatitoParser.PDER, 0)

        def llamada(self):
            return self.getTypedRuleContext(PatitoParser.LlamadaContext,0)


        def signoOpc(self):
            return self.getTypedRuleContext(PatitoParser.SignoOpcContext,0)


        def ID(self):
            return self.getToken(PatitoParser.ID, 0)

        def cte(self):
            return self.getTypedRuleContext(PatitoParser.CteContext,0)


        def getRuleIndex(self):
            return PatitoParser.RULE_factor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFactor" ):
                listener.enterFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFactor" ):
                listener.exitFactor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFactor" ):
                return visitor.visitFactor(self)
            else:
                return visitor.visitChildren(self)




    def factor(self):

        localctx = PatitoParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_factor)
        try:
            self.state = 285
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 274
                self.match(PatitoParser.PIZQ)
                self.state = 275
                self.expresion()
                self.state = 276
                self.match(PatitoParser.PDER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 278
                self.llamada()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 279
                self.signoOpc()
                self.state = 280
                self.match(PatitoParser.ID)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 282
                self.signoOpc()
                self.state = 283
                self.cte()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SignoOpcContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MAS(self):
            return self.getToken(PatitoParser.MAS, 0)

        def MENOS(self):
            return self.getToken(PatitoParser.MENOS, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_signoOpc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSignoOpc" ):
                listener.enterSignoOpc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSignoOpc" ):
                listener.exitSignoOpc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSignoOpc" ):
                return visitor.visitSignoOpc(self)
            else:
                return visitor.visitChildren(self)




    def signoOpc(self):

        localctx = PatitoParser.SignoOpcContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_signoOpc)
        try:
            self.state = 290
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [13]:
                self.enterOuterAlt(localctx, 1)
                self.state = 287
                self.match(PatitoParser.MAS)
                pass
            elif token in [14]:
                self.enterOuterAlt(localctx, 2)
                self.state = 288
                self.match(PatitoParser.MENOS)
                pass
            elif token in [29, 30, 31]:
                self.enterOuterAlt(localctx, 3)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CteContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CTE_ENT(self):
            return self.getToken(PatitoParser.CTE_ENT, 0)

        def CTE_FLOT(self):
            return self.getToken(PatitoParser.CTE_FLOT, 0)

        def getRuleIndex(self):
            return PatitoParser.RULE_cte

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCte" ):
                listener.enterCte(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCte" ):
                listener.exitCte(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCte" ):
                return visitor.visitCte(self)
            else:
                return visitor.visitChildren(self)




    def cte(self):

        localctx = PatitoParser.CteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_cte)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 292
            _la = self._input.LA(1)
            if not(_la==30 or _la==31):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[32] = self.exp_sempred
        self._predicates[33] = self.termino_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def exp_sempred(self, localctx:ExpContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         

    def termino_sempred(self, localctx:TerminoContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 2)
         




