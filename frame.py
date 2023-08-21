class Env():
    def __init__(self, previous_env):
        self.bindings = []
        self.values = []
        self.parent_env = previous_env

    def addVar(self, binding, value):
        index = len(self.bindings)
        if binding in self.bindings:
            raise Exception("the variable of name: " + binding + " is already defined")
        self.bindings.append(binding)
        self.values.append(value)

    def lookupvar(self, var_name):
        if var_name not in self.bindings:
            if self.parent_env == None:
                raise Exception("Variable of name: " + var_name + " not defined")
            else:
                return self.parent_env.lookupvar(var_name)
        index = self.bindings.index(var_name)
        return self.values[index]
