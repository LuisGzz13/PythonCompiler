# Generated from Patito.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PatitoParser import PatitoParser
else:
    from PatitoParser import PatitoParser

# This class defines a complete generic visitor for a parse tree produced by PatitoParser.

class PatitoVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PatitoParser#programa.
    def visitPrograma(self, ctx:PatitoParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#varsOpc.
    def visitVarsOpc(self, ctx:PatitoParser.VarsOpcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#funcsOpc.
    def visitFuncsOpc(self, ctx:PatitoParser.FuncsOpcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#vars.
    def visitVars(self, ctx:PatitoParser.VarsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#declaracionList.
    def visitDeclaracionList(self, ctx:PatitoParser.DeclaracionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#declaracion.
    def visitDeclaracion(self, ctx:PatitoParser.DeclaracionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#idLista.
    def visitIdLista(self, ctx:PatitoParser.IdListaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#idResto.
    def visitIdResto(self, ctx:PatitoParser.IdRestoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#tipo.
    def visitTipo(self, ctx:PatitoParser.TipoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#funcs.
    def visitFuncs(self, ctx:PatitoParser.FuncsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#tipoFunc.
    def visitTipoFunc(self, ctx:PatitoParser.TipoFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#paramsOpc.
    def visitParamsOpc(self, ctx:PatitoParser.ParamsOpcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#paramLista.
    def visitParamLista(self, ctx:PatitoParser.ParamListaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#paramResto.
    def visitParamResto(self, ctx:PatitoParser.ParamRestoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#llamada.
    def visitLlamada(self, ctx:PatitoParser.LlamadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#argsOpc.
    def visitArgsOpc(self, ctx:PatitoParser.ArgsOpcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#argLista.
    def visitArgLista(self, ctx:PatitoParser.ArgListaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#argResto.
    def visitArgResto(self, ctx:PatitoParser.ArgRestoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#cuerpo.
    def visitCuerpo(self, ctx:PatitoParser.CuerpoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#estatutoList.
    def visitEstatutoList(self, ctx:PatitoParser.EstatutoListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#estatuto.
    def visitEstatuto(self, ctx:PatitoParser.EstatutoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#asigna.
    def visitAsigna(self, ctx:PatitoParser.AsignaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#condicion.
    def visitCondicion(self, ctx:PatitoParser.CondicionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#sinoOpc.
    def visitSinoOpc(self, ctx:PatitoParser.SinoOpcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#ciclo.
    def visitCiclo(self, ctx:PatitoParser.CicloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#imprime.
    def visitImprime(self, ctx:PatitoParser.ImprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#retorno.
    def visitRetorno(self, ctx:PatitoParser.RetornoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#impLista.
    def visitImpLista(self, ctx:PatitoParser.ImpListaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#impResto.
    def visitImpResto(self, ctx:PatitoParser.ImpRestoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#impElem.
    def visitImpElem(self, ctx:PatitoParser.ImpElemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#expresion.
    def visitExpresion(self, ctx:PatitoParser.ExpresionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#relOpc.
    def visitRelOpc(self, ctx:PatitoParser.RelOpcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#opRel.
    def visitOpRel(self, ctx:PatitoParser.OpRelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#exp.
    def visitExp(self, ctx:PatitoParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#termino.
    def visitTermino(self, ctx:PatitoParser.TerminoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#factor.
    def visitFactor(self, ctx:PatitoParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#signoOpc.
    def visitSignoOpc(self, ctx:PatitoParser.SignoOpcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatitoParser#cte.
    def visitCte(self, ctx:PatitoParser.CteContext):
        return self.visitChildren(ctx)



del PatitoParser