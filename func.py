from frame import Env


class Function():
    def __init__(self, bindings, func):
        self.func = func
        self.bindings = bindings
        self.env = None

    def applyFunc(self, args,env):
        self.env=Env(env)
        if len(self.bindings) != len(args):
            raise Exception("function requires " + str(len(self.bindings)) + " arguments but is called with "
                            + str(len(args)) + " arguments")
        for i in range(len(args)):
            self.env.addVar(self.bindings[i], args[i])

    def getfuncbody(self):
        return self.func

    def getfuncenv(self):
        return self.env
