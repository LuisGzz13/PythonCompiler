# Generated from Patito.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PatitoParser import PatitoParser
else:
    from PatitoParser import PatitoParser

# This class defines a complete listener for a parse tree produced by PatitoParser.
class PatitoListener(ParseTreeListener):

    # Enter a parse tree produced by PatitoParser#programa.
    def enterPrograma(self, ctx:PatitoParser.ProgramaContext):
        pass

    # Exit a parse tree produced by PatitoParser#programa.
    def exitPrograma(self, ctx:PatitoParser.ProgramaContext):
        pass


    # Enter a parse tree produced by PatitoParser#varsOpc.
    def enterVarsOpc(self, ctx:PatitoParser.VarsOpcContext):
        pass

    # Exit a parse tree produced by PatitoParser#varsOpc.
    def exitVarsOpc(self, ctx:PatitoParser.VarsOpcContext):
        pass


    # Enter a parse tree produced by PatitoParser#funcsOpc.
    def enterFuncsOpc(self, ctx:PatitoParser.FuncsOpcContext):
        pass

    # Exit a parse tree produced by PatitoParser#funcsOpc.
    def exitFuncsOpc(self, ctx:PatitoParser.FuncsOpcContext):
        pass


    # Enter a parse tree produced by PatitoParser#vars.
    def enterVars(self, ctx:PatitoParser.VarsContext):
        pass

    # Exit a parse tree produced by PatitoParser#vars.
    def exitVars(self, ctx:PatitoParser.VarsContext):
        pass


    # Enter a parse tree produced by PatitoParser#declaracionList.
    def enterDeclaracionList(self, ctx:PatitoParser.DeclaracionListContext):
        pass

    # Exit a parse tree produced by PatitoParser#declaracionList.
    def exitDeclaracionList(self, ctx:PatitoParser.DeclaracionListContext):
        pass


    # Enter a parse tree produced by PatitoParser#declaracion.
    def enterDeclaracion(self, ctx:PatitoParser.DeclaracionContext):
        pass

    # Exit a parse tree produced by PatitoParser#declaracion.
    def exitDeclaracion(self, ctx:PatitoParser.DeclaracionContext):
        pass


    # Enter a parse tree produced by PatitoParser#idLista.
    def enterIdLista(self, ctx:PatitoParser.IdListaContext):
        pass

    # Exit a parse tree produced by PatitoParser#idLista.
    def exitIdLista(self, ctx:PatitoParser.IdListaContext):
        pass


    # Enter a parse tree produced by PatitoParser#idResto.
    def enterIdResto(self, ctx:PatitoParser.IdRestoContext):
        pass

    # Exit a parse tree produced by PatitoParser#idResto.
    def exitIdResto(self, ctx:PatitoParser.IdRestoContext):
        pass


    # Enter a parse tree produced by PatitoParser#tipo.
    def enterTipo(self, ctx:PatitoParser.TipoContext):
        pass

    # Exit a parse tree produced by PatitoParser#tipo.
    def exitTipo(self, ctx:PatitoParser.TipoContext):
        pass


    # Enter a parse tree produced by PatitoParser#funcs.
    def enterFuncs(self, ctx:PatitoParser.FuncsContext):
        pass

    # Exit a parse tree produced by PatitoParser#funcs.
    def exitFuncs(self, ctx:PatitoParser.FuncsContext):
        pass


    # Enter a parse tree produced by PatitoParser#tipoFunc.
    def enterTipoFunc(self, ctx:PatitoParser.TipoFuncContext):
        pass

    # Exit a parse tree produced by PatitoParser#tipoFunc.
    def exitTipoFunc(self, ctx:PatitoParser.TipoFuncContext):
        pass


    # Enter a parse tree produced by PatitoParser#paramsOpc.
    def enterParamsOpc(self, ctx:PatitoParser.ParamsOpcContext):
        pass

    # Exit a parse tree produced by PatitoParser#paramsOpc.
    def exitParamsOpc(self, ctx:PatitoParser.ParamsOpcContext):
        pass


    # Enter a parse tree produced by PatitoParser#paramLista.
    def enterParamLista(self, ctx:PatitoParser.ParamListaContext):
        pass

    # Exit a parse tree produced by PatitoParser#paramLista.
    def exitParamLista(self, ctx:PatitoParser.ParamListaContext):
        pass


    # Enter a parse tree produced by PatitoParser#paramResto.
    def enterParamResto(self, ctx:PatitoParser.ParamRestoContext):
        pass

    # Exit a parse tree produced by PatitoParser#paramResto.
    def exitParamResto(self, ctx:PatitoParser.ParamRestoContext):
        pass


    # Enter a parse tree produced by PatitoParser#llamada.
    def enterLlamada(self, ctx:PatitoParser.LlamadaContext):
        pass

    # Exit a parse tree produced by PatitoParser#llamada.
    def exitLlamada(self, ctx:PatitoParser.LlamadaContext):
        pass


    # Enter a parse tree produced by PatitoParser#argsOpc.
    def enterArgsOpc(self, ctx:PatitoParser.ArgsOpcContext):
        pass

    # Exit a parse tree produced by PatitoParser#argsOpc.
    def exitArgsOpc(self, ctx:PatitoParser.ArgsOpcContext):
        pass


    # Enter a parse tree produced by PatitoParser#argLista.
    def enterArgLista(self, ctx:PatitoParser.ArgListaContext):
        pass

    # Exit a parse tree produced by PatitoParser#argLista.
    def exitArgLista(self, ctx:PatitoParser.ArgListaContext):
        pass


    # Enter a parse tree produced by PatitoParser#argResto.
    def enterArgResto(self, ctx:PatitoParser.ArgRestoContext):
        pass

    # Exit a parse tree produced by PatitoParser#argResto.
    def exitArgResto(self, ctx:PatitoParser.ArgRestoContext):
        pass


    # Enter a parse tree produced by PatitoParser#cuerpo.
    def enterCuerpo(self, ctx:PatitoParser.CuerpoContext):
        pass

    # Exit a parse tree produced by PatitoParser#cuerpo.
    def exitCuerpo(self, ctx:PatitoParser.CuerpoContext):
        pass


    # Enter a parse tree produced by PatitoParser#estatutoList.
    def enterEstatutoList(self, ctx:PatitoParser.EstatutoListContext):
        pass

    # Exit a parse tree produced by PatitoParser#estatutoList.
    def exitEstatutoList(self, ctx:PatitoParser.EstatutoListContext):
        pass


    # Enter a parse tree produced by PatitoParser#estatuto.
    def enterEstatuto(self, ctx:PatitoParser.EstatutoContext):
        pass

    # Exit a parse tree produced by PatitoParser#estatuto.
    def exitEstatuto(self, ctx:PatitoParser.EstatutoContext):
        pass


    # Enter a parse tree produced by PatitoParser#asigna.
    def enterAsigna(self, ctx:PatitoParser.AsignaContext):
        pass

    # Exit a parse tree produced by PatitoParser#asigna.
    def exitAsigna(self, ctx:PatitoParser.AsignaContext):
        pass


    # Enter a parse tree produced by PatitoParser#condicion.
    def enterCondicion(self, ctx:PatitoParser.CondicionContext):
        pass

    # Exit a parse tree produced by PatitoParser#condicion.
    def exitCondicion(self, ctx:PatitoParser.CondicionContext):
        pass


    # Enter a parse tree produced by PatitoParser#sinoOpc.
    def enterSinoOpc(self, ctx:PatitoParser.SinoOpcContext):
        pass

    # Exit a parse tree produced by PatitoParser#sinoOpc.
    def exitSinoOpc(self, ctx:PatitoParser.SinoOpcContext):
        pass


    # Enter a parse tree produced by PatitoParser#ciclo.
    def enterCiclo(self, ctx:PatitoParser.CicloContext):
        pass

    # Exit a parse tree produced by PatitoParser#ciclo.
    def exitCiclo(self, ctx:PatitoParser.CicloContext):
        pass


    # Enter a parse tree produced by PatitoParser#imprime.
    def enterImprime(self, ctx:PatitoParser.ImprimeContext):
        pass

    # Exit a parse tree produced by PatitoParser#imprime.
    def exitImprime(self, ctx:PatitoParser.ImprimeContext):
        pass


    # Enter a parse tree produced by PatitoParser#impLista.
    def enterImpLista(self, ctx:PatitoParser.ImpListaContext):
        pass

    # Exit a parse tree produced by PatitoParser#impLista.
    def exitImpLista(self, ctx:PatitoParser.ImpListaContext):
        pass


    # Enter a parse tree produced by PatitoParser#impResto.
    def enterImpResto(self, ctx:PatitoParser.ImpRestoContext):
        pass

    # Exit a parse tree produced by PatitoParser#impResto.
    def exitImpResto(self, ctx:PatitoParser.ImpRestoContext):
        pass


    # Enter a parse tree produced by PatitoParser#impElem.
    def enterImpElem(self, ctx:PatitoParser.ImpElemContext):
        pass

    # Exit a parse tree produced by PatitoParser#impElem.
    def exitImpElem(self, ctx:PatitoParser.ImpElemContext):
        pass


    # Enter a parse tree produced by PatitoParser#expresion.
    def enterExpresion(self, ctx:PatitoParser.ExpresionContext):
        pass

    # Exit a parse tree produced by PatitoParser#expresion.
    def exitExpresion(self, ctx:PatitoParser.ExpresionContext):
        pass


    # Enter a parse tree produced by PatitoParser#relOpc.
    def enterRelOpc(self, ctx:PatitoParser.RelOpcContext):
        pass

    # Exit a parse tree produced by PatitoParser#relOpc.
    def exitRelOpc(self, ctx:PatitoParser.RelOpcContext):
        pass


    # Enter a parse tree produced by PatitoParser#opRel.
    def enterOpRel(self, ctx:PatitoParser.OpRelContext):
        pass

    # Exit a parse tree produced by PatitoParser#opRel.
    def exitOpRel(self, ctx:PatitoParser.OpRelContext):
        pass


    # Enter a parse tree produced by PatitoParser#exp.
    def enterExp(self, ctx:PatitoParser.ExpContext):
        pass

    # Exit a parse tree produced by PatitoParser#exp.
    def exitExp(self, ctx:PatitoParser.ExpContext):
        pass


    # Enter a parse tree produced by PatitoParser#termino.
    def enterTermino(self, ctx:PatitoParser.TerminoContext):
        pass

    # Exit a parse tree produced by PatitoParser#termino.
    def exitTermino(self, ctx:PatitoParser.TerminoContext):
        pass


    # Enter a parse tree produced by PatitoParser#factor.
    def enterFactor(self, ctx:PatitoParser.FactorContext):
        pass

    # Exit a parse tree produced by PatitoParser#factor.
    def exitFactor(self, ctx:PatitoParser.FactorContext):
        pass


    # Enter a parse tree produced by PatitoParser#signoOpc.
    def enterSignoOpc(self, ctx:PatitoParser.SignoOpcContext):
        pass

    # Exit a parse tree produced by PatitoParser#signoOpc.
    def exitSignoOpc(self, ctx:PatitoParser.SignoOpcContext):
        pass


    # Enter a parse tree produced by PatitoParser#cte.
    def enterCte(self, ctx:PatitoParser.CteContext):
        pass

    # Exit a parse tree produced by PatitoParser#cte.
    def exitCte(self, ctx:PatitoParser.CteContext):
        pass



del PatitoParser