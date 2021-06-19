from grammars import yacc
import cmd


class dbms(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'DBMS > '

    def onecmd(self, line):
        yacc.parse(line)


if __name__ == '__main__':
    print("基于Python的小型dbms")
    print("学号：17030130021 姓名：张维越")
    dbms().cmdloop()
