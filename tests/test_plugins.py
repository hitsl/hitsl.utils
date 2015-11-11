# -*- coding: utf-8 -*-
from hitsl_utils.plugins import ComponentManager, Component, Interface, ExtensionPoint, implementer

__author__ = 'viruzzz-kun'


class I1(Interface):
    pass


class I2(Interface):
    pass


class C1(Component, ComponentManager):
    ep = ExtensionPoint(I1)
    er = ExtensionPoint(I2)

    def test(self):
        print "C1.test()"
        for e in self.ep:
            e.test1()
        for e in self.er:
            e.test2()


@implementer(I1)
class C2(Component):
    def test1(self):
        print "C2.test1()"


@implementer(I1, I2)
class C3(Component):
    def test1(self):
        print "C3.test1()"

    def test2(self):
        print "C3.test2()"


# manager = ComponentManager()
# manager[C1].test()

manager = C1()
manager[C1].test()

print manager[C2]
