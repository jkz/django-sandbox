from django.test import TestCase
from django.db import IntegrityError

from refs import Ref, ref

from . import models as m

class SandboxTest(TestCase):
    def test_basic(self):
        foo = m.Foo.objects.create(name='FOO')
        bar = m.Bar.objects.create(name='BAR')

        quux = m.Quux.objects.create(ref1=foo, ref2=foo)

        rfoo = ref(foo)
        rbar = ref(bar)
        rquux = ref(quux)

        self.assertEqual(m.Quux.objects.get(ref1=foo, ref2=foo), quux)
        self.assertEqual(m.Quux.objects.get(ref1=rfoo, ref2=foo), quux)
        self.assertEqual(m.Quux.objects.get(ref1=foo, ref2=rfoo), quux)
        self.assertEqual(m.Quux.objects.get(ref1=rfoo, ref2=rfoo), quux)

        self.assertEqual(Ref.objects.with_content_type(foo).count(), 1)
        self.assertEqual(Ref.objects.with_content_type(bar).count(), 1)
        self.assertEqual(Ref.objects.count(), 3)

        m.Quux.objects.create(ref1=foo, ref2=bar)
        self.assertRaises(IntegrityError, lambda: m.Quux.objects.create(ref1=foo, ref2=bar))

