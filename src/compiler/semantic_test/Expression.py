import lark
class ExpressionTree(lark.Tree):
	def __init__(self,data,children=[]):
		super().__init__(data,children)
		self.does_variate=True
class ExpressionVariable(ExpressionTree):
	def __init__(self,data,var_name,children=[]):
		super().__init__(data,children)
		self.var_name=var_name
class ExpressionActivation(ExpressionVariable):pass
class ExpressionVector(ExpressionVariable):pass
class ExpressionInt(int):
	def __init__(self,*args,**kwargs):
		self.does_variate=False
	def __new__(cls,*args,**kwargs):
		return int.__new__(cls,int(*args,**kwargs))
class ExpressionList(list):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.data="list"


class Expression():#custom trasnformer
	op_relacional_table={
		">" :lambda x,y:ExpressionInt(x> y),
		">=":lambda x,y:ExpressionInt(x>=y),
		"<" :lambda x,y:ExpressionInt(x< y),
		"<=":lambda x,y:ExpressionInt(x<=y),
		"==":lambda x,y:ExpressionInt(x==y),
		"!=":lambda x,y:ExpressionInt(x!=y)
	}
	soma_table={
		"+":lambda x,y:x+y,
		"-":lambda x,y:x-y
	}
	mult_table={
		"*":lambda x,y:x* y,
		"/":lambda x,y:x//y
	}
	def install(self,tree):
		if not isinstance(tree,lark.Tree):
			return tree
		args=[self.install(children) for children in tree.children]
		f=getattr(self,tree.data)
		if f==None:
			raise RuntimeError(f"Unexpected error {tree.data} not defined")
		ans=f(args)
		tree.expression=ans
		return ans
	def expression(self,args):
		if len(args)==3:
			return ExpressionTree("=",[args[0],args[2]])
		return args[0]
	def expression_simples(self,args):
		if len(args)==3:
			if isinstance(args[0],lark.Tree) or isinstance(args[2],lark.Tree):
				return ExpressionTree(args[1],[args[0],args[2]])
			return Expression.op_relacional_table[args[1]](args[0],args[2])
		return args[0]
	def s_expression(self,args):
		if len(args)==3:
			if isinstance(args[0],lark.Tree) or isinstance(args[2],lark.Tree):
				return ExpressionTree(args[1],[args[0],args[2]])
			return Expression.soma_table[args[1]](args[0],args[2])
		return args[0]
	def termo(self,args):

		if len(args)==3:
			if isinstance(args[0],lark.Tree) or isinstance(args[2],lark.Tree):
				return ExpressionTree(args[1],[args[0],args[2]])
			return Expression.mult_table[args[1]](args[0],args[2])
		return args[0]
	def soma(self,args):
		"""
		soma: SUMOP
		"""
		return args[0].value
	def op_relacional(self,args):
		"""
		op_relacional: RELOP
		"""
		return args[0].value
	def mult(self,args):
		"""
		mult: MULTOP
		"""
		return args[0].value

	def variable(self,args):
		"""
		varible: ID 
		| ID S_OPEN expressao S_CLOSE
		"""
		if len(args)==1:
			return ExpressionVariable("variavel",args[0].value)
		return ExpressionVector("vetor",args[0].value,[args[2]])
	def argumentos(self,args):
		"""
		argumentos: lista_argumentos 
		| 
		"""
		if len(args)==0:
			return []
		return args[0]
	def lista_argumentos(self,args):
		"""
		lista_argumentos COMMA expressao 
		| expressao
		"""
		if len(args)==3:
			#TODO FIX THIS HACK
			return ExpressionList(args[0]+[args[2]])
		return ExpressionList([args[0]])
	
	
def is_head(tree):
	if tree==None: #safe switch
		return True
	tree=tree.parent
	while tree:
		if tree.data=="expressao":
			return False
		tree=tree.parent
	return True
def install_expression(tree):
	for subtree in tree.iter_subtrees():
		if not (subtree.data=="expressao" and is_head(subtree)):
			continue
		subtree.is_head=True
		Expression().install(subtree)